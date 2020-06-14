class GradeItem():
    """ Represents a Moodle's grade item.
    ---
    Contains the grade item's value, name and type.
    """
    def __init__(self, grade):
        """ Constructor.
        ---
            Parameters:
                - forum: JSONObject from Moodle webservice containing the grade item.
        """
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
        """ Redefine the str method.
        ---
            Returns:
                String with the grade item's name and value
        """
        return self.get_name() + ' ' + str(self.get_value())
