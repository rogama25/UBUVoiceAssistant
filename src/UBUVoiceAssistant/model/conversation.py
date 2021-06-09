from typing import Dict
from . import User
from . import Message


class Conversation():
    def __init__(self, json: dict) -> None:
        self.__conversation_id: int = json["id"]
        self.__isread: bool = json["isread"]
        if self.__isread == True:
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
        self.__messages: Dict[int, Message]
        for message in json["messages"]:
            self.__messages[message["id"]] = Message(message)

    def get_conversation_id(self) -> int:
        return self.__conversation_id

    def get_isread(self) -> bool:
        return self.__isread

    def get_unreadcount(self) -> int:
        return self.__unreadcount

    def get_name(self) -> str:
        return self.__name
    
    def get_subname(self) -> str:
        return self.__subname

    def get_members(self) -> Dict[int, User]:
        return self.__members
    
    def get_messages(self) -> Dict[int, Message]:
        return self.__messages