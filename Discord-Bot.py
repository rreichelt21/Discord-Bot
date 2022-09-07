import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv
import youtube_dl
import asyncio

bot = commands.Bot(command_prefix = '/', intents=discord.Intents.all())

#Gets bot token from .env file
load_dotenv()

#Prints to terminal when bot is ready
@bot.event
async def on_ready():
    
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_member_join(member:discord.Member):
    
    guild = bot.get_guild(974527457883471903) #Replace with your server ID

    #sends a private DM to user when they join the server
    await member.send(f'Welcome to the {guild.name} server, {member.mention}!')

#Sends message in Discord channel when user sends a ! command in chat
@bot.event
async def on_message(message):
    
    if message.author == bot.user:
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

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")
@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")
@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

#Uses bot token from .env file in order to run bot
bot.run(os.getenv('DiscordToken'))