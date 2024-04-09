#!/bin/bash

# Run the python script
source /Users/jacobcote/3.9venv/bin/activate 

# Run the python script
python3 test.py

# Deactivate the virtual environment
deactivate

source /Users/jacobcote/instabotvenv/bin/Activate

python3 insta_bot.py

#remove temp files
rm thumbnail.jpg
rm test.mp4
rm test2.mp4
rm speech.mp3

