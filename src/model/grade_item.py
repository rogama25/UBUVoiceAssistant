class GradeItem():
    def __init__(self, grade):
        self.__value = grade['graderaw']
        self.__name = grade['itemname']
        self.__type = grade['itemtype']

    def get_value(self):
        return self.__value

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def __str__(self):
        return self.get_name() + ' ' + str(self.get_value())
