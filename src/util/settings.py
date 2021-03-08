import json
from typing import Any


class Singleton(type): # https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass = Singleton):
    def __init__(self) -> None:
        self._config = {}
        self.load_settings()

    def __getitem__(self, key: str) -> None:
        return self._config[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._config[key] = value

    def load_settings(self) -> None:
        try:
            with open("~/.config/UBUVoiceAssistant/config.cfg") as config_file:
                self._config = json.load(config_file)
        except OSError as e:
            print("Error loading config file", e)
        if not "user" in self:
            self["user"] = None
        if not "host" in self:
            self["host"] = None
        if not "lang" in self:
            self["lang"] = "es_ES"

    def save_settings(self) -> None:
        try:
            with open("~/.config/UBUVoiceAssistant/config.cfg", "w") as config_file:
                json.dump(self._config, config_file)
        except OSError as e:
            print("Error saving config file", e)