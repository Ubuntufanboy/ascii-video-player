"""
Thanks to the following sources
numpy
pygame community
tqdm
Pillow
ffmpeg
GNU coreutils
"""

import sys
import time
import os
import pygame
import logging
import numpy as np
from tqdm import tqdm
from PIL import Image
from threading import Thread
from shutil import rmtree
from blessed import Terminal
from multiprocessing import Pool

term = Terminal() # Initialise blessed

'''https://stackoverflow.com/questions/5174810/how-to-turn-off-blinking-cursor-in-command-window'''
'''This section of the script hides the terminal terminal cursor'''

if os.name == 'nt':
    import msvcrt
    import ctypes
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

if os.name == 'nt':
    ci = _CursorInfo()
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    ci.visible = False
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
elif os.name == 'posix' or os.name == "linux" or os.name == "linux2":
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


# Extract the .asciivideo file
try:
    video = sys.argv[1]
    fps = float(sys.argv[2])  # Ensure FPS is valid
except IndexError:
    print(f"Usage: python {os.path.relpath(__file__)} <asciivideo_file> <fps>")
    sys.exit(1)
except ValueError:
    print("FPS must be a number.")
    sys.exit(1)


logger = logging.Logger("Ascii video logger")

try:
    verbose = sys.argv[2]
    if verbose == "debug":
        logger.setLevel(10)
    elif verbose == "warning":
        logger.setLevel(30)
except IndexError:
    logger.setLevel(40) # Only error

if not video.endswith(".asciivideo"):
    logger.error("No video file provided")
    sys.exit(1)

tar_name = video.replace(".asciivideo", ".tar.gz")
os.system(f"mv {video} {tar_name}")
os.system(f"tar xf {tar_name}")
os.system(f"mv {tar_name} {video}")

# Get frame number

os.chdir("target")
os.chdir("metadata")
with open("framenum.txt", 'r') as f:
    frame_number = int(f.read())
os.chdir("..")
os.chdir("..")

# Let the fun begin
print("Please do NOT resize the screen")
time.sleep(2)

'''Get columns and lines of terminal'''
x = os.get_terminal_size().columns
y = os.get_terminal_size().lines

try: #Just in case
    os.chdir("target")
except Exception:
    os.mkdir("target")
    os.chdir("target")

'''In case the directory resized already exists we remove everything inside and recreate it'''
try:
    os.mkdir("resized")
except FileExistsError:
    rmtree("resized")
    os.mkdir("resized")

for i in tqdm(range(1, frame_number+1)):
    image = Image.open(f"img/output{i}.png")
    image = image.resize((x, y))
    image.save(f"resized/new{i}.png")

slackers = frame_number // 4
nuli = frame_number - (slackers * 3)

w1 = []
w2 = []
w3 = []
w4 = []


def process(img: np.ndarray) -> str:
    """
    This function turns a numpy array of brightness values into a string
    that has each character representing the brightness of the pixel
    in the given frame
    """
    vals = np.array([0, 50, 100, 150, 200, 255])  # These are the thresholds
    symbs = np.array(list(" +$#&@"))
    positions = np.searchsorted(vals, img.reshape(-1), "right") - 1
    symb_img = symbs[positions].reshape(img.shape)  # map numbers to charecters
    return "".join(symb_img.reshape(-1))  # Returns the final image


# Must be in img dir for this to work
current = os.getcwd()

def is_valid(local_frames: list) -> bool:
    """
    Simple verification function
    to catch users changing the
    terminal window so the user
    will not be confused why
    the screen is glitched
    """
    hor = os.get_terminal_size().columns
    ver = os.get_terminal_size().lines
    for string in local_frames:
        if len(string) != hor * ver:
            return False
    return True


# Worker nodes
def worker1():
    for i in tqdm(range(1, nuli+1)):
        try:
            with Image.open(f"{current}/resized/new{i}.png") as img:
                img = img.getdata(0)
                img = np.array(img)
                w1.append(process(img))
        except Exception as e:
            print(e)
    if not is_valid(w1):
        logger.error("Content was couripted")
        exit(1)


def worker2():
    for i in range(nuli+1, nuli+slackers+1):
        try:
            with Image.open(f"{current}/resized/new{i}.png") as img:
                img = img.getdata(0)
                img = np.array(img)
                w2.append(process(img))
        except Exception as e:
            print(e)


def worker3():
    for i in range(nuli+slackers+1, nuli+slackers+slackers+1):
        try:
            with Image.open(f"{current}/resized/new{i}.png") as img:
                img = img.getdata(0)
                img = np.array(img)
                w3.append(process(img))
        except Exception as e:
            print(e)


def worker4():
    for i in range(nuli+slackers+slackers+1, nuli+(slackers*3)+1):
        try:
            with Image.open(f"{current}/resized/new{i}.png") as img:
                img = img.getdata(0)
                img = np.array(img)
                w4.append(process(img))
        except Exception as e:
            print(e)


th1 = Thread(target=worker1)
th2 = Thread(target=worker2)
th3 = Thread(target=worker3)
th4 = Thread(target=worker4)

th1.start()
th2.start()
th3.start()
th4.start()

while len(w1) < nuli or len(w2) < slackers or len(w3) < slackers or len(w4) < slackers:
    pass
frames = w1 + w2 + w3 + w4

if not is_valid(frames):
    logger.error("Content was courupted")
    sys.exit(1)

pygame.mixer.init()
if os.name == 'nt':
    pygame.mixer.music.load(f"{current}\\audio\\audio.mp3")
else:
    pygame.mixer.music.load(f"{current}/audio/audio.mp3")

os.chdir("..")
try:
    rmtree("target") #Using python modules for compatibility with windows machines
except FileNotFoundError:
    pass
except PermissionError:
    pass
logger.debug("Video playback started")
frame = 0
next_call = time.perf_counter()

pygame.mixer.music.play() #Play extracted audio

"""
Here is what happens down below
1. Terminal gets full screened so it doesn't display random characters when doing CTRL+C
2. Putting the frames in a bugger, moving the terminal cursor, not only we basically removed the flashing
effect after doing clear, but it also ensures smooth play

And after that the video ends it exits.
"""

with term.fullscreen():
    while True:
        if time.perf_counter() > next_call:
            next_call += 1/fps # the FPS the user chooses
            try:
                frame_buffer = term.move_yx(0, 0) + frames[frame]
                print(frame_buffer, end='')  # Print all the data in one go
            except IndexError:
                break # Video finished
            frame += 1

'''Show terminal cursor'''

if os.name == 'nt':
    ci = _CursorInfo()
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    ci.visible = True
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
elif os.name == 'posix' or os.name == "linux" or os.name == "linux2":
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()