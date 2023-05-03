import sys
import os

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

# refresh img folder to prevent weird stuff
os.system("rm -rf target")
os.system("mkdir target/img -p")
os.system("mkdir target/audio -p")
# Get random audio name to prevent overwriting

# Extract audio from video
os.system(f"ffmpeg -i {video_file} target/audio/audio.mp3")

print("Congrats! The audio has been extracted from the video sucessfully")

os.system(f"ffmpeg -i {video_file} -vf fps=15 target/img/output%d.png")

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
print("finishing up...")
os.system("rm -rf target")
print("done!")
