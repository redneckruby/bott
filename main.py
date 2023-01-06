import discord
import os
import threading
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
global val
val = False

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents, command_prefix='!')

tree = app_commands.CommandTree(client, fallback_to_global=True)


def ben():
    global val
    val = True
    print('Start')


def bon():
    global val
    val = False
    print('Stop')


@client.event
async def on_ready():
    await tree.sync(guild=None)
    print("Reddy")
    print("-------------")


@tree.command(name="henlo", guild=None)
async def henlo(ctx):
    """Responds with fren to command !henlo"""
    await ctx.response.send_message("fren")


@tree.command(name="frog", guild=None)
async def frog(ctx):
    """Responds with fren to command !henlo"""
    await ctx.response.send_message("🐸")


@tree.command(name="startfrog", guild=None)
async def start(ctx):
    """Begins reacting to every message with :frog:"""
    await ctx.response.send_message("Going froggie mode 🐸")
    ben()


@tree.command(name="stopfrog", guild=None)
async def stop(ctx):
    """Stops reacting to every message with :frog:"""
    await ctx.response.send_message("Going sleepy mode 😴")
    bon()


@client.event
async def on_message(message):
    emoji = '🐸'
    if val:
        await message.add_reaction(emoji)


client.run(TOKEN)
