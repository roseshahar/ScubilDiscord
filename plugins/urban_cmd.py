import urllib.request
import json
from urllib.parse import quote
import utils


@utils.register_command('urban')
def query_urban_dictionary(client, message, args):
    """
    "urban PHRASE": search PHRASE on urban (a dictionary)
    ***----***
    """
    try:
        args = quote(args)
        query_data = urllib.request.urlopen(f'http://api.urbandictionary.com/v0/define?term={args}').read()
        decoded_data = json.loads(query_data)

        return f'**Word:** {decoded_data["list"][0]["word"]}\n {decoded_data["list"][0]["definition"]}'
    except:
        return "Sorry, I couldn't find anything on that"
