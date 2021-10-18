import discord

client = discord.Client()

@client.event
async def on_ready():
	print("We are live as {}".format(client))

@client.event
async def on_message(message):
	if message.author == client:
		return
	
	if message.content.startwith("/guru"):
		await message.channel.send("Hello there")