import sys
import spotipy
import spotipy.util as util
import req
import RPi.GPIO as GPIO
import threading
import json
import time

username = "bigmambo"
scope = "streaming playlist-read-private playlist-read-collaborative user-library-read user-library-read playlist-modify-private user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played"
token = util.prompt_for_user_token(username,scope,client_id='a7864bbc8098453b903abd5008c5a38e',client_secret='4d7d1c6f760c49b4b858572921f9e649',redirect_uri='http://localhost:8888/callback')
sp = spotipy.Spotify(auth=token)
Button_A = 23
Button_B = 16
Button_C = 21
Enc_A1 = 24
Enc_A2 = 22
Enc_B1 = 5
Enc_B2 = 6
Enc_C1 = 13
Enc_C2 = 19

chan_list = [Button_A, Button_B, Button_C, Enc_A1, Enc_A2, Enc_B1, Enc_B2, Enc_C1, Enc_C2]
GPIO.setmode(GPIO.BCM)

GPIO.setup(Button_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Button_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Button_C, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Enc_A1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Enc_A2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Enc_B1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Enc_B2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Enc_C1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Enc_C2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

delta1 = 0
delta2= 0
delta3 = 0
Current_A1 = 1
Current_A2 = 1
Current_B1 = 1
Current_B2 = 1
Current_C1 = 1
Current_C2 = 1
Switch_A1 = GPIO.input(Enc_A1)
Switch_A2 = GPIO.input(Enc_A2)
Switch_B1 = GPIO.input(Enc_B1)
Switch_B2 = GPIO.input(Enc_B2)
Switch_C1 = GPIO.input(Enc_C1)
Switch_C2 = GPIO.input(Enc_C2)
LockRotary = threading.Lock()

def rotary_interrupt1(A1_or_A2):
    global delta1, Current_A1, Current_A2, LockRotary

    if Current_A1 == Switch_A1 and Current_A2 == Switch_A2:
        return

    Current_A1 = Switch_A1
    Current_A2 = Switch_A2

    if (Switch_A1 and Switch_A2):
        LockRotary.acquire()
        if A1_or_A2 == Enc_A2:
            delta1 += 1
        else:
            delta1 -= 1
        LockRotary.release()
    return

def rotary_interrupt2(B1_or_B2):
    global delta2, Current_B1, Current_B2, LockRotary

    if Current_B1 == Switch_B1 and Current_B2 == Switch_B2:
        return

    Current_B1 = Switch_B1
    Current_B2 = Switch_B2

    if (Switch_B1 and Switch_B2):
        LockRotary.acquire()
        if B1_or_B2 == Enc_B2:
            delta2 += 1
        else:
            delta2 -= 1
        LockRotary.release()
    return

def rotary_interrupt3(C1_or_C2):
    global delta3, Current_C1, Current_C2, LockRotary

    if Current_C1 == Switch_C1 and Current_C2 == Switch_C2:
        return

    Current_C1 = Switch_C1
    Current_C2 = Switch_C2

    if (Switch_C1 and Switch_C2):
        LockRotary.acquire()
        if C1_or_C2 == Enc_C2:
            delta3 += 1
        else:
            delta3 -= 1
        LockRotary.release()
    return

def volume():
    v = req.get('/v1/me/player')
    v_json = json.loads(v)
    vol = v_json["volume_percent"]
    return vol

def play_pause(channel):
    r = req.get('/v1/me/player')
    play_pause_json = json.loads(r)
    if play_pause_json["is_playing"] == "true":
        req.put('/v1/me/player/play')
    else:
        req.put('/v1/me/player/pause')

def volume_knob():
    v = volume()
    vol = (5 * (v/5)) + (delta1 * 5)
    if vol < 0:
        vol = 0
    elif vol > 100:
        vol = 100
    req.put('/v1/me/player/volume', vol)
    delta1 = 0

def next_track(channel):
    req.post('/v1/me/player/next')

def previous_track(channel):
    req.post('/v1/me/player/previous')

def main():

    GPIO.add_event_detect(Button_A, GPIO.RISING, callback=play_pause, bouncetime=200)
    GPIO.add_event_detect(Button_B, GPIO.RISING, callback=next_track, bouncetime=200)
    GPIO.add_event_detect(Button_C, GPIO.RISING, callback=previous_track, bouncetime=200)
    GPIO.add_event_detect(Enc_A1, GPIO.RISING, callback=rotary_interrupt1)
    GPIO.add_event_detect(Enc_A2, GPIO.RISING, callback=rotary_interrupt1)
    GPIO.add_event_detect(Enc_B1, GPIO.RISING, callback=rotary_interrupt2)
    GPIO.add_event_detect(Enc_B2, GPIO.RISING, callback=rotary_interrupt2)
    GPIO.add_event_detect(Enc_C1, GPIO.RISING, callback=rotary_interrupt3)
    GPIO.add_event_detect(Enc_C2, GPIO.RISING, callback=rotary_interrupt3)

    while True:
        time.sleep(0.1)
        if delta1 != 0:
            volume_knob()
            print(delta1)


main()
