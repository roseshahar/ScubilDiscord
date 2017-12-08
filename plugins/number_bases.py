import discord
import string
import utils


@utils.register_command('hex2dec', ['bot'])
def hex_to_dec_cmd(client, message, args):
    """
    "hex2dec NUM": convert an hex number to decimal
    ***----***
    """
    if len(args) < 2:
        return 'Illegal'
    try:
        result = str(int(args, 16))
        if '0x' not in args.lower():
            args = '0x' + args
        return args + ' = ' + result
    except:
        return 'Illegal'


@utils.register_command('dec2hex', ['bot'])
def dec_to_hex_cmd(client, message, args):
    """
    "dec2hex NUM": convert a decimal number to hexadecimal
    ***----***
    """
    if len(args) < 2:
        return 'Illegal'
    try:
        num = int(args)
        return hex(num)
    except:
        return 'Illegal'


@utils.register_command('convert', ['bot'])
def num_converter_cmd(client, message, args):
    """
    "convert VAL": convert VAL
    ***----***
    """
    try:
        num = args.split(' ')[0]

        if num.startswith('0x'):
            decimal = int(num, 16)
            char = chr(decimal)
            octal = oct(decimal)
            binary = bin(decimal)
            hexa = num
        elif num.isdigit():
            decimal = int(num)
            char = chr(decimal)
            octal = oct(decimal)
            binary = bin(decimal)
            hexa = hex(decimal)
        else:
            decimal = ord(num)
            char = num
            octal = oct(decimal)
            binary = bin(decimal)
            hexa = hex(decimal)

        return discord.Embed(title='Conversion',
                             description=f'Decimal: {decimal}\nHexadecimal: {hexa}\nOctal: {octal}\n'
                                         f'Binary: {binary}\nUnicode: {char}',
                             color=3447003)
    except:
        return discord.Embed(title='Sorry', description='Correct Usage: $convert <input>', color=0xff5b4c)
