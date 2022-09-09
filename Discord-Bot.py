from modulefinder import IMPORT_NAME
import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv
import wavelink

client = commands.Bot(command_prefix = '/', intents=discord.Intents.all())

#Gets bot token from .env file
load_dotenv()

#Prints to terminal when bot is ready
@client.event
async def on_ready():
    
    print(f'We have logged in as {client.user}')

@client.event
async def on_member_join(member:discord.Member):
    
    guild = client.get_guild(974527457883471903) #Replace with your server ID

    #sends a private DM to user when they join the server
    await member.send(f'Welcome to the {guild.name} server, {member.mention}!')

#Sends message in Discord channel when user sends a ! command in chat
@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    #!help command
    if message.content.startswith('/help'):
        await message.channel.send('List of commands: /help, /hello, /kanye')

    #!hello command
    if message.content.startswith('/hello'):
        await message.channel.send('Hello!')

    #!kanye command
    if message.content.startswith('/kanye'):
        await message.channel.send('https://open.spotify.com/playlist/37i9dQZF1DZ06evO3nMr04?si=8b5b982b9c744141')
        await message.channel.send('https://tenor.com/view/kanye-west-stare-staring-funny-gif-13590085')

    #!clear command (with manage messages permission enabled, max 100 messages)
    if message.content.startswith('/clear') and message.author.guild_permissions.manage_messages is True:
            await message.channel.purge(limit=100)

class CustomPlayer(wavelink.Player):

    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()

# HTTPS and websocket operations
@client.event
async def on_ready():
    client.loop.create_task(connect_nodes())


# helper function
async def connect_nodes():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(
        bot=client,
        host='127.0.0.1',
        port=2333,
        password='@deve7hAy02',
    )


# events

@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f'Node: <{node.identifier}> is ready!')


@client.event
async def on_wavelink_track_end(player: CustomPlayer, track: wavelink.Track, reason):
    if not player.queue.is_empty:
        next_track = player.queue.get()
        await player.play(next_track)


# commands

@client.command()
async def connect(ctx):
    vc = ctx.voice_client # represents a discord voice connection
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        return await ctx.send("Please join a voice channel to connect.")

    if not vc:
        await ctx.author.voice.channel.connect(cls=CustomPlayer())
    else:
        await ctx.send("The bot is already connected to a voice channel")


@client.command()
async def disconnect(ctx):
    vc = ctx.voice_client
    if vc:
        await vc.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def play(ctx, *, search: wavelink.YouTubeTrack):
    vc = ctx.voice_client
    if not vc:
        custom_player = CustomPlayer()
        vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)

    if vc.is_playing():

        vc.queue.put(item=search)

        await ctx.send(embed=discord.Embed(
            title=search.title,
            url=search.uri,
            author=ctx.author,
            description=f"Queued {search.title} in {vc.channel}"
        ))
    else:
        await vc.play(search)

        await ctx.send(embed=discord.Embed(
            title=vc.source.title,
            url=vc.source.uri,
            author=ctx.author,
            description=f"Playing {vc.source.title} in {vc.channel}"
        ))


@client.command()
async def skip(ctx):
    vc = ctx.voice_client
    if vc:
        if not vc.is_playing():
            return await ctx.send("Nothing is playing.")
        if vc.queue.is_empty:
            return await vc.stop()

        await vc.seek(vc.track.length * 1000)
        if vc.is_paused():
            await vc.resume()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    vc = ctx.voice_client
    if vc:
        if vc.is_playing() and not vc.is_paused():
            await vc.pause()
        else:
            await ctx.send("Nothing is playing.")
    else:
        await ctx.send("The bot is not connected to a voice channel")


@client.command()
async def resume(ctx):
    vc = ctx.voice_client
    if vc:
        if vc.is_paused():
            await vc.resume()
        else:
            await ctx.send("Nothing is paused.")
    else:
        await ctx.send("The bot is not connected to a voice channel")


# error handling

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Could not find a track.")
    else:
        await ctx.send("Please join a voice channel.")

#Uses bot token from .env file in order to run bot
client.run(os.getenv('DiscordToken'))
