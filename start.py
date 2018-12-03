import requests
import time
import json
from rocketchat.api import RocketChatAPI

class SecBot:

    def __init__(self, name, domain, room, login, password):
        self.name = name
        self.login = login
        self.domain = domain
        self.password = password
        self.room = room
        self.room_id = ''
        self.api = None
        self.processed = []

        self.targets = {
            '192.168.1.1': {
                'comments': 'Router!',
                'services': {
                    '21': 'ftp',
                    '22': 'ssh',
                    '9989': 'http',
                }
            },
            '192.168.1.3': {
                'comments': '',
                'services': {
                    '80': 'http',
                }
            },
        }

        self.load_status()
        self.api = RocketChatAPI(settings={
            'username': self.login, 
            'password': self.password, 
            'domain': self.domain,
        })
        self.room_id = self.get_room_id('pentest-rdc')
    
    def read_messages(self):
        res = self.api.get_private_room_history(self.room_id)
        for r in res['messages']:
            yield r

    def post(self, message):
        self.api.send_message(message, self.room)

    def process_message(self, message):
        # {
        #     '_id': '9ota4D4ewkJpEmFBT', 
        #     'rid': 'TJf4aSR5Bo765XZk8', 
        #     'msg': 'Is Bob there?', 
        #     'ts': '2018-12-02T14:08:21.850Z', 
        #     'u': {
        #         '_id': 'Nd3f8bzCzSmWrLc32', 
        #         'username': 'tiao', 
        #         'name': 'Tiao'
        #     }, 
        #     '_updatedAt': '2018-12-02T14:08:21.863Z', 
        #     'editedBy': None, 
        #     'editedAt': None, 
        #     'emoji': None, 
        #     'avatar': None, 
        #     'alias': None, 
        #     'customFields': None, 
        #     'groupable': None, 
        #     'attachments': None, 
        #     'reactions': None, 
        #     'mentions': [], 
        #     'channels': []
        # }


        # TODO: Process zenmap output
        # TODO: Allow users to book one IP for investigation
        # TODO: List non-investigated IPs
        # TODO: List ports for one IP
        # TODO: Propose tools commands to execute

        if message['_id'] not in self.processed and message['u']['username'] != self.login:
            print('Processing', message)


            if 'Bob' in message['msg']:
                s = message['u']['username']
                self.post('@%s, who is Bob?' % s)

            if '@secbot' in message['msg']:
                s = message['u']['username']

                if 'targets' in message['msg']:
                    print('listing targets')
                    msg = ''
                    ts = self.targets
                    for i in ts:
                        msg += i + ' ' + ts[i]['comments'] + '\n'
                        print('test')
                    self.post(msg)

        





            self.processed.append(message['_id'])








    def get_room_id(self, room):
        rooms = self.api.get_private_rooms()
        print(rooms)
        for r in rooms:
            if r['name'] == room:
                return r['id']
        return ''

    def load_status(self):
        with open('status.json', 'r') as f:
            data = json.load(f)
            self.processed = data['processed']
            print('Processed', self.processed)

    def save_status(self):
        data = {}
        data['processed'] = self.processed
        with open('status.json', 'w') as f:
            json.dump(data, f)

    def start(self):
        while 1:
            for m in self.read_messages():
                self.process_message(m)
            time.sleep(0.5)

try:
    s = SecBot('SuperSec', 'http://localhost:3000', 'pentest-rdc', 'secbot', 'NoSegfault4Secbots!')
    s.start()

except Exception as e:
    print(e)
    s.save_status()
