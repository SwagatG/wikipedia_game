import wikipedia
import json

BLACKLIST = 'blacklist.json'

def validate(*args):
    with open(BLACKLIST, 'r') as readfile:
        blacklist = json.loads(readfile)

    if len(blacklist) == 0:
        blacklist = [];

    errors = [];
    for arg in args:
        try:
            test = wikipedia.WikipediaPage(title=arg).links
        except:
            errors.append(arg)
            blacklist.append

    if len(errors):
        black

    return errors
