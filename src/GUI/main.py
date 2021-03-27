"""Module for the main UI
"""
from PyQt5.QtCore import QTimer
from src.GUI.link_mycroft import LinkMycroft
import sys
import requests
import time
import subprocess
from threading import Thread
from os import path
from PyQt5 import QtWidgets, uic
from mycroft_bus_client import MessageBusClient
from ..webservice.web_service import WebService
from .message_box import MessageBox
from .progress_box import ProgressBox
from ..util.lang import Translator
from ..util.util import create_server_socket

translator = Translator()
_ = translator.translate


class LoginWindow(QtWidgets.QMainWindow):
    """Class for the login window
    """

    def __init__(self):
        super().__init__()
        uic.loadUi("./GUI/forms/login.ui", self)
        self.dropLang: QtWidgets.QComboBox
        self.dropLang.addItems(translator.find_available_languages())
        self.dropLang.currentIndexChanged.connect(self.on_lang_changed)
        self.btnLogin: QtWidgets.QPushButton
        self.btnLogin.clicked.connect(self.on_login)
        self.update_texts()
        self.mycroft_started = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_mycroft_started)
        self.show()

    # pylint: disable=R0201
    def on_lang_changed(self, value: int) -> None:
        """Function that gets called when the selected language changes

        Args:
            value (int): new position of the dropdown menu
        """
        translator.change_language(value)

    def on_login(self):
        user = str(self.tbxUser.text())
        password = self.tbxPassword.text()
        host = str(self.tbxHost.text())

        if not host:
            host = "https://ubuvirtual.ubu.es"

        ws = WebService()
        ws.set_host(host)

        try:
            ws.set_url_with_token(user, password)
        # If the credentials are incorrect
        except KeyError:
            MessageBox(_("invalid credentials")).exec_()
            return
        except requests.exceptions.MissingSchema:
            MessageBox(_("missing url schema")).exec_()
            return
        ws.initialize_useful_data()

        # If Moodle lang is different from the selected
        if ws.get_lang() not in translator.get_current_language():
            MessageBox(_("language not supported by moodle")).exec_()
        ws.set_user_courses()

        self.starting_window = ProgressBox(_("starting mycroft"))
        self.starting_window.show()

        server_socket = Thread(target=create_server_socket, args=[self.ws])
        server_socket.setDaemon(True)
        server_socket.start()

        mycroft_starter = Thread(self.start_mycroft)
        mycroft_starter.start()

        self.timer.start(1000)

    def update_texts(self) -> None:
        """Retranslates the UI texts
        """
        self.btnLogin.setText(_("login"))
        self.chkHost.setText(_("remember host"))
        self.chkUser.setText(_("remember username"))
        self.lblHost.setText(_("moodle url"))
        self.lblPassword.setText(_("password"))
        self.lblUser.setText(_("username"))

    def start_mycroft(self):
        def f_mycroft_started():
            self.mycroft_started = True

        self.bus = MessageBusClient()
        self.bus.on("mycroft.ready", f_mycroft_started)
        subprocess.run("docker start mycroft", shell=True)
        time.sleep(2)
        try:
            result = subprocess.run("docker exec mycroft ./startup.sh",
                                    text=True, shell=True, capture_output=True, timeout=5)
        except subprocess.TimeoutExpired:
            pass

    def check_mycroft_started(self):
        """Checks if Mycroft was started and launches next window
        """
        if not self.mycroft_started:
            return
        self.timer.stop()
        self.starting_window.close()
        if not path.isfile("~/.config/mycroft-docker/identity/identity2.json"):
            self.new_window = LinkMycroft(self.bus)
            self.hide()
            self.new_window.show()
            self.new_window.closed_signal.connect(self.check_mycroft_started)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    app.exec_()
