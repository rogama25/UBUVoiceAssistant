import sys
from mycroft import MycroftSkill, intent_handler # type: ignore
sys.path.append("/usr/lib/UBUVoiceAssistant") # type: ignore
from util import util # type: ignore


class UbuMessagesSkill(MycroftSkill):

    def __init__(self):
        super().__init__()
        self.forums = {}
        self.learning = True

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler("UnreadMessages.intent")
    def handle_unread_messages(self, message):
        self.speak_dialog("no.unread.messages")

    @intent_handler("SendMessage.intent")
    def handle_send_message(self, message):
        user = self.get_response("to.who")

def create_skill():
    return UbuMessagesSkill()