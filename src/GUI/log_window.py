from PyQt5 import QtWidgets


class LogDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setWindowTitle('UBUAssistant Logs')

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(LogTab('/var/log/mycroft/voice.log'), 'voice.log')
        self.tabs.addTab(LogTab('/var/log/mycroft/audio.log'), 'audio.log')
        self.tabs.addTab(LogTab('/var/log/mycroft/skills.log'), 'skills.log')
        self.tabs.addTab(LogTab('/var/log/mycroft/enclosure.log'), 'enclosure.log')
        self.tabs.addTab(LogTab('/var/log/mycroft/bus.log'), 'bus.log')
        self.tabs.addTab(LogTab('logs.log'), 'app.log')

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.tabs)
        self.setLayout(self.vbox)


class LogTab(QtWidgets.QPlainTextEdit):
    def __init__(self, file):
        super().__init__()
        # self.resize(self.width(), self.height())
        logs = open(file, 'r').read()
        self.setPlainText(logs)
