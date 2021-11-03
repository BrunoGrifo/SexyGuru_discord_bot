#import random
#import os
#import string
#import requests
#import urllib

from flask import Flask
#from flask import make_response
from flask import session
from flask import redirect
from flask import request
from threading import Thread

from spotify import auth_url
from spotify import authorize


app = Flask('')
app.secret_key = "sexyguru"

@app.route('/')
def auth():
	return redirect(auth_url())

@app.route('/callback')
def callback():
	auth_token = request.args['code']
	auth_header = authorize(auth_token)
	session['auth_header'] = auth_header
	return "Guru authorized"

def spotify_playlist():
	print(session['auth_header'])


def run():
	app.run(host='0.0.0.0', port=8080)

def keep_alive():
	t = Thread(target=run)
	t.start()