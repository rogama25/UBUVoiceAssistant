# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Desktop/2nd.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import socket, pickle
import subprocess
import re
import time
from threading import Thread
from webservice.web_service import WebService
from PyQt5 import QtCore, QtGui, QtWidgets
from mycroft_bus_client import MessageBusClient, Message



class AppMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ws = WebService.get_instance()
        self.host = 'localhost'
        self.port = 5055
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        self.mycroft_response = ''
        self.mic_muted = False
        self.title = 'UBUAssistant'
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 600
        self.next_form = 0
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

        self.pushButton_mic = QtWidgets.QPushButton(self)
        self.pushButton_mic.setGeometry(QtCore.QRect(350, 260, 24, 24))
        self.mic_icon = QtGui.QIcon()
        self.mic_icon.addPixmap(QtGui.QPixmap("mic.png"))
        self.mic_muted_icon = QtGui.QIcon()
        self.mic_muted_icon.addPixmap(QtGui.QPixmap("mic_muted.png"))
        self.pushButton_mic.setIcon(self.mic_icon)
        self.pushButton_mic.clicked.connect(self.on_mic_pressed)

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
        self.vertical_layout_questions.addWidget(self.label_questions1)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setGeometry(QtCore.QRect(50, 300, 400, 220))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.formLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.formLayoutWidget.setGeometry(QtCore.QRect(50, 300, 400, 220))
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.scrollArea.setWidget(self.formLayoutWidget)

        self.log_dialog = QtWidgets.QDialog(self)
        self.log_dialog.setWindowTitle('UBUAssistant Logs')
        self.log_dialog.resize(600, 600)

        self.log_text = QtWidgets.QPlainTextEdit(self.log_dialog)
        self.log_text.resize(600, 600)

        self.pushButton_logs = QtWidgets.QPushButton(self)
        self.pushButton_logs.setGeometry(QtCore.QRect(400, 10, 80, 40))
        self.pushButton_logs.clicked.connect(self.on_logs_pressed)

        self.retranslate_ui(self)

        subprocess.Popen(['bash', '/home/adp1002/mycroft-core/start-mycroft.sh', 'restart', 'all'])


        #while(True):
        self.server_socket.listen(1)
        client_socket, address = self.server_socket.accept()
        webservice_data = pickle.dumps(self.ws)
        client_socket.send(webservice_data)

        self.bus = MessageBusClient()
        event_thread = Thread(target=self.connect, args=[self.bus])
        event_thread.setDaemon(True)
        event_thread.start()

        self.bus.on('speak', self.handle_speak)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit_chat_message.setPlaceholderText(_translate("MainWindow", "O puedes escribir tu pregunta..."))
        self.label_chat_title.setText(_translate("MainWindow", "Conversacion"))
        self.pushButton_send.setText(_translate("MainWindow", "Enviar"))
        self.pushButton_logs.setText(_translate("MainWindow", "Abrir Logs"))
        self.label_questions_title.setText(_translate("MainWindow", "Puedes preguntar: Hey Mycroft..."))
        self.label_questions1.setText(_translate("MainWindow", "TextLabel"))

    def update_chat(self, source, message):
        tmp_label = QtWidgets.QLabel(self.formLayoutWidget)
        tmp_label.setWordWrap(True)
        if source == 'r':
            self.formLayout.setWidget(self.next_form, QtWidgets.QFormLayout.FieldRole, tmp_label)
        elif source == 'u':
            self.formLayout.setWidget(self.next_form, QtWidgets.QFormLayout.LabelRole, tmp_label)
        tmp_label.setText(message)
        self.next_form+=1


    def on_logs_pressed(self):
        logs = open('logs.txt', 'r').read()
        self.log_text.setPlainText(logs)
        self.log_dialog.show()

    def handle_speak(self, message):
        self.mycroft_response = message.data.get('utterance')
        self.mycroft_responded = True

    def connect(self, bus):
        self.bus.run_forever()


    def on_send_pressed(self):
        utterance = self.lineEdit_chat_message.text()
        self.update_chat('u', utterance)
        self.bus.emit(Message('recognizer_loop:utterance', {'utterances': [utterance]}))
        time.sleep(1)
        self.update_chat('r', self.mycroft_response)
        self.mycroft_responded = False
        self.mycroft_response = ''
        self.lineEdit_chat_message.setText('')

    def on_mic_pressed(self):
        if self.mic_muted:
            self.mic_muted = False
            self.pushButton_mic.setIcon(self.mic_icon)
            self.bus.emit(Message('mycroft.mic.unmute'))
        else:
            self.mic_muted = True
            self.pushButton_mic.setIcon(self.mic_muted_icon)
            self.bus.emit(Message('mycroft.mic.mute'))
