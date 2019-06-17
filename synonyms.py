# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import requests
import json
import os
import time
import re
import argparse

from dotenv import load_dotenv
load_dotenv()

HEADERS = {
    'app_id': os.getenv('APP_ID'),
    'app_key': os.getenv('APP_KEY')
}

ROOT_URL = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en'
LANG = 'en'


def main():
    args = parse_args()
    steplog = steplogger()
    with open(args.out, 'w+') as fp:
        for word in parse_words(args.text):
            print(f'step: {next(steplog)}; {word}')
            try:
                fp.write(oxford_synonyms(word))
            except requests.HTTPError:
                print(f'skipped: {word}')
            
def parse_words(wordfile):
    with open(wordfile) as fp:
        for w in set(tokens(fp.read())):
            if len(w) > 2:
                yield w

def tokens(text):
    "List all the word tokens (consecutive letters) in a text. Normalize to lowercase."
    return re.findall('[a-z]+', text.lower())

def oxford_synonyms(word):
    'Get synonyms for a given word fro the oxford dictionary API'
    url = '{}/{}/synonyms'.format(ROOT_URL, word)
    r = requests.get(url, headers=HEADERS)
    if not r.ok:
        r.raise_for_status()
    return json.dumps(r.json()) + '\n'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--out', help='output file for results', default='data/_synonym.nd.json')
    parser.add_argument(
        '-t', '--text', help='filepath to text corpora', default='data/words')
    return parser.parse_args()

def steplogger():
    'simple counter to see how many requests we have made'
    i = 0
    while True:
        i += 1
        yield i

if __name__ == '__main__':
    main()
