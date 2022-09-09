import discord
from discord.ext import commands
import wavelink
import os

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())