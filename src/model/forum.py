"""Module for the Forum class
"""

from typing import List
from ..model.discussion import Discussion

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

    def get_id(self) -> int: # TODO Revisar si es correcto
        """Gets the id of the Forum

        Returns:
            int: Forum id
        """
        return self.__id

    def get_name(self) -> str:
        """Gets the forum name

        Returns:
            str: Forum name
        """
        return self.__name

    def get_discussions(self) -> List[Discussion]:
        """Gets the Discussions of the Forum

        Returns:
            List[Discussion]: List of Discussions
        """
        return self.__discussions
