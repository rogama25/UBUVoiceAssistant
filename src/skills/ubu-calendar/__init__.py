import sys
from os.path import expanduser
sys.path.append(expanduser('~') + '/UBUAssistant/src')
import re
from datetime import datetime, timedelta
from mycroft import MycroftSkill, intent_handler
from webservice.web_service import WebService
from util import util

class UbuCalendarSkill(MycroftSkill):

    def __init__(self):
        super().__init__()
        self.learning = True
        self.months = {'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5,
                       'junio':6, 'julio':7, 'agosto':8, 'septiembre':9,
                       'octubre':10, 'noviembre':11, 'diciembre':12}

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler('UpcomingEvents.intent')
    def handle_upcoming_events_intent(self, message):
        events = self.ws.get_calendar_upcoming_view()
        self.speak(util.text_to_speech(events))

    @intent_handler('DayEvents.intent')
    def handle_day_events_intent(self, message):
        self.month = str(self.months[message.data['month']])
        events = self.ws.get_calendar_day_view(year=str(message.data['year']), month=self.month, day=str(message.data['day']))
        self.speak(util.text_to_speech(events))

    @intent_handler('CourseEvents.intent')
    def handle_course_events_intent(self, message):
        course = message.data['course']
        id = util.get_course_id_by_name(course, self.ws.get_user_courses().items())
        if id:
            events = self.ws.get_calendar_events_by_courseid(id)
            self.speak(util.text_to_speech(events))
        else:
            self.speak_dialog('no.course')

    @intent_handler('RecentUpdates.intent')
    def handle_course_updates(self, message):
        course = message.data['course']
        course_id = util.get_course_id_by_name(course, self.ws.get_user_courses().items())
        cmids = self.ws.get_course_updates_since(course_id, int(datetime.timestamp(datetime.today() - timedelta(days=1))))
        module_names = self.ws.get_course_module(cmids)
        if module_names:
            self.speak(util.text_to_speech(module_names))
        else:
            self.speak_dialog('changes')

    def stop(self):
        pass

def create_skill():
    return UbuCalendarSkill()
