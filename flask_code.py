import random
import os
import string
import requests
import urllib

from flask import Flask
from flask import make_response
from flask import redirect
from flask import request
from threading import Thread

from spotify import auth_url


app = Flask('')

@app.route('/')
def auth():
	return redirect(auth_url())

@app.route('/callback')
def authorize():
	auth_token = request.args['code']
	print(auth_token)
	return "Guru authorized"


def run():
	app.run(host='0.0.0.0', port=8080)

def keep_alive():
	t = Thread(target=run)
	t.start()