import sys
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler # type: ignore
from mycroft.audio import wait_while_speaking
sys.path.append("/usr/lib/UBUVoiceAssistant") # type: ignore
from UBUVoiceAssistant.util import util # type: ignore
from UBUVoiceAssistant.model.conversation import Conversation


class UbuMessagesSkill(MycroftSkill):

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler(IntentBuilder("UnreadMessagesIntent").require("UnreadMessagesVoc"))
    def handle_unread_messages(self, message):
        self.speak("Dame un momento, por favor")
        convers = self.ws.get_conversations_with_messages()
        messages = {}
        msg_from = {}
        for conver in convers:
            messages.update(conver.get_messages())
            for m in conver.get_messages().values():
                msg_from[m.get_message_id()] = list(conver.get_members().values())[0].get_fullname()
        l = messages.keys()
        l = sorted(l, reverse=True)
        for n, m in enumerate(l):
            self.speak(msg_from[m] + " dice " + messages[m].get_clean_text())
            wait_while_speaking()
            if n == 4:
                break

    @intent_handler(IntentBuilder("SendMessage").require("EnviarAPersona"))
    def send_message(self, message):
        persona = message.data.get("EnviarAPersona")
        self.speak(persona)

def create_skill():
    return UbuMessagesSkill()