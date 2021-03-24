from threading import Thread
import subprocess
from typing import List
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
        super().__init__()
        uic.loadUi("./GUI/forms/chat-window.ui", self)
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

        self.color = self.palette().color(QtGui.QPalette.ColorRole.Background).getRgb()
        self.btnMute.clicked.connect(self.on_send_pressed)

        self.dangerous_skills = ['mycroft-volume.mycroftai',
                                 'mycroft-stop.mycroftai',
                                 'fallback-unknown.mycroftai',
                                 'fallback-query.mycroftai',
                                 'mycroft-configuration.mycroftai']

        [self.active_skills.append(name) for name in listdir('/opt/mycroft/skills/')
            if path.isdir('/opt/mycroft/skills/' + name) and name not in self.dangerous_skills]  # type: ignore

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_for_chat_update)  # type: ignore
        self.timer.start(1000)

        self.bus.on("speak", self.handle_speak)
        self.bus.on("recognizer_loop:utterance", self.handle_utterance)

        self.bus.emit(Message("skillmanager.deactivate", {"skill": "mycroft-volume.mycroftai"}))

        self.web: QWebEngineView
        self.web.page().runJavaScript

    def update_texts(self):
        pass

    def update_chat(self, source: str):
        pass

    def handle_speak(self, message: Message):
        self.mycroft_response = message.data.get("utterance")

    def handle_utterance(self, message: Message):
        self.user_utterance = message.data["utterances"][0]

    def check_for_chat_update(self):
        if self.user_utterance:
            self.update_chat("u")
        if self.mycroft_response:
            self.update_chat("r")
