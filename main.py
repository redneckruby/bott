import discord
import os
import atexit
from discord import app_commands
from dotenv import load_dotenv


# defines intents
intents = discord.Intents.default()

# allows message content to be accessed and manipulated
intents.message_content = True

# global check variables
global val
val = False
global check
check = False

# allows token to be stored in ENV file securely
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# defines client intents and commands
client = discord.Client(intents=intents, command_prefix='!')

# makes tree for commands
tree = app_commands.CommandTree(client, fallback_to_global=True)


# sets val true, starting frog reactions
def begin():
    global val
    val = True
    print('Start')


# sets val false, starting frog reactions
def end():
    global val
    val = False
    print('Stop')


# saves archive when program exits
def exit_handler():
    print('Exiting . . .')
    if check:
        print('Saving file')
        global outfile
        outfile.close()


# prints message when login and connection is successful (bot is up and running)
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
    begin()


@tree.command(name="stopfrog", guild=None)
async def stop(ctx):
    """Stops reacting to every message with :frog:"""
    await ctx.response.send_message("Going sleepy mode 😴")
    end()


@tree.command(name="archivefrog", guild=None)
async def readwrite(ctx):
    """Reads and write every message in channel to archive.txt"""
    await ctx.response.send_message("Archiving 🐸")
    global check
    check = True

    global outfile
    outfile = open('archive.txt', 'a', encoding='utf-8')


@tree.command(name="noarchivefrog", guild=None)
async def end(ctx):
    """Stops archiving messages"""
    await ctx.response.send_message("Not archiving 😔")
    global check
    check = False

    global outfile
    outfile.close()


@tree.command(name="allarchivefrog", guild=None)
async def arc(ctx):
    """Archives all messages"""
    global outfile
    outfile = open('archive.txt', 'a', encoding='utf-8')

    await archive_all(ctx, outfile)
    await ctx.followup.send('Done!')


# archives each message in a channel
async def archive_all(para, file):

    await para.response.send_message("Archiving all messages in channel . . .")

    async for message in para.channel.history(limit=None, oldest_first=True):
        try:

            print(f'{str(message.attachments)}:{str(message.created_at)}:{str(message.channel)}:'
                  f'{str(message.author)}:{str(message.content)}')

            file.write(f'|{str(message.attachments)}:{str(message.created_at)}:{str(message.channel)}:'
                          f'{str(message.author)}:{str(message.content)}|\n')

        except UnicodeEncodeError:
            print('Unicode encoding error')
        except ValueError:
            print('Error converting message to string')
        except:
            print('Error')

    file.close()
    print('All messages archived and saved')


# for each message, if val add reaction frog
# if check, archive message
@client.event
async def on_message(message):
    if val:
        await message.add_reaction('🐸')

    if check:
        try:
            print('archiving...')

            print(f'{str(message.attachments)}:{str(message.created_at)}:{str(message.channel)}:'
                  f'{str(message.author)}:{str(message.content)}')

            outfile.write(f'|{str(message.attachments)}:{str(message.created_at)}:{str(message.channel)}:'
                          f'{str(message.author)}:{str(message.content)}|\n')

            await message.add_reaction('📚')

        except UnicodeEncodeError as err:
            print(err)
            print('Error writing emoji')
        except ValueError:
            print('Error converting message to string')
        except:
            print('Error')


# run at program exit
atexit.register(exit_handler)

client.run(TOKEN)
