# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Desktop/2nd.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
#import socket, pickle
import subprocess
import re
import time
from os import path, listdir
from threading import Thread
from webservice.web_service import WebService
from PyQt5 import QtCore, QtGui, QtWidgets
from mycroft_bus_client import MessageBusClient, Message
from util import util



class AppMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ws = WebService.get_instance()
        self.user_utterance = ''
        self.mycroft_response = ''
        self.mic_muted = False
        self.active_skills = []
        self.unactive_skills = []
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
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(100, 250, 300, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.label_chat_title = QtWidgets.QLabel(self.centralwidget)
        self.label_chat_title.setGeometry(QtCore.QRect(200, 260, 120, 14))
        font_chat_title = QtGui.QFont()
        font_chat_title.setPointSize(14)
        self.label_chat_title.setFont(font_chat_title)

        self.lineEdit_chat_message = self.lineEdit_user = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_chat_message.setGeometry(QtCore.QRect(50, 550, 350, 30))

        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send.setGeometry(QtCore.QRect(399, 550, 50, 30))
        self.pushButton_send.clicked.connect(self.on_send_pressed)

        self.pushButton_mic = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_mic.setGeometry(QtCore.QRect(350, 260, 24, 24))
        self.mic_icon = QtGui.QIcon()
        self.mic_icon.addPixmap(QtGui.QPixmap("mic.png"))
        self.mic_muted_icon = QtGui.QIcon()
        self.mic_muted_icon.addPixmap(QtGui.QPixmap("mic_muted.png"))
        self.pushButton_mic.setIcon(self.mic_icon)
        self.pushButton_mic.clicked.connect(self.on_mic_pressed)

        self.label_questions_title = QtWidgets.QLabel(self.centralwidget)
        self.label_questions_title.setGeometry(QtCore.QRect(20, 10, 315, 40))
        font_questions_title = QtGui.QFont()
        font_questions_title.setPointSize(16)
        self.label_questions_title.setFont(font_questions_title)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 50, 360, 190))

        self.vertical_layout_questions = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_questions.setContentsMargins(0, 0, 0, 0)


        self.label_questions1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.vertical_layout_questions.addWidget(self.label_questions1)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(50, 300, 400, 220))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()

        self.formLayout = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.log_dialog = QtWidgets.QDialog(self)
        self.log_dialog.setWindowTitle('UBUAssistant Logs')
        self.log_dialog.resize(600, 600)

        self.log_text = QtWidgets.QPlainTextEdit(self.log_dialog)
        self.log_text.resize(600, 600)

        self.pushButton_logs = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_logs.setGeometry(QtCore.QRect(370, 10, 120, 40))
        self.pushButton_logs.clicked.connect(self.on_logs_pressed)

        self.skills_dialog = QtWidgets.QDialog(self)
        self.skills_dialog.setWindowTitle('Mycroft Skills')
        self.skills_dialog.resize(600, 600)

        self.pushButton_skills = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_skills.setGeometry(QtCore.QRect(370, 60, 120, 40))
        self.pushButton_skills.clicked.connect(self.on_skills_pressed)

        self.pushButton_manage_skills = QtWidgets.QPushButton(self.skills_dialog)
        self.pushButton_manage_skills.setGeometry(QtCore.QRect(470, 10, 120, 40))
        self.pushButton_manage_skills.clicked.connect(self.on_manage_skills_pressed)

        [self.active_skills.append(name) for name in listdir('/opt/mycroft/skills/') if path.isdir('/opt/mycroft/skills/' + name)]

        self.timer  = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_for_chat_update)
        self.timer.start()

        self.retranslate_ui(self)

        subprocess.Popen(['bash', path.expanduser('~') + '/mycroft-core/start-mycroft.sh', 'debug'])

        server_socket = Thread(target=util.create_server_socket, args=[util.SOCKET_HOST, util.SOCKET_PORT, self.ws])
        server_socket.setDaemon(True)
        server_socket.start()

        self.bus = MessageBusClient()
        event_thread = Thread(target=self.connect, args=[self.bus])
        event_thread.setDaemon(True)
        event_thread.start()

        self.bus.on('speak', self.handle_speak)
        self.bus.on('recognizer_loop:utterance', self.handle_utterance)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UBUAssistant"))
        self.lineEdit_chat_message.setPlaceholderText(_translate("MainWindow", "O puedes escribir tu pregunta..."))
        self.label_chat_title.setText(_translate("MainWindow", "Conversacion"))
        self.pushButton_send.setText(_translate("MainWindow", "Enviar"))
        self.pushButton_logs.setText(_translate("MainWindow", "Abrir Logs"))
        self.pushButton_skills.setText(_translate("MainWindow", "Administrar Skills"))
        self.label_questions_title.setText(_translate("MainWindow", "Puedes preguntar: Hey Mycroft..."))
        self.label_questions1.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_manage_skills.setText(_translate("MainWindow", "Activar/Desactivar"))

    def update_chat(self, source):
        tmp_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        tmp_label.setWordWrap(True)
        if source == 'r':
            self.formLayout.setWidget(self.next_form, QtWidgets.QFormLayout.FieldRole, tmp_label)
            tmp_label.setText(self.mycroft_response)
            self.mycroft_response = ''
        elif source == 'u':
            self.formLayout.setWidget(self.next_form, QtWidgets.QFormLayout.LabelRole, tmp_label)
            tmp_label.setText(self.user_utterance)
            self.user_utterance = ''
        self.next_form+=1

    def handle_speak(self, message):
        self.mycroft_response = message.data.get('utterance')

    def handle_utterance(self, message):
        self.user_utterance = message.data['utterances'][0]

    def connect(self, bus):
        self.bus.run_forever()

    def check_for_chat_update(self):
        if self.user_utterance:
            self.update_chat('u')
        if self.mycroft_response:
            self.update_chat('r')

    def on_send_pressed(self):
        self.user_utterance = self.lineEdit_chat_message.text()
        self.bus.emit(Message('recognizer_loop:utterance', {'utterances': [self.user_utterance]}))
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

    def on_logs_pressed(self):
        logs = open('logs.txt', 'r').read()
        self.log_text.setPlainText(logs)
        self.log_dialog.show()

    def on_skills_pressed(self):

        self.scrollArea_skills = QtWidgets.QScrollArea(self.skills_dialog)
        self.scrollArea_skills.setGeometry(QtCore.QRect(10, 10, 450, 580))
        self.scrollArea_skills.setWidgetResizable(True)
        self.scrollAreaWidgetContents_skills = QtWidgets.QWidget()
        self.scrollArea_skills.setWidget(self.scrollAreaWidgetContents_skills)

        self.skills_vlayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_skills)
        self.skills_vlayout.setGeometry(QtCore.QRect(10, 10, 450, 580))

        self.active_skills_checkBoxes = []
        self.unactive_skills_checkBoxes = []
        label = QtWidgets.QLabel(self.scrollAreaWidgetContents_skills)
        label.setText('Skills activas')
        self.skills_vlayout.addWidget(label)
        for name in self.active_skills:
            checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_skills)
            checkBox.setText(name)
            self.active_skills_checkBoxes.append(checkBox)
            self.skills_vlayout.addWidget(checkBox)
        label = QtWidgets.QLabel(self.scrollAreaWidgetContents_skills)
        label.setText('Skills inactivas')
        self.skills_vlayout.addWidget(label)
        for name in self.unactive_skills:
            checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_skills)
            checkBox.setText(name)
            self.unactive_skills_checkBoxes.append(checkBox)
            self.skills_vlayout.addWidget(checkBox)
        self.skills_dialog.show()

    def on_manage_skills_pressed(self):
        deactivated = []
        activated = []
        for cb in self.active_skills_checkBoxes:
            if cb.isChecked():
                self.bus.emit(Message('skillmanager.deactivate', {'skill': cb.text()}))
                deactivated.append(cb.text())

        for cb in self.unactive_skills_checkBoxes:
            if cb.isChecked():
                self.bus.emit(Message('skillmanager.activate', {'skill': cb.text()}))
                activated.append(cb.text())

        self.skills_dialog.hide()

        self.active_skills = [skill for skill in self.active_skills if skill not in deactivated]
        self.active_skills.extend(activated)

        self.unactive_skills = [skill for skill in self.unactive_skills if skill not in activated]
        self.unactive_skills.extend(deactivated)

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox()
        close.setText("Estas seguro?")
        close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        close = close.exec()

        if close == QtWidgets.QMessageBox.Yes:
            subprocess.run(['bash', path.expanduser('~') + '/mycroft-core/stop-mycroft.sh'])
            event.accept()
        else:
            event.ignore()
