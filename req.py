import requests
import spotipy.util as util

token = util.prompt_for_user_token(username,scope,client_id='a7864bbc8098453b903abd5008c5a38e',client_secret='4d7d1c6f760c49b4b858572921f9e649',redirect_uri='http://localhost:8888/callback')

class Req:
    def put( endpoint ):
        r = requests.put('https://api.spotify.com' + endpoint, headers={'Authorization': 'Bearer ' + token})

    def get( endpoint ):
        r = requests.get('https://api.spotify.com' + endpoint, headers={'Authorization': 'Bearer ' + token})

    def post( endpoint ):
        r = requests.post('https://api.spotify.com' + endpoint, headers={'Authorization': 'Bearer ' + token})