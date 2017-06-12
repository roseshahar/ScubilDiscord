import discord
import asyncio
from commands import commands

client = discord.Client()

token = open('token.txt').read().strip('\n')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('$'):
        command = message.content.strip('$').split(' ')[0]
        args = message.content.replace('$' + command + ' ', '', 1)
        if command in commands.keys():
            await client.send_message(message.channel, message.author.mention)
            await commands[command](client, message, args)
        else:
            await client.send_message(message.channel, message.author.mention + '\n"${}" is not supported!'.format(command))

        # if message.content.startswith('!test'):
        #     await client.send_message(message.channel, 'Here is you test message, @' + message.author.name)
        # elif message.content.startswith('!sleep'):
        #     await asyncio.sleep(5)
        #     await client.send_message(message.channel, 'Done sleeping')


client.run(token)
