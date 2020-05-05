class Discussion():
    def __init__(self, discussion):
        self.__discussion_id = discussion['discussion']
        self.__name = discussion['name']

    def get_discussion_id(self):
        return self.__discussion_id

    def get_name(self):
        return self.__name
