from collections import namedtuple
from functools import wraps

Command = namedtuple('Command', 'name function channels more_args')
ChName = namedtuple('ChannelName', 'string is_part')


def function_registerer():
    """
    create a list of functions from all the functions that @ that function
    """
    functions_list = []

    def registrar_warp(name, available_at=None, more_args=None):
        if more_args is None:
            more_args = {}
        if available_at is None:
            channels = None
        else:
            channels = []
            for ch_name in available_at:  # type: str
                if ch_name.startswith('#'):
                    channels.append(ChName(string=ch_name[1:], is_part=False))
                else:
                    channels.append(ChName(string=ch_name, is_part=True))

        def registrar(func):
            functions_list.append(Command(name=name, function=func, channels=channels, more_args=more_args))
            return func

        return registrar

    registrar_warp.functions_list = functions_list
    return registrar_warp


def admin(func):
    @wraps(func)
    def wrapped(client, message, args):
        if message.author.server.owner.top_role not in message.author.roles:
            return
        return func(client, message, args)
    return wrapped


def is_right_channel(name_str, channel_name):
    if channel_name.is_part:
        return name_str in channel_name
    else:
        return name_str == channel_name.string


register_command = function_registerer()
