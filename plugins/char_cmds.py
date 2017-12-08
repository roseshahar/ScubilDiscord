import utils


@utils.register_command('ord', ['bot'])
def ord_cmd(client, message, args):
    """
    "ord CHAR": display the ascii value of a CHAR
    ***----***
    """
    if len(args) != 1:
        return 'Illegal'
    try:
        dec = ord(args)
        hexa = hex(dec)
        return "'" + args + "' = " + str(dec) + " dec / " + hexa + " hex"
    except:
        return 'Illegal'


@utils.register_command('chr', ['bot'])
def chr_cmd(client, message, args):
    """
    "chr NUM": convert NUM to a char
    ***----***
    """
    if 'x' in args:
        try:
            args = str(int(args, 16))
        except:
            return 'Illegal'
    if len(args) < 2 or not args.isdigit():
        return 'Illegal'

    try:
        return 'chr({}) = {}'.format(args, chr(int(args)))
    except:
        return '123'
