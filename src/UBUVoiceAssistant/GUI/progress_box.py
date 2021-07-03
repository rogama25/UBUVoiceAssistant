"""Module for infinite progress bars
"""
from PyQt5 import QtWidgets


class ProgressBox(QtWidgets.QProgressDialog):
    """Class for infinite progress bars
    """

    def __init__(self, text: str):
        super().__init__(text, "Cancel", 0, 0)
        self.setWindowTitle("UBUVoiceAssistant")
        self.setModal(True)
        self.setCancelButton(None)  # type: ignore
        self.forceShow()
        self.setFixedSize(self.size())
        self.done = False

    def closeEvent(self, event) -> None:
        """This event gets triggered when trying to close the Window. We ignore them if we haven't
            finished yet

        Args:
            event: Qt Close event
        """
        if not self.done:
            event.ignore()
        else:
            event.accept()
