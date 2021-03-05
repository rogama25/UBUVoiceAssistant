import gettext
from babel import Locale
from typing import Union, List
import os


class Translator:
    def __init__(self, lang: str) -> None:
        self._lang = None
        self._available_langs = []
        self._language_names = []
        self._domain = "UBUVoiceAssistant"
        self._lang_dir = "./lang"
        self.find_available_languages()
        self.change_language(lang)

    def change_language(self, lang: Union[str, int]) -> None:
        if isinstance(lang, int):
            self.change_language(self._available_langs[lang])
        self._lang = lang
        translator = gettext.translation(
            self._domain, self._lang_dir, [self._lang])
        translator.install()

    def translate(self, string: str) -> str:
        return _(string)

    def find_available_languages(self) -> List[str]:
        self._available_langs = []
        self._language_names = []
        for locale in os.listdir(self._lang_dir):
            if os.path.isfile(self._lang_dir + "/" + locale + "/LC_MESSAGES/" + self._domain + ".mo"):
                self._available_langs.append(locale)
                self._language_names.append(
                    Locale(*locale.split("_")).language_name)
        return self._language_names
