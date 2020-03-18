# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Desktop/2nd.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class AppMainWindow(QtWidgets.QMainWindow):
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

        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(100, 250, 300, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        #self.line.setObjectName("line")

        self.label_chat_title = QtWidgets.QLabel(self)
        self.label_chat_title.setGeometry(QtCore.QRect(200, 260, 120, 14))
        font_chat_title = QtGui.QFont()
        font_chat_title.setPointSize(14)
        self.label_chat_title.setFont(font_chat_title)
        #self.label_chat_title.setObjectName("label_chat_title")

        self.lineEdit_chat_message = self.lineEdit_user = QtWidgets.QLineEdit(self)
        self.lineEdit_chat_message.setGeometry(QtCore.QRect(50, 550, 350, 30))

        self.pushButton_send = QtWidgets.QPushButton(self)
        self.pushButton_send.setGeometry(QtCore.QRect(399, 550, 50, 30))
        self.pushButton_send.clicked.connect(self.on_send_pressed)

        self.label_questions_title = QtWidgets.QLabel(self)
        self.label_questions_title.setGeometry(QtCore.QRect(20, 10, 315, 40))
        font_questions_title = QtGui.QFont()
        font_questions_title.setPointSize(16)
        self.label_questions_title.setFont(font_questions_title)
        #self.label_questions_title.setObjectName("label_questions_title")

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 50, 360, 190))
        #self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vertical_layout_questions = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_questions.setContentsMargins(0, 0, 0, 0)
        #self.vertical_layout_questions.setObjectName("vertical_layout_questions")

        self.label_questions1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        #self.label_questions1.setObjectName("label_questions1")
        self.vertical_layout_questions.addWidget(self.label_questions1)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 240, 400, 200))
        #self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        #self.horizontalLayout.setObjectName("horizontalLayout")

        self.vertical_layout_user = QtWidgets.QVBoxLayout()
        #self.vertical_layout_user.setObjectName("vertical_layout_user")
        self.horizontalLayout.addLayout(self.vertical_layout_user)

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.vertical_layout_response = QtWidgets.QVBoxLayout()
        #self.vertical_layout_response.setObjectName("vertical_layout_response")
        self.horizontalLayout.addLayout(self.vertical_layout_response)

        self.retranslate_ui(self)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit_chat_message.setPlaceholderText(_translate("MainWindow", "O puedes escribir tu pregunta..."))
        self.label_chat_title.setText(_translate("MainWindow", "Conversacion"))
        self.pushButton_send.setText(_translate("MainWindow", "Enviar"))
        self.label_questions_title.setText(_translate("MainWindow", "Puedes preguntar: Hey Mycroft..."))
        self.label_questions1.setText(_translate("MainWindow", "TextLabel"))

    def update_chat(source, message):
        pass

    def on_send_pressed(self):
        self.pushButton_send.setText("Test")
