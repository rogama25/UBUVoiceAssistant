"""Module for the linking Mycroft to web UI
"""
import re
import time
import sys
from threading import Thread
import subprocess
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from mycroft_bus_client import MessageBusClient, Message  # type: ignore
from ..util.lang import Translator
from .message_box import MessageBox
from .progress_box import ProgressBox

_ = Translator().translate


class LinkMycroft(QtWidgets.QMainWindow):
    """Class for the linking Mycroft to web UI
    """

    def __init__(self, bus: MessageBusClient) -> None:
        self.closed_signal = pyqtSignal()
        super().__init__()
        uic.loadUi("./UBUVoiceAssistant/GUI/forms/link-mycroft.ui", self)
        self.page = 0
        self.done = False
        self.code = _("wait a second")

        self.btnPrev.setIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowLeft)
        self.btnPrev.clicked.connect(self.go_previous)
        self.btnNext.setIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowRight)
        self.btnNext.clicked.connect(self.go_next)

        self.file = open("/var/log/mycroft-docker/skills.log", "rb")
        self.file.seek(0, 2)  # Goes to the end of the file
        msg = Message("recognizer_loop:utterance",
                      utterance=[_("pair device")])
        # On other languages different than English, we must send again the phrase for it to start pairing
        bus.emit(msg)
        bus.on("configuration.updated", self.pairing_done)
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_pairing_code)  # type: ignore

        self.code_checker = Thread(target=self.read_pairing_code)
        self.code_checker.start()
        self.timer.start(1000)

    def pairing_done(self):
        self.done = True
        self.file.close()
        self.close()

    def add_pairing_code(self):
        self.lblCode.setText(self.code)

    def read_pairing_code(self):
        while not self.done:
            line = self.file.readline()
            if line:
                matches = re.findall(
                    "(?<=" + re.escape("PairingSkill | Pairing code: ") + ").+(?=\n)", line)
                self.code = matches[0]
            else:
                time.sleep(1)

    def update_texts(self):
        self.lblWelcome.setText(_("welcome!"))
        self.lblFirstRun.setText(_("it's your first time using"))
        self.btnPrev.setText(_("previous"))
        self.btnNext.setText(_("next"))
        self.lblRegisterAddDevice.setText(
            _("create an account and click add a device"))
        self.lblSelectVoice.setText(_("select google voice"))
        self.lblInfoCode.setText(_("input this code on the website"))

    def go_next(self):
        self.hide_all_elements()
        self.page = min(2, self.page + 1)
        if self.page == 1:
            self.imgSelectVoice.setVisible(True)
            self.lblSelectVoice.setVisible(True)
            self.btnPrev.setEnabled(True)
            self.btnNext.setEnabled(True)

        elif self.page == 2:
            self.picInputCode.setVisible(True)
            self.lblInfoCode.setVisible(True)
            self.lblCode.setVisible(True)
            self.btnPrev.setEnabled(True)

    def go_previous(self):
        self.hide_all_elements()
        self.page = max(0, self.page - 1)
        if self.page == 1:
            self.imgSelectVoice.setVisible(True)
            self.lblSelectVoice.setVisible(True)
            self.btnPrev.setEnabled(True)
            self.btnNext.setEnabled(True)

        elif self.page == 0:
            self.imgAddDevice.setVisible(True)
            self.lblRegisterAddDevice.setVisible(True)
            self.btnNext.setEnabled(True)

    def hide_all_elements(self):
        self.imgSelectVoice.setVisible(False)
        self.imgAddDevice.setVisible(False)
        self.picInputCode.setVisible(False)

        self.lblRegisterAddDevice.setVisible(False)
        self.lblSelectVoice.setVisible(False)
        self.lblInfoCode.setVisible(False)
        self.lblCode.setVisible(False)

        self.btnPrev.setEnabled(False)
        self.btnNext.setEnabled(False)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.done:
            self.closed_signal.emit()  # type: ignore
            event.accept()
        else:
            self.close_window = MessageBox(_("are you sure?"))
            self.close_window.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
            self.close_window.exec()
            if self.close == QtWidgets.QMessageBox.Yes:
                self.timer.stop()
                self.closing_window = ProgressBox(_("closing mycroft"))
                self.closing_window.show()
                self.closing_thread = CloseMycroft()
                self.closing_thread.finished.connect(  # type: ignore
                    self.finish_exit)
                self.closing_thread.start()
            else:
                event.ignore()

    def finish_exit(self):
        sys.exit(0)


class CloseMycroft(QThread):
    def run(self):
        subprocess.run("docker stop mycroft", shell=True)
