"""Module for Message Windows
"""
from PyQt5 import QtWidgets

class MessageBox(QtWidgets.QMessageBox):
    """Class for Message Windows
    """
    def __init__(self, text: str):
        super().__init__()
        self.setWindowTitle("UBUVoiceAssistant")
        self.setText(text)
        self.setFixedSize(self.size())
