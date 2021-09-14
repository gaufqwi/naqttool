import re
import argparse
import nltk.data
import bs4
import requests
from unicodedata import normalize
from os.path import isfile
from sys import exit

from template import Template
# from ankiconnect import AnkiConnect
# from ankimodels import naqt_basic_model_params

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# Helper functions
def tag_split(tags):
    return [t.strip() for t in tags.split(',')]

def check_output_file(f, overwrite_ok=False):
    if isfile(f) and not overwrite_ok:
        exit(f'{f} already exists. Use -y option to force overwrite')

def get_input_file(filename, ext='txt'):
    try:
        return open(filename, 'r')
    except FileNotFoundError:
        try:
            return open(f'{filename}.{ext}', 'r')
        except FileNotFoundError:
            exit(f'{filename} not found')

def parse_li(li):
    result = {'prompts': [], 'subject': None}
    result['subject'] = li.select('span.label,a.label')[0].get_text()
    content = str(li)[4:-5]
    sentences = tokenizer.tokenize(content)
    for s in sentences:
        prompt = {'text': '', 'terms': []}
        sentence_soup = bs4.BeautifulSoup(s, 'html.parser')
        prompt['terms'] = [normalize('NFKD', term.get_text()) for term in sentence_soup.select('span.ygk-term')]
        prompt['text'] = normalize('NFKD', sentence_soup.get_text())
        # Sanitize a little if text begins with subject
        prompt['text'] = re.sub(f'^{result["subject"]}\s*(\(.+\))?\s*:\s*', r'\1 ', prompt['text'])
        result['prompts'].append(prompt)
    return result

# Subcommands
def anki(args):
    tfile = get_input_file(args.template, 'txt')
    template = Template(f=tfile)
    template.to_anki(args.deck)

# def dbtest(args):
#     anki = AnkiConnect()
#     if anki.ensure_notetype(naqt_basic_model_params):
#         print("Model type created")
#     else:
#         print("Model type already exists")

def fetch(args):
    url = args.url if args.url else f'https://www.naqt.com/you-gotta-know/{args.page}.html'
    dest = args.dest if args.dest else f'{args.page}.txt'
    check_output_file(dest, args.overwrite_ok or args.stdout)
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')
    template = Template(source=url, tags=args.tags, category=args.category)
    for ul in soup.select('ul.ygk'):
        for li in ul.select('li'):
            item = parse_li(li)
            item['cloze'] = args.cloze
            template.add_item(item)
    if args.stdout:
        template.write()
    else:
        template.write(open(dest, "w"))

def json(args):
    tfile = get_input_file(args.template, 'txt')
    template = Template(f=tfile)
    jfile = args.dest if args.dest else f'{args.template}.json'
    check_output_file(jfile, args.overwrite_ok or args.stdout)
    if args.stdout:
        template.to_json()
    else:
        template.to_json(f=open(jfile, "w"))

def parse_arguments():
    parser = argparse.ArgumentParser(prog='naqttool.sh', description="Process You Gotta Knows from NAQT into Anki cards")
    subparsers = parser.add_subparsers(help='Commands')
    # fetch
    parser_fetch = subparsers.add_parser('fetch', help='Fetch and parse a NAQT into template')
    parser_fetch.add_argument('page', help='Page name on NAQT site', nargs='?', metavar="PAGE")
    parser_fetch.add_argument('--url', help='Explicit URL of page to parse')
    parser_fetch.add_argument('--stdout', help='Send output to STDOUT', action='store_true')
    parser_fetch.add_argument('-y', help='Overwrite existing files', action='store_true', dest='overwrite_ok')
    parser_fetch.add_argument('--dest', help='Template filename')
    parser_fetch.add_argument('--cat', help='Set category field for generated cards', dest='category')
    parser_fetch.add_argument('--cloze', help='Generate prompts as Cloze items', action='store_true')
    parser_fetch.add_argument('--tag', help='Set tag(s) for generated cards', dest='tags', action='extend', type=tag_split, default=[])
    parser_fetch.set_defaults(func=fetch)
    # anki
    parser_anki = subparsers.add_parser('anki', help='Parse a template and create flashcards via AnkiConnect')
    parser_anki.add_argument('template', help='Template filename', metavar='TEMPLATE')
    parser_anki.add_argument('deck', help='Anki deck name', metavar='DECK')
    parser_anki.set_defaults(func=anki)
    # json
    parser_json = subparsers.add_parser('json', help='Parse a template and output JSON')
    parser_json.add_argument('template', help='Template filename', metavar='TEMPLATE')
    parser_json.add_argument('--dest', help='JSON filename')
    parser_json.add_argument('--stdout', help='Send output to STDOUT', action='store_true')
    parser_json.add_argument('-y', help='Overwrite existing files', action='store_true', dest='overwrite_ok')
    parser_json.set_defaults(func=json)
    return parser.parse_args()

# if __name__ == '__main__':
#     args = parse_arguments()
#     args.func(args)