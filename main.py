import sys
import spotipy
import spotipy.util as util
from req import Req
import RPi.GPIO as GPIO
import json

username = "bigmambo"
scope = "streaming playlist-read-private playlist-read-collaborative user-library-read user-library-read playlist-modify-private user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played"
token = util.prompt_for_user_token(username,scope,client_id='a7864bbc8098453b903abd5008c5a38e',client_secret='4d7d1c6f760c49b4b858572921f9e649',redirect_uri='http://localhost:8888/callback')
sp = spotipy.Spotify(auth=token)

chan_list = [8]
GPIO.setmode(GPIO.BOARD)
GPIO.setup(chan_list, GPIO.IN)

def play_pause(channel):
    play_pause_json = json.loads(req.get('/v1/me/player'))
    if play_pause_json["is_playing"] == "true":
        req.put('/v1/me/player/play')
    else:
        req.put('/v1/me/player/pause')

GPIO.add_event_detect(8, GPIO.RISING, callback=play_pause, bouncetime=200)
