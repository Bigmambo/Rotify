import sys
import spotipy
import spotipy.util as util
import Req
import RPi.GPIO as GPIO
import threading
import json
import time

username = "bigmambo"
scope = "streaming playlist-read-private playlist-read-collaborative user-library-read user-library-read playlist-modify-private user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played"
token = util.prompt_for_user_token(username,scope,client_id='a7864bbc8098453b903abd5008c5a38e',client_secret='4d7d1c6f760c49b4b858572921f9e649',redirect_uri='http://localhost:8888/callback')
sp = spotipy.Spotify(auth=token)
Button_A = 8
Enc_A1 = 7
Enc_A2 = 10

chan_list = [Button_A, Enc_A1, Enc_A2]
GPIO.setmode(GPIO.BOARD)
GPIO.setup(chan_list, GPIO.IN)

delta = 0
Current_A1 = 1
Current_A2 = 1
Switch_A1 = GPIO.input(Enc_A1)
Switch_A2 = GPIO.input(Enc_A2)
LockRotary = threading.Lock()

def rotary_interrupt(A_or_B):
    global delta, Current_A1, Current_A2, LockRotary

    if Current_A1 == Switch_A1 and Current_A2 == Switch_A2:
        return

    Current_A1 = Switch_A1
    Current_A2 = Switch_A2

    if (Switch_A1 and Switch_A2):
        LockRotary.acquire()
        if A_or_B == Enc_A2:
            delta += 1
        else:
            delta -= 1
        LockRotary.release()
    return


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
    if delta!=0:
        vol = (5 * (v/5)) + (delta * 5)
        if vol < 0:
            vol = 0
        elif vol > 100:
            vol = 100
    put('/v1/me/player/volume', vol)
    delta = 0

def main():

    GPIO.add_event_detect(Button_A, GPIO.RISING, callback=play_pause, bouncetime=200)
    GPIO.add_event_detect(Enc_A1, GPIO.RISING, callback=rotary_interrupt)
    GPIO.add_event_detect(Enc_A2, GPIO.RISING, callback=rotary_interrupt)

    while True:
        time.sleep(0.1)
        volume = volume_knob()

main()
