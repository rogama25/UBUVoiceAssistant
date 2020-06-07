class Forum():

    def __init__(self, forum, discussions):
        self.__id = forum['id']
        self.__name = forum['name']
        self.__discussions = discussions

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_discussions(self):
        return self.__discussions
