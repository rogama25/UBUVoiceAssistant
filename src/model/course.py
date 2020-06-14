class Course():
    """ Represents a Moodle's course.
    ---
    Contains the course's id and name, along with the forums, events and grades.
    """

    def __init__(self, course):
        """ Constructor.
        ---
            Parameters:
                - course: JSONObject from Moodle webservice containing the course.
        """
        self.__course_id = str(course['id'])
        self.__name = course['displayname']
        self.__grades = []
        self.__events = []
        self.__forums = []

    def get_id(self):
        return self.__course_id

    def get_name(self):
        return self.__name

    def get_grades(self):
        return self.__grades

    def set_grades(self, grades):
        self.__grades = grades

    def get_events(self):
        return self.__events

    def set_events(self, events):
        self.__events = events

    def get_forums(self):
        return self.__forums

    def set_forums(self, forums):
        self.__forums = forums
