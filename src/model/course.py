class Course():

    def __init__(self, course):
        self.__id = course['id']
        self.__name = course['displayname']
        # self.__grades = []
        self.__events = []
        self.__forums = []

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    '''def get_grades(self):
        return self.__grades

    def set_grades(self, grades):
        self.__grades = grades'''

    def get_events(self):
        return self.__events

    def set_events(self, events):
        self.__events = events
