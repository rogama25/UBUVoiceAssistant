import sys
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler  # type: ignore
from mycroft.audio import wait_while_speaking
sys.path.append("/usr/lib/UBUVoiceAssistant")  # type: ignore
from UBUVoiceAssistant.util import util  # type: ignore


class UbuMessagesSkill(MycroftSkill):

    def __init__(self):
        super().__init__()
        self.request_stop = False

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler(IntentBuilder("UnreadMessagesIntent").require("UnreadMessagesVoc"))
    def recent_messages(self, message):
        self.request_stop = False
        self.speak("Dame un momento, por favor")
        convers = self.ws.get_conversations_with_messages()
        messages = {}
        msg_from = {}
        for conver in convers:
            messages.update(conver.get_messages())
            for m in conver.get_messages().values():
                msg_from[m.get_message_id()] = util.reorder_name(
                    list(conver.get_members().values())[0].get_fullname())
        l = messages.keys()
        l = sorted(l, reverse=True)
        for n, m in enumerate(l):
            self.speak(msg_from[m] + " dice: " + messages[m].get_clean_text())
            wait_while_speaking()
            if n == 4 or self.request_stop:
                break

    @intent_handler(IntentBuilder("SendMessage").require("EnviarAPersona"))
    def send_message(self, message):
        persona = message.data.get("EnviarAPersona")
        self.ask_yesno("Enviar a " + persona + "?")
        convers = self.ws.get_conversations()
        id_convers = {}
        for conver in convers:
            id_convers[util.reorder_name(list(conver.get_members().values())[
                                         0].get_fullname())] = conver.get_conversation_id()
        if persona in id_convers:
            conversation_id = id_convers[persona]
            # send message logic
        else:
            self.speak("No existe esa persona en la lista de conversaciones")

    def stop(self):
        self.request_stop = True


def create_skill():
    return UbuMessagesSkill()
