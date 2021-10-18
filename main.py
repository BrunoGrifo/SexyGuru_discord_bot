import os
import json
import discord
import requests
from jokepy import Jokepy

client = discord.Client()

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



client.run(os.environ['TOKEN'])