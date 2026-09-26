from PySide6.QtWidgets import QMainWindow

from ui.library_page import LibraryPage
from ui.reader_page import ReaderPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EPUB Reader")
        self.resize(1200, 800)

        self.show_library()

    def show_library(self):
        self.library_page = LibraryPage()
        self.setCentralWidget(self.library_page)

    def show_reader(self, book):
        self.reader_page = ReaderPage(book)
        self.setCentralWidget(self.reader_page)