import re


class Event():

    def __init__(self, event):
        self.__name = event['name']
        self.__date = re.sub('<.*?>', '', event['formattedtime'])

    def get_name(self):
        return self.__name

    def get_date(self):
        return self.__date

    def __str__(self):
        return self.get_date() + ' ' + self.get_name()
