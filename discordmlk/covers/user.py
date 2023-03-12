from discordmlk.covers.cover import Cover

class User(Cover):

    def _init(self):
        self.name = self._get_data('username')
        self.public_flags = self._get_data('public_flags')
        self.id = self._get_data('id')
        self.display_name = self._get_data('display_name')
        self.discriminator = self._get_data('discriminator')
        self.avatar_decoration = self._get_data('avatar_decoration')
        self.avatar = self._get_data('avatar')