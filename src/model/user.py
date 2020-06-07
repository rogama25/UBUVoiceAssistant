class User():

    def __init__(self, id):
        self.__id = id
        self.__courses = {}
        self.__final_grades = []

    def get_id(self):
        return self.__id

    def get_courses(self):
        return self.__courses

    def set_courses(self, courses):
        for course in courses:
            self.__courses[course.get_id()] = course

    def get_final_grades(self):
        return self.__final_grades

    def set_final_grades(self, grades):
        self.__final_grades = grades
