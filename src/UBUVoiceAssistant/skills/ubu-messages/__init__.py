import sys
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler # type: ignore
from mycroft.audio import wait_while_speaking
sys.path.append("/usr/lib/UBUVoiceAssistant") # type: ignore
from UBUVoiceAssistant.util import util # type: ignore


class UbuMessagesSkill(MycroftSkill):

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler(IntentBuilder("UnreadMessagesIntent").require("UnreadMessagesVoc"))
    def handle_unread_messages(self, message):
        convers = self.ws.get_conversations_with_messages()
        messages = {}
        for conver in convers:
            messages.update(conver.get_messages())
        l = messages.keys()
        l = sorted(l, reverse=True)
        for n, m in enumerate(l):
            self.speak(messages[m].get_clean_text())
            wait_while_speaking()
            if n == 4:
                break

def create_skill():
    return UbuMessagesSkill()