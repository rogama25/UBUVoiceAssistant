"""Module for the linking Mycroft to web UI
"""
import re
import time
from PyQt5 import QtWidgets
from mycroft_bus_client import MessageBusClient, Message # type: ignore
from ..util.lang import Translator

_ = Translator().translate

class LinkMycroft(QtWidgets.QMainWindow):
    """Class for the linking Mycroft to web UI
    """
    def __init__(self, bus: MessageBusClient) -> None:
        super().__init__()
        self.page = 0
        self.done = False
        self.code = _("wait a second")
        self.file = open("/var/log/mycroft-docker/skills.log", "rb")
        self.file.seek(0, 2) # Goes to the end of the file
        msg = Message("recognizer_loop:utterance", utterance=[_("pair device")])
        # On other languages different than English, we must send again the phrase for it to start pairing
        bus.emit(msg)
        bus.on("configuration.updated", self.pairing_done)

    def pairing_done(self):
        self.done = True
        self.file.close()
        self.close()

    def add_pairing_code(self):
        self.tbxCode.setText(self.code)

    def read_pairing_code(self):
        while not self.done:
            line = self.file.readline()
            if line:
                matches = re.findall("(?<=" + re.escape("PairingSkill | Pairing code: ") + ").+(?=\n)", line)
                self.code = matches[0]
            else:
                time.sleep(0.5)

