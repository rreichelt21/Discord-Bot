import discord
import os
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()

client = discord.Client(intents=discord.Intents.all())

#Prints to terminal when bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

#Sends message in Discord channel when user sends a ! command in chat
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #!help command
    if message.content.startswith('!help'):
        await message.channel.send('List of commands: !help, !hello, !kanye')

    #!hello command
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    #!kanye command
    if message.content.startswith('!kanye'):
        await message.channel.send('https://open.spotify.com/playlist/37i9dQZF1DZ06evO3nMr04?si=8b5b982b9c744141')
        await message.channel.send('https://tenor.com/view/kanye-west-stare-staring-funny-gif-13590085')

    #!clear command (with manage messages permission, max 100 messages)
    if message.content.startswith('!clear'):
        if message.author.guild_permissions.manage_messages:
            await message.channel.purge(limit=100)
        else:
            await message.channel.send('You do not have permission to clear the channel.')

@client.event
async def on_member_join(user, member):
    
    #sends a private DM to user when they join the server
    message = f'Welcome to the server {member.mention}!'
    await user.send(message)

client.run(os.getenv('DiscordToken'))