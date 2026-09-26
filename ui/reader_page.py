from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSplitter,
)
from PySide6.QtWebEngineWidgets import QWebEngineView


class ReaderPage(QWidget):
    def __init__(self, book, parent=None):
        super().__init__(parent)

        # Application state
        self.current_book = book
        self.current_chapter = 0
        self.current_position = 0

        self.setup_ui()
        self.populate_contents()
        self.load_chapter(0)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # -------------------------
        # Top toolbar
        # -------------------------

        toolbar = QHBoxLayout()

        back_button = QPushButton("← Library")
        back_button.clicked.connect(self.go_back)

        self.title_label = QLabel(self.current_book.title)
        self.title_label.setAlignment(Qt.AlignCenter)

        menu_button = QPushButton("☰")

        toolbar.addWidget(back_button)
        toolbar.addStretch()
        toolbar.addWidget(self.title_label)
        toolbar.addStretch()
        toolbar.addWidget(menu_button)

        main_layout.addLayout(toolbar)

        # -------------------------
        # Main content
        # -------------------------

        splitter = QSplitter(Qt.Horizontal)

        # Table of contents
        self.contents = QListWidget()
        self.contents.setMinimumWidth(200)
        self.contents.itemClicked.connect(self.chapter_selected)

        splitter.addWidget(self.contents)

        # Book content
        self.web_view = QWebEngineView()
        splitter.addWidget(self.web_view)

        splitter.setSizes([220, 800])

        main_layout.addWidget(splitter)

        # -------------------------
        # Bottom navigation
        # -------------------------

        navigation = QHBoxLayout()

        self.previous_button = QPushButton(
            "← Previous Chapter"
        )
        self.previous_button.clicked.connect(
            self.previous_chapter
        )

        self.next_button = QPushButton(
            "Next Chapter →"
        )
        self.next_button.clicked.connect(
            self.next_chapter
        )

        navigation.addWidget(self.previous_button)
        navigation.addStretch()
        navigation.addWidget(self.next_button)

        main_layout.addLayout(navigation)

    def populate_contents(self):
        self.contents.clear()

        for index, chapter in enumerate(
            self.current_book.chapters
        ):
            item = QListWidgetItem(chapter.title)

            # Store chapter index inside the list item
            item.setData(Qt.UserRole, index)

            self.contents.addItem(item)

    def load_chapter(self, index):
        if not self.current_book.chapters:
            self.web_view.setHtml(
                "<h1>No chapters found.</h1>"
            )
            return

        if index < 0 or index >= len(
            self.current_book.chapters
        ):
            return

        self.current_chapter = index

        chapter = self.current_book.chapters[index]

        self.web_view.setHtml(chapter.content)

        # Highlight current chapter in contents
        self.contents.setCurrentRow(index)

        self.update_navigation_buttons()

    def chapter_selected(self, item):
        index = item.data(Qt.UserRole)

        self.load_chapter(index)

    def previous_chapter(self):
        if self.current_chapter > 0:
            self.load_chapter(
                self.current_chapter - 1
            )

    def next_chapter(self):
        if self.current_chapter < len(
            self.current_book.chapters
        ) - 1:
            self.load_chapter(
                self.current_chapter + 1
            )

    def update_navigation_buttons(self):
        self.previous_button.setEnabled(
            self.current_chapter > 0
        )

        self.next_button.setEnabled(
            self.current_chapter
            < len(self.current_book.chapters) - 1
        )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.previous_chapter()
            return

        if event.key() == Qt.Key_Right:
            self.next_chapter()
            return

        super().keyPressEvent(event)

    def go_back(self):
        window = self.window()

        if hasattr(window, "show_library"):
            window.show_library()