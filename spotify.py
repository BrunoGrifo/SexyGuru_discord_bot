import random
import os
import string
import requests
import urllib

def auth_url():
	base_url =  "https://accounts.spotify.com/authorize?"
	url_par = {
		'client_id':  os.environ['SPOTIFY_CLIENT_ID'],
		'response_type': 'code',
		'redirect_uri': 'https://Sexy-Guru-bot.brunogrifo.repl.co/callback' ,
		'state':  ''.join(random.choices(string.ascii_lowercase + string.digits, k = 16)),
		'scope': 'playlist-modify-public'
	}
	return base_url + urllib.parse.urlencode(url_par)