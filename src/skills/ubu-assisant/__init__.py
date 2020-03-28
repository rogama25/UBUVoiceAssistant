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
sys.path.append('/home/adp1002/UBUCalendar/src')
import socket, pickle
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from webservice.web_service import WebService

class UbuAssistantSkill(MycroftSkill):

    def __init__(self):
        super().__init__()
        self.host = 'localhost'
        self.port = 5555
        self.learning = True

    def initialize(self):
        #my_setting = self.settings.get('my_setting')
        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))
        webservice_data = self.client_socket.recv(4096)
        self.ws = pickle.loads(webservice_data)
        self.client_socket.close()


    @intent_handler('UpcomingEvents.intent')
    def handle_upcoming_events_intent(self, message):
        events = self.ws.get_calendar_upcoming_view()
        text = ''
        for event in events:
            text = text + ' '.join(event)
            text = text + '.'
        self.speak(text)

    @intent_handler('DayEvents.intent')
    def handle_day_events_intent(self, message):
        self.ws.get_calendar_upcoming_view()
        self.speak('Hola')

    def stop(self):
        pass


def create_skill():
    return UbuAssistantSkill()
