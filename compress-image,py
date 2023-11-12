import numpy as np
from sklearn.decomposition import TruncatedSVD
from PIL import Image, ImageOps

from argparse import ArgumentParser

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
    im = ImageOps.grayscale(im)
    return im

if __name__ == "__main__":
    parser = ArgumentParser(prog="Image compression via T-HOSVD")
    parser.add_argument("img", type=str)
    parser.add_argument("--rank", dest="rank", type=int, default=100)
    args = parser.parse_args()

    s = load_img(args.img)
    ci = compress(s, args.rank)
    ci.save(f"{args.img}-rank={args.rank}.png")   

