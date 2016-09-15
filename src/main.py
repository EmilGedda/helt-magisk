import discord

bot = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print('User: ' + client.user.name)
    print('ID:   ' + client.user.id)
    print('------')

with open('../.bot-token', 'r') as tokenfile:
    bot.run(tokenfile.read().replace('\n', ''))
