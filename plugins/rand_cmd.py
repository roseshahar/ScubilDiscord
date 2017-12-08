import utils
from random import randint


@utils.register_command('rand', ['bot'])
def rand_cmd(client, message, args):
    """
    "rand START END": generate a random number between START & END
    ***----***
    """
    if len(args) < 2:
        return 'Illegal'
    num1 = args.split(' ')[0]
    try:
        num2 = args.split(' ')[1]
    except:
        return 'Illegal'
    if not (num1.isdigit() and num2.isdigit()):
        return 'Illegal'
    try:
        return 'Result: ' + str(randint(float(num1), float(num2)))
    except:
        return 'LOL?'
