import requests
#Regular Expressions
import re

class WebService:
    __instance = None

    #Singleton
    def __init__(self):
        WebService.__instance = self

    @staticmethod
    def get_instance():
        if WebService.__instance == None:
            return WebService()
        return WebService.__instance

    def set_host(self,host):
        self.__host = host

    def set_url_with_token(self, username, password):
        url = self.__host + '/login/token.php'
        url_params = {'username':username, 'password':password, 'service':'moodle_mobile_app'}
        r = requests.get(url, params=url_params).json()
        token = r['token']
        self.__url_with_token = self.__host + '/webservice/rest/server.php?wstoken=' + token + '&moodlewsrestformat=json&wsfunction='

    def get_userid(self):
        if self.__userid == 0:
            url = self.__url_with_token + 'core_webservice_get_site_info'
            r = requests.get(url).json()
            self.__userid = r['userid']
        return self.__userid

    def get_calendar_day_view(self, year, month, day):
        url = self.__url_with_token + 'core_calendar_get_calendar_day_view&year=' + year + '&month=' + month + '&day=' + day
        r = requests.get(url).json()
        return r

    def get_calendar_events_by_courseid(self, courseid):
        url = self.__url_with_token + 'core_calendar_get_action_events_by_course&courseid=' + courseid
        r = requests.get(url).json()
        return r

    def get_calendar_upcoming_view(self):
        url = self.__url_with_token + 'core_calendar_get_calendar_upcoming_view'
        r = requests.get(url).json()
        events = r['events']
        events_info = []
        for event in events:
            event_info = []
            date = re.sub('<.*?>', '', event['formattedtime'])
            event_info.append(date)
            event_info.append(event['name'])
            events_info.append(event_info)
        return events_info
