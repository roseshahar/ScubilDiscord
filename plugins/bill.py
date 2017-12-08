from urllib.parse import quote
import utils


@utils.register_command('bill', ['bot'])
def bill_cmd(client, message, args):
    """
    generate a bill meme with your name
    ***----***
    """
    return 'http://belikebill.azurewebsites.net/billgen-API.php?default=1&name={}&sex=m' \
        .format(quote(message.author.display_name))
