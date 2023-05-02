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
import numpy as np
from tqdm import tqdm
from PIL import Image
from threading import Thread

# Extract the .asciivideo file
try:
    video = sys.argv[1]
except IndexError:
    print("Please provide a asciivideo file!")
    sys.exit(1)

if not video.endswith(".asciivideo"):
    print("Invalid format!")
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

# Get audio file name

os.chdir("target")
os.chdir("audio")
os.system("ls > audioname.txt")
with open("audioname.txt", 'r') as f:
    audioname = f.read()
    audioname = audioname.replace("\naudioname.txt", "")
    audioname = audioname.replace("audioname.txt", "")
    audioname = audioname.replace("\n", "")
    audioname = audioname.replace("audioname.txt", "")
    print(f"DEBUG: {audioname}")
os.system("rm audioname.txt")
os.chdir("..")

# Let the fun begin
print("Hey! I am grabbing the size of your terminal please don't move!")
time.sleep(1)
x = os.get_terminal_size().columns
y = os.get_terminal_size().lines

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
    vals = np.array([0, 50, 100, 150, 200, 255])  # These are the thresholds
    symbs = np.array(list(" +$#&@"))
    positions = np.searchsorted(vals, img.reshape(-1), "right") - 1
    symb_img = symbs[positions].reshape(img.shape)  # map numbers to charecters
    return "".join(symb_img.reshape(-1))  # Returns the final image


# Must be in img dir for this to work
current = os.getcwd()


def is_valid(frames: list) -> bool:
    x = os.get_terminal_size().columns
    y = os.get_terminal_size().lines
    for frame in frames:
        if len(frame) != x * y:
            return False
    return True


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
        print("Content was courputed")
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
    print("Input was courputed!")
    sys.exit(1)
pygame.mixer.init()
pygame.mixer.music.load(f"{current}/audio/{audioname}")
print("Show time!")

frame = 0
next_call = time.perf_counter()
pygame.mixer.music.play()
while 1:
    if time.perf_counter() > next_call:
        next_call += 1/15
        os.system("clear")
        try:
            print(frames[frame])
        except IndexError:
            break
        frame += 1
