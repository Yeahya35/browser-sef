from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog

from models.bookmark_manager import BookmarkManager
from views.directory_selection import DirectorySelectionDialog


class BookmarkController:
    def __init__(self, view):
        self.view = view
        self.model = BookmarkManager()
        self.directorySelectionView = DirectorySelectionDialog()

    def add_bookmark(self, title, url, directory="default"):
        dir_dialog = self.directorySelectionView
        if dir_dialog.exec_() == QDialog.Accepted:
            selected_directory = dir_dialog.getSelectedDirectory()
            print("SELCECTED_DIR")
            print(selected_directory)
            favicon_url = self.get_favicon_url(url)
            bookmark_info = {'url': url, 'title': title, 'favicon': favicon_url}
            bookmarks = self.model.load_bookmarks(selected_directory)
            if bookmark_info not in bookmarks:
                bookmarks.append(bookmark_info)
                self.directorySelectionView.save_bookmarks_to_directory(selected_directory, bookmarks)
        favicon_url = self.get_favicon_url(url)
        bookmark_info = {'url': url, 'title': title, 'favicon': favicon_url}
        self.model.add_bookmark(bookmark_info)

    def get_favicon_url(self, url):
        domain = QUrl(url).host()
        return f"https://www.google.com/s2/favicons?domain={domain}"

