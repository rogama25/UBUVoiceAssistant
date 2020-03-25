# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.
import sys
sys.path.append('/home/adp1002/')
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from UBUCalendar.src.webservice.web_service import WebService

class UbuAssistantSkill(MycroftSkill):
    ws = WebService.get_instance()
    def __init__(self):
        super().__init__()
        #self.ws.set_host('https://school.moodledemo.net')
        #self.ws.set_url_with_token('student','moodle')
        self.learning = True

    def initialize(self):
        my_setting = self.settings.get('my_setting')

    @intent_handler('UpcomingEvents.intent')
    def handle_upcoming_events_intent(self, message):
        events = self.ws.get_calendar_upcoming_view()
        text = ''
        for event in events:
            text = text + ' '.join(event)
            text = text + '.'
        self.speak(text)

    def stop(self):
        pass


def create_skill():
    return UbuAssistantSkill()
