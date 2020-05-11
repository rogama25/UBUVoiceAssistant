import sys
from os.path import expanduser
sys.path.append(expanduser('~') + '/UBUCalendar/src')
import re
from datetime import datetime
from mycroft import MycroftSkill, intent_handler
from webservice.web_service import WebService
from model.discussion import Discussion
from model.forum import Forum
from util import util

class UbuCourseSkill(MycroftSkill):

    def __init__(self):
        super().__init__()
        self.forums = {}
        self.learning = True

    def initialize(self):
        self.ws = util.get_data_from_server(util.SOCKET_HOST, util.SOCKET_PORT)

    @intent_handler('CourseForums.intent')
    def handle_course_forums(self, message):
        course = message.data['course']
        course_id = util.get_course_id_by_name(course, self.ws.get_user_courses().items())
        #If the user never looked the course forums up
        if not course_id in self.forums:
            forums = self.ws.get_course_forums(course_id)
            course_forums = []
            for forum in forums:
                forum_discussions = []
                discussions = self.ws.get_forum_discussions(str(forum['id']))
                for discussion in discussions['discussions']:
                    forum_discussions.append(Discussion(discussion))
                course_forums.append(Forum(forum,forum_discussions))
            self.forums[course_id] = course_forums
        #Read forums
        self.speak('Estos son los foros de ' + course, wait=True)
        for forum in self.forums[course_id]:
            self.speak(forum.get_name(), wait=True)
            resp = self.get_response('¿Quieres ver las discusiones de este foro?')
            if resp == 'si':
                chosen_forum = forum
                break
        #Read discussions
        self.speak('Estas son las discusiones de ' +  chosen_forum.get_name(), wait=True)
        for discussion in chosen_forum.get_discussions():
            self.speak(discussion.get_name(), wait=True)
            resp = self.get_response('¿Quieres ver los posts de esta discusión?')
            if resp == 'si':
                chosen_discussion = discussion
                break
        #Read posts
        posts = self.ws.get_forum_discussion_posts(str(chosen_discussion.get_id()))
        complete = self.get_response('¿Quieres que te lea la discusión completa?')
        if resp == 'si':
            discussion = []
            for post in reversed(posts['posts']):
                discussion.append(post['userfullname'] + ', dijo: ' + post['message'])
            self.speak(str(discussion).strip('[]'))
        else:
            for post in reversed(posts['posts']):
                self.speak(post['userfullname'] + ', dijo: ' + post['message'], wait=True)
                resp = self.get_response('¿Quieres que te lea el siguiente post?')
                if resp == 'no':
                    break

    def stop(self):
        pass

def create_skill():
    return UbuCourseSkill()
