from discordmlk.covers.cover import Cover

class Attachment(Cover):

    def _init(self):
        self.type = self._get_data('content_type')
        self.url = self._get_data('url')
        self.proxy_url = self._get_data('proxy_url')
        self.id = self._get_data('id')
        self.filename = self._get_data('filename')
        self.size = self._get_data('size')
        self.height = self._get_data('height')
        self.width = self._get_data('width')