import sys
from os.path import expanduser
sys.path.append(expanduser('~') + '/UBUCalendar/src')
import socket, pickle
import re
from datetime import datetime
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from webservice.web_service import WebService
from util import util

class UbuGradesSkill(MycroftSkill):

    def __init__(self):
        super().__init__()
        self.forums = {}
        self.learning = True

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler('Grades.intent')
    def handle_grades_intent(self, message):
        grades = self.ws.get_final_grades(self.ws.get_userid())
        self.speak(util.text_to_speech(grades))

    @intent_handler('CourseGrades.intent')
    def handle_course_grades(self, message):
        course = message.data['course']
        course_id = util.get_course_id_by_name(course, self.ws.get_user_courses().items())
        grades = self.ws.get_course_grades(course_id)
        self.speak(util.text_to_speech(grades))

    def stop(self):
        pass

def create_skill():
    return UbuGradesSkill()
