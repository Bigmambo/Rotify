import requests
import spotipy.util as util

username = "bigmambo"
scope = "streaming playlist-read-private playlist-read-collaborative user-library-read user-library-read playlist-modify-private user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played"
token = util.prompt_for_user_token(username,scope,client_id='a7864bbc8098453b903abd5008c5a38e',client_secret='4d7d1c6f760c49b4b858572921f9e649',redirect_uri='http://localhost:8888/callback')

def put( endpoint, parameters ):
    r = requests.put('https://api.spotify.com' + endpoint, headers={'Authorization': 'Bearer ' + token}, params=parameters)

def get( endpoint ):
    r = requests.get('https://api.spotify.com' + endpoint, headers={'Authorization': 'Bearer ' + token})
    return r

def post( endpoint ):
    r = requests.post('https://api.spotify.com' + endpoint, headers={'Authorization': 'Bearer ' + token})
