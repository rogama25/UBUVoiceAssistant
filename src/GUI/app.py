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
from GUI.log_window import LogDialog
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
        self.title = 'UBUAssistant 1.2'
        self.top = 0
        self.left = 0
        self.width = 500
        self.height = 600
        self.next_message = 0
        self.intent_labels = []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.center_on_screen()
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacer_item, 1, 2, 1, 3)

        self.verticalLayout_intents = QtWidgets.QVBoxLayout()
        self.gridLayout.addLayout(self.verticalLayout_intents, 2, 1, 1, 1)

        self.label_intent1 = self.create_intent_label()
        self.label_intent2 = self.create_intent_label()
        self.label_intent3 = self.create_intent_label()
        self.label_intent4 = self.create_intent_label()
        self.label_intent5 = self.create_intent_label()
        self.label_intent6 = self.create_intent_label()
        self.label_intent7 = self.create_intent_label()

        self.line = QtWidgets.QFrame(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(size_policy)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.line, 3, 1, 1, 5)

        self.lineEdit_chat_message = QtWidgets.QLineEdit(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.lineEdit_chat_message.sizePolicy().hasHeightForWidth())
        self.lineEdit_chat_message.setSizePolicy(size_policy)
        self.gridLayout.addWidget(self.lineEdit_chat_message, 8, 1, 1, 4)


        self.label_intents_title = QtWidgets.QLabel(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_intents_title.sizePolicy().hasHeightForWidth())
        self.label_intents_title.setSizePolicy(size_policy)
        font_questions_title = QtGui.QFont()
        font_questions_title.setPointSize(16)
        self.label_intents_title.setFont(font_questions_title)
        self.gridLayout.addWidget(self.label_intents_title, 1, 1, 1, 1)


        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(size_policy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 768, 410))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.gridLayout_conversation = QtWidgets.QGridLayout()
        self.verticalLayout.addLayout(self.gridLayout_conversation)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 7, 1, 1, 5)

        self.label_chat_title = QtWidgets.QLabel(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_chat_title.sizePolicy().hasHeightForWidth())
        font_chat_title = QtGui.QFont()
        font_chat_title.setPointSize(14)
        self.label_chat_title.setSizePolicy(size_policy)
        self.label_chat_title.setFont(font_chat_title)
        self.gridLayout.addWidget(self.label_chat_title, 5, 1)

        self.pushButton_mic = QtWidgets.QPushButton(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.pushButton_mic.sizePolicy().hasHeightForWidth())
        self.pushButton_mic.setSizePolicy(size_policy)
        self.mic_icon = QtGui.QIcon()
        self.mic_icon.addPixmap(QtGui.QPixmap("imgs/mic.svg"))
        self.mic_muted_icon = QtGui.QIcon()
        self.mic_muted_icon.addPixmap(QtGui.QPixmap("imgs/mic_muted.svg"))
        self.pushButton_mic.setIcon(self.mic_icon)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(115, 210, 22))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        self.pushButton_mic.setPalette(palette)
        self.pushButton_mic.clicked.connect(self.on_mic_pressed)
        self.gridLayout.addWidget(self.pushButton_mic, 5, 5)

        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send.setGeometry(QtCore.QRect(399, 550, 50, 30))
        self.pushButton_send.setPalette(palette)
        self.pushButton_send.clicked.connect(self.on_send_pressed)
        self.gridLayout.addWidget(self.pushButton_send, 8, 5, 1, 1)

        self.pushButton_logs = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_logs.setGeometry(QtCore.QRect(370, 10, 120, 40))
        self.logs_file_icon = QtGui.QIcon()
        self.logs_file_icon.addPixmap(QtGui.QPixmap("imgs/file.svg"))
        self.pushButton_logs.setIcon(self.logs_file_icon)
        self.pushButton_logs.clicked.connect(self.on_logs_pressed)
        self.gridLayout.addWidget(self.pushButton_logs, 1, 5, 1, 1)

        self.skills_dialog = QtWidgets.QDialog(self)
        self.skills_dialog.setWindowTitle('Mycroft Skills')
        self.skills_dialog.resize(600, 600)

        self.pushButton_skills = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_skills.setGeometry(QtCore.QRect(370, 60, 120, 40))
        self.skills_list_icon = QtGui.QIcon()
        self.skills_list_icon.addPixmap(QtGui.QPixmap("imgs/list.svg"))
        self.pushButton_skills.setIcon(self.skills_list_icon)
        self.pushButton_skills.clicked.connect(self.on_skills_pressed)
        self.gridLayout.addWidget(self.pushButton_skills, 2, 5, 1, 1)

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

        # Wait until Mycroft services are started, there might be a better solution
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
            self.label_intent2.setText('...dime los eventos de (asignatura)"')
            self.label_intent5.setText('...dime los foros de (asignatura)"')
            self.label_intent6.setText('...dime mis notas"')
            self.label_intent3.setText('...dime los eventos del (dia) de (mes) de (año)"')
            self.label_intent4.setText('...dime los cambios en (asignatura)"')
            self.label_intent7.setText('...dime las notas de (asignatura)"')
            self.pushButton_manage_skills.setText("Guardar")
        elif environ['lang'] == 'en-us':
            self.lineEdit_chat_message.setPlaceholderText("Or you can ask via text")
            self.label_chat_title.setText("Conversation")
            self.pushButton_send.setText("Send")
            self.pushButton_logs.setText("Open Logs")
            self.pushButton_skills.setText("Manage Skills")
            self.pushButton_mic.setText('Mute')
            self.label_intents_title.setText('You can ask: "Hey Mycroft...')
            self.label_intent1.setText('...open the calendar"')
            self.label_intent5.setText('...tell me about the forums of (course)"')
            self.label_intent6.setText('...tell me my grades"')
            self.label_intent2.setText('...tell me about the events of (course)"')
            self.label_intent3.setText('...tell me about the events on (month) (day) (year)"')
            self.label_intent4.setText('...tell me about the changes of (course)"')
            self.label_intent7.setText('...tell me the grades of (course)')
            self.pushButton_manage_skills.setText("Save")

    def create_intent_label(self):
        intent_label = QtWidgets.QLabel(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(intent_label.sizePolicy().hasHeightForWidth())
        intent_label.setSizePolicy(size_policy)
        self.verticalLayout_intents.addWidget(intent_label)
        return intent_label

    def update_chat(self, source):
        """ Adds a new label to the chat's gridLayout to the corresponding side
        ---
            Parameters:
                - Char source: 'r' to add to the right side (the response)
                               'u' to add to the left side (the user)
        """
        tmp_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        tmp_label.setWordWrap(True)
        if source == 'r':
            self.gridLayout.addWidget(tmp_label, self.next_message, 1)
            self.gridLayout_conversation.addWidget(tmp_label, self.next_message, 1)
            tmp_label.setText(self.mycroft_response)
            self.mycroft_response = ''
        elif source == 'u':
            self.gridLayout_conversation.addWidget(tmp_label, self.next_message, 0)
            tmp_label.setText(self.user_utterance)
            self.user_utterance = ''
        self.next_message+=1

    def handle_speak(self, message):
        self.mycroft_response = message.data.get('utterance')

    def handle_utterance(self, message):
        self.user_utterance = message.data['utterances'][0]

    def check_for_chat_update(self):
        """ Checks if there's a new message either in self.user_utterance or
            self.mycroft_response and updates the chat if so
        """
        if self.user_utterance:
            self.update_chat('u')
        if self.mycroft_response:
            self.update_chat('r')

    def on_send_pressed(self):
        self.user_utterance = self.lineEdit_chat_message.text()
        self.bus.emit(Message('recognizer_loop:utterance', {'utterances': [self.user_utterance]}))
        self.lineEdit_chat_message.setText('')

    def on_mic_pressed(self):
        # Switch between muted and unmuted when the mic is pressed
        if self.mic_muted:
            self.mic_muted = False
            self.pushButton_mic.setIcon(self.mic_icon)
            self.pushButton_mic.setText('Mute')
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(115, 210, 22))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
            self.pushButton_mic.setPalette(palette)
            self.bus.emit(Message('mycroft.mic.unmute'))
        else:
            self.mic_muted = True
            self.pushButton_mic.setIcon(self.mic_muted_icon)
            self.pushButton_mic.setText('Unmute')
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(255, 35, 35))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
            self.pushButton_mic.setPalette(palette)
            self.bus.emit(Message('mycroft.mic.mute'))

    def on_logs_pressed(self):
        self.log_dialog = LogDialog()
        self.log_dialog.show()

    def on_skills_pressed(self):

        scroll_area_skills = QtWidgets.QScrollArea(self.skills_dialog)
        scroll_area_skills.setGeometry(QtCore.QRect(10, 10, 450, 580))
        scroll_area_skills.setWidgetResizable(True)
        scroll_area_widget_skills = QtWidgets.QWidget()
        scroll_area_skills.setWidget(scroll_area_widget_skills)

        skills_grid_layout = QtWidgets.QGridLayout(scroll_area_widget_skills)
        skills_grid_layout.setGeometry(QtCore.QRect(10, 10, 450, 580))

        self.active_skills_checkBoxes = []
        self.unactive_skills_checkBoxes = []

        # Create checkboxes for every skill in self.active_skills
        for count, name in enumerate(self.active_skills):
            check_box = QtWidgets.QCheckBox(scroll_area_widget_skills)
            spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            check_box.setText(name)
            check_box.setChecked(True)
            logo = QtWidgets.QLabel(scroll_area_widget_skills)
            if 'ubu' in name:
                logo.setPixmap(QtGui.QPixmap('imgs/ubu_logo.jpg').scaled(20, 20))
            else:
                logo.setPixmap(QtGui.QPixmap('imgs/Mycroft_logo.png').scaled(20, 20))
            self.active_skills_checkBoxes.append(check_box)
            skills_grid_layout.addWidget(logo, count, 0)
            skills_grid_layout.addWidget(check_box, count, 1)
            skills_grid_layout.addItem(spacer, count, 2, QtCore.Qt.AlignLeft)

        # Create checkboxes for every skill in self.unactive_skills
        for count, name in enumerate(self.unactive_skills, len(self.active_skills)):
            check_box = QtWidgets.QCheckBox(scroll_area_widget_skills)
            check_box.setText(name)
            logo = QtWidgets.QLabel(scroll_area_widget_skills)
            if 'ubu' in name:
                logo.setPixmap(QtGui.QPixmap('imgs/ubu_logo.jpg').scaled(20, 20))
            else:
                logo.setPixmap(QtGui.QPixmap('imgs/Mycroft_logo.png').scaled(20, 20))
            self.unactive_skills_checkBoxes.append(check_box)
            skills_grid_layout.addWidget(logo, count, 0)
            skills_grid_layout.addWidget(check_box, count, 1)
            skills_grid_layout.addItem(spacer, count, 2, QtCore.Qt.AlignLeft)

        self.skills_dialog.show()

    def on_manage_skills_pressed(self):
        """ Adds the checked skills to self.active_skills and the unchecked to
            self.unactive_skills and activates or deactivates those skills.
        """
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

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.on_send_pressed()

    def center_on_screen(self):
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def closeEvent(self, event):
        self.close = QtWidgets.QMessageBox()
        self.close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.close.setWindowTitle('UBUAssistant 1.2')
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
