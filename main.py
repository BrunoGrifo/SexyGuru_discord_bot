import os
import string
import json
import random
import discord
import requests
from jokepy import Jokepy
import urllib
from discord.ext import commands


from flask_code import keep_alive
from flask_code import spotify_playlist



bot = commands.Bot(command_prefix='/')

bad_words = ["fdx", "foda-se", "crlh", "caralho", "puta", "merda", "putedo", "cona", "paneleiro", "foder", "porra", "cabrão", "cabrao", "badalhoco", "badalhoca", "anormal", "rabeta", "xupa", "xupa-mos", "porca", "rabilas", "merdoso", "fufa", "caralhinho", "punheta", "canalha", "bicha", "bichona"]

bad_words_lecture = [
"Fala bem que já tens dentes!", 
"Reparei que disseste uma palavra feia...voltas a dizer uma dessas e levas um rotativo nos olhos!",
"Palavras feias não são bem vindas no Reino do Grifo",
"Cristão não fala palavrão!",
"Xô Satanás! Vai dizer palavrões para longe!",
"Pai nosso que estás no céu perdoai este pecador pois ele não sabe falai em condições e livrai-lhe de todos os palavrões, amén."
]
						
def loginSpotify():
	base_url =  "https://accounts.spotify.com/authorize?"
	url_par = {
		'client_id':  os.environ['SPOTIFY_CLIENT_ID'],
		'response_type': 'code',
		'redirect_uri': 'http://localhost:8888/callback/' ,
		'state':  ''.join(random.choices(string.ascii_lowercase + string.digits, k = 16)),
		'scope': 'playlist-modify-public'
	}
	response = requests.get(base_url + urllib.parse.urlencode(url_par))
	return response.json()
	
def get_joke():
	j = Jokepy(categories=['Dark'])  # Initialise the class
	return j.get_joke()

def get_compliment():
	response = requests.get('https://complimentr.com/api')
	json_data = json.loads(response.text)
	return json_data['compliment']

def get_fact():
	response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
	json_data = json.loads(response.text)
	return json_data['text']

@bot.event
async def on_ready():
	print("We are live as {}".format(bot.user))

@bot.event
async def on_message(message):
	if any(word.lower() in message.content for word in bad_words):
			await message.channel.send(random.choice(bad_words_lecture))
	await bot.process_commands(message)

@bot.command(name = "test")
async def test(ctx, *args):
	 await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

@bot.command(name = "hello")
async def hello(ctx):
	 await ctx.send('Hello {}\n{}'.format(ctx.author.name, get_compliment()))

@bot.command(name = "guru")
async def guru(ctx):
	 await ctx.send(get_fact())





keep_alive()
bot.run(os.environ['TOKEN'])