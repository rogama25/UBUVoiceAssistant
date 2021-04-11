from threading import Thread
import subprocess
import sys
import os
from typing import List, Union
from os import path, listdir
from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from mycroft_bus_client import Message, MessageBusClient  # type: ignore
from ..util.lang import Translator
from .message_box import MessageBox
from .progress_box import ProgressBox
from ..webservice import WebService

_ = Translator().translate


class ChatWindow(QtWidgets.QMainWindow):
    def __init__(self, bus: MessageBusClient, ws: WebService) -> None:
        super().__init__(parent=None)
        uic.loadUi("./UBUVoiceAssistant/GUI/forms/chat-window.ui", self)
        self.bus = bus
        self.ws = ws
        self.user_utterance = ""
        self.mycroft_response = ""
        self.mic_muted = False
        self.active_skills: List[str] = []
        self.inactive_skills: List[str] = []
        self.next_message = 0
        self.intent_labels = []

        self.mic_icon = QtGui.QIcon(QtGui.QPixmap("UBUVoiceAssistant/imgs/ic.svg"))
        self.mic_muted_icon = QtGui.QIcon(QtGui.QPixmap("UBUVoiceAssistant/imgs/mic_muted.svg"))

        self.color: List[Union[int, float]] = list(
            self.palette().color(QtGui.QPalette.ColorRole.Background).getRgb())
        # We need to divide this to get a floating value for HTML
        self.color[3] /= 255.0
        self.btnMute.clicked.connect(self.on_mic_pressed)

        self.on_mic_pressed(True)

        self.btnConfig.clicked.connect(self.on_skills_pressed)

        self.dangerous_skills = ['mycroft-volume.mycroftai',
                                 'mycroft-stop.mycroftai',
                                 'fallback-unknown.mycroftai',
                                 'fallback-query.mycroftai',
                                 'mycroft-configuration.mycroftai']

        [self.active_skills.append(name) for name in listdir('/opt/mycroft/skills/')  # type: ignore
            if path.isdir('/opt/mycroft/skills/' + name) and name not in self.dangerous_skills]

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_for_chat_update)  # type: ignore
        self.timer.start(1000)

        self.bus.on("speak", self.handle_speak)
        self.bus.on("recognizer_loop:utterance", self.handle_utterance)

        self.bus.emit(Message("skillmanager.deactivate", {
                      "skill": "mycroft-volume.mycroftai"}))

        self.web: QWebEngineView
        self.web.loadFinished.connect(self.set_elements_web)
        self.web.load(QtCore.QUrl.fromLocalFile(
            os.path.abspath(os.getcwd())+"/UBUVoiceAssistant/GUI/forms/chat_window_html/message-bubbles.html"))
        self.update_texts()
        # with open("./UBUVoiceAssistant/GUI/forms/chat_window_html/message-bubbles.html") as file:
        #     self.web.setHtml(file.read(), baseUrl=QtCore.QUrl().fromLocalFile(
        #         os.path.abspath(os.getcwd())+"/UBUVoiceAssistant/GUI/forms/chat_window_html"))

    def set_elements_web(self):
        print(self.color)
        js_color = "document.body.style.backgroundColor = 'rgba(" + ','.join(
            map(str, self.color)) + ")';"
        self.web.page().runJavaScript(js_color)
        self.web.page().runJavaScript("document.documentElement.style.overflowX = 'hidden';")
        message = _("Hey, I'm Mycroft\n")
        message += _("Just say: \"Hey Mycroft!\" and then ask one of these:\n\n")
        message += "· " + _("Open the calendar\n")
        message += "· " + _("Tell me about the forums of (course)\n")
        message += "· " + _("Tell me my grades\n")
        message += "· " + _("Tell me about the events of (course)\n")
        message += "· " + _("Tell me about the events on (month) (day) (year)\n")
        message += "· " + _("Tell me about the changes of (course)\n")
        message += "· " + _("Tell me the grades of (course)\n\n")
        message += _("And, if you want me to stop, say \"stop\"\n")
        js_string = "var chat = document.getElementById('chat-window');\n"
        js_string += "var msg = document.createElement('li');\n"
        js_string += "msg.appendChild(document.createTextNode(`" + \
            message + "`));\n"
        js_string += "chat.appendChild(msg);"
        self.web.page().runJavaScript(js_string)

    def update_texts(self):
        self.btnConfig.setText(_("Manage skills"))
        self.btnSend.setText(_("Send"))
        self.tbxInput.setPlaceholderText(_("Type your command here..."))

    def update_chat(self, source: str, message: str):
        js_string = "var chat = document.getElementById('chat-window');\n"
        js_string += "var msg = document.createElement('li');\n"
        if source == "u":
            js_string += "msg.classList.add('right-msg');\n"
        js_string += "msg.appendChild(document.createTextNode(`" + \
            message + "`));\n"
        js_string += "chat.appendChild(msg);\n"
        js_string += "window.scrollTo(0,document.body.scrollHeight);"
        print(js_string)
        self.web.page().runJavaScript(js_string)

    def handle_speak(self, message: Message):
        self.mycroft_response = message.data.get("utterance")

    def handle_utterance(self, message: Message):
        self.user_utterance = message.data["utterances"][0]

    def check_for_chat_update(self):
        if self.user_utterance:
            self.update_chat("u", self.user_utterance)
            self.user_utterance = ""
        if self.mycroft_response:
            self.update_chat("r", self.mycroft_response)
            self.mycroft_response = ""

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.close_window = MessageBox(_("Are you sure?"))
        self.close_window.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.close_res = self.close_window.exec()
        print(self.close_res)
        if self.close_res == QtWidgets.QMessageBox.Yes:
            self.timer.stop()
            self.closing_window = ProgressBox(
                _("Closing Mycroft, please wait..."))
            self.closing_window.show()
            self.closing_thread = CloseMycroft()
            self.closing_thread.finished.connect(  # type: ignore
                self.finish_exit)
            self.closing_thread.start()
        else:
            event.ignore()

    def finish_exit(self):
        sys.exit(0)

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.on_send_pressed()

    def on_send_pressed(self):
        self.user_utterance = self.tbxInput.text()
        self.bus.emit(Message('recognizer_loop:utterance', {
                      'utterances': [self.user_utterance]}))
        self.tbxInput.setText('')

    def on_mic_pressed(self, startup: bool = False):
        # Switch between muted and unmuted when the mic is pressed
        if self.mic_muted or startup:
            self.mic_muted = False
            self.btnMute.setIcon(self.mic_icon)
            self.btnMute.setText(_('Mute'))
            self.btnMute.setStyleSheet("background-color: green")
            self.bus.emit(Message('mycroft.mic.unmute'))
        else:
            self.mic_muted = True
            self.btnMute.setIcon(self.mic_muted_icon)
            self.btnMute.setText(_('Unmute'))
            self.btnMute.setStyleSheet("background-color: red")
            self.bus.emit(Message('mycroft.mic.mute'))

    def on_skills_pressed(self):

        self.skills_dialog = QtWidgets.QDialog(self)
        self.skills_dialog.setWindowTitle('Mycroft Skills')
        self.skills_dialog.resize(600, 600)

        self.pushButton_manage_skills = QtWidgets.QPushButton(self.skills_dialog)
        self.pushButton_manage_skills.setGeometry(QtCore.QRect(470, 10, 120, 40))
        self.pushButton_manage_skills.clicked.connect(self.on_manage_skills_pressed)

        self.pushButton_manage_skills.setText(_("Save"))

        scroll_area_skills = QtWidgets.QScrollArea(self.skills_dialog)
        scroll_area_skills.setGeometry(QtCore.QRect(10, 10, 450, 580))
        scroll_area_skills.setWidgetResizable(True)
        scroll_area_widget_skills = QtWidgets.QWidget()
        scroll_area_skills.setWidget(scroll_area_widget_skills)

        skills_grid_layout = QtWidgets.QGridLayout(scroll_area_widget_skills)
        skills_grid_layout.setGeometry(QtCore.QRect(10, 10, 450, 580))

        self.active_skills_checkBoxes = []
        self.inactive_skills_checkBoxes = []

        # Create checkboxes for every skill in self.active_skills
        for count, name in enumerate(self.active_skills):
            check_box = QtWidgets.QCheckBox(scroll_area_widget_skills)
            spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            check_box.setText(name)
            check_box.setChecked(True)
            logo = QtWidgets.QLabel(scroll_area_widget_skills)
            if 'ubu' in name:
                logo.setPixmap(QtGui.QPixmap('UBUVoiceAssistant/imgs/ubu_logo.jpg').scaled(20, 20))
            else:
                logo.setPixmap(QtGui.QPixmap('UBUVoiceAssistant/imgs/Mycroft_logo.png').scaled(20, 20))
            self.active_skills_checkBoxes.append(check_box)
            skills_grid_layout.addWidget(logo, count, 0)
            skills_grid_layout.addWidget(check_box, count, 1)
            skills_grid_layout.addItem(spacer, count, 2, QtCore.Qt.AlignLeft)

        # Create checkboxes for every skill in self.inactive_skills
        for count, name in enumerate(self.inactive_skills, len(self.active_skills)):
            check_box = QtWidgets.QCheckBox(scroll_area_widget_skills)
            check_box.setText(name)
            logo = QtWidgets.QLabel(scroll_area_widget_skills)
            if 'ubu' in name:
                logo.setPixmap(QtGui.QPixmap('UBUVoiceAssistant/imgs/ubu_logo.jpg').scaled(20, 20))
            else:
                logo.setPixmap(QtGui.QPixmap('UBUVoiceAssistant/imgs/Mycroft_logo.png').scaled(20, 20))
            self.inactive_skills_checkBoxes.append(check_box)
            skills_grid_layout.addWidget(logo, count, 0)
            skills_grid_layout.addWidget(check_box, count, 1)
            skills_grid_layout.addItem(spacer, count, 2, QtCore.Qt.AlignLeft)

        self.skills_dialog.show()

    def on_manage_skills_pressed(self):
        """ Adds the checked skills to self.active_skills and the unchecked to
            self.inactive_skills and activates or deactivates those skills.
        """
        deactivated = []
        activated = []
        for cb in self.active_skills_checkBoxes:
            if not cb.isChecked():
                self.bus.emit(Message('skillmanager.deactivate', {'skill': cb.text()}))
                deactivated.append(cb.text())

        for cb in self.inactive_skills_checkBoxes:
            if cb.isChecked():
                self.bus.emit(Message('skillmanager.activate', {'skill': cb.text()}))
                activated.append(cb.text())

        self.active_skills = [skill for skill in self.active_skills if skill not in deactivated]
        self.active_skills.extend(activated)

        self.inactive_skills = [skill for skill in self.inactive_skills if skill not in activated]
        self.inactive_skills.extend(deactivated)

        self.skills_dialog.hide()
        self.on_skills_pressed()


class CloseMycroft(QtCore.QThread):
    def run(self):
        subprocess.run("/usr/lib/mycroft-core/stop-mycroft.sh", shell=True)
        self.finished.emit()
