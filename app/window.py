from PySide6.QtWidgets import QMainWindow

from ui.library_page import LibraryPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EPUB Reader")
        self.resize(1000, 700)

        self.setup_ui()

    def setup_ui(self):
        library_page = LibraryPage()

        self.setCentralWidget(library_page)