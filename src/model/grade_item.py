class GradeItem():

    def __init__(self, grade_item):
        self.__grade = grade_item['graderaw']

    def get_grade(self):
        return self.__grade

    def get_course(self):
        return self.get_course()

    def set_course(self, course):
        self.__course = course
