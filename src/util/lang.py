"""Module for lang-related utils
"""
import gettext
from typing import Union, List, Tuple
import os
import json
from babel import Locale # type: ignore
from ..util.util import Singleton


class Translator(metaclass = Singleton):
    """A class with some translation-related utilities. It's a Singleton.
    """
    def __init__(self, lang: str = "en_US") -> None:
        """Constructor of the Translator class

        Args:
            lang (str): Language to use. A string like "en_US" for American English
                or "es_ES" for Spanish
        """
        self._lang: str = None  # type: ignore
        #String like "en_US"
        self._available_langs: List[str] = []
        self._language_names: List[str] = []
        self._domain = "UBUVoiceAssistant"
        self._lang_dir = "./lang"
        self._translator: gettext.NullTranslations = None # type: ignore
        self.find_available_languages()
        self.change_language(lang)

    def change_language(self, lang: Union[str, int]) -> None:
        """Changes the language of the translator

        Args:
            lang (Union[str, int]): The language string or the index of it in self._available_langs
        """
        if isinstance(lang, int):
            self.change_language(self._available_langs[lang])
        else:
            self._lang = lang
            self._translator = gettext.translation(
                self._domain, self._lang_dir, [self._lang])
            self.update_mycroft_config()

    def translate(self, string: str) -> str:
        """Gets the translated string

        Args:
            string (str): string to translate

        Returns:
            str: translated string
        """
        return self._translator.gettext(string)

    def find_available_languages(self) -> List[str]:
        """Finds and returns the available languages

        Returns:
            List[str]: List of available languages.
                Every language is identified by its readable name, like "English" or "Spanish"
        """
        self._available_langs = []
        self._language_names = []
        for locale in os.listdir(self._lang_dir):
            if os.path.isfile(self._lang_dir + "/" + locale + "/LC_MESSAGES/" +
                              self._domain + ".mo"):
                self._available_langs.append(locale)
                self._language_names.append(
                    Locale(*locale.split("_")).language_name)
        return self._language_names

    def get_current_language(self) -> Tuple[str, str]:
        """Gets the current selected language

        Returns:
            Tuple[str]: Tuple. language code, readable name ("en_US", "English")
        """
        current_name = self._language_names[self._available_langs.index(
            self._lang)]
        return self._lang, current_name

    def update_mycroft_config(self) -> None:
        """Updates Mycroft config file.
        """
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
