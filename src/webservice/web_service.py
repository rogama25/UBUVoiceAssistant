import requests
from model.course import Course
from model.user import User


class WebService:

    def set_host(self, host):
        self.__host = host

    # Code to obtain the user's cookies/session for web scraping
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
        """ Gets Moodle's token and initializes the url
        ---
            Sends a POST request to [host]/login/token.php with the user's
            username and password to get the user's token and adds the token to
            the URL along with some URL params such as moodlewsrestformat=json
            and the key wsfunction.
        ---
            Parameters:
                username: user's Moodle username
                password: user's Moodle password
        """
        url = self.__host + '/login/token.php'
        url_params = {'username': username, 'password': password, 'service': 'moodle_mobile_app'}
        r = requests.post(url, params=url_params).json()
        token = r['token']
        self.__url_with_token = self.__host + '/webservice/rest/server.php?wstoken=' \
            + token + '&moodlewsrestformat=json&wsfunction='

    def initialize_useful_data(self):
        """ Initializes data needed for some requests or functionality.
        ---
            Sends a GET request using core_webservice_get_site_info to retrieve
            data such as the user's id and the Moodle's language.
        """
        url = self.__url_with_token + 'core_webservice_get_site_info'
        r = requests.get(url).json()
        self.__user = User(str(r['userid']))
        self.__lang = r['lang']

    def get_lang(self):
        return self.__lang

    def get_user(self):
        return self.__user

    def set_user_courses(self):
        """ Gets and sets the user's courses
        ---
            Sends a GET request using core_enrol_get_users_courses to retrieve
            the courses that the user is enrolled in.
        """
        url = self.__url_with_token + 'core_enrol_get_users_courses&userid=' + self.get_user().get_id()
        r = requests.get(url).json()
        self.__user_courses = []
        for course in r:
            course = Course(course)
            self.__user_courses.append(course)
            self.get_user().set_course(course)

    def get_user_courses(self):
        return self.__user_courses

    def get_calendar_day_view(self, year, month_number, day):
        """ GET request using core_calendar_get_calendar_day_view
        ---
            Parameters:
                - String year
                - String month
                - String day

            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'core_calendar_get_calendar_day_view&year=' \
            + year + '&month=' + month_number + '&day=' + day
        r = requests.get(url).json()
        return r

    def get_calendar_events_by_courseid(self, courseid):
        """ GET request using core_calendar_get_action_events_by_course
        ---
            Parameters:
                - String courseid: id of the course to get the events from
            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'core_calendar_get_action_events_by_course&courseid=' + courseid
        r = requests.get(url).json()
        return r

    def get_calendar_upcoming_view(self):
        """ GET request using core_calendar_get_action_events_by_course
        ---
            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'core_calendar_get_calendar_upcoming_view'
        r = requests.get(url).json()
        return r

    def get_final_grades(self):
        """ GET request using gradereport_overview_get_course_grades
        ---
            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'gradereport_overview_get_course_grades&userid=' + self.get_user().get_id()
        r = requests.get(url).json()
        grades = []
        for course_grade in r['grades']:
            course_id = course_grade['courseid']
            course = self.get_user().get_courses().get(str(course_id))
            grade = course_grade['grade']
            grades.append(course.get_name() + ' ' + grade)
        return grades

    def get_course_updates_since(self, courseid, timestamp):
        """ GET request using core_course_get_updates_since
        ---
            Parameters:
                - String courseid: id of the course to get the events from
                - timestamp: with the date to get the events since

            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'core_course_get_updates_since&courseid=' \
            + courseid + '&since=' + str(timestamp)
        r = requests.get(url).json()
        updated_modules_ids = []
        for updates in r['instances']:
            updated_modules_ids.append(updates['id'])
        return updated_modules_ids

    def get_course_module(self, cmid_array):
        """ GET request using core_course_get_course_module
        ---
            Parameters:
                - cmid_array: array with the course modules ids

            Returns: JSONObject with the request response.
        """
        updated_modules = []
        for cmid in cmid_array:
            url = self.__url_with_token + 'core_course_get_course_module&cmid=' + str(cmid)
            r = requests.get(url).json()
            updated_modules.append(r['cm']['name'])
        return updated_modules

    def get_course_grades(self, courseid):
        """ GET request using gradereport_user_get_grade_items
        ---
            Parameters:
                - String courseid: id of the course to get the grades from

            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'gradereport_user_get_grade_items&courseid=' \
            + courseid + '&userid=' + self.get_user().get_id()
        r = requests.get(url).json()
        return r['usergrades'][0]

    def get_course_forums(self, courseid):
        """ GET request using mod_forum_get_forums_by_courses
        ---
            Parameters:
                - String courseid: id of the course to get the froums from

            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'mod_forum_get_forums_by_courses&courseids[0]=' + courseid
        r = requests.get(url).json()
        return r

    def get_forum_discussions(self, forumid):
        """ GET request using mod_forum_get_forum_discussions
        ---
            Parameters:
                - String forumid: id of the forum to get the discussions from

            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'mod_forum_get_forum_discussions&forumid=' + forumid
        r = requests.get(url).json()
        return r

    def get_forum_discussion_posts(self, discussionid):
        """ GET request using mod_forum_get_forum_discussion_posts
        ---
            Parameters:
                - String discussionid: id of the discussion to get the posts from

            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'mod_forum_get_forum_discussion_posts&discussionid=' + discussionid
        r = requests.get(url).json()
        return r
