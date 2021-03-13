"""Module for the main UI
"""
import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ..webservice.web_service import WebService
from ..util.lang import Translator

translator = Translator("en_US")
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
        self.update_texts()
        self.show()

    # pylint: disable=R0201
    def on_lang_changed(self, value: int) -> None:
        """Function that gets called when the selected language changes

        Args:
            value (int): new position of the dropdown menu
        """
        translator.change_language(value)

    def update_texts(self) -> None:
        """Retranslates the UI texts
        """
        self.btnLogin.setText(_("login"))
        self.chkHost.setText(_("remember host"))
        self.chkUser.setText(_("remember username"))
        self.lblHost.setText(_("moodle url"))
        self.lblPassword.setText(_("password"))
        self.lblUser.setText(_("username"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    app.exec_()
