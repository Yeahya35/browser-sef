# models/bookmark_manager.py

import json
import os

BOOKMARKS_DIR = "bookmarks"

class BookmarkManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BookmarkManager, cls).__new__(cls)
            cls._instance.bookmarks = []
            cls._instance.load_bookmarks("default")
        return cls._instance

    def load_bookmarks(self, directory="default"):
        filepath = os.path.join(BOOKMARKS_DIR, directory + '.json')
        print("FILE PATH")
        print(filepath)
        if not os.path.exists(BOOKMARKS_DIR):
            os.makedirs(BOOKMARKS_DIR)
        try:
            with open(filepath, 'r') as f:
                self.bookmarks = json.load(f)
                print("BOOKMARKS")
                print(self.bookmarks)
                return self.bookmarks
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_bookmarks_to_directory(self, directory, bookmarks):
        filepath = os.path.join(BOOKMARKS_DIR, directory + '.json')
        with open(filepath, 'w') as f:
            json.dump(bookmarks, f)

    def add_bookmark(self, bookmark_info):
        if bookmark_info not in self.bookmarks:
            self.bookmarks.append(bookmark_info)
            self.save_bookmarks_to_directory("default", self.bookmarks)

    def save_bookmarks_to_directory(self, directory, bookmarks):
        filepath = os.path.join(BOOKMARKS_DIR, directory + '.json')
        with open(filepath, 'w') as f:
            json.dump(bookmarks, f, indent=4)