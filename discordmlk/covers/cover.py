
class Cover:

    def __init__(self, json_object=None):
        if json_object is None or not isinstance(json_object, dict):
            self._json_object = {}
        else:
            self._json_object = json_object
        self._init()

    def _init(self):
        pass

    def _get_data(self, data):
        if data in self._json_object:
            return self._json_object[data]

    def _set_data(self, key, data):
        self._json_object[key] = data

    def get_json(self):
        return self._json_object
