import numpy as np
from PIL import Image, ImageOps

from argparse import ArgumentParser

def flattening(tensor, dimi):
    return np.reshape(np.moveaxis(tensor, dimi, 0), (tensor.shape[dimi],-1))    

def hosvd(tensor : np.ndarray):
    core_tensor = tensor.copy()
    left_singular_basis = []

    for k in range(tensor.ndim):
        unfold = np.reshape(np.moveaxis(tensor, k, 0), (tensor.shape[k], -1))
        U, _, _ = np.linalg.svd(
            unfold,
            full_matrices=False,
            compute_uv=True,
        )
        left_singular_basis.append(U)
        U_c = U.T.conj()
        core_tensor = np.tensordot(core_tensor, U_c, (0, 1))

    return left_singular_basis, core_tensor

def thosvd(tensor : np.ndarray, rank : int):
    core_tensor = tensor
    print(core_tensor.shape)
    left_singular_basis = []
    
    print("SOMETHING")
    for k in range(tensor.ndim):
        print(f"{k=}")
        # TODO: The following two steps are too expensive!
        unfold = flattening(tensor, k) #np.reshape(np.moveaxis(tensor, k, 0), (tensor.shape[k], -1))
        
        U, _, _ = np.linalg.svd(
            unfold,
            full_matrices=True,
            compute_uv=True,
            hermitian=False
        )
        left_singular_basis.append(U[:,:rank])
        #print(left_singular_basis)
        # Reduced basis
        U_c = U#.T.conj()
        core_tensor = np.tensordot(core_tensor, U_c, (0, 1))

    return left_singular_basis, core_tensor

def compress_colored_img(image, rank : int):
    # TODO: CHECK!
    img_tensor = np.asarray(image)
    L, C = thosvd(img_tensor, rank)
    for j, l in enumerate(L):
        C = np.tensordot(C, l.T, (0,1))
    compressed_tensor = C
    new_image = Image.fromarray(np.uint8(compressed_tensor), mode="RGB")
    return new_image

def compress(grayscale_image, r):
    # Load from PIL to numpy
    workableimage = np.asarray(grayscale_image)
    # This compress the image via svd
    U,D,Vt = np.linalg.svd(workableimage)    
    newimage = np.minimum(U[:,:r] @ np.diag(D[:r]) @ Vt[:r,:],
            np.array(255))
    # Load it back in PIL
    compressed_image = Image.fromarray(np.uint8(newimage), mode="L")

    return compressed_image

def load_img(filepath):
    im = Image.open(filepath)
    #im = ImageOps.grayscale(im)
    return im

if __name__ == "__main__":
    parser = ArgumentParser(prog="Image compression via T-HOSVD")
    parser.add_argument("img", type=str)
    parser.add_argument("--rank", dest="rank", type=int, default=100)
    args = parser.parse_args()

    s = load_img(args.img) 
    #ci = compress(ImageOps.grayscale(s), args.rank)
    ci = compress_colored_img(s, args.rank)
    ci.save(f"{args.img}-rank={args.rank}.png")   

