"""WebService file
"""
from typing import Dict, List, Optional, Union

import requests

from ..model.conversation import Conversation
from ..model.course import Course
from ..model.user import User


class WebService:
    """WebService class
    """
    def __init__(self) -> None:
        self.__host: str = ""
        self.__url_with_token: str = ""
        self.__user: User = None
        self.__lang: str = ""
        self.__user_courses: List[Course] = []

    def set_host(self, host: str):
        """Sets the WebService host

        Args:
            host (str): A string with the host name
        """
        self.__host = host

    # Code to obtain the user's cookies/session for web scraping
    # def set_session_cookies(self, username, password):
    #     self.__session = requests.Session()
    #     host_login = "https://ubuvirtual.ubu.es/login/index.php"

    #     page = self.__session.get(host_login)
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     login_token = soup.find('input', {'name': 'logintoken'})
    #     login_token = login_token.get('value')
    #     form_params = {'username': username, 'password': password, 'logintoken':login_token}

    #     self.__session.post(host_login, data=form_params)
    #     #soup = BeautifulSoup(page.content, 'html.parser')
    #     #session_key = soup.find('script', {'type':'text/javascript'})
    #     #session_key = str(session_key).split('"sesskey":"')[1].split('"')[0]
    #     #print(session_key)
    #     self.cookies = self.__session.cookies.get_dict()

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
        req = requests.post(url, params=url_params).json()
        token = req['token']
        self.__url_with_token = self.__host + '/webservice/rest/server.php?wstoken=' \
            + token + '&moodlewsrestformat=json&wsfunction='

    def initialize_useful_data(self):
        """ Initializes data needed for some requests or functionality.
        ---
            Sends a GET request using core_webservice_get_site_info to retrieve
            data such as the user's id and the Moodle's language.
        """
        url = self.__url_with_token + 'core_webservice_get_site_info'
        req = requests.get(url).json()
        self.__user = User(str(req['userid']))
        self.__lang = req['lang']

    def get_lang(self) -> str:
        """Gets Moodle language

        Returns:
            str: A string containing the Moodle language
        """
        return self.__lang

    def get_user(self) -> User:
        """Gets the current user

        Returns:
            User: the current User object
        """
        return self.__user

    def set_user_courses(self):
        """ Gets and sets the user's courses
        ---
            Sends a GET request using core_enrol_get_users_courses to retrieve
            the courses that the user is enrolled in.
        """
        url = (self.__url_with_token + 'core_enrol_get_users_courses&userid='
            + self.get_user().get_id())
        req = requests.get(url).json()
        self.__user_courses = []
        for course in req:
            course = Course(course)
            self.__user_courses.append(course)
            self.get_user().set_course(course)

    def get_user_courses(self) -> List[Course]:
        """Gets the list of courses for the current user

        Returns:
            List[Course]: List of Courses
        """
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
        req = requests.get(url).json()
        return req

    def get_calendar_events_by_courseid(self, courseid):
        """ GET request using core_calendar_get_action_events_by_course
        ---
            Parameters:
                - String courseid: id of the course to get the events from
            Returns: JSONObject with the request response.
        """
        url = (self.__url_with_token + 'core_calendar_get_action_events_by_course&courseid='
            + courseid)
        req = requests.get(url).json()
        return req

    def get_calendar_upcoming_view(self):
        """ GET request using core_calendar_get_action_events_by_course
        ---
            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'core_calendar_get_calendar_upcoming_view'
        req = requests.get(url).json()
        return req

    def get_final_grades(self):
        """ GET request using gradereport_overview_get_course_grades
        ---
            Returns: JSONObject with the request response.
        """
        url = (self.__url_with_token + 'gradereport_overview_get_course_grades&userid='
            + self.get_user().get_id())
        req = requests.get(url).json()
        grades = []
        for course_grade in req['grades']:
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
        req = requests.get(url).json()
        updated_modules_ids = []
        for updates in req['instances']:
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
            req = requests.get(url).json()
            updated_modules.append(req['cm']['name'])
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
        req = requests.get(url).json()
        return req['usergrades'][0]

    def get_course_forums(self, courseid):
        """ GET request using mod_forum_get_forums_by_courses
        ---
            Parameters:
                - String courseid: id of the course to get the froums from

            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'mod_forum_get_forums_by_courses&courseids[0]=' + courseid
        req = requests.get(url).json()
        return req

    def get_forum_discussions(self, forumid):
        """ GET request using mod_forum_get_forum_discussions
        ---
            Parameters:
                - String forumid: id of the forum to get the discussions from

            Returns: JSONObject with the request response.
        """
        url = self.__url_with_token + 'mod_forum_get_forum_discussions&forumid=' + forumid
        req = requests.get(url).json()
        return req

    def get_forum_discussion_posts(self, discussionid):
        """ GET request using mod_forum_get_forum_discussion_posts
        ---
            Parameters:
                - String discussionid: id of the discussion to get the posts from

            Returns: JSONObject with the request response.
        """
        url = (self.__url_with_token + 'mod_forum_get_forum_discussion_posts&discussionid='
            + discussionid)
        req = requests.get(url).json()
        return req

    def get_conversations(self) -> List[Conversation]:
        url = (self.__url_with_token + "core_message_get_conversations")
        params = {"userid": self.get_user().get_id()}
        req = requests.get(url, params).json()
        result: List[Conversation] = []
        for conversation in req["conversations"]:
            result.append(Conversation(conversation))
        return result

    def get_conversations_with_messages(self) -> List[Conversation]:
        convers = self.get_conversations()
        url = (self.__url_with_token + "core_message_get_conversation")
        result: List[Conversation] = []
        for c in convers:
            params = {
                "userid": self.get_user().get_id(),
                "conversationid": c.get_conversation_id(),
                "includecontactrequests": 0,
                "includeprivacyinfo": 0
            }
            req = requests.get(url, params).json()
            result.append(Conversation(req))
        return result

    def send_message_to_conversation(self, message: str, conversation: int):
        url = (self.__url_with_token + "core_message_send_messages_to_conversation")
        params: Dict[str, Union[str, int]] = {
            "conversationid": conversation,
            "messages[0][text]": message,
            "messages[0][textformat]": 2 # PLAIN
        }
        req = requests.get(url, params).json()

    def send_message_to_user(self, message: str, user: int):
        url = (self.__url_with_token + "core_message_send_instant_messages")
        params: Dict[str, Union[str, int]] = {
            "messages[0][touserid]": user,
            "messages[0][text]": message,
            "messages[0][textformat]": 2 # PLAIN
        }
        req = requests.get(url, params).json()

    def check_can_message_user(self, user: int) -> bool:
        url = (self.__url_with_token + "core_message_get_member_info")
        params = {
            "referenceuserid": self.__user.get_id(),
            "userids[0]": user,
            "includeprivacyinfo": 1
        }
        req = requests.get(url, params).json()
        return bool(req[0]["canmessage"])

    def get_participants_by_course(self, course: int) -> List[User]:
        url = (self.__url_with_token + "core_enrol_get_enrolled_users")
        params = {"courseid": course}
        req = requests.get(url, params).json()
        result = []
        for participant in req:
            result.append(User(participant))
        return result
