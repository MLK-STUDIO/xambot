from discordmlk.covers.cover import Cover
from discordmlk.covers.user import User

class Embed(Cover):

    def _init(self):
        self.title = self._get_data('title')
        self.type = self._get_data('type')
        self.description = self._get_data('description')
        self.url = self._get_data('url')
        self.timestamp = self._get_data('timestamp')
        self.color = self._get_data('color')
        self.footer = self._get_data('footer')
        self.image = self._get_data('image')
        self.thumbnail = self._get_data('thumbnail')
        self.video = self._get_data('video')
        self.provider = self._get_data('provider')
        self.author = User(self._get_data('author'))
        self.fields = self._get_data('fields')


class Footer(Cover):
    def _init(self):
        self.text = self._get_data('text')