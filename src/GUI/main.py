import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ..webservice.web_service import WebService
from ..util.lang import Translator

translator = Translator("en_US")
_ = translator.translate

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./GUI/forms/login.ui", self)
        self.dropLang: QtWidgets.QComboBox
        self.dropLang.addItems(translator.find_available_languages())
        self.dropLang.currentIndexChanged.connect(self.on_lang_changed)
        self.update_texts()
        self.show()

    def on_lang_changed(self, value: int) -> None:
        translator.change_language(value)

    def update_texts(self) -> None:
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
