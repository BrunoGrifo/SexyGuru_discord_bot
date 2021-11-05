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
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
SPOTIFY_PLAYLIST_URL = "{}/{}/{}".format(SPOTIFY_API_BASE_URL, 'v1', 'playlists')
SPOTIFY_SEARCH_URL = "{}/{}/{}".format(SPOTIFY_API_BASE_URL, 'v1', 'search')




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

def get_playlist(auth_header, playlist_id):
		url = "{}/{}".format(SPOTIFY_PLAYLIST_URL, playlist_id)
		resp = requests.get(url, headers=auth_header)
		return resp.json()

def get_search(auth_header, arg1, arg2):
		url_par = {
			"type": arg1,
			"q": arg2,
			"limit": 5
		}
		search = urllib.parse.urlencode(url_par)
		url = "{}?{}".format(SPOTIFY_SEARCH_URL, search)
		resp = requests.get(url, headers=auth_header)
		return resp.json()

