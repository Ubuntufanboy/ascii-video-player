import sys
import os
from shutil import rmtree
import cv2
from time import sleep

try:
    video_file = sys.argv[1]
except IndexError:
    print("Please provide a mp4 file")
    sys.exit(1)

if not os.path.isfile(video_file):
    print(f"{video_file} does not exist!")
    sys.exit(1)
if not video_file.endswith(".mp4"):
    print(f"{video_file}'s format is not supported!")
    sys.exit(1)

#Get video FPS
#It's gonna get used in the ffmpeg command to ensure that the audio and video are synced
video_file = os.path.abspath(video_file).replace("\\", "/")

# refresh img folder to prevent weird stuff
try:
    rmtree("target")
except FileNotFoundError:
    pass
except PermissionError:
    pass
if os.name == 'nt':
    os.system("mkdir target\\img")
    os.system("mkdir target\\audio")
else:
    os.system("mkdir target/img -p")
    os.system("mkdir target/audio -p")

# Extract audio from video
os.system(f"ffmpeg -i {video_file} target/audio/audio.mp3")

print("The audio has been extracted from the video sucessfully")

fps = cv2.VideoCapture(video_file)
fps = fps.get(cv2.CAP_PROP_FPS)

os.system(f"ffmpeg -i {video_file} -vf fps={fps} target/img/output%d.png") # Converts video into numbered png
                                                                        # At a rate of the video FPS

count = 0
dir_path = f"{os.getcwd()}/target/img"

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        if path.startswith("output") and path.endswith(".png"):
            count += 1

os.chdir("target")
os.system("mkdir metadata")
os.chdir("metadata")
os.system(f"printf {count} > framenum.txt")
os.chdir("..")
os.chdir("..")

os.system("tar cf target.tar.gz ./target")
exported = video_file.replace(".mp4", ".asciivideo")
os.system(f"mv target.tar.gz {exported}")
print("Finishing up...")
rmtree("target")
print("Done!")
print(f"Command to play video: python play.py {os.path.relpath(exported)} {fps}")
