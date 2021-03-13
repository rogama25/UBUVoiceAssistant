import json
from typing import Any
from util import Singleton


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
        except OSError as ex:
            print("Error loading config file", ex)
        if "user" not in self:
            self["user"] = None
        if "host" not in self:
            self["host"] = None
        if "lang" not in self:
            self["lang"] = "es_ES"

    def save_settings(self) -> None:
        try:
            with open("~/.config/UBUVoiceAssistant/config.cfg", "w") as config_file:
                json.dump(self._config, config_file)
        except OSError as ex:
            print("Error saving config file", ex)
