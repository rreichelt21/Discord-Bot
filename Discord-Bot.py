import discord
import os

from dotenv import load_dotenv
load_dotenv()

client = discord.Client(intents=discord.Intents.all())

#Prints to console when bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

#Sends a message on Discord server when user sends a !Hello command in chat
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

#Sends a message on Discord server when user sends a !kanye command in chat
    if message.content.startswith('!kanye'):
        await message.channel.send('https://open.spotify.com/playlist/37i9dQZF1DZ06evO3nMr04?si=8b5b982b9c744141')
        await message.channel.send('https://tenor.com/view/kanye-west-stare-staring-funny-gif-13590085')

client.run(os.getenv('DiscordToken'))
