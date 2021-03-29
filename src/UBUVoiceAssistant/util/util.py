"""Module for general utilities
"""
import pickle
import socket
import re
from os import environ
from typing import List, Optional
from ..model.course import Course

SOCKET_HOST = 'localhost'
SOCKET_PORT = 5555
BUFF_SIZE = 4096
moodle_words = {'opens': 'se abre', 'closes': 'se cierra', '&aacute;': 'á',
                '&eacute;': 'é', '&iacute;': 'í', '&oacute;': 'ó',
                '&uacute;': 'ú', '\xa0': ' '}


def create_server_socket(unserialized_data, host=SOCKET_HOST, port=SOCKET_PORT): # TODO Document
    """Creates a server socket

    Args:
        unserialized_data ([type]): [description]
        host ([type], optional): [description]. Defaults to SOCKET_HOST.
        port ([type], optional): [description]. Defaults to SOCKET_PORT.
    """
    server_socket = socket.socket()
    server_socket.bind((host, port))
    data = pickle.dumps(unserialized_data)
    while True:
        server_socket.listen()
        client_socket, _ = server_socket.accept()
        client_socket.send(data)


def get_data_from_server(host=SOCKET_HOST, port=SOCKET_PORT): # TODO Document
    """Gets data from the server.

    Args:
        host ([type], optional): [description]. Defaults to SOCKET_HOST.
        port ([type], optional): [description]. Defaults to SOCKET_PORT.

    Returns:
        [type]: [description]
    """
    client_socket = socket.socket()
    client_socket.connect((host, port))
    data = b''
    while True:
        part = client_socket.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    data_arr = pickle.loads(data)
    client_socket.close()
    return data_arr


def text_to_speech(string_array: List[str]) -> str:
    """Gets better text-to-speech strings

    Args:
        string_array (List[str]): List of original strings

    Returns:
        str: Better string
    """
    text = ''
    for string in string_array:
        text = text + string + '.\n'
    return translate_moodle_words(text)


def translate_moodle_words(string: str) -> str:
    """Gets better strings for Moodle texts

    Args:
        string (str): Original strings

    Returns:
        str: Better strings
    """
    if environ['lang'] == 'es-es':
        for k, val in moodle_words.items():
            string = re.sub(k, val, string)
    return string


def get_course_id_by_name(course_to_find: str, user_courses: List[Course]) -> Optional[Course]:
    """Finds a course by its name

    Args:
        course_to_find (str): Name of the course
        user_courses (List[Course]): List of user's courses

    Returns:
        Optional[Course]: Returns the Couse object, or None if it couldn't be found.
    """
    for course in user_courses:
        if course_to_find.upper() in course.get_name().upper():
            return str(course.get_id())
    return None

class Singleton(type): # https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """Singleton class
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
