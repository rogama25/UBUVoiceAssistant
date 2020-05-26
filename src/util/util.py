import pickle
import socket
import re

SOCKET_HOST = 'localhost'
SOCKET_PORT = 5555


def create_server_socket(unserialized_data, host=SOCKET_HOST, port=SOCKET_PORT):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    data = pickle.dumps(unserialized_data)
    while True:
        server_socket.listen()
        client_socket, address = server_socket.accept()
        client_socket.send(data)


def get_data_from_server(host=SOCKET_HOST, port=SOCKET_PORT):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    webservice_data = client_socket.recv(4096)
    client_socket.close()
    return pickle.loads(webservice_data)


def convert_events_to_readable_text(events):
    events_info = []
    for event in events:
        event_info = []
        date = re.sub('<.*?>', '', event['formattedtime'])
        event_info.append(date)
        event_info.append(event['name'])
        events_info.append(event_info)
    return events_info


def text_to_speech(string_array):
    text = ''
    for string in string_array:
        text = text + ' '.join(string)
        text = text + '.'
    return text


def get_course_id_by_name(course_to_find, user_courses):
    for id, name in user_courses:
        if course_to_find.upper() in name:
            return str(id)
    return None
