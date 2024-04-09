from instagrapi import Client
import json

keys = json.loads(open('keys.json').read())

cl = Client()
ACCOUNT_USERNAME = keys['insta_username']
ACCOUNT_PASSWORD = keys['insta_password']
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
medias = cl.user_medias(user_id, 20)

clip_path = "test2.mp4"


cl.clip_upload(path= 'test2.mp4', caption= "Today's daily animal fact ! #Animals #animallovers #nature #planet #wildlife #wild", thumbnail= 'thumbnail.jpg')


