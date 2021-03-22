"""Module for infinite progress bars
"""
from PyQt5 import QtWidgets

class ProgressBox(QtWidgets.QProgressDialog):
    """Class for infinite progress bars
    """
    def __init__(self, text:str):
        super().__init__(text, "Cancel", 0, 0, self)
        self.setWindowTitle("UBUVoiceAssistant")
        self.setModal(True)
        self.setCancelButton(None) # type: ignore
        self.forceShow()
