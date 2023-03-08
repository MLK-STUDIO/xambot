import websocket
import time
import threading
import json
import requests

class Discord:
    def __init__(self, token, asynchronously=False):
        self.__recieve_message_function = None
        self.__token = token
        if not asynchronously:
            self.__message_processing()
        else:
            threading.Thread(target=self.__message_processing).start()
        self.__session = requests.Session()
        self.__session.headers.update({'authorization': self.__token})

    @staticmethod
    def __send_json_request(goal, request):
        goal.send(json.dumps(request))

    @staticmethod
    def __recieve_json_response(goal):
        response = goal.recv()
        if response:
            return json.loads(response)

    def __heartbeat(self, goal, interval):
        while True:
            time.sleep(interval)
            payload = {
                'op': 1,
                'd': 'null'
            }
            self.__send_json_request(goal, payload)

    def __message_processing(self):
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
        response = self.__recieve_json_response(ws)

        heartbeat_interval = response['d']['heartbeat_interval'] / 1000
        threading.Thread(target=self.__heartbeat, args=(ws, heartbeat_interval)).start()
        payload = {
            'op': 2,
            'd': {
                'token': self.__token,
                'properties': {
                    '$os': 'linux',
                    '$browser': 'chrome',
                    '$device': 'pc'
                }
            }
        }
        ws.send(json.dumps(payload))

        while True:
            try:
                response = json.loads(ws.recv())
                if self.__recieve_message_function is not None:
                    self.__recieve_message_function(response)
            except:
                pass


    def set_recieve_message_function(self, function):
        self.__recieve_message_function = function

    def send_slash_command(self, application_id, guild_id, channel_id, session_id, command_name, user_id):
        command = self.get_application_command(application_id, channel_id, command_name)
        command_version = command['version']
        command_id = command['id']
        data = {
            'application_id': application_id,
            'guild_id': guild_id,
            'channel_id': channel_id,
            'session_id': session_id,
            'data': {
                    'version': command_version,
                    'id': command_id,
                    'name': command_name,
                    'options': [{
                        'type': 6,
                        'name': 'user',
                        'value': user_id
                    }]
            }, 'type': 2
        }
        return self.__session.post('https://discord.com/api/v9/interactions', json=data)

    def send_message(self, channel_id, message):
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        return self.__session.post(url, json={'content': message})

    def get_application_command(self, application_id, channel_id, command_name):
        url = f'https://discord.com/api/v9/channels/{channel_id}/application-commands/search?type=1&application_id={application_id}'
        application_commands = json.loads(self.__session.get(url).text)['application_commands']
        for command in application_commands:
            if command['name'] == command_name:
                return command
        return {}