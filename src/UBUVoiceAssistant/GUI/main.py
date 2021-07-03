"""Module for the main UI
"""
import subprocess
import sys
from os import path
from threading import Thread

import requests
import simplejson
from mycroft_bus_client import MessageBusClient
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QIcon

from ..GUI.link_mycroft import LinkMycroft
from ..util.lang import Translator
from ..util.settings import Settings
from ..util.util import create_server_socket
from ..webservice.web_service import WebService
from .chat_window import ChatWindow
from .message_box import MessageBox
from .progress_box import ProgressBox

translator = Translator()
_ = translator.translate


class LoginWindow(QtWidgets.QMainWindow):
    """Class for the login window
    """

    def __init__(self):
        super().__init__()
        uic.loadUi("./UBUVoiceAssistant/GUI/forms/login.ui", self)
        self.cfg = Settings()
        self.dropLang: QtWidgets.QComboBox
        self.dropLang.addItems(translator.find_available_languages())
        if self.cfg["user"]:
            self.tbxUser.setText(self.cfg["user"])
            self.chkUser.setChecked(True)
        if self.cfg["host"]:
            self.tbxHost.setText(self.cfg["host"])
            self.chkHost.setChecked(True)
        self.dropLang.setCurrentIndex(translator.get_language_index(self.cfg["lang"]))
        self.on_lang_changed(translator.get_language_index(self.cfg["lang"]))
        self.dropLang.currentIndexChanged.connect(self.on_lang_changed)
        self.btnLogin: QtWidgets.QPushButton
        self.btnLogin.clicked.connect(self.on_login)
        self.update_texts()
        self.mycroft_started = False
        self.finished = False
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_mycroft_started)
        self.setFixedSize(self.size())
        self.show()
        if self.tbxUser.text():
            self.tbxPassword.setFocus()
        else:
            self.tbxUser.setFocus()

    # pylint: disable=R0201
    def on_lang_changed(self, value: int) -> None:
        """Function that gets called when the selected language changes

        Args:
            value (int): new position of the dropdown menu
        """
        print("Lang changed", value)
        translator.change_language(value)
        self.update_texts()

    def on_login(self):
        """This runs when the user clicks the login button or press enter
        """
        user = str(self.tbxUser.text())
        password = self.tbxPassword.text()
        host = str(self.tbxHost.text())

        if not host:
            host = "https://ubuvirtual.ubu.es"

        self.webservice = WebService()
        self.webservice.set_host(host)

        try:
            self.webservice.set_url_with_token(user, password)
        # If the credentials are incorrect
        except KeyError:
            MessageBox(_("Invalid Moodle username or password.")).exec_()
            return
        except requests.exceptions.MissingSchema:
            MessageBox(_("Missing http:// or https:// at the beginning")).exec_()
            return
        except (requests.exceptions.ConnectionError, simplejson.errors.JSONDecodeError):
            MessageBox(_("Connection error. Please check that the URL is correct, your Internet connection is working and the server is up.")).exec_()
            return

        if self.chkUser.isChecked():
            self.cfg["user"] = user
        if self.chkHost.isChecked():
            self.cfg["host"] = host
        self.cfg["lang"] = translator.get_current_language()[0]
        self.cfg.save_settings()
        self.webservice.initialize_useful_data()

        # If Moodle lang is different from the selected
        if not translator.check_language_supported(self.webservice.get_lang()):
            MessageBox(_("This language is not supported by your Moodle server")).exec_()
        self.webservice.set_user_courses()

        self.starting_window = ProgressBox(_("Starting Mycroft, please wait..."))
        self.starting_window.show()

        server_socket = Thread(target=create_server_socket, args=[self.webservice])
        server_socket.setDaemon(True)
        server_socket.start()

        mycroft_starter = Thread(target=self.start_mycroft)
        mycroft_starter.start()

        self.timer.start(1000)

    def update_texts(self) -> None:
        """Retranslates the UI texts
        """
        print("Updating texts...", _("Login"))
        self.btnLogin.setText(_("Login"))
        self.chkHost.setText(_("Remember host"))
        self.chkUser.setText(_("Remember username"))
        self.lblHost.setText(_("Moodle url"))
        self.lblPassword.setText(_("Password"))
        self.lblUser.setText(_("Username"))

    def start_mycroft(self):
        """Starts Mycroft and checks for when it's ready
        """
        def f_mycroft_started(event):
            self.mycroft_started = True

        self.bus = MessageBusClient()
        self.set_reconnect_1s()
        self.bus.on("mycroft.ready", f_mycroft_started)
        self.bus.on("error", self.set_reconnect_1s)
        self.bus.on("open", self.set_reconnect_1s)
        subprocess.run(
            "/usr/lib/mycroft-core/start-mycroft.sh all", shell=True)
        self.bus.run_in_thread()
        print("Launched Mycroft")

    def check_mycroft_started(self):
        """Checks if Mycroft was started and launches next window
        """
        if not self.mycroft_started:
            return
        self.timer.stop()
        self.starting_window.done = True
        self.starting_window.close()
        print("Pairing file:", path.isfile(path.expanduser("~/.mycroft/identity/identity2.json")))
        if not path.isfile(path.expanduser("~/.mycroft/identity/identity2.json")):
            self.new_window = LinkMycroft(self.bus)
            self.new_window.show()
            self.hide()
            self.new_window.closed_signal.connect(self.check_mycroft_started)
        else:
            if not self.finished:
                self.new_window = ChatWindow(self.bus, self.webservice)
                self.new_window.show()
                self.new_window.tbxInput.setFocus()
                self.hide()
                self.finished = True

    def set_reconnect_1s(self, event = None):
        """Set the bus reconnect time to 1 second
        """
        print("Set reconnect time")
        self.bus.retry = 0.5

    def keyPressEvent(self, event):
        """This happens when the user press a key

        Args:
            event: Qt Keypress event
        """
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.on_login()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("UBUVoiceAssistant")
    app.setWindowIcon(QIcon("UBUVoiceAssistant/imgs/appicon.png"))
    window = LoginWindow()
    app.exec_()
