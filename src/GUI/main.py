# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/adp/Desktop/main1.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append('.')
from app import AppMainWindow
from os import path, environ
from webservice.web_service import WebService


class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.user_data_file = 'user_data.txt'
        self.title = 'UBUAssistant'
        self.top = 100
        self.left = 100
        self.width = 750
        self.height = 600
        environ['lang'] = 'es-es'
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.invalid_credentials = QtWidgets.QMessageBox()

        self.center_on_screen()

        self.centralwidget = QtWidgets.QWidget(self)

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setPixmap(QtGui.QPixmap('imgs/UBUAssistant_logo.png').scaled(443,300))
        self.label_logo.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_logo, 1, 1, 1, 6)

        self.checkBox_remember_user = QtWidgets.QCheckBox(self.centralwidget)
        self.gridLayout.addWidget(self.checkBox_remember_user, 6, 4, 1, 1)

        self.checkBox_remember_host = QtWidgets.QCheckBox(self.centralwidget)
        self.gridLayout.addWidget(self.checkBox_remember_host, 6, 5, 1, 1)

        self.pushButton_login = QtWidgets.QPushButton(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(115, 210, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        self.pushButton_login.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_login.setFont(font)
        self.pushButton_login.clicked.connect(self.on_login_pressed)
        self.gridLayout.addWidget(self.pushButton_login, 7, 4, 2, 2)

        self.label_user = QtWidgets.QLabel(self.centralwidget)
        self.label_user.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_user, 2, 4, 1, 1)

        self.label_password = QtWidgets.QLabel(self.centralwidget)
        self.label_password.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_password, 3, 4, 1, 1)

        self.label_host = QtWidgets.QLabel(self.centralwidget)
        self.label_host.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label_host, 4, 4, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem1, 6, 1, 1, 1)

        self.lineEdit_host = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit_host, 4, 5, 1, 1)

        self.lineEdit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.lineEdit_password, 3, 5, 1, 1)

        self.comboBox_language = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_language.setGeometry(QtCore.QRect(350, 10, 140, 25))
        self.comboBox_language.addItem(QtGui.QIcon('imgs/spain_flag.png'), 'Español')
        self.comboBox_language.addItem(QtGui.QIcon('imgs/us_flag.png'), 'English')
        self.comboBox_language.currentTextChanged.connect(self.on_lang_selected)
        self.gridLayout.addWidget(self.comboBox_language, 0, 6, 1, 1)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 6, 1, 1)

        self.lineEdit_user = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit_user, 2, 5, 1, 1)

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem3, 9, 1, 1, 1)

        # spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.gridLayout.addItem(spacerItem4, 1, 1, 1, 1)

        self.setCentralWidget(self.centralwidget)

        self.load_settings()
        self.retranslate_ui()
        self.show()

    def retranslate_ui(self):
        if self.user:
            self.lineEdit_user.setText(self.user)
        if self.host:
            self.lineEdit_host.setText(self.host)

        if environ['lang'] == 'es-es':
            self.checkBox_remember_user.setText('Recordar usuario')
            self.checkBox_remember_host.setText('Recordar host')
            self.pushButton_login.setText('Acceder')
            self.label_user.setText('Usuario')
            self.label_password.setText('Contraseña')
            self.label_host.setText('Host')
            self.lineEdit_host.setPlaceholderText("https://www.ejemplo.com")
            self.invalid_credentials.setText('Los credenciales introducidos no son válidos')
        elif environ['lang'] == 'en-us':
            self.checkBox_remember_user.setText('Remember user')
            self.checkBox_remember_host.setText('Remember host')
            self.pushButton_login.setText('Login')
            self.label_user.setText('User')
            self.label_password.setText('Password')
            self.label_host.setText('Host')
            self.lineEdit_user.setText('adp1002@alu.ubu.es')
            self.lineEdit_host.setText('https://ubuvirtual.ubu.es')
            self.lineEdit_host.setPlaceholderText("https://www.example.com")
            self.invalid_credentials.setText('The given credentials are invalid')

    def on_lang_selected(self, value):
        if value == 'Español':
            environ['lang'] = 'es-es'
        elif value == 'English':
            environ['lang'] = 'en-us'

        self.retranslate_ui()

    def on_login_pressed(self):
        user = str(self.lineEdit_user.text())
        password = self.lineEdit_password.text()
        host = str(self.lineEdit_host.text())

        ws = WebService()
        ws.set_host(host)
        # ws.set_session_cookies(user,password)
        try:
            ws.set_url_with_token(user, password)
        except KeyError:
            self.invalid_credentials.exec()
            return
        ws.set_userid()
        ws.set_user_courses()

        with open(self.user_data_file, 'r') as data:
            data_lines = data.readlines()
            if self.checkBox_remember_user.isChecked():
                data_lines[0] = user+'\n'
            if self.checkBox_remember_host.isChecked():
                data_lines[1] = host+'\n'
            data_lines[2] = environ['lang']

        with open(self.user_data_file, 'w') as data:
            data.writelines(data_lines)

        settings_path = path.expanduser('~') + '/mycroft-core/mycroft/configuration/mycroft.conf'

        with open(settings_path, 'r') as file:
            settings = file.readlines()
            settings[22] = '  "lang": "' + environ['lang'] + '",\n'

        with open(settings_path, 'w') as file:
            file.writelines(settings)

        self.app_window = AppMainWindow()
        self.app_window.show()
        self.hide()

    def load_settings(self):
        with open(self.user_data_file, 'r') as data:
            data_lines = data.readlines()
            self.user = data_lines[0].strip()
            self.host = data_lines[1].strip()
            environ['lang'] = data_lines[2].strip()

    def center_on_screen(self):
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                    (resolution.height() / 2) - (self.frameSize().height() / 2))

    def closeEvent(self, event):
        self.close = QtWidgets.QMessageBox()
        if environ['lang'] == 'es-es':
            self.close.setText("¿Estas seguro?")
        elif environ['lang'] == 'en-us':
            self.close.setText("Are you sure?")
        self.close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.close = self.close.exec()

        if self.close == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = LoginWindow()
    sys.exit(app.exec_())
