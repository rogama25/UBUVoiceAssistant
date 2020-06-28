import pickle
import socket
import re
from os import environ

SOCKET_HOST = 'localhost'
SOCKET_PORT = 5555
BUFF_SIZE = 4096
moodle_words = {'opens': 'se abre', 'closes': 'se cierra', '&aacute;': 'á',
                '&eacute;': 'é', '&iacute;': 'í', '&oacute;': 'ó',
                '&uacute;': 'ú', '\xa0': ' '}


def create_server_socket(unserialized_data, host=SOCKET_HOST, port=SOCKET_PORT):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    data = pickle.dumps(unserialized_data)
    while True:
        server_socket.listen()
        client_socket, _ = server_socket.accept()
        client_socket.send(data)


def get_data_from_server(host=SOCKET_HOST, port=SOCKET_PORT):
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


def text_to_speech(string_array):
    text = ''
    for string in string_array:
        text = text + string + '.\n'
    return translate_moodle_words(text)


def translate_moodle_words(string):
    if environ['lang'] == 'es-es':
        for k, v in moodle_words.items():
            string = re.sub(k, v, string)
    return string


def get_course_id_by_name(course_to_find, user_courses):
    for course in user_courses:
        if course_to_find.upper() in course.get_name().upper():
            return str(course.get_id())
    return None
