import json
import os

from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QDialogButtonBox, QLabel, QDialog

BOOKMARKS_DIR = "bookmarks"


class DirectorySelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Bookmark Directory")

        self.directoryComboBox = QComboBox()
        self.directoryComboBox.addItems(self.list_bookmark_directories())
        self.directoryComboBox.setEditable(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select or create a directory:"))
        layout.addWidget(self.directoryComboBox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def getSelectedDirectory(self):
        directory = self.directoryComboBox.currentText()
        # Remove .json extension if present
        if directory.endswith('.json'):
            directory = directory[:-5]
        return directory

    def list_bookmark_directories(self):
        if not os.path.exists(BOOKMARKS_DIR):
            os.makedirs(BOOKMARKS_DIR)
        return [f[:-5] for f in os.listdir(BOOKMARKS_DIR) if f.endswith('.json')]

    def save_bookmarks_to_directory(self,directory, bookmarks):
        filepath = os.path.join(BOOKMARKS_DIR, directory + '.json')
        with open(filepath, 'w') as f:
            json.dump(bookmarks, f)
