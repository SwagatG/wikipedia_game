import wikipedia
import json

BLACKLIST = 'blacklist.json'

def validate(*args):
    try:
        print("11")
        with open(BLACKLIST, 'r') as readfile:
            print("12")
            blacklist = json.loads(readfile)
        print("13")
        if len(blacklist) == 0:
            print("14")
            blacklist = [];
    except:
        blacklist = [];
        print("15")

    errors = [];
    for arg in args:
        print("16")
        try:
            test = wikipedia.WikipediaPage(title=arg).links
            print("17")
        except:
            print("18")
            errors.append(arg)
            blacklist.append(arg)

    print("19")
    if len(errors):
        with open (BLACKLIST, 'w') as writefile:
            print("110")
            json.dumps(blacklist)
    print("111")
    return errors
