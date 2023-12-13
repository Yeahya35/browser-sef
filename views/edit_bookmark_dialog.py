from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon


class EditBookmarkDialog(QDialog):
    def __init__(self, parent=None, title="", url=""):
        super().__init__(parent)
        self.titleEdit = QLineEdit(title, self)
        self.urlEdit = QLineEdit(url, self)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.titleEdit)
        layout.addWidget(QLabel("URL:"))
        layout.addWidget(self.urlEdit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getInputs(self):
        return self.titleEdit.text(), self.urlEdit.text()


