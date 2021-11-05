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
from flask_code import spotify_search
from flask_code import spotify_add_track



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

search_guide = """
>>> **Search Guide**

- /search album <album_input>

- /search artist <artist_input>

- /search track <track_input> | <track_input>,<artist_input>
"""

invalid_command = """```diff
- Warning! Invalid command.
```
"""
						
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


@bot.command(name = "hello")
async def hello(ctx):
	 	await ctx.send('Hello {}\n{}'.format(ctx.author.name, get_compliment()))


@bot.command(name = "guru")
async def guru(ctx):
		await ctx.send(get_fact())


@bot.command(name = "playlist")
async def playlist(ctx):
		response = spotify_playlist()
		print(response['external_urls']['spotify'])
		await ctx.send(response['external_urls']['spotify'])


@bot.command(name = "add")
async def add(ctx, arg):
		response = spotify_add_track(arg)
		await ctx.send(response)


@bot.command(name = "search")
async def search(ctx, *args):
		if len(args) < 2:
			await ctx.send(search_guide)
		elif args[0].lower() not in ["album", "artist", "track"]:
			await ctx.send(invalid_command)
			await ctx.send(search_guide)
		elif args[0].lower() == "track":
			result = spotify_search(args[0], " ".join(args[1:]))
			if not result or not result["tracks"]:
				await ctx.send("There are no tracks with that name!")
			dict_search_for(result["tracks"]["items"])
			await ctx.send(dict_search_for(result["tracks"]["items"]))

		#response = spotify_playlist()
		#await ctx.send(response['external_urls']['spotify'])
		else:
			await ctx.send("testing...")
		

def dict_search_for(json_dict):
	songs_list = ""
	for obj in json_dict:
		songs_list += "ID:{} \n{}\n\n".format(obj["id"], obj["external_urls"]["spotify"])
	
	search_guide = """>>> **Tracks** \n{}""".format(songs_list)
	return search_guide


keep_alive()
bot.run(os.environ['TOKEN'])