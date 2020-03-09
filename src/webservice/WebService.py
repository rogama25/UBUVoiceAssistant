import requests

class WebService:
    __host = "https://ubuvirtual.ubu.es"
    __token = ''
    __userid = 0
    __url_with_token = ''
    __userid


    def set_host(self,host):
        self.__host = host

    def set_url_with_token(self, username, password):
        url = self.__host + "/login/token.php"
        print(url)
        url_params = {'username':username, 'password':password, 'service':'moodle_mobile_app'}
        r = requests.get(url, params=url_params).json()
        self.__token = r['token'])
        self.__url_with_token = self.__host + '/webservice/rest/server.php?wstoken=' + self.__token + '&moodlewsrestformat=json&wsfunction='

    def get_userid(self):
        url = self.__url_with_token + 'core_webservice_get_site_info'
        r = requests.get(url).json()
        self.__userid = r['userid']

    def get_calendar_day_view(self, year, month, day):
        url = self.__url_with_token + 'core_calendar_get_calendar_day_view&year=' + year + '&month=' + month + '&day=' + day
        r = requests.get(url).json()
        return r

    def get_calendar_events_by_courseid(courseid):
        url = self.__url_with_token + 'core_calendar_get_action_events_by_course&courseid=' + courseid
        r = requests.get(url).json()
        return r
