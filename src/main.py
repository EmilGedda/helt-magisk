import datetime
import discord
import os
import subprocess
import threading

bot = discord.Client()
name = 'helt-magisk'
ver = '0.1.0'

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

@bot.event
async def on_ready():
    print('Starting {} v{}...'.format(name, ver))
    print('------')
    print('User: ' + bot.user.name)
    print('ID:   ' + bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if (message.content.startswith('!magisk') or
        message.content.startswith('!heltmagisk') or 
        message.content.startswith('!nairn') or
        message.content.startswith('!druggo')):

        chan = message.author.voice_channel
        now = datetime.datetime.now()
        print('[{}:{}:{}] Summoned by {}'.format(spad(now.hour),
                spad(now.minute), spad(now.second), message.author.name))

        voice = await bot.join_voice_channel(chan)
        song = afterski_short
    
        if (message.content.startswith('!druggo')):
            song = druggo
        elif (message.content.startswith('!nairn')):
            song = nairn
        elif (message.content.startswith('!heltmagisk')):
            song = afterski_long

        event = threading.Event()
        player = voice.create_ffmpeg_player(
                song, after=lambda: event.set())
        player.start()

        try:
            await bot.delete_message(message)
        except:
            print('Unable to delete message!')

        event.wait()
        await voice.disconnect()

def spad(s):
    if (s < 10):
        return '0' + str(s)
    return str(s)

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../.bot-token')
afterski_long = os.path.join(dir, '../afterski-long.ogg')
afterski_short = os.path.join(dir, '../afterski-short.ogg')
nairn = os.path.join(dir, '../nairn2.ogg')
druggo = os.path.join(dir, '../druggo.ogg')

with open(filename, 'r') as tokenfile:
    bot.run(tokenfile.read().replace('\n', ''))
