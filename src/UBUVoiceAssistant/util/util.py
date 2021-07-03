"""Module for general utilities
"""
import pickle
import socket
import re
from typing import List, Optional
from ..model.course import Course
from .settings import Settings

SOCKET_HOST = 'localhost'
SOCKET_PORT = 5555
BUFF_SIZE = 4096
moodle_words = {'opens': 'se abre', 'closes': 'se cierra', '&aacute;': 'á',
                '&eacute;': 'é', '&iacute;': 'í', '&oacute;': 'ó',
                '&uacute;': 'ú', '\xa0': ' '}


def create_server_socket(unserialized_data, host=SOCKET_HOST, port=SOCKET_PORT):
    """Creates a server socket. This is used to send the webservice object from the frontend
        to the backend

    Args:
        unserialized_data ([type]): unserialized data to send
        host ([type], optional): ip to bind the socket to. Defaults to SOCKET_HOST.
        port ([type], optional): port to listen. Defaults to SOCKET_PORT.
    """
    server_socket = socket.socket()
    server_socket.bind((host, port))
    data = pickle.dumps(unserialized_data)
    while True:
        server_socket.listen()
        client_socket, _ = server_socket.accept()
        client_socket.send(data)


def get_data_from_server(host=SOCKET_HOST, port=SOCKET_PORT):
    """Gets data from the server. This is used to get the webservice object in the skills

    Args:
        host ([type], optional): host where it's the socket. Defaults to SOCKET_HOST.
        port ([type], optional): port where it's the socket. Defaults to SOCKET_PORT.

    Returns:
        Unserialized data. This will usually be a webservice
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
    cfg = Settings()
    if cfg['lang'] == 'es-es':
        for k, val in moodle_words.items():
            string = re.sub(k, val, string)
    return string


def get_course_id_by_name(course_to_find: str, user_courses: List[Course]) -> Optional[str]:
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


def reorder_name(fullname: str) -> str:
    """Reorders the name from "surname, name" to "name surname". Doesn't change anything if there
        is no comma in the text.

    Args:
        fullname (str): fullname to reorder

    Returns:
        str: ordered fullname
    """
    try:
        lastname, firstname = fullname.split(", ")
        return " ".join([firstname, lastname])
    except ValueError:
        return fullname
