"""Module of the Discussion class
"""

class Discussion():
    """ Represents a Moodle's discussion.
    ---
    Contains the discussion's id and name.
    """
    def __init__(self, discussion):
        """ Constructor.
        ---
            Parameters:
                - discussion: JSONObject from Moodle webservice containing the discussion.
        """
        self.__discussion_id = discussion['discussion']
        self.__name = discussion['name']

    def get_id(self) -> int:
        """Gets the id of the discussion

        Returns:
            int: id of the discussion
        """
        return self.__discussion_id

    def get_name(self) -> str:
        """Gets the name of the discussion

        Returns:
            str: name of the discussion
        """
        return self.__name
