from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append('.')
from webservice.web_service import WebService
from GUI.app import AppMainWindow

class LoginWindow(QtWidgets.QMainWindow):


    def __init__(self):
        super().__init__()
        self.title = 'UBUAssistant'
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 600
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.checkBox_remember_user = QtWidgets.QCheckBox(self)
        self.checkBox_remember_user.setGeometry(QtCore.QRect(70, 420, 140, 25))
        #self.checkBox_remember_user.setObjectName('checkBox_remember_user')

        self.checkBox_remember_host = QtWidgets.QCheckBox(self)
        self.checkBox_remember_host.setGeometry(QtCore.QRect(70, 450, 140, 25))
        #self.checkBox_remember_host.setObjectName('checkBox_remember_host')

        self.pushButton_login = QtWidgets.QPushButton(self)
        self.pushButton_login.setGeometry(QtCore.QRect(220, 500, 100, 40))
        #self.pushButton_login.setObjectName('pushButton_login')
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
        #self.comboBox_language.setObjectName('comboBox_language')

        self.label_user = QtWidgets.QLabel(self)
        self.label_user.setGeometry(QtCore.QRect(140, 290, 51, 25))
        #self.label_user.setObjectName('label_user')

        self.label_password = QtWidgets.QLabel(self)
        self.label_password.setGeometry(QtCore.QRect(113, 320, 81, 25))
        #self.label_password.setObjectName('label_password')

        self.label_host = QtWidgets.QLabel(self)
        self.label_host.setGeometry(QtCore.QRect(160, 350, 31, 25))
        #self.label_host.setObjectName('label_host')

        self.lineEdit_user = QtWidgets.QLineEdit(self)
        self.lineEdit_user.setGeometry(QtCore.QRect(210, 290, 231, 25))
        self.lineEdit_user.setObjectName('lineEdit_user')

        self.lineEdit_password = QtWidgets.QLineEdit(self)
        self.lineEdit_password.setGeometry(QtCore.QRect(210, 320, 231, 25))
        #self.lineEdit_password.setObjectName('lineEdit_password')
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.lineEdit_host = QtWidgets.QLineEdit(self)
        self.lineEdit_host.setGeometry(QtCore.QRect(210, 350, 231, 25))
        self.lineEdit_host.setPlaceholderText("https://www.example.com")
        #self.lineEdit_host.setObjectName('lineEdit_host')

        self.retranslateUi(self)
        self.show()
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.checkBox_remember_user.setText(_translate('MainWindow', 'Recordar usuario'))
        self.checkBox_remember_host.setText(_translate('MainWindow', 'Recordar host'))
        self.pushButton_login.setText(_translate('MainWindow', 'Acceder'))
        self.label_user.setText(_translate('MainWindow', 'Usuario'))
        self.label_password.setText(_translate('MainWindow', 'Contraseña'))
        self.label_host.setText(_translate('MainWindow', 'Host'))
        self.lineEdit_user.setText(_translate('MainWindow', 'adp1002@alu.ubu.es'))
        self.lineEdit_host.setText(_translate('MainWindow', 'https://ubuvirtual.ubu.es'))

    def on_login_pressed(self):

        user = str(self.lineEdit_user.text())
        password = self.lineEdit_password.text()
        host = str(self.lineEdit_host.text())

        ws = WebService()
        ws.set_host(host)
        ws.set_url_with_token(user,password)


        self.app_window = AppMainWindow()
        self.app_window.show()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = LoginWindow()
    sys.exit(app.exec_())
