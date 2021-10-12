"""
Store and retrieve configuration values
"""


class Configuration:
    def __init__(self, key, value):
        print("CONFIGS INSTANTIATED SET NAME")
        print(key)
        print(value)
        self.key = value

    @property
    def app_name(self):
        return self._app_name
