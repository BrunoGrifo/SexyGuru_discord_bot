import random
import os
import json
import string
import requests
import urllib
import base64

# spotify endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com"
SPOTIFY_AUTH_URL = "{}/{}".format(SPOTIFY_AUTH_BASE_URL, 'authorize?')
SPOTIFY_TOKEN_URL = "{}/{}".format(SPOTIFY_AUTH_BASE_URL, 'api/token')
SPOTIFY_TRACK_URL = "{}/{}/{}".format(SPOTIFY_AUTH_BASE_URL, 'v1', 'tracks')




def auth_url():
	url_par = {
		'client_id':  os.environ['SPOTIFY_CLIENT_ID'],
		'response_type': 'code',
		'redirect_uri': os.environ['REDIRECT_URI'],
		'state':  ''.join(random.choices(string.ascii_lowercase + string.digits, k = 16)),
		'scope': 'playlist-modify-public'
	}
	return SPOTIFY_AUTH_URL + urllib.parse.urlencode(url_par)

def authorize(auth_token):

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": os.environ['REDIRECT_URI']
    }
    
    base64encoded = base64.b64encode(("{}:{}".format(os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET'])).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header

def get_playlist(auth_header, track_id):
    url = "{}/{}".format(SPOTIFY_TRACK_URL, track_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()

