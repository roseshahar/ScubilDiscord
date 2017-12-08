from plugins.karma import _get_karma, _take_karma
import collections
import utils

Item = collections.namedtuple('Item', 'name,type,value,price')

items = [
    Item(name='Uber - Role', type='role', value='Uber', price=50),
    Item(name='1337 - Role', type='role', value='1337', price=30),
    Item(name='Cyber - Role', type='role', value='Cyber', price=20),
    Item(name='root - Role', type='role', value='root', price=10),
    Item(name='Skid - Role', type='role', value='Skid', price=5),
]


@utils.register_command('buy', ['karma-store'])
async def buy_item(client, message, args):
    """
    you can buy role with this command
    ***----***
    """
    try:
        index = int(args)
    except:
        await client.send_message(message.author, 'Syntax error when buying')
        await client.delete_message(message)
        return
    await buy(client, message.author, index)
    await client.delete_message(message)


async def buy(client, member, index):
    try:
        wanted = items[index]
    except:
        await client.send_message(member, 'Invalid item selected')
        return
    user_id = member.id
    if _get_karma(user_id) >= wanted.price:
        _take_karma(0, user_id, wanted.price)
        if wanted.type == 'role':
            role_obj = find_role_by_name(member.server.roles, wanted.value)
            await _set_role(client, member, role_obj)
    await client.send_message(member, 'Insufficient funds. Get more karma by helping other users')


async def _set_role(client, member, role):
    await client.add_roles(member, role)


def find_role_by_name(roles, name):
    for role in roles:
        if role.name.upper() == name.upper():
            return role
    return None
