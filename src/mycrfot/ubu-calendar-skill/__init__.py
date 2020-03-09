from mycroft import MycroftSkill, intent_file_handler


class UbuCalendar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('my.test.intent')
    def handle_calendar_ubu(self, message):
        self.speak_dialog('my.test')


def create_skill():
    return UbuCalendar()

