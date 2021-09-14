import requests

class AnkiConnect:
    def __init__(self, host='http://localhost', port=8765):
        self.url = f'{host}:{port}'

    def send_command(self, action, params=None):
        command = {"action": action, "version": 6}
        if params:
            command['params'] = params
        response = requests.post(self.url, json=command).json()
        if response['error']:
            raise Exception(response['error'])
        return response

    def add_note (self, deck, model, fields, tags=[], media=[]):
        params = {
            'note': {
                'deckName': deck,
                'modelName': model,
                'fields': fields,
                'options': {
                    'allowDuplicate': True
                },
                'tags': tags
            }
        }
        self.send_command('addNote', params)
        for name, data in media:
            params = {
                'filename': name,
                'data': data
            }
            self.send_command('storeMediaFile', params)

    def ensure_deck(self, deck):
        response = self.send_command('deckNames')
        if deck not in response['result']:
            self.send_command('createDeck', {'deck': deck})

    def ensure_notetype(self, params):
        response = self.send_command('modelNames')
        if params['modelName'] not in response['result']:
            self.send_command('createModel', params)
            return True
        return False

    def find_notes_by_deck (self, deck):
        params = {'query': f'deck:"{deck}"'}
        response = self.send_command('findNotes', params)
        return response['result']

    def get_note_info (self, notes):
        response = self.send_command('notesInfo', {"notes": notes})
        return response['result']

    def update_note_fields (self, id, fields):
        self.send_command('updateNoteFields', {'note': {'id': id, 'fields': fields}})

