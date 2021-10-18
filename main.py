import os
import discord

client = discord.Client()

@client.event
async def on_ready():
	print("We are live as {}".format(client.user))

@client.event
async def on_message(message):
	if message.author == client:
		return
	
	if message.content.startswith("/guru"):
		await message.channel.send("Hello there")


client.run(os.environ['TOKEN'])