# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/adp/Desktop/final.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import subprocess
import time
from os import path, listdir, environ
from threading import Thread
from webservice.web_service import WebService
from PyQt5 import QtCore, QtGui, QtWidgets
from mycroft_bus_client import MessageBusClient, Message
from log_window import LogDialog
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
        self.top = 0
        self.left = 0
        self.width = 500
        self.height = 600
        self.next_form = 0
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.center_on_screen()
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 3)

        self.line = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.line, 6, 1, 1, 5)

        self.lineEdit_chat_message = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_chat_message.sizePolicy().hasHeightForWidth())
        self.lineEdit_chat_message.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.lineEdit_chat_message, 11, 1, 1, 4)

        self.label_intent3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_intent3.sizePolicy().hasHeightForWidth())
        self.label_intent3.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label_intent3, 4, 1, 1, 1)

        self.label_intents_title = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_intents_title.sizePolicy().hasHeightForWidth())
        self.label_intents_title.setSizePolicy(sizePolicy)
        font_questions_title = QtGui.QFont()
        font_questions_title.setPointSize(16)
        self.label_intents_title.setFont(font_questions_title)
        self.gridLayout.addWidget(self.label_intents_title, 1, 1, 1, 1)

        self.label_intent2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_intent2.sizePolicy().hasHeightForWidth())
        self.label_intent2.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label_intent2, 3, 1, 1, 1)

        self.label_intent1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_intent1.sizePolicy().hasHeightForWidth())
        self.label_intent1.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label_intent1, 2, 1, 1, 1)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 768, 410))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.gridLayout_conversation = QtWidgets.QGridLayout()
        self.verticalLayout.addLayout(self.gridLayout_conversation)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 10, 1, 1, 5)

        self.label_chat_title = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_chat_title.sizePolicy().hasHeightForWidth())
        font_chat_title = QtGui.QFont()
        font_chat_title.setPointSize(14)
        self.label_chat_title.setSizePolicy(sizePolicy)
        self.label_chat_title.setFont(font_chat_title)
        self.gridLayout.addWidget(self.label_chat_title, 8, 1)

        self.pushButton_mic = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_mic.sizePolicy().hasHeightForWidth())
        self.pushButton_mic.setSizePolicy(sizePolicy)
        self.mic_icon = QtGui.QIcon()
        self.mic_icon.addPixmap(QtGui.QPixmap("mic.png"))
        self.mic_muted_icon = QtGui.QIcon()
        self.mic_muted_icon.addPixmap(QtGui.QPixmap("mic_muted.png"))
        self.pushButton_mic.setIcon(self.mic_icon)
        self.pushButton_mic.clicked.connect(self.on_mic_pressed)
        self.gridLayout.addWidget(self.pushButton_mic, 8, 5)

        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send.setGeometry(QtCore.QRect(399, 550, 50, 30))
        self.pushButton_send.clicked.connect(self.on_send_pressed)
        self.gridLayout.addWidget(self.pushButton_send, 11, 5, 1, 1)

        self.pushButton_logs = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_logs.setGeometry(QtCore.QRect(370, 10, 120, 40))
        self.pushButton_logs.clicked.connect(self.on_logs_pressed)
        self.gridLayout.addWidget(self.pushButton_logs, 1, 5, 1, 1)

        self.skills_dialog = QtWidgets.QDialog(self)
        self.skills_dialog.setWindowTitle('Mycroft Skills')
        self.skills_dialog.resize(600, 600)

        self.pushButton_skills = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_skills.setGeometry(QtCore.QRect(370, 60, 120, 40))
        self.pushButton_skills.clicked.connect(self.on_skills_pressed)
        self.gridLayout.addWidget(self.pushButton_skills, 3, 5, 1, 1)

        self.pushButton_manage_skills = QtWidgets.QPushButton(self.skills_dialog)
        self.pushButton_manage_skills.setGeometry(QtCore.QRect(470, 10, 120, 40))
        self.pushButton_manage_skills.clicked.connect(self.on_manage_skills_pressed)

        # List of the skills that the user should not interact with
        dangerous_skills = ['mycroft-volume.mycroftai',
                            'mycroft-stop.mycroftai',
                            'fallback-unknown.mycroftai',
                            'fallback-query.mycroftai',
                            'mycroft-configuration.mycroftai']

        # List of the skills in the /opt/mycroft/skills folder
        [self.active_skills.append(name) for name in listdir('/opt/mycroft/skills/') \
            if path.isdir('/opt/mycroft/skills/' + name) and name not in dangerous_skills]

        # Check if the chat needs to be updated every second
        self.timer  = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_for_chat_update)
        self.timer.start()

        self.retranslate_ui()

        # Send the webservice class to Mycroft
        server_socket = Thread(target=util.create_server_socket, args=[self.ws])
        server_socket.setDaemon(True)
        server_socket.start()

        # Start Mycroft services
        subprocess.run(['bash', path.expanduser('~') + '/mycroft-core/start-mycroft.sh', 'all', 'restart'])

        # Wait until the MessageBus is started, there might be a better solution
        time.sleep(15)

        # Thread connected to Mycroft MessageBusClient
        self.bus = MessageBusClient()
        self.bus.run_in_thread()
        self.bus.on('speak', self.handle_speak)
        self.bus.on('recognizer_loop:utterance', self.handle_utterance)

        # Deactivate mycroft-volume.mycroftai skill, mic works weird when it's active
        self.bus.emit(Message('skillmanager.deactivate', {'skill': 'mycroft-volume.mycroftai'}))

    def retranslate_ui(self):
        if environ['lang'] == 'es-es':
            self.lineEdit_chat_message.setPlaceholderText("O puedes escribir tu pregunta")
            self.label_chat_title.setText("Conversacion")
            self.pushButton_send.setText("Enviar")
            self.pushButton_logs.setText("Abrir Logs")
            self.pushButton_skills.setText("Administrar Skills")
            self.pushButton_mic.setText('Mute')
            self.label_intents_title.setText('Puedes preguntar: "Hey Mycroft...')
            self.label_intent1.setText('...abre el calendario"')
            self.label_intent2.setText('...dime los foros de (asignatura)"')
            self.label_intent3.setText('...dime mis notas"')
            # self.label_questions4.setText('...dime los eventos de (asignatura)"')
            # self.label_questions5.setText("")
            self.pushButton_manage_skills.setText("Guardar")
        elif environ['lang'] == 'en-us':
            self.lineEdit_chat_message.setPlaceholderText("Or you can ask via text")
            self.label_chat_title.setText("Conversation")
            self.pushButton_send.setText("Send")
            self.pushButton_logs.setText("Open Logs")
            self.pushButton_skills.setText("Manage Skills")
            self.label_intents_title.setText("You can ask: Hey Mycroft...")
            self.label_intent1.setText('"...open the calendar"')
            self.label_intent2.setText('"...tell me about the forums of (course)"')
            self.label_intent3.setText('"...tell me my grades"')
            # self.label_questions4.setText('"...tell me about the events of (course)"')
            # self.label_questions5.setText("")
            self.pushButton_manage_skills.setText("Save")

    def update_chat(self, source):
        tmp_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        tmp_label.setWordWrap(True)
        if source == 'r':
            self.gridLayout.addWidget(tmp_label, self.next_form, 1)
            self.gridLayout_conversation.addWidget(tmp_label, self.next_form, 1)
            tmp_label.setText(self.mycroft_response)
            self.mycroft_response = ''
        elif source == 'u':
            self.gridLayout_conversation.addWidget(tmp_label, self.next_form, 0)
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
            self.pushButton_mic.setText('Mute')
            self.bus.emit(Message('mycroft.mic.unmute'))
        else:
            self.mic_muted = True
            self.pushButton_mic.setIcon(self.mic_muted_icon)
            self.pushButton_mic.setText('Unmute')
            self.bus.emit(Message('mycroft.mic.mute'))

    def on_logs_pressed(self):
        self.log_dialog = LogDialog()
        self.log_dialog.show()

    def on_skills_pressed(self):

        scrollArea_skills = QtWidgets.QScrollArea(self.skills_dialog)
        scrollArea_skills.setGeometry(QtCore.QRect(10, 10, 450, 580))
        scrollArea_skills.setWidgetResizable(True)
        scrollAreaWidgetContents_skills = QtWidgets.QWidget()
        scrollArea_skills.setWidget(scrollAreaWidgetContents_skills)

        skills_grid_layout = QtWidgets.QGridLayout(scrollAreaWidgetContents_skills)
        skills_grid_layout.setGeometry(QtCore.QRect(10, 10, 450, 580))

        self.active_skills_checkBoxes = []
        self.unactive_skills_checkBoxes = []

        for count, name in enumerate(self.active_skills):
            checkBox = QtWidgets.QCheckBox(scrollAreaWidgetContents_skills)
            spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            checkBox.setText(name)
            checkBox.setChecked(True)
            logo = QtWidgets.QLabel(scrollAreaWidgetContents_skills)
            if 'ubu' in name:
                logo.setPixmap(QtGui.QPixmap('ubu_logo.jpg').scaled(20, 20))
            else:
                logo.setPixmap(QtGui.QPixmap('Mycroft_logo.png').scaled(20, 20))
            self.active_skills_checkBoxes.append(checkBox)
            skills_grid_layout.addWidget(logo, count, 0)
            skills_grid_layout.addWidget(checkBox, count, 1)
            skills_grid_layout.addItem(spacer, count, 2, QtCore.Qt.AlignLeft)

        for count, name in enumerate(self.unactive_skills, len(self.active_skills)):
            checkBox = QtWidgets.QCheckBox(scrollAreaWidgetContents_skills)
            checkBox.setText(name)
            logo = QtWidgets.QLabel(scrollAreaWidgetContents_skills)
            if 'ubu' in name:
                logo.setPixmap(QtGui.QPixmap('ubu_logo.jpg').scaled(20, 20))
            else:
                logo.setPixmap(QtGui.QPixmap('Mycroft_logo.png').scaled(20, 20))
            self.unactive_skills_checkBoxes.append(checkBox)
            skills_grid_layout.addWidget(logo, count, 0)
            skills_grid_layout.addWidget(checkBox, count, 1)
            skills_grid_layout.addItem(spacer, count, 2, QtCore.Qt.AlignLeft)

        self.skills_dialog.show()

    def on_manage_skills_pressed(self):
        deactivated = []
        activated = []
        for cb in self.active_skills_checkBoxes:
            if not cb.isChecked():
                self.bus.emit(Message('skillmanager.deactivate', {'skill': cb.text()}))
                deactivated.append(cb.text())

        for cb in self.unactive_skills_checkBoxes:
            if cb.isChecked():
                self.bus.emit(Message('skillmanager.activate', {'skill': cb.text()}))
                activated.append(cb.text())

        self.active_skills = [skill for skill in self.active_skills if skill not in deactivated]
        self.active_skills.extend(activated)

        self.unactive_skills = [skill for skill in self.unactive_skills if skill not in activated]
        self.unactive_skills.extend(deactivated)

        self.skills_dialog.hide()
        self.on_skills_pressed()

    def center_on_screen(self):
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def closeEvent(self, event):
        self.close = QtWidgets.QMessageBox()
        self.close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        if environ['lang'] == 'es-es':
            self.close.setText("¿Estas seguro?")
        elif environ['lang'] == 'en-us':
            self.close.setText("Are you sure?")
        self.close = self.close.exec()

        if self.close == QtWidgets.QMessageBox.Yes:
            self.timer.stop()
            subprocess.run(['bash', path.expanduser('~') + '/mycroft-core/stop-mycroft.sh'])
            event.accept()
        else:
            event.ignore()
