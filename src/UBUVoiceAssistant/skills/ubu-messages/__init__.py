import sys
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler # type: ignore
sys.path.append("/usr/lib/UBUVoiceAssistant") # type: ignore
from util import util # type: ignore


class UbuMessagesSkill(MycroftSkill):

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler(IntentBuilder("UnreadMessages").require("UnreadMessages"))
    def handle_unread_messages(self, message):
        self.speak_dialog("no.unread.messages")

def create_skill():
    return UbuMessagesSkill()