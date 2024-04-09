#!/bin/bash

if [ ! -d ./venv ]; then
  echo "Creating virtual environment..."
  python -m venv venv
  source /Users/jacobcote/venv/bin/activate 
  pip install -r requirements.txt
fi
if [ ! -d ./venv ]; then
  source /Users/jacobcote/venv/bin/activate 
fi


# Run the python script
python3 test.py

# Deactivate the virtual environment
deactivate

source /Users/jacobcote/instabotvenv/bin/Activate

python3 insta_bot.py

#remove temp files
rm thumbnail.jpg
rm test.mp4
rm text.txt
rm test2.mp4
rm speech.mp3

