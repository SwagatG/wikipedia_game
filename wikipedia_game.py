import json
import argparse
import requests
import random
import wikipedia

MAX_RESULTS= 100
WORD_LABEL = 'word'
STRONG_WORD_RELATION_API = "https://api.datamuse.com/words?rel_trg={word}&max=" + str(MAX_RESULTS)
WEAK_WORD_RELATION_API = "https://api.datamuse.com/words?rel_trg={word}&max=" + str(MAX_RESULTS)
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/{word}"      
STATUS_FILE = 'computation_status.json'

def string_to_title(string):
    return string.replace(' ', '+')

def string_to_url(string):      
    return WIKIPEDIA_URL.format(word=string.replace(' ', '_'))

def contruct_word_relation(end_page, api_call):
    relations = [end_page.lower()]
    s = requests.Session()
    
    r = s.get(api_call.format(word=end_page));
    data = json.loads(r.text)

    for result in data:
        relations.append(result[WORD_LABEL].lower())

    return relations

def compare_links_and_relations(relations, current_links, path):
    match = False

    # print ("CURRLINKS for: " + str(current_links))
    # input("Press Enter to continue...")

    for word in relations:
        for link in current_links:
            match = False
            for node in path:
                if ((link.lower() == node.lower()) or ("disambiguation" in link.lower())) :
                    match=True
            if (not match):
                if (word == link.lower()):
                    #print (link.lower())
                    #print ("PATH: " + str(path))
                    #input("Press Enter to continue...")
                    return link
                elif (word in link.lower()):
                    #print (link.lower())
                    #print ("PATH: " + str(path))
                    #input("Press Enter to continue...")
                    return link


    # for word in relations:
    #     for link in current_links:
    #         if word == link.lower():
    #             match = True
    #             for node in path:
    #                 print(word + " vs. " + node.lower())
    #                 if link.lower() == node.lower():
    #                     match = False
    #             if match:
    #                 return link

    # for word in relations:
    #     for link in current_links:
    #         if word in link.lower():
    #             match = True
    #             # print(word + " vs. " + str(path))
    #             for node in path:
    #                 print(word + " vs. " + node.lower())
    #                 if link.lower() == node.lower():
    #                     match = False
    #             if match:
    #                 return link

    return None

def main(args):

    print(str(args))
    start_page = args.start_page
    end_page = args.end_page
    limit = args.limit

    strong_relations = contruct_word_relation(string_to_title(end_page), STRONG_WORD_RELATION_API);
    weak_relations = None

    link_count = 0
    path = [start_page]
    current_page = start_page
    match_found = False
    current_links = []

    response = {}
    response['start_page'] = start_page
    response['end_page'] = end_page
    response['length'] = current_links
    response['path'] = []
    response['complete'] = match_found

    while (link_count < limit and (not match_found)):
        try:
            current_links = wikipedia.WikipediaPage(title=path[-1]).links
        except:
            broken=path[-1]
            del path[-1]
            current_links = wikipedia.WikipediaPage(path[-1]).links
            current_links.remove(broken)
            link_count -= 1

        current_page = compare_links_and_relations(strong_relations, current_links, path)

        if not current_page:
            print("WEAK")
            if not weak_relations:
                weak_relations = contruct_word_relation(string_to_title(end_page), WEAK_WORD_RELATION_API);
            current_page = compare_links_and_relations(weak_relations, current_links, path)

        if not current_page:
            print("RANDOM")
            current_page = current_links[random.randrange(0, len(current_links))]

        path.append(current_page)
        link_count += 1
        if current_page == end_page:
            match_found = True

        print(str(link_count) + ": " + str(path))

        response['length'] = link_count
        page = {}
        page['title'] = path[-1]
        page['url'] = string_to_url(page['title'])
        response['path'].append(page)
        response['complete'] = match_found

        with open(STATUS_FILE, 'w') as outfile:
            json.dump(response, outfile)

    print("THIS IS THE PATH: " + str(path))

    # print(wikipedia.WikipediaPage(title=args.start_page).links)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plays the Wikipedia Game')
    parser.add_argument('start_page', help='The name of the starting article.', type=str)
    parser.add_argument('end_page', help='The name of the target article.', type=str)
    parser.add_argument('-l', '--limit', nargs='?', help='The number of articles after which to give up.', type=int)

    args = parser.parse_args();
    main(args)