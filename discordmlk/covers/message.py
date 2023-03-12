from discordmlk.covers.attachment import Attachment
from discordmlk.covers.embed import Embed
from discordmlk.covers.cover import Cover
from discordmlk.covers.user import User
from datetime import datetime

class Message(Cover):

    def __init__(self, json_object, channel_id=None):
        super().__init__(json_object)

    def _init(self):
        self.type = self._get_data('type')
        self.tts = self._get_data('tts')
        self.mention_roles = self._get_data('mention_roles')
        self.mention_everyone = self._get_data('mention_everyone')
        self.id = self._get_data('id')
        self.flags = self._get_data('flags')
        self.edited_timestamp = self._get_data('edited_timestamp')
        self.content = self._get_data('content')
        self.components = self._get_data('components')
        self.channel_id = self._get_data('channel_id')
        self.author = User(self._get_data('author'))
        self.nonce = self._get_data('nonce')
        self.guild_id = self._get_data('guild_id')
        self.member = self._get_data('member')

        attachments = self._get_data('attachments')
        if attachments is not None:
            self.attachments = [Attachment(attach) for attach in attachments]


        self.message_reference = {}
        if self.type == 19:
            self.referenced_message = Message(self._get_data('referenced_message'))
            self.message_reference['message_id'] = self._get_data('message_reference')['message_id']
            self.message_reference['channel_id'] = self._get_data('message_reference')['channel_id']

        mentions = self._get_data('mentions')
        if mentions is not None:
            self.mentions = [User(mention) for mention in self._get_data('mentions')]

        embeds = self._get_data('embeds')
        if embeds is not None:
            self.embeds = [Embed(emb) for emb in self._get_data('embeds')]

        time = self._get_data('timestamp')
        if time is not None:
            self.timestamp = datetime.strptime(time.split('.')[0], '%Y-%m-%dT%H:%M:%S')

    def set_message(self, channel_id, content):
        self._json_object['content'] = content
        self._json_object['channel_id'] = channel_id

    def reply_to(self, guild_id, channel_id, message_id):
        self._json_object['message_reference'] = {
            'message_id': message_id,
            'channel_id': channel_id,
            'guild_id': guild_id
        }
