"""Module for the conversation class"""
from typing import Dict
from .user import User
from .message import Message


class Conversation():
    """Class for the Moodle conversations"""
    def __init__(self, json: dict) -> None:
        self.__conversation_id: int = json["id"]
        self.__isread: bool = json["isread"]
        if self.__isread is True:
            self.__unreadcount = 0
        else:
            self.__unreadcount = json["unreadcount"]
        self.__name: str = json["name"]
        if self.__name is None:
            self.__name = ""
        self.__subname: str = json["subname"]
        if self.__subname is None:
            self.__subname = ""
        self.__members: Dict[int, User] = {}
        for member in json["members"]:
            self.__members[member["id"]] = User(member)
        self.__messages: Dict[int, Message] = {}
        for message in json["messages"]:
            self.__messages[message["id"]] = Message(message)

    def get_conversation_id(self) -> int:
        """Gets the conversation id

        Returns:
            int: conversation id
        """
        return self.__conversation_id

    def get_isread(self) -> bool:
        """Gets if the conversation is read

        Returns:
            bool: true if is read, false if not
        """
        return self.__isread

    def get_unreadcount(self) -> int:
        """Gets the number of unread messages

        Returns:
            int: unread messages count
        """
        return self.__unreadcount

    def get_name(self) -> str:
        """Gets the name for the conversation

        Returns:
            str: conversation name
        """
        return self.__name

    def get_subname(self) -> str:
        """Gets the subname for the conversation

        Returns:
            str: conversation subname
        """
        return self.__subname

    def get_members(self) -> Dict[int, User]:
        """Gets the members of the conversation

        Returns:
            Dict[int, User]: Dictionary userid, user
        """
        return self.__members

    def get_messages(self) -> Dict[int, Message]:
        """Gets the messages in a conversation

        Returns:
            Dict[int, Message]: Dictionary messageid, message
        """
        return self.__messages
