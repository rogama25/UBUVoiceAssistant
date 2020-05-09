import requests
#Regular Expressions
import re
from bs4 import BeautifulSoup

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

    def set_session_cookies(self, username, password):
        self.__session = requests.Session()
        host_login = "https://ubuvirtual.ubu.es/login/index.php"

        page = self.__session.get(host_login)
        soup = BeautifulSoup(page.content, 'html.parser')
        login_token = soup.find('input', {'name': 'logintoken'})
        login_token = login_token.get('value')
        form_params = {'username': username, 'password': password, 'logintoken':login_token}

        self.__session.post(host_login, data=form_params)
        #soup = BeautifulSoup(page.content, 'html.parser')
        #session_key = soup.find('script', {'type':'text/javascript'})
        #session_key = str(session_key).split('"sesskey":"')[1].split('"')[0]
        #print(session_key)
        self.cookies = self.__session.cookies.get_dict()

    def set_url_with_token(self, username, password):
        url = self.__host + '/login/token.php'
        url_params = {'username':username, 'password':password, 'service':'moodle_mobile_app'}
        r = requests.post(url, params=url_params).json()
        token = r['token']
        self.__url_with_token = self.__host + '/webservice/rest/server.php?wstoken=' + token + '&moodlewsrestformat=json&wsfunction='

    def set_userid(self):
        url = self.__url_with_token + 'core_webservice_get_site_info'
        r = requests.get(url).json()
        self.__userid = str(r['userid'])

    def get_userid(self):
        return self.__userid

    def set_user_courses(self):
        url = self.__url_with_token + 'core_enrol_get_users_courses&userid=' + self.__userid
        r = requests.get(url).json()
        self.__user_courses = {}
        for course in r:
            id = course['id']
            name = course['displayname']
            self.__user_courses[id] = name

    def get_user_courses(self):
        return self.__user_courses

    def get_calendar_day_view(self, year, month, day):
        url = self.__url_with_token + 'core_calendar_get_calendar_day_view&year=' + year + '&month=' + month + '&day=' + day
        r = requests.get(url).json()
        events = self.convert_events_to_readable_text(r['events'])
        return events

    def get_calendar_events_by_courseid(self, courseid):
        url = self.__url_with_token + 'core_calendar_get_action_events_by_course&courseid=' + courseid
        r = requests.get(url).json()
        events = self.convert_events_to_readable_text(r['events'])
        return events

    def get_calendar_upcoming_view(self):
        url = self.__url_with_token + 'core_calendar_get_calendar_upcoming_view'
        r = requests.get(url).json()
        events = self.convert_events_to_readable_text(r['events'])
        return events

    def get_final_grades(self, userid):
        url = self.__url_with_token + 'gradereport_overview_get_course_grades&userid=' + userid
        r = requests.get(url).json()
        grades = []
        for course_grade in r['grades']:
            id = course_grade['courseid']
            course = self.__user_courses.get(id)
            grade = course_grade['grade']
            grades.append((course, grade))
        return grades

    def get_course_updates_since(self, courseid, timestamp):
        url = self.__url_with_token + 'core_course_get_updates_since&courseid=' + courseid + '&since=' + str(timestamp)
        r = requests.get(url).json()
        updated_modules_ids = []
        for updates in r['instances']:
            updated_modules_ids.append(updates['id'])
        return updated_modules_ids

    def get_course_module(self, cmid_array):
        updated_modules = []
        for cmid in cmid_array:
            url = self.__url_with_token + 'core_course_get_course_module&cmid=' + str(cmid)
            r = requests.get(url).json()
            updated_modules.append(r['cm']['name'])
        return updated_modules

    def get_course_grades(self, courseid):
        page = self.__session.get('https://ubuvirtual.ubu.es/grade/report/user/index.php?id=' + courseid ,cookies=self.cookies)
        soup = BeautifulSoup(page.content, 'html.parser')
        grades = []
        for tr in soup.find_all('tr')[2:]:
            grades_table = tr.find_all(['th','td'])
            if len(grades_table) == 7:
                grades.append(grades_table[0].get_text() + ': ' + grades_table[2].get_text())
            elif len(grades_table) != 0:
                grades.append(grades_table[1].get_text())
        return grades

    def get_course_forums(self, courseid):
        url = self.__url_with_token + 'mod_forum_get_forums_by_courses&courseids[0]=' + courseid
        r = requests.get(url).json()
        return r

    def get_forum_discussions(self, forumid):
        url = self.__url_with_token + 'mod_forum_get_forum_discussions&forumid=' + forumid
        r = requests.get(url).json()
        return r

    def get_forum_discussion_posts(self, discussionid):
        url = self.__url_with_token + 'mod_forum_get_forum_discussion_posts&discussionid=' + discussionid
        r = requests.get(url).json()
        return r

    def convert_events_to_readable_text(self, events):
        events_info = []
        for event in events:
            event_info = []
            date = re.sub('<.*?>', '', event['formattedtime'])
            event_info.append(date)
            event_info.append(event['name'])
            events_info.append(event_info)
        return events_info
