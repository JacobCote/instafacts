from pathlib import Path
from openai import OpenAI
import json
import os
import pexelsPy
import requests
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import random
import json


with open('animals.txt') as file:
    lines = [line.rstrip() for line in file]
    
## load keys
keys = json.loads(open('keys.json').read())


## chose random animal
animal = random.choice(lines)


client = OpenAI( api_key=keys['openai_api_key'])

speech_file_path = Path(__file__).parent / "speech.mp3"
prompt = f"give me an interesting fact about the animal : {animal}. only give me the fact in a short text of about 100 words with a small introduction to spike the curiosity of a reader. the respons should be in a json format. fact : the fact "

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt},
    
  ]
)

fact_text = response.choices[0].message.content

fact_text = json.loads(fact_text)["fact"]

response = client.audio.speech.create(
  model="tts-1",
  voice="echo",
  input=fact_text,
)
response.stream_to_file('speech.mp3')
response.stream_to_file(speech_file_path)

pexels_api_key = keys['pexels_api_key']


api = pexelsPy.API(pexels_api_key)

api.search_videos(animal, page=1, results_per_page=5)
videos = api.get_videos()

durations = []
for i,video in enumerate(videos):
  durations.append(video.duration)

idx = 0
for ind,i in enumerate(durations):
  if i >30 and i < 60:
    print('ICI')
    idx = ind
    break
  else:
    idx = durations.index(max(durations))
  


url_video = 'https://www.pexels.com/video/' + str(videos[idx].id) + '/download'

r = requests.get(url_video)

# insert a new line after the 4th space for syncing with the audio
list_text = []
space_count = 0
last_index =0
for index,i in enumerate(fact_text):
  if i == ' ':
    space_count += 1
    if space_count == 4:
      space_count = 0
      list_text.append(fact_text[last_index:index] + '\n')
      last_index = index +1
  if index == len(fact_text)-1:
    list_text.append(fact_text[last_index:index] + '\n')


print(list_text)
fact_text = ''.join(list_text)

with open('text.txt', 'w+') as outfile:
    outfile.write(fact_text)

with open('test.mp4', 'wb') as outfile:
    outfile.write(r.content)
    
    
os.system('python3 -m aeneas.tools.execute_task \
    speech.mp3 \
    text.txt \
    "task_language=eng|os_task_file_format=json|is_text_type=plain" \
    map.json')

#load map.json
with open('map.json') as f:
  data = json.load(f)
  
end_time = float(data['fragments'][-1]['end'])

clip = VideoFileClip("test.mp4")

##crop the video to the length of the audio add 1 second for beginning and 1 second for the end
clip = clip.subclip(0, end_time+2)

## crop size for square video
w, h = clip.size
middle = (w/2, h/2)
side = min(w, h)
x1 = middle[0] - side/2
x2 = middle[0] + side/2
y1 = middle[1] - side/2
y2 = middle[1] + side/2
clip = clip.crop(x1, y1, x2, y2)

## add the audio
clip = clip.set_audio(AudioFileClip("speech.mp3"))

##add subtitles
subs = []
for i in data['fragments'] :
  start = float(i['begin'])
  end = float(i['end'])
  text = i['lines'][0]
  subs.append(((start, end), text))
  
## write the video
#adjust the font size to fit the video
font_size = clip.h//20

generator = lambda txt: TextClip(txt, font='Arial', fontsize=font_size, color='white', stroke_color='black', stroke_width=1).set_duration(2)


subtitles = SubtitlesClip(subs, generator)
result = CompositeVideoClip([clip, subtitles.set_pos(('center','center'))])

result.write_videofile("test2.mp4")


## make thumbnail






api.search_photos(animal, page=1, results_per_page=30)
photos = api.get_photos()

idx = random.randint(0, len(photos)-1)
photo = photos[idx]
img_url = 'https://www.pexels.com/photo/' + str(photo.id) + '/download'




r = requests.get(img_url)

with open('thumbnail.jpg', 'wb') as outfile:
    outfile.write(r.content)

## crop the thumbnail to a square
thumbnail = ImageClip('thumbnail.jpg')
w, h = thumbnail.size
middle = (w/2, h/2)
side = min(w, h)
x1 = middle[0] - side/2
x2 = middle[0] + side/2
y1 = middle[1] - side/2
y2 = middle[1] + side/2
thumbnail = thumbnail.crop(x1, y1, x2, y2)

## write image
thumbnail.save_frame("thumbnail.jpg")





  



