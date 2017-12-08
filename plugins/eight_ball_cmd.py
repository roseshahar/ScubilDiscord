import utils
import random
from functools import reduce

ANSWERS = [
    "Definitely",
    "Yes",
    "Probably",
    "Maybe",
    "Probably Not",
    "No",
    "Definitely Not",
    "I don't know",
    "Ask Later",
    "I'm too tired",
]


@utils.register_command('8ball')
def eight_ball_cmd(client, message, args):
    """
    gives you the right answer with pure magic
    ***----***
    """
    if args.endswith('?'):
        index = (int(message.author.id) + reduce(lambda x, y: x + y, map(ord, args))) % len(ANSWERS)
        return ANSWERS[index]
    return 'Please ask a question'
