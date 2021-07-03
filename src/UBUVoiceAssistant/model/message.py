"""Module for the message class
"""
from bs4 import BeautifulSoup


class Message():
    """Class for the messages
    """
    def __init__(self, json: dict) -> None:
        self.__message_id: int = json["id"]
        self.__useridfrom: int = json["useridfrom"]
        self.__text: str = json["text"]
        self.__timecreated: int = json["timecreated"]

    def get_message_id(self) -> int:
        """Gets the message id

        Returns:
            int: message id
        """
        return self.__message_id

    def get_useridfrom(self) -> int:
        """Gets the user id who sent this message

        Returns:
            int: user id
        """
        return self.__useridfrom

    def get_text(self) -> str:
        """Gets the raw text of the message

        Returns:
            str: text
        """
        return self.__text

    def get_timecreated(self) -> int:
        """Gets the timestamp of the message

        Returns:
            int: unix time of the message
        """
        return self.__timecreated

    def get_clean_text(self) -> str:
        """Gets the text of the message, without any HTML tags

        Returns:
            str: text
        """
        return BeautifulSoup(self.__text, "html.parser").get_text()
