from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QApplication, QAction, QToolBar, QLineEdit, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QUrl
import sys

from controllers.bookmark_controller import BookmarkController
from models.bookmark_manager import BookmarkManager
from views.bookmark_dialog import BookmarkDialog
from views.edit_bookmark_dialog import EditBookmarkDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.bookmark_manager = BookmarkManager()
        self.bookmark_controller = BookmarkController(self)
        self.setup_ui()

    def setup_ui(self):
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)
        self.setup_navigation_toolbar()
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

    def setup_navigation_toolbar(self):
        navbar = QToolBar("Navigation")
        self.addToolBar(navbar)

        back_btn = QAction(QIcon('resources/icons/back.png'), 'Back', self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon('resources/icons/forward.png'), 'Forward', self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon('resources/icons/reload.png'), 'Reload', self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction(QIcon('resources/icons/home.png'), 'Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        navbar.setIconSize(QSize(16, 16))
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("""
                            QLineEdit {
                                margin-top:2px;
                                margin-bottom:2px;
                                height: 20px;
                                border-radius: 15px;
                                padding: 5px;
                            }
                        """)
        navbar.addWidget(self.url_bar)

        add_bookmark_btn = QAction(QIcon('resources/icons/star.png'), 'Add to Bookmark', self)
        add_bookmark_btn.triggered.connect(self.add_bookmark)
        navbar.addAction(add_bookmark_btn)

        bookmark_action = QAction(QIcon('resources/icons/bookmark.png'), 'Bookmarks', self)
        bookmark_action.triggered.connect(self.show_bookmark_menu)
        navbar.addAction(bookmark_action)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl('http://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(self.update_urlbar)  # Corrected connection
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        if self.tabs.count() == 0:
            return
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl)

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def update_urlbar(self, qurl):
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def add_bookmark(self):
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_url = current_browser.url().toString()
            current_title = current_browser.page().title()

            editDialog = EditBookmarkDialog(self, title=current_title, url=current_url)
            if editDialog.exec_() == QDialog.Accepted:
                new_title, new_url = editDialog.getInputs()
                # Use the controller to add the bookmark
                self.bookmark_controller.add_bookmark(new_title, new_url)

    def show_bookmark_menu(self):
        loaded_bookmarks = self.bookmark_manager.load_bookmarks("default")
        print("show main bookmarks")
        print(loaded_bookmarks)
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            self.dialog = BookmarkDialog(current_browser, loaded_bookmarks)
            self.dialog.show()
        else:
            print("No web browser found in the current tab.")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName('My Cool Browser')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
