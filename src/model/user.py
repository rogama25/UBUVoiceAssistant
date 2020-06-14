class User():
    """ Represents a Moodle's user.
    ---
    Contains the user's id and courses.
    """

    def __init__(self, user_id):
        """ Constructor.
        ---
            Parameters:
                - user_id: int with the user's id.
        """
        self.__user_id = user_id
        # dict with the key being the course's id and the value the Course object
        self.__courses = {}
        self.__final_grades = []

    def get_id(self):
        return self.__user_id

    def get_courses(self):
        return self.__courses

    def set_courses(self, courses):
        for course in courses:
            self.set_course(course)

    def get_course(self, course_id):
        return self.__courses.get(course_id)

    def set_course(self, course):
        self.__courses[course.get_id()] = course

    def get_final_grades(self):
        return self.__final_grades

    def set_final_grades(self, grades):
        self.__final_grades = grades
