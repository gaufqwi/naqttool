import sys
import re
import json

from ankiconnect import AnkiConnect
from ankimodels import naqt_basic_model_params, naqt_cloze_model_params

line_re = re.compile('^([A-Z]+):\s*(.*)$')
starredline_re = re.compile('^(\*)?([A-Z]+):\s*(.*)$')

class Template:
    def __init__(self, source=None, category=None, tags=[], f=None):
        self.category = category
        self.tags = tags
        self.source = source
        self.raw_items = []
        self.cooked_items = []
        if f:
            self.from_file(f)

    def from_file(self, f):
        content = f.read()
        f.close()
        parts = [part.strip() for part in content.split('===')]
        # Read header
        if len(parts[0]) > 0:
            for line in parts[0].split('\n'):
                m = line_re.match(line)
                if m:
                    if m.group(1) == 'CATEGORY':
                        self.category = m.group(2)
                    elif m.group(1) == 'SOURCE':
                        self.source = m.group(2)
                    elif m.group(1) == 'TAGS':
                        self.tags = [t.strip() for t in m.group(2).split(',')]
        # Read items
        for part in parts[1:]:
            blocks  = [block.strip() for block in part.split('---')]
            if len(blocks[0]) > 0:
                m = line_re.match(blocks[0])
                if m and m.group(1) == 'SUBJECT':
                    subject = m.group(2)
                else:
                    subject = None
            for block in blocks[1:]:
                answer = []
                prompt = None
                cloze = False
                extra = None
                tags = []
                for line in block.split('\n'):
                    m = starredline_re.match(line)
                    if m and m.group(1) == '*':
                        if m.group(2) == 'PROMPT':
                            prompt = m.group(3).strip()
                            cloze = False
                        elif m.group(2) == 'CLOZE':
                            prompt = m.group(3).strip()
                            cloze = True
                        elif m.group(2) == 'TERM' or m.group(2) == 'ANSWER':
                            answer.append(m.group(3))
                        elif m.group(2) == 'EXTRA':
                            extra = m.group(3)
                        elif m.group(2) == 'TAGS':
                            tags = [t.strip() for t in m.group(3).split(',')]
                if prompt and (len(answer) > 0 or subject or cloze):
                    item = {'text': prompt, 'cloze': cloze, 'tags': tags}
                    if len(answer) > 0:
                        item['answer'] = ', '.join(answer)
                    elif not cloze:
                        item['answer'] = subject
                    if extra:
                        item['extra'] = extra
                    self.cooked_items.append(item)


    def add_item(self, item):
        self.raw_items.append(item)

    def write(self, f=sys.stdout):
        print(f'SOURCE: {self.source}', file=f)
        if self.category:
            print(f'CATEGORY: {self.category}', file=f)
        if self.tags:
            print(f'TAGS: {", ".join(self.tags)}', file=f)
        for item in self.raw_items:
            print('===', file=f)
            print(f'SUBJECT: {item["subject"]}', file=f)
            for prompt in item['prompts']:
                print('---', file=f)
                for term in prompt['terms']:
                    print(f'TERM: {term}', file=f)
                if item['cloze']:
                    print(f'CLOZE: {prompt["text"]}', file=f)
                else:
                    print(f'PROMPT: {prompt["text"]}', file=f)
                print('EXTRA:', file=f)
                print('TAGS:', file=f)

    def to_json(self, f=sys.stdout):
        items = self.cooked_items
        for item in items:
            if self.source:
                item['source'] = self.source
            if self.category:
                item['category'] = self.category
            if self.tags:
                item['tags'] += self.tags
        print(json.dumps(items, indent=2), file=f)

    def to_anki(self, deck):
        anki = AnkiConnect()
        anki.ensure_notetype(naqt_basic_model_params)
        anki.ensure_notetype(naqt_cloze_model_params)
        anki.ensure_deck(deck)
        for item in self.cooked_items:
            if item['cloze']:
                ankirep = {
                    'Text': item['text'],
                    'Category': getattr(self, 'category', ''),
                    'Source': getattr(self, 'source', ''),
                    'Extra': item.get('extra', '')
                }
                anki.add_note(deck, 'NAQT Cloze', ankirep, getattr(self, 'tags', []) + item.get('tags', []))
            else:
                ankirep = {
                    'Prompt': item['text'],
                    'Answer': item['answer'],
                    'Category': getattr(self, 'category', ''),
                    'Source': getattr(self, 'source', ''),
                    'Extra': item.get('extra', '')
                }
                anki.add_note(deck, 'NAQT Basic', ankirep, getattr(self, 'tags', []) + item.get('tags', []))