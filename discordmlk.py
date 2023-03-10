import websocket
import threading
import requests
import json
import time

class Discord:
    __gateway_url = 'wss://gateway.discord.gg/?v=10&encoding=json'
    __event_functions = {}


    def __init__(self, token):
        self.__token = token
        self.__session_id = None
        self.__sequence_number = 'null'
        self.__resume_gateway_url = None

        self.__websocket_init()
        self.__requests_session_init()

    def __websocket_init(self, reconnect=False):
        self.__ws = websocket.WebSocket()
        self.__ws.connect(self.__gateway_url if not reconnect else self.__resume_gateway_url)
        response = self.__get_response()

        heartbeat_interval = response['d']['heartbeat_interval'] / 1000
        threading.Thread(target=self.__start_heartbeat, args=(heartbeat_interval,)).start()

        if reconnect:
            payload = {
                "op": 6,
                "d": {
                    "token": self.__token,
                    "session_id": self.__session_id,
                    "seq": self.__sequence_number
                }
            }
            response = self.__send_json_request(payload)

        if not reconnect or response['op'] == 9:
            payload = {
                "op": 2,
                "d": {
                    "token": self.__token,
                    "properties": {
                        "os": "linux",
                        "browser": "chrome",
                        "device": "pc"
                    }
                }
            }
            response = self.__send_json_request(payload)
            self.__resume_gateway_url = response['d']['resume_gateway_url']
            self.__session_id = response['d']['session_id']

        threading.Thread(target=self.__events_apply).start()

    def __websocket_reconnect(self):
        self.__websocket_init(reconnect=True)
        self.__send_log_to_console('WebSocket Reconnected.')

    def __requests_session_init(self):
        self.__session = requests.Session()
        self.__session.headers.update({
            'authorization': self.__token
        })

    def __start_heartbeat(self, heartbeat_interval):
        try:
            while True:
                self.__send_heartbeat()
                time.sleep(heartbeat_interval)
        except:
            return

    def __send_heartbeat(self):
        payload = {
            'op': 1,
            'd': self.__sequence_number
        }
        self.__send_json_request(payload)

    def __get_response(self):
        response = self.__ws.recv()
        if response:
            response = json.loads(response)

            if response['s']:
                self.__sequence_number = response['s']
            if response['op'] == 1:
                self.__send_heartbeat()

            self.__send_log_to_console(response)

            return response

    def __send_json_request(self, payload):
        self.__ws.send(json.dumps(payload))
        return self.__get_response()

    def __send_log_to_console(self, message):
        print(f'{time.strftime("%H:%M:%S")}:', message)

    def __events_apply(self):
        while True:
            try:
                response = self.__get_response()
            except:
                print('WebSocket Disconnected...')
                self.__websocket_reconnect()
                return
            if response:

                if response['t'] == 'MESSAGE_CREATE':
                    if 'on_message' in self.__event_functions:
                        self.__event_functions['on_message'](response['d'])

    def event(self, function):
        self.__event_functions[function.__name__] = function

    def send_message(self, channel_id, message):
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        return self.__session.post(url, json={'content': message})

    def send_slash_command(self, application_id, guild_id, channel_id, command_name, user_id):
        command = self.get_application_command(application_id, channel_id, command_name)
        command_version = command['version']
        command_id = command['id']
        data = {
            'application_id': application_id,
            'guild_id': guild_id,
            'channel_id': channel_id,
            'session_id': self.__session_id,
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

    def get_application_command(self, application_id, channel_id, command_name):
        url = f'https://discord.com/api/v9/channels/{channel_id}/application-commands/search?type=1&application_id={application_id}'
        application_commands = json.loads(self.__session.get(url).text)['application_commands']
        for command in application_commands:
            if command['name'] == command_name:
                return command