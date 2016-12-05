import datetime
import discord
import os
import subprocess
import threading
import random

bot = discord.Client()
name = 'helt-magisk'
ver = '0.1.0'
FNULL =open(os.devnull, 'w')

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

@bot.event
async def on_ready():
    print('Starting {} v{}...'.format(name, ver))
    print('Copyright (C) 2016 Emil Gedda')
    print('User: ' + bot.user.name)
    print('ID:   ' + bot.user.id)
    indexsounds()
    print('Loaded sounds...')

@bot.event
async def on_message(messageobj):
    message = messageobj.content[1:]

    if message not in sounds:
        print('[{:02d}:{:02d}:{:02d}] {} tried to play played {}'.format(now.hour,
        now.minute, now.second, messageobj.author.name, message))
        return

    chan = messageobj.author.voice_channel
    now = datetime.datetime.now()
    voice = await bot.join_voice_channel(chan)
    song = random.choice(sounds[message])

    print('[{:02d}:{:02d}:{:02d}] {} played {}'.format(now.hour,
        now.minute, now.second, messageobj.author.name, song))

    event = threading.Event()
    player = voice.create_ffmpeg_player(
            song, after=lambda: event.set(),
            stderr=FNULL)
    player.start()

    try:
        await bot.delete_message(messageobj)
    except:
        print('Unable to delete message!')

    event.wait()
    sleep(0.05)
    await voice.disconnect()

def indexsounds():
    abspath = lambda d,f: list(map(lambda a: os.path.join(d, a), f))
    for root, category, files in os.walk(soundsdir):
        oggs = list(filter(lambda x: x.endswith('.ogg'), files))
        if not oggs:
            continue
        print("Found folder: {} => {}".format(os.path.basename(root), abspath(root, oggs)))

        sounds[os.path.basename(root)] = abspath(root, oggs)
        for sound in oggs:
            print("Found sound: {} => {}".format(os.path.splitext(sound)[0], abspath(root, [sound])))

            sounds[os.path.splitext(sound)[0]] = abspath(root, [sound])

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../.bot-token')
soundsdir = os.path.join(dir, '../sounds')
sounds = dict()

with open(filename, 'r') as tokenfile:
    bot.run(tokenfile.read().replace('\n', ''))
