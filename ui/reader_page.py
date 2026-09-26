from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from PySide6.QtWebEngineWidgets import QWebEngineView


class ReaderPage(QWidget):
    def __init__(self, book, parent=None):
        super().__init__(parent)

        self.book = book

        self.setup_ui()
        self.load_first_chapter()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Top bar
        toolbar = QHBoxLayout()

        back_button = QPushButton("← Library")
        back_button.clicked.connect(self.go_back)

        title_label = QLabel(self.book.title)
        title_label.setAlignment(Qt.AlignCenter)

        menu_button = QPushButton("☰")

        toolbar.addWidget(back_button)
        toolbar.addStretch()
        toolbar.addWidget(title_label)
        toolbar.addStretch()
        toolbar.addWidget(menu_button)

        layout.addLayout(toolbar)

        # Web view
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

    def load_first_chapter(self):
        if not self.book.chapters:
            self.web_view.setHtml(
                "<h1>No chapters found.</h1>"
            )
            return

        chapter = self.book.chapters[0]

        self.web_view.setHtml(chapter.content)

    def go_back(self):
        window = self.window()

        if hasattr(window, "show_library"):
            window.show_library()