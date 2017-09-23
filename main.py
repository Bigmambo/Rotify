import sys
import spotipy
import spotipy.util as util
from req import Req
import RPi.GPIO as GPIO
import gaugette.rotary_encoder
import json
import time

username = "bigmambo"
scope = "streaming playlist-read-private playlist-read-collaborative user-library-read user-library-read playlist-modify-private user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played"
token = util.prompt_for_user_token(username,scope,client_id='a7864bbc8098453b903abd5008c5a38e',client_secret='4d7d1c6f760c49b4b858572921f9e649',redirect_uri='http://localhost:8888/callback')
sp = spotipy.Spotify(auth=token)

encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(7, 10)
encoder.start()

chan_list = [8]
GPIO.setmode(GPIO.BOARD)
GPIO.setup(chan_list, GPIO.IN)
GPIO.add_event_detect(8, GPIO.RISING, callback=play_pause, bouncetime=200)

def volume():
    v = get('/v1/me/player')
    v_json = json.loads(v)
    vol = v_json["volume_percent"]
    return vol

def play_pause(channel):
    r = get('/v1/me/player')
    play_pause_json = json.loads(r)
    if play_pause_json["is_playing"] == "true":
        put('/v1/me/player/play')
    else:
        put('/v1/me/player/pause')

def volume_knob():
    v = volume()
    delta = encoder.get_delta()
    if delta!=0:
        vol = (5 * (v/5)) + (delta * 5)
        if vol < 0:
            vol = 0
        elif vol > 100:
            vol = 100
    put('/v1/me/player/volume', vol)

while True:
    volume = volume_knob()
