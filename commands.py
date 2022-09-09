import discord
from discord.ext import commands

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@client.event
async def on_member_join(member:discord.Member):
    
    guild = client.get_guild(974527457883471903) #Replace with your server ID

    #sends a private DM to user when they join the server
    await member.send(f'Welcome to the {guild.name} server, {member.mention}!')