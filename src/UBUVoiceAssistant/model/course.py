"""Module for the Course class
"""

from typing import Dict, List, Union

from .event import Event
from .forum import Forum
from .grade_item import GradeItem


class Course():
    """ Represents a Moodle's course.
    ---
    Contains the course's id and name, along with the forums, events and grades.
    """

    def __init__(self, course):
        """ Constructor.
        ---
            Parameters:
                - course: JSONObject from Moodle webservice containing the course.
        """
        self.__course_id = str(course['id'])
        self.__name = course['displayname']
        self.__grades = []
        self.__events = []
        self.__forums = []
        self.__participants: Dict[int, "User"] = {}

    def get_id(self) -> int: # TODO revisar
        """Gets the Course id

        Returns:
            int: Course id
        """
        return self.__course_id

    def get_name(self) -> str:
        """Gets the name of the Course

        Returns:
            str: name of the Course
        """
        return self.__name

    def get_grades(self) -> List[GradeItem]:
        """Gets the list of grades

        Returns:
            List[GradeItem]: List of grades
        """
        return self.__grades

    def set_grades(self, grades: List[GradeItem]):
        """Sets the list of grades

        Args:
            grades (List[GradeItem]): List of grades
        """
        self.__grades = grades

    def get_events(self) -> List[Event]:
        """Gets the list of events

        Returns:
            List[Event]: List of events
        """
        return self.__events

    def set_events(self, events: List[Event]):
        """Sets the list of events

        Args:
            events (List[Event]): List of events
        """
        self.__events = events

    def get_forums(self) -> List[Forum]:
        """Gets the list of forums

        Returns:
            List[Forum]: List of forums
        """
        return self.__forums

    def set_forums(self, forums: List[Forum]):
        """Gets the list of forums

        Args:
            forums (List[Forum]): List of forums
        """
        self.__forums = forums

    def set_participants(self, participants: Union[List["User"], Dict[int, "User"]]):
        if isinstance(participants, List):
            self.__participants = {}
            for p in participants:
                self.__participants[p.get_id()] = p
            return
        else:
            self.__participants = participants
    
    def get_participants(self) -> Dict[int, "User"]:
        return self.__participants
