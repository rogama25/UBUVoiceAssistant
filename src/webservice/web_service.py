import requests
from util import util
from model.course import Course
from model.event import Event
from model.user import User


class WebService:
    __instance = None

    # Singleton
    def __init__(self):
        WebService.__instance = self

    @staticmethod
    def get_instance():
        if WebService.__instance is None:
            return WebService()
        return WebService.__instance

    def set_host(self, host):
        self.__host = host

    # Código para obtener las cookies del usuario para Web Scraping
    '''def set_session_cookies(self, username, password):
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
        self.cookies = self.__session.cookies.get_dict()'''

    def set_url_with_token(self, username, password):
        url = self.__host + '/login/token.php'
        url_params = {'username': username, 'password': password, 'service': 'moodle_mobile_app'}
        r = requests.post(url, params=url_params).json()
        token = r['token']
        self.__url_with_token = self.__host + '/webservice/rest/server.php?wstoken=' \
            + token + '&moodlewsrestformat=json&wsfunction='

    def initialize_useful_data(self):
        url = self.__url_with_token + 'core_webservice_get_site_info'
        r = requests.get(url).json()
        self.__user = User(str(r['userid']))
        self.__lang = r['lang']

    def get_lang(self):
        return self.__lang

    def get_user(self):
        return self.__user

    def set_user_courses(self):
        url = self.__url_with_token + 'core_enrol_get_users_courses&userid=' + self.get_user().get_id()
        r = requests.get(url).json()
        self.__user_courses = []
        for course in r:
            self.__user_courses.append(Course(course))

        self.__user.set_courses(self.__user_courses)

    def get_user_courses(self):
        return self.__user_courses

    def get_calendar_day_view(self, year, month, day):
        events = []
        url = self.__url_with_token + 'core_calendar_get_calendar_day_view&year=' \
            + year + '&month=' + month + '&day=' + day
        r = requests.get(url).json()
        for event in r['events']:
            events.append(Event(event))
        return events

    def get_calendar_events_by_courseid(self, courseid):
        events = []
        url = self.__url_with_token + 'core_calendar_get_action_events_by_course&courseid=' + courseid
        r = requests.get(url).json()
        for event in r['events']:
            events.append(Event(event))
        return events

    def get_calendar_upcoming_view(self):
        events = []
        url = self.__url_with_token + 'core_calendar_get_calendar_upcoming_view'
        r = requests.get(url).json()
        for event in r['events']:
            events.append(Event(event))
        return events

    def get_final_grades(self):
        url = self.__url_with_token + 'gradereport_overview_get_course_grades&userid=' + self.get_user().get_id()
        r = requests.get(url).json()
        grades = []
        for course_grade in r['grades']:
            course_id = course_grade['courseid']
            course = self.__user.get_courses().get(course_id)
            grade = course_grade['grade']
            grades.append(course.get_name() + ' ' + grade)
        return grades

    def get_course_updates_since(self, courseid, timestamp):
        url = self.__url_with_token + 'core_course_get_updates_since&courseid=' \
            + courseid + '&since=' + str(timestamp)
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
        grades = []
        url = self.__url_with_token + 'gradereport_user_get_grade_items&courseid=' \
            + courseid + '&userid=' + self.get_user().get_id()
        r = requests.get(url).json()
        grades_dict = r['usergrades'][0]
        for grade in grades_dict['gradeitems']:
            grade_value = grade['graderaw']
            if grade_value and (grade['itemtype'] == 'mod'):
                grades.append(grade['itemname'] + ' ' + str(grade_value))
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
