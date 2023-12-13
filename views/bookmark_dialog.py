import json
import os
import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from models.bookmark_manager import BookmarkManager


class BookmarkDialog(QDialog):
    def __init__(self, browser, bookmarks):
        super().__init__()
        self.browser = browser
        self.bookmarks = bookmarks
        self.manager = BookmarkManager()
        self.setWindowTitle("Bookmarks")
        self.init_ui()
        self.update_bookmarks(self.bookmarks)

        self.populate_bookmark_directories()
        self.listWidget.itemClicked.connect(self.on_item_clicked)

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.listWidget = QListWidget(self)
        self.search_bar = QLineEdit()
        self.directoryComboBox = QComboBox(self)
        self.search_bar.textChanged.connect(self.filter_bookmarks)
        self.listWidget.itemClicked.connect(self.on_item_clicked)
        self.directoryComboBox.currentIndexChanged.connect(self.on_directory_changed)
        self.layout.addWidget(self.directoryComboBox)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.listWidget)

        self.setStyleSheet("""
                    QDialog {
                        background-color: #333;
                    }
                    QListWidget {
                        background-color: #333;
                        color: #fff;
                        border: none;
                    }
                    QListWidget::item {
                        padding: 10px;
                    }
                    QListWidget::item:selected {
                        background-color: #555;
                    }
                """)

    def update_bookmarks(self, bookmarks):
        self.listWidget.clear()
        # for bookmark in bookmarks:
        #     item = QListWidgetItem(bookmark['title'], self.listWidget)
        #     item.setData(Qt.UserRole, bookmark['url'])
        for bookmark in bookmarks:
            favicon_path = f"resources/favicons/{bookmark['title']}.ico"
            print(favicon_path)
            if not os.path.exists(favicon_path):
                self.download_favicon(bookmark['favicon'], favicon_path)

            item = QListWidgetItem(QIcon(favicon_path), bookmark['title'])
            item.setData(Qt.UserRole, bookmark['url'])
            self.listWidget.addItem(item)

    def on_item_clicked(self, item):
        url = item.data(Qt.UserRole)
        self.browser.setUrl(QUrl(url))
        self.close()

    def filter_bookmarks(self, text):
        # Clear the list
        self.listWidget.clear()

        # Add items that contain the search text
        for bookmark in self.bookmarks:
            if text.lower() in bookmark['url'].lower() or text.lower() in bookmark['title'].lower():
                favicon_path = f"resources/favicons/{bookmark['title']}.ico"
                item = QListWidgetItem(QIcon(favicon_path), bookmark['title'])
                item.setData(Qt.UserRole, bookmark)
                self.listWidget.addItem(item)

    def populate_bookmark_directories(self):
        # List all bookmark directories
        directories = self.list_bookmark_directories()
        self.directoryComboBox.addItems(directories)

    def list_bookmark_directories(self):
        bookmarks_dir = "bookmarks"
        return [f[:-5] for f in os.listdir(bookmarks_dir) if f.endswith('.json')]

    def on_directory_changed(self):
        selected_directory = self.directoryComboBox.currentText()
        print("CATEGORY_SELECTED")
        print(selected_directory)
        # self.load_bookmarks_from_directory(selected_directory)
        self.bookmarks = self.manager.load_bookmarks(selected_directory)
        self.update_bookmarks(self.bookmarks)

    def item_clicked(self, item):
        url = item.data(Qt.UserRole)
        self.browser.setUrl(QUrl(url))
        self.close()

    def download_favicon(self,url, save_path):
        try:
            print("HERE_URL")
            print(url)
            print("HERE_PATH")
            print(save_path)
            response = requests.get(url)
            response.raise_for_status()
            with open(save_path, 'wb') as f:
                f.write(response.content)
                print("in while")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
