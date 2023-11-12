import numpy as np
import sys
from os import system, name
from time import sleep
from playsound import playsound
from random import choice
from functools import partial

from argparse import ArgumentParser

emoji_list = ["\U0001f3c6", # trophy
        "\U0001f9ff", # nazar amulet
        "\U0001f3ae", # video game
        "\U0001f3a8", # artist palette
        "\U0001f9f6", # yarn
        "\U0001f451", # crown
        "\U0001f3a9", # top hat
        "\U0001f3a7", # headphone
        "\U0001f3ba"] # trumpet

def display_remaining_time(t : int = 0) -> None:
    """
        Computes and display the time remaining.
    """
    h = t // 3600 
    m = t % 3600 // 60 
    s = t % 60

    sys.stdout.write("\r" + f"Time remaining {choice(emoji_list)}: {h}h:{m}m:{s}s " + "\r") 
    sys.stdout.flush()

def show_title(title : str = "", spongebob : bool = False) -> None:
    """
        Shows title, if needed.

        spongebob = True, writes a title in the following manner:
            ''HeLlo wOrLd''.
        
    """
    if title == "":
        return None

    colored_title = ""
    # Show the title using a different color for each letter
    for i, c in enumerate(title):
         
        if spongebob and i % 2 == 0:
            c = c.upper()
        
        cc = f"\u001b[{31 + i % 7}m{c}" 

        colored_title = colored_title + cc
    print(f"### {colored_title}")

def timesup() -> None:
    """
        Output when the timer is up.
    """
    print("\nTime's up!\U0001f389")

def clock(time :int = 1, showtitle: "function" = show_title) -> None:
    """
        This method serves as a clock to the various 
        features of the timer.
    """
    # Clear screen
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")
    
    # Ticks and show remaining time
    showtitle()
    while time > 0:
        time -= 1
        sleep(1)
        display_remaining_time(time)

    timesup()

def help():
   print("""
            This small utility provides a fancy timer.

            Flags:
            -t [title] = set the title of the clock
            -h [integer] = number of hours to wait
            -m [integer] = number of minutes to wait
            -s [integer] = number of seconds to wait
            -sponge [True=1/False=0] = title in spongegbob-meme style
         """)

if __name__ == "__main__":
    parser = ArgumentParser(prog="A CLI for a task tomato timer")
    parser.add_argument("-H", 
                        dest='hours', 
                        type=int, 
                        help='int: hours for the task to complete',
                        default=0)
    parser.add_argument("-M", 
                        dest='minutes', 
                        type=int, 
                        help='int: minutes for the task to complete',
                        default=0)
    parser.add_argument("-S", 
                        dest='seconds', 
                        type=int, 
                        help='int: seconds for the task to complete',
                        default=0)
    parser.add_argument("--sponge", 
                        dest='sponge', 
                        type=bool, 
                        help='bool: task title style "sponge"',
                        default=False)
    parser.add_argument("--title", 
                        dest='title', 
                        type=str, 
                        help='str: title of the task to complete', 
                        default="")

    args   = parser.parse_args()
    time   = 0 
    title  = args.title
    sponge = args.sponge
    time  += args.hours * 3600 + args.minutes * 60 + args.seconds

    if time > 0:
        clock(time, partial(show_title, title, sponge))
        playsound('default.mp3')


