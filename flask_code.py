#import random
import os
#import string
import requests
#import urllib
import base64
import json

from flask import Flask
#from flask import make_response
from flask import session
from flask import redirect
from flask import request
from threading import Thread

from spotify import auth_url
from spotify import authorize
from spotify import get_playlist
from spotify import get_search

from replit import db

SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com"
SPOTIFY_TOKEN_URL = "{}/{}".format(SPOTIFY_AUTH_BASE_URL, 'api/token')


app = Flask('')
app.secret_key = "sexyguru"

@app.route('/')
def auth():
	return redirect(auth_url())

@app.route('/callback')
def callback():
	auth_token = request.args['code']
	auth_header = authorize(auth_token)
	db['auth_header'] = auth_header
	return "Guru authorized"

def spotify_playlist():
	refresh_token()
	result = get_playlist(db['auth_header'], "3ZG0ZD5d6pMNKvhf6sfGHj")
	return result

def spotify_search(arg1, arg2):
	result = get_search(db['auth_header'], arg1, arg2)
	#refresh_token(db['auth_header'])
	return result


def refresh_token():
	base64encoded = base64.b64encode(("{}:{}".format(os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET'])).encode())
	headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
	code_payload = {
		"grant_type": "refresh_token",
		"refresh_token": db["refresh_token"]
	}
	post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)
	response_data = json.loads(post_request.text)
	access_token = response_data["access_token"]
	auth_header = {"Authorization": "Bearer {}".format(access_token)}
	db['auth_header'] = auth_header

def run():
	app.run(host='0.0.0.0', port=8080)

def keep_alive():
	t = Thread(target=run)
	t.start()