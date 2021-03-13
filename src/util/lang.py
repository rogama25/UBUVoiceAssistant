import gettext
from typing import Union, List, Tuple
import os
import json
from babel import Locale
from util import Singleton


class Translator(metaclass = Singleton):
    def __init__(self, lang: str) -> None:
        self._lang = None  # String like en_US
        self._available_langs = []
        self._language_names = []
        self._domain = "UBUVoiceAssistant"
        self._lang_dir = "./lang"
        self._translator: gettext.GNUTranslations = None
        self.find_available_languages()
        self.change_language(lang)

    def change_language(self, lang: Union[str, int]) -> None:
        if isinstance(lang, int):
            self.change_language(self._available_langs[lang])
        self._lang = lang
        self._translator = gettext.translation(
            self._domain, self._lang_dir, [self._lang])
        self.update_mycroft_config()

    def translate(self, string: str) -> str:
        return self._translator.gettext(string)

    def find_available_languages(self) -> List[str]:
        self._available_langs = []
        self._language_names = []
        for locale in os.listdir(self._lang_dir):
            if os.path.isfile(self._lang_dir + "/" + locale + "/LC_MESSAGES/" +
                              self._domain + ".mo"):
                self._available_langs.append(locale)
                self._language_names.append(
                    Locale(*locale.split("_")).language_name)
        return self._language_names

    def get_current_language(self) -> Tuple[str]:
        current_name = self._language_names[self._available_langs.index(
            self._lang)]
        return self._lang, current_name

    def update_mycroft_config(self) -> None:
        lang_string = self.get_current_language()[0].lower().replace("_", "-")
        with open("~/.config/mycroft-docker/mycroft.conf", "r") as mycroft_cfg_file:
            mycroft_cfg = json.load(mycroft_cfg_file)
        mycroft_cfg["lang"] = lang_string
        if "tts" not in mycroft_cfg:
            mycroft_cfg["tts"] = {}
        mycroft_cfg["tts"]["module"] = "google"
        if "google" not in mycroft_cfg["tts"]:
            mycroft_cfg["tts"]["google"] = {}
        mycroft_cfg["tts"]["google"]["lang"] = lang_string
        mycroft_cfg["tts"]["google"]["slow"] = False
        with open("~/.config/mycroft-docker/mycroft.conf", "w") as mycroft_cfg_file:
            json.dump(mycroft_cfg, mycroft_cfg_file)
