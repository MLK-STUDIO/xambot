from discordmlk.covers.cover import Cover

class SlashCommand(Cover):

    def __init__(self, application_id, guild_id, channel_id, command_name):
        super().__init__()

        data = {
            'version': '',
            'id': '',
            'name': command_name,
            'options': []
        }

        self._set_data('application_id', application_id)
        self._set_data('session_id', '')
        self._set_data('guild_id', guild_id)
        self._set_data('channel_id', channel_id)
        self._set_data('type', 2)
        self._set_data('data', data)

    def set_command_name(self, name):
        self._json_object['data']['name'] = name

    def add_option(self, type, name, value):
        data = {
            'type': type,
            'name': name,
            'value': value
        }
        self._json_object['data']['options'].append(data)