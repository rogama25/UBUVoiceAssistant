import re


class Event():
    """ Represents a Moodle's event.
    ---
    Contains the event's name and date.
    """

    def __init__(self, event):
        """ Constructor.
        ---
            Parameters:
                - event: JSONObject from Moodle webservice containing the event.
        """
        self.__name = event['name']
        self.__date = re.sub('<.*?>', '', event['formattedtime'])

    def get_name(self):
        return self.__name

    def get_date(self):
        return self.__date

    def __str__(self):
        """ Redefine the str method.
        ---
            Returns:
                String with the event's date and name
        """
        return self.get_date() + ' ' + self.get_name()
