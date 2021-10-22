import os
import json
import random
import discord
import requests
from jokepy import Jokepy

client = discord.Client()

bad_words = ["fdx", "foda-se", "crlh", "caralho", "puta", "merda", "putedo", "cona", "paneleiro", "foder", "porra", "cabrão", "cabrao", "badalhoco", "badalhoca", "anormal", "rabeta", "xupa", "xupa-mos", "porca", "rabilas", "merdoso", "fufa", "caralhinho", "punheta", "canalha", "bicha", "bichona"]

bad_words_lecture = [
"Fala bem que já tens dentes!", 
"Reparei que disseste uma palavra feia...voltas a dizer uma dessas e levas um rotativo nos olhos!",
"Palavras feias não são bem vindas no Reino do Grifo",
"Cristão não fala palavrão!",
"Xô Satanás! Vai dizer palavrões para longe!",
"Pai nosso que estás no céu perdoai este pecador pois ele não sabe falai em condições e livrai-lhe de todos os palavrões, amén."
]

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

@client.event
async def on_ready():
	print("We are live as {}".format(client.user))

@client.event
async def on_message(message):
	if message.author == client:
		return

	if message.content.startswith("/hello"):
		await message.channel.send('Hello {}\n{}'.format(message.author.name, get_compliment()))
	
	if message.content.startswith("/guru"):
		await message.channel.send(get_fact())

	if any(word.lower() in message.content for word in bad_words):
		await message.channel.send(random.choice(bad_words_lecture))







client.run(os.environ['TOKEN'])