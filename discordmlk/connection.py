import websocket
import threading
import requests
import json
import time

from discordmlk import covers


class Discord:
    __gateway_url = 'wss://gateway.discord.gg/?v=10&encoding=json'
    __event_functions = {}
    id = ''

    def __init__(self, token=None, login=None, password=None):
        if login is not None and password is not None and token is None:
            token = self.__login(login, password)
        if token is None:
            print("I don't have token.")
            return
        self.__token = token
        self.__session_id = None
        self.__sequence_number = 'null'
        self.__resume_gateway_url = None

        self.__websocket_init()
        self.__requests_session_init()

    def __login(self, login, password):
        payload = {
            'login': login,
            'password': password,
        }
        response = json.loads(requests.post('https://discord.com/api/v9/auth/login', json=payload).text)
        print(response)
        return response['token']

    def __websocket_init(self, reconnect=False):
        ws = websocket.WebSocket()
        ws.connect(self.__gateway_url if not reconnect else self.__resume_gateway_url)
        response = self.__get_response(ws)

        self.__send_log_to_console('Hello', response)

        heartbeat_interval = response['d']['heartbeat_interval'] / 1000
        threading.Thread(target=self.__start_heartbeat, args=(ws, heartbeat_interval,)).start()

        if reconnect:
            payload = {
                "op": 6,
                "d": {
                    "token": self.__token,
                    "session_id": self.__session_id,
                    "seq": self.__sequence_number
                }
            }
            response = self.__send_json_request(ws, payload)
            self.__send_log_to_console('Resume', response)

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
            response = self.__send_json_request(ws, payload)
            self.__send_log_to_console('Identify', response)

            self.id = response['d']['user']['id']
            self.__resume_gateway_url = response['d']['resume_gateway_url']
            self.__session_id = response['d']['session_id']
        threading.Thread(target=self.__events_apply, args=(ws,)).start()

    def __websocket_reconnect(self):
        self.__websocket_init(reconnect=True)
        self.__send_log_to_console('Connection', 'WebSocket Reconnected.')

    def __requests_session_init(self):
        self.__session = requests.Session()
        self.__session.headers.update({
            'authorization': self.__token
        })

    def __start_heartbeat(self, ws, heartbeat_interval):
        try:
            while True:
                time.sleep(heartbeat_interval)
                self.__send_heartbeat(ws)
        except:
            return

    def __send_heartbeat(self, ws):
        payload = {
            'op': 1,
            'd': self.__sequence_number
        }
        self.__send_json_request(ws, payload)

    def __get_response(self, ws):
        response = ws.recv()
        if response:
            response = json.loads(response)

            if response['s']:
                self.__sequence_number = response['s']
            if response['op'] == 1:
                self.__send_heartbeat(ws)
            return response

    def __send_json_request(self, ws, payload):
        ws.send(json.dumps(payload))
        return self.__get_response(ws)

    def __send_log_to_console(self, author, message):
        print(f'\033[95m{time.strftime("%H:%M:%S")} FROM {author}: \033[93m{message}\033[0m')

    def __events_apply(self, ws):
        while True:
            try:
                response = self.__get_response(ws)
            except:
                print('Connection', 'WebSocket Disconnected...')
                self.__websocket_reconnect()
                return

            if response:
                if response['op'] == 11:
                    self.__send_log_to_console('Heartbeat ACK', response)
                    continue
                self.__send_log_to_console('Events', response)
                if response['t'] == 'MESSAGE_CREATE':
                    if 'on_message' in self.__event_functions:
                        msg = covers.Message(response['d'])
                        threading.Thread(target=self.__event_functions['on_message'], args=(msg,)).start()

    def event(self, function):
        self.__event_functions[function.__name__] = function




    def send_slash_command(self, slash_command):
        command_data = slash_command.get_json()

        application_id = command_data['application_id']
        channel_id = command_data['channel_id']
        command_name = command_data['data']['name']
        command = self.get_application_command(application_id, channel_id, command_name)

        command_data['session_id'] = self.__session_id
        command_data['data']['version'] = command['version']
        command_data['data']['id'] = command['id']

        return self.__session.post('https://discord.com/api/v9/interactions', json=command_data)
    def get_application_command(self, application_id, channel_id, command_name):
        url = f'https://discord.com/api/v9/channels/{channel_id}/application-commands/search?type=1&application_id={application_id}'
        application_commands = json.loads(self.__session.get(url).text)['application_commands']
        for command in application_commands:
            if command['name'] == command_name:
                return command

    def send_message(self, message):
        url = f'https://discord.com/api/v9/channels/{message.get_json()["channel_id"]}/messages'
        return self.__session.post(url, json=message.get_json())
