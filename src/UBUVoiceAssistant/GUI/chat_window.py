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

        self.mic_icon = QtGui.QIcon(QtGui.QPixmap("imgs/ic.svg"))
        self.mic_muted_icon = QtGui.QIcon(QtGui.QPixmap("imgs/mic_muted.svg"))

        self.color: List[Union[int, float]] = list(
            self.palette().color(QtGui.QPalette.ColorRole.Background).getRgb())
        # We need to divide this to get a floating value for HTML
        self.color[3] /= 255.0
        self.btnMute.clicked.connect(self.on_send_pressed)

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
        self.web.loadFinished.connect(self.update_texts)
        self.web.load(QtCore.QUrl.fromLocalFile(
            os.path.abspath(os.getcwd())+"/UBUVoiceAssistant/GUI/forms/chat_window_html/message-bubbles.html"))
        # with open("./UBUVoiceAssistant/GUI/forms/chat_window_html/message-bubbles.html") as file:
        #     self.web.setHtml(file.read(), baseUrl=QtCore.QUrl().fromLocalFile(
        #         os.path.abspath(os.getcwd())+"/UBUVoiceAssistant/GUI/forms/chat_window_html"))

    def update_texts(self):
        print(self.color)
        js_color = "document.body.style.backgroundColor = 'rgba(" + ','.join(
            map(str, self.color)) + ")';"
        self.web.page().runJavaScript(js_color)
        self.web.page().runJavaScript("document.documentElement.style.overflowX = 'hidden';")

    def update_chat(self, source: str, message: str):
        js_string = "var chat = document.getElementById('chat-window');\n"
        js_string += "var msg = document.createElement('li');\n"
        if source == "u":
            js_string += "msg.classList.add('right-msg');\n"
        js_string += "msg.appendChild(document.createTextNode(`" + \
            message + "`));\n"
        js_string += "chat.appendChild(msg);"
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
            self.closing_window = ProgressBox(_("Closing Mycroft, please wait..."))
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
        self.bus.emit(Message('recognizer_loop:utterance', {'utterances': [self.user_utterance]}))
        self.tbxInput.setText('')


class CloseMycroft(QtCore.QThread):
    def run(self):
        subprocess.run("/usr/lib/mycroft-core/stop-mycroft.sh", shell=True)
        self.finished.emit()
