class Forum():
    """ Represents a Moodle's forum.
    ---
    Contains the forum's id and name, along with its discussions.
    """
    def __init__(self, forum, discussions):
        """ Constructor.
        ---
            Parameters:
                - forum: JSONObject from Moodle webservice containing the course.
                - discussions: Discussion[] containing the forum's discussions.
        """
        self.__id = forum['id']
        self.__name = forum['name']
        self.__discussions = discussions

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_discussions(self):
        return self.__discussions
