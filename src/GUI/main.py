from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append('.')
from final import AppMainWindow
from os import path
from webservice.web_service import WebService


class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'UBUAssistant'
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 600
        self.lang = 'es-es'
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.checkBox_remember_user = QtWidgets.QCheckBox(self)
        self.checkBox_remember_user.setGeometry(QtCore.QRect(70, 420, 140, 25))

        self.checkBox_remember_host = QtWidgets.QCheckBox(self)
        self.checkBox_remember_host.setGeometry(QtCore.QRect(70, 450, 140, 25))

        self.pushButton_login = QtWidgets.QPushButton(self)
        self.pushButton_login.setGeometry(QtCore.QRect(220, 500, 100, 40))
        self.pushButton_login.clicked.connect(self.on_login_pressed)

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(115, 210, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        self.pushButton_login.setPalette(palette)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_login.setFont(font)

        self.comboBox_language = QtWidgets.QComboBox(self)
        self.comboBox_language.setGeometry(QtCore.QRect(350, 10, 140, 25))
        self.comboBox_language.addItem(QtGui.QIcon('spain_flag.png'), 'Español')
        self.comboBox_language.addItem(QtGui.QIcon('us_flag.png'), 'English')
        self.comboBox_language.currentTextChanged.connect(self.on_lang_selected)

        self.label_user = QtWidgets.QLabel(self)
        self.label_user.setGeometry(QtCore.QRect(140, 290, 51, 25))
        self.label_user.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.label_password = QtWidgets.QLabel(self)
        self.label_password.setGeometry(QtCore.QRect(113, 320, 81, 25))
        self.label_password.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.label_host = QtWidgets.QLabel(self)
        self.label_host.setGeometry(QtCore.QRect(160, 350, 31, 25))
        self.label_host.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.lineEdit_user = QtWidgets.QLineEdit(self)
        self.lineEdit_user.setGeometry(QtCore.QRect(210, 290, 231, 25))

        self.lineEdit_password = QtWidgets.QLineEdit(self)
        self.lineEdit_password.setGeometry(QtCore.QRect(210, 320, 231, 25))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.lineEdit_host = QtWidgets.QLineEdit(self)
        self.lineEdit_host.setGeometry(QtCore.QRect(210, 350, 231, 25))

        self.load_settings()
        self.retranslateUi()
        self.show()

    def retranslateUi(self):
        if self.user:
            self.lineEdit_user.setText(self.user)
        if self.host:
            self.lineEdit_host.setText(self.host)

        if self.lang == 'es-es':
            self.checkBox_remember_user.setText('Recordar usuario')
            self.checkBox_remember_host.setText('Recordar host')
            self.pushButton_login.setText('Acceder')
            self.label_user.setText('Usuario')
            self.label_password.setText('Contraseña')
            self.label_host.setText('Host')
            self.lineEdit_host.setPlaceholderText("https://www.ejemplo.com")
        elif self.lang == 'en-us':
            self.checkBox_remember_user.setText('Remember user')
            self.checkBox_remember_host.setText('Remember host')
            self.pushButton_login.setText('Login')
            self.label_user.setText('User')
            self.label_password.setText('Password')
            self.label_host.setText('Host')
            self.lineEdit_user.setText('adp1002@alu.ubu.es')
            self.lineEdit_host.setText('https://ubuvirtual.ubu.es')
            self.lineEdit_host.setPlaceholderText("https://www.example.com")

    def on_lang_selected(self, value):
        if value == 'Español':
            self.lang = 'es-es'
        elif value == 'English':
            self.lang = 'en-us'

        self.retranslateUi()

    def on_login_pressed(self):
        user = str(self.lineEdit_user.text())
        password = self.lineEdit_password.text()
        host = str(self.lineEdit_host.text())

        with open('user_data.txt', 'r') as data:
            data_lines = data.readlines()
            if self.checkBox_remember_user.isChecked():
                data_lines[0] = user+'\n'
            if self.checkBox_remember_host.isChecked():
                data_lines[1] = host+'\n'
            data_lines[2] = self.lang

        with open('user_data.txt', 'w') as data:
            data.writelines(data_lines)

        self.update_lang()

        ws = WebService()
        ws.set_host(host)
        # ws.set_session_cookies(user,password)
        ws.set_url_with_token(user, password)
        ws.set_userid()
        ws.set_user_courses()

        self.app_window = AppMainWindow(self.lang)
        self.app_window.show()
        self.close()

    def load_settings(self):
        with open('user_data.txt', 'r') as data:
            data_lines = data.readlines()
            self.user = data_lines[0].strip()
            self.host = data_lines[1].strip()
            self.lang = data_lines[2].strip()

    def update_lang(self):
        settings_path = path.expanduser('~') + '/mycroft-core/mycroft/configuration/mycroft.conf'

        with open(settings_path, 'r') as file:
            settings = file.readlines()
            settings[22] = '  "lang": "' + self.lang + '",\n'

        with open(settings_path, 'w') as file:
            file.writelines(settings)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = LoginWindow()
    sys.exit(app.exec_())
