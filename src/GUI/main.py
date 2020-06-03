from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append('.')
from app import AppMainWindow
from os import path, environ
from webservice.web_service import WebService


class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'UBUAssistant'
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 600
        environ['lang'] = 'es-es'
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.invalid_credentials = QtWidgets.QMessageBox()

        self.center_on_screen()

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

        self.retranslateUi()

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

        with open('user_data.txt', 'r') as data:
            data_lines = data.readlines()
            if self.checkBox_remember_user.isChecked():
                data_lines[0] = user+'\n'
            if self.checkBox_remember_host.isChecked():
                data_lines[1] = host+'\n'
            data_lines[2] = environ['lang']

        with open('user_data.txt', 'w') as data:
            data.writelines(data_lines)

        settings_path = path.expanduser('~') + '/mycroft-core/mycroft/configuration/mycroft.conf'

        with open(settings_path, 'r') as file:
            settings = file.readlines()
            settings[22] = '  "lang": "' + environ['lang'] + '",\n'

        with open(settings_path, 'w') as file:
            file.writelines(settings)

        self.app_window = AppMainWindow()
        self.app_window.show()
        self.close()

    def load_settings(self):
        with open('user_data.txt', 'r') as data:
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
