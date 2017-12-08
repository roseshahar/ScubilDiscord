import os
import re
import sys
import utils
import discord
import asyncio
import inspect
from plugins import *
from collections import namedtuple

Command = namedtuple('Command', 'function channels more_args')
DIR = os.path.dirname(__file__) + '/'
TOKEN_PATH = 'token.txt'
CMD_SIGN = '%'

if len(sys.argv) > 1:
    TOKEN_PATH = sys.argv[1]
TOKEN = open(TOKEN_PATH).read().strip('\n')

commands = {}
client = discord.Client()


@client.event
async def on_member_join(member):
    server = member.server
    fmt = "Welcome {0.mention}!\n"
    await client.send_message(server, server.owner.top_role.mention + '\n ' + fmt.format(member))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


async def process_cmd(message):
    split = message.content[1:].split()
    cmd = split[0]
    args = ' '.join(split[1:])

    if cmd in commands.keys():
        if commands[cmd].channels is None:
            if inspect.iscoroutinefunction(commands[cmd].function):
                await commands[cmd].function(client, message, args, **commands[cmd].more_args)
            else:
                ans = commands[cmd].function(client, message, args, **commands[cmd].more_args)
                if type(ans) is str:
                    await client.send_message(message.channel, message.author.mention + '\n' + ans)
                elif type(ans) is discord.Embed:
                    await client.send_message(message.channel, message.author.mention, embed=ans)
        elif any([utils.is_right_channel(message.channel.name, channel) for channel in commands[cmd].channels]):
            if inspect.iscoroutinefunction(commands[cmd].function):
                await commands[cmd].function(client, message, args, **commands[cmd].more_args)
            else:
                ans = commands[cmd].function(client, message, args, **commands[cmd].more_args)
                if type(ans) is str:
                    await client.send_message(message.channel, message.author.mention + '\n' + ans)
                elif type(ans) is discord.Embed:
                    await client.send_message(message.channel, message.author.mention, embed=ans)
        else:
            await client.send_message(message.channel, '**Oops...**  you can\'t use that command in this channel')
    else:
        await client.send_message(message.channel, '**Oops...**  unknown command *{1}{0}* \n'
                                                   '(use {1}help to see the list of commands)'.format(cmd, CMD_SIGN))


@utils.register_command('help', ['bot'])
async def get_help(bot, message, args):
    """
    Sends a 'help' message
    ***----***
    """
    help_msg = "**__Help:__**\n\n"

    for command_name, command_func, command_channels, command_args in utils.register_command.functions_list:
        if hasattr(command_func, '__doc__') and isinstance(command_func.__doc__, str):
            doc = command_func.__doc__.split("***----***")[0].lstrip().rstrip()
        else:
            doc = ""
        help_msg += "**%s%s** - *%s*\n" % (CMD_SIGN, command_name, doc)
    await bot.send_message(message.channel, help_msg)


@utils.register_command('ping', ['bot'])
async def ping_cmd(bot, message, args):
    """
    return a pong
    ***----***
    """
    await bot.send_message(message.channel, "Pong!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith(CMD_SIGN):
        await process_cmd(message)
    if re.match("^ע[ד]+[ ]*מת[י]+$", message.content):
        await client.send_message(message.channel, message.author.mention + '\nשתוק יצעיר פעור ולח')

for cmd_name, cmd_func, cmd_channels, cmd_args in utils.register_command.functions_list:
    commands[cmd_name] = Command(function=cmd_func, channels=cmd_channels, more_args=cmd_args)
client.run(TOKEN)
