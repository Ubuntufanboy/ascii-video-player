# The .asciivideo Codec 📺
### Feature rich video player with few dependencies. Works great with tty machines 🚀

There will be a demo picture and demo video here later!

# WARNING ⚠️
## This project is not fully functional yet and bugs do appear quite often. This is simply a testing phase to find these bugs

# Install instructions

### Currently we only support debian based distros but unoffical support for Arch, OpenSUSE, and other linux distrobutions are planned

1. ``sudo apt-get update``
2. ``sudo apt install ffmpeg python3 python3-pip``
3. ``python3 -m pip install --upgrade Pillow # Recent changes to Pillow might cause this to give an error but if it works, Great``
4. ``pip3 install tqdm``
5. ``pip3 install numpy``
6. ``pip3 install pygame``
7. ``sudo apt install git``
8. ``git clone https://github.com/Ubuntufanboy/ascii-video-player``

# Usage guide

1. have an mp4 file in the same folder or be prepared to provide the full video path
2. run ``python3 mp4_to_asciivideo.py your_file.mp4``
3. run ``python3 play.py the_same_video_file_but_not_mp4.asciivideo``
4. once done, run rm -rf target (This step will be removed in the future but for now you need to do it)

## PLEASE report any bugs to me in an issue (No such thing as a dumb question)!

I appriciate the support! 🛐
