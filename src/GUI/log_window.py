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
        MAX_LINES = 1000
        lines = open(file, 'r').readlines()
        n_lines = len(lines)

        if n_lines > MAX_LINES:
            lines = lines[n_lines-MAX_LINES:]
            updated_logs = open(file, 'w+')
            [updated_logs.write(line) for line in lines]
            updated_logs.close()

        logs = open(file, 'r')

        self.setPlainText(logs.read())
