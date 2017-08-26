import os
import pickle

import time

import utils

user_data = {}
_karma_file = 'karma.pkl'
_file_loaded = False
_last_karma_time = {}
_time_between_karma = 60 * 30  # half an hour, in seconds


def add_karma_cmd(client, message, args):
    if not _file_loaded:
        load_karma()
    try:
        from_id = message.author.id
        to_id = message.mentions[0].id
        user_nick = message.mentions[0].nick
        if user_nick is None:
            user_nick = message.mentions[0].name
    except:
        return ' No user specified!'
    if to_id == from_id:
        return "4ril??"
    if not _eligible_to_give(from_id, to_id):
        return 'You can give karma to %s again in more %d minutes' % \
               (user_nick, (_time_between_karma - (time.time() - _last_karma_time[(from_id, to_id)])) / 60)
    _add_karma(from_id, to_id)
    return '%s has %s karma' % (user_nick, _get_karma(to_id))


@utils.admin
def set_karma_cmd(client, message, args):
    if not _file_loaded:
        load_karma()
    try:
        user_id = message.mentions[0].id
        user_nick = message.mentions[0].nick
        if user_nick is None:
            user_nick = message.mentions[0].name
        num = int(args.split(' ')[1])
    except Exception as e:
        print(e)
        return ' No user specified!'
    _set_karma(user_id, num)
    return '%s has %s karma' % (user_nick, _get_karma(user_id))


def get_karma_cmd(client, message, args):
    if not _file_loaded:
        load_karma()
    try:
        user_id = message.mentions[0].id
        user_nick = message.mentions[0].nick
        if user_nick is None:
            user_nick = message.mentions[0].name
    except:
        return ' You have %s karma' % (_get_karma(message.author.id))
    return '%s has %s karma' % (user_nick, _get_karma(user_id))


def _set_karma_time(from_id, to_id):
    t = int(time.time())
    _last_karma_time[(from_id, to_id)] = t


def _eligible_to_give(from_id, to_id):
    if (from_id, to_id) not in _last_karma_time:
        return True
    return (int(time.time()) - _last_karma_time[(from_id, to_id)]) > _time_between_karma


def _add_karma(from_id, to_id):
    if to_id not in user_data:
        user_data[to_id] = 1
    else:
        user_data[to_id] += 1
    _set_karma_time(from_id, to_id)
    save_karma()


def _set_karma(from_id, to_id, num=1):
    user_data[to_id] = num
    _set_karma_time(from_id, to_id)
    save_karma()


def _take_karma(from_id, to_id, num=1):
    if to_id not in user_data:
        user_data[to_id] = 0
    else:
        user_data[to_id] -= num
    _set_karma_time(from_id, to_id)
    save_karma()


def _dec_karma(from_id, to_id):
    if to_id not in user_data:
        user_data[to_id] = 0
    else:
        user_data[to_id] -= 1
        if user_data[to_id] < 0:
            user_data[to_id] = 0
    _set_karma_time(from_id, to_id)
    save_karma()


def _get_karma(user_id):
    load_karma()
    if user_id not in user_data:
        return 0
    return user_data[user_id]


def load_karma():
    global _file_loaded
    if _file_loaded:
        return
    if os.path.isfile(_karma_file):
        with open(_karma_file, 'rb') as handle:
            global user_data
            user_data = pickle.load(handle)
    _file_loaded = True


def save_karma():
    with open(_karma_file, 'wb') as handle:
        pickle.dump(user_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
