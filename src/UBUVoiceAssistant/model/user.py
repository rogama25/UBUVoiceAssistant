"""Module fo the User class
"""

from typing import Dict, List, Optional, Union

from .course import Course
from .grade_item import GradeItem


class User():
    """ Represents a Moodle's user.
    ---
    Contains the user's id and courses.
    """

    def __init__(self, user: Union[int, dict]):
        """ Constructor.
        ---
            Parameters:
                - user_id: int with the user's id.
        """
        self.__courses: Dict[int, Course] = {}
        self.__final_grades: List[GradeItem] = []
        if isinstance(user, int):
            self.__user_id = user
            self.__fullname = ""
        else:
            self.__user_id = user["id"]
            self.__fullname = user["fullname"]

    def get_id(self) -> int:
        """Gets the id of the user

        Returns:
            int: user id
        """
        return self.__user_id

    def get_courses(self) -> Dict[int, Course]:
        """Gets the list of courses

        Returns:
            Dict[Course]: Dictionary of courses
        """
        return self.__courses

    def set_courses(self, courses: List[Course]):
        """Sets the list of courses

        Args:
            courses (List[Course]): List of courses
        """
        for course in courses:
            self.set_course(course)

    def get_course(self, course_id: int) -> Optional[Course]:
        """Gets a course from id

        Args:
            course_id (int): course id

        Returns:
            Course: Course
        """
        return self.__courses.get(course_id)

    def set_course(self, course: Course):
        """Sets a course to the user

        Args:
            course (Course): Course
        """
        self.__courses[course.get_id()] = course

    def get_final_grades(self) -> List[GradeItem]:
        """Gets a list of the final grades

        Returns:
            List: List of grades
        """
        return self.__final_grades

    def set_final_grades(self, grades: List[GradeItem]):
        """Sets the list of final grades

        Args:
            grades (List[GradeItem]): list of grades
        """
        self.__final_grades = grades

    def set_fullname(self, name: str):
        self.__fullname = name

    def get_fullname(self) -> str:
        return self.__fullname
