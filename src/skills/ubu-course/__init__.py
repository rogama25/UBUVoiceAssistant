import sys
from os.path import expanduser
from mycroft import MycroftSkill, intent_handler
from util import util
sys.path.append(expanduser('~') + '/UBUAssistant/src')
from model.discussion import Discussion
from model.forum import Forum


class UbuCourseSkill(MycroftSkill):

    def __init__(self):
        super().__init__()
        self.forums = {}
        self.learning = True

    def initialize(self):
        self.ws = util.get_data_from_server()

    @intent_handler('CourseForums.intent')
    def handle_course_forums(self, message):
        course = message.data['course']
        course_id = util.get_course_id_by_name(course, self.ws.get_user_courses().items())
        if course_id:
            # If the user never looked the course forums up
            if course_id not in self.forums:
                forums = self.ws.get_course_forums(course_id)
                course_forums = []
                for forum in forums:
                    forum_discussions = []
                    discussions = self.ws.get_forum_discussions(str(forum['id']))
                    for discussion in discussions['discussions']:
                        forum_discussions.append(Discussion(discussion))
                    course_forums.append(Forum(forum, forum_discussions))
                self.forums[course_id] = course_forums
            # Read forums
            self.speak_dialog('forums', data={'course': course}, wait=True)
            for forum in self.forums[course_id]:
                self.speak(forum.get_name(), wait=True)
                resp = self.get_response(dialog='forum.discussions')
                if resp.lower() in ('si', 'sí', 'yes'):
                    chosen_forum = forum
                    break
            # Read discussions
            self.speak_dialog('discussion', data={'forum': chosen_forum.get_name()}, wait=True)
            for discussion in chosen_forum.get_discussions():
                self.speak(discussion.get_name(), wait=True)
                resp = self.get_response(dialog='discussion.posts')
                if resp in ('si', 'sí', 'yes'):
                    chosen_discussion = discussion
                    break
            # Read posts
            posts = self.ws.get_forum_discussion_posts(str(chosen_discussion.get_id()))
            complete = self.get_response(dialog='whole.discussion')
            if complete.lower() in ('si', 'sí', 'yes'):
                discussion = []
                for post in reversed(posts['posts']):
                    discussion.append(post['userfullname'] + ': ' + post['message'])
                self.speak(str(discussion).strip('[]'))
            else:
                for post in reversed(posts['posts']):
                    resp = self.get_response(dialog='next.post')
                    if resp.lower() == 'no':
                        break
                    self.speak(post['userfullname'] + ': ' + post['message'])

        else:
            self.speak_dialog('no.course')

    def stop(self):
        pass


def create_skill():
    return UbuCourseSkill()
