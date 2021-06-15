from bs4 import BeautifulSoup

class Message():
    def __init__(self, json: dict) -> None:
        self.__message_id: int = json["id"]
        self.__useridfrom: int = json["useridfrom"]
        self.__text: str = json["text"]
        self.__timecreated: int = json["timecreated"]

    def get_message_id(self) -> int:
        return self.__message_id
    
    def get_useridfrom(self) -> int:
        return self.__useridfrom
    
    def get_text(self) -> str:
        return self.__text

    def get_timecreated(self) -> int:
        return self.__timecreated

    def get_clean_text(self) -> str:
        return BeautifulSoup(self.__text, "html.parser").get_text()