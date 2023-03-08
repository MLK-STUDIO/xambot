import threading
import websocket
import requests
import json
import time

class Discord:
    def __init__(self, token):
        self.__recieve_message_function = None
        self.__requests_session_init(token)
        self.__web_socket_init(token)

    def __init_event(self, function, recieve_message_function):
        return threading.Thread(target=function, args=(recieve_message_function,)).start()

    def __requests_session_init(self, token):
        self.__session = requests.Session()
        self.__session.headers.update({
            'authorization': token
        })

    def __web_socket_init(self, token):
        self.__ws = websocket.WebSocket()
        self.__ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')

        event = self.__recieve_json_response()

        heartbeat_inteval = event['d']['heartbeat_interval'] / 1000
        threading.Thread(target=self.__heartbeat, args=(heartbeat_inteval,)).start()
        payload = {
            'op': 2,
            'd': {
                'token': token,
                'properties': {
                    '$os': 'linux',
                    '$browser': 'chrome',
                    '$device': 'pc'
                }
            }
        }
        self.__send_json_request(payload)

    def __heartbeat(self, interval):
        print('----Heartbeat begin----')
        while True:
            time.sleep(interval)
            payload = {
                'op': 1,
                'd': 'null'
            }
            self.__send_json_request(payload)
            print('----Heartbeat send----')

    def __send_json_request(self, payload):
        self.__ws.send(json.dumps(payload))

    def __recieve_json_response(self):
        response = self.__ws.recv()
        if response:
            return json.loads(response)

    def __message_processing(self, function):
        while True:
            try:
                response = json.loads(self.__ws.recv())
                function(response)
            except:
                pass

    def set_recieve_message_function(self, recieve_message_function):
        self.__init_event(self.__message_processing, recieve_message_function)

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