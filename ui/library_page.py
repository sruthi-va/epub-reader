from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QScrollArea,
    QGridLayout,
    QFileDialog,
    QMessageBox,
    QFrame,
)

from epub.parser import EPUBParser
from reader.database import Database
from ui.book_card import BookCard


class LibraryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.database = Database()
        self.current_sort = "recent"

        self.setup_ui()
        self.load_library()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Page header
        header = QVBoxLayout()
        header.setSpacing(2)

        title = QLabel("MY LIBRARY")
        title.setObjectName("pageTitle")

        subtitle = QLabel("YOUR EPUB COLLECTION")
        subtitle.setObjectName("pageSubtitle")

        header.addWidget(title)
        header.addWidget(subtitle)

        layout.addLayout(header)

        # Toolbar
        toolbar = QHBoxLayout()

        toolbar.addStretch()

        # Sort dropdown
        sort_label = QLabel("Sort by:")

        self.sort_combo = QComboBox()

        self.sort_combo.addItem(
            "Recently Opened",
            "opened",
        )

        self.sort_combo.addItem(
            "Recently Added",
            "recent",
        )

        self.sort_combo.addItem(
            "Title",
            "title",
        )

        self.sort_combo.addItem(
            "Author",
            "author",
        )

        self.sort_combo.currentIndexChanged.connect(
            self.change_sort
        )

        toolbar.addWidget(sort_label)
        toolbar.addWidget(self.sort_combo)

        # Add book button
        add_button = QPushButton("+ Add Book")
        add_button.setObjectName("addBookButton")
        add_button.clicked.connect(
            self.add_book
        )

        toolbar.addWidget(add_button)

        layout.addLayout(toolbar)

        divider = QFrame()
        divider.setFrameShape(
            QFrame.Shape.HLine
        )
        divider.setObjectName("pageDivider")

        layout.addWidget(divider)

        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()

        self.book_grid = QGridLayout(
            scroll_content
        )

        self.book_grid.setSpacing(20)

        scroll_area.setWidget(
            scroll_content
        )

        layout.addWidget(scroll_area)

        status = QLabel("EPUB READER // LOCAL LIBRARY")
        status.setObjectName("statusLabel")

        layout.addWidget(status)

    def load_library(self):
        books = self.database.get_books(
            sort_by=self.current_sort
        )

        # Remove existing cards
        while self.book_grid.count():
            item = self.book_grid.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        # Add cards
        for index, book in enumerate(books):
            card = BookCard(book)

            card.clicked.connect(
                self.open_book
            )

            card.remove_clicked.connect(
                self.remove_book
            )

            row = index // 3
            column = index % 3

            self.book_grid.addWidget(
                card,
                row,
                column,
            )

    def add_book(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select EPUB",
            "",
            "EPUB files (*.epub)",
        )

        if not file_path:
            return

        try:
            parser = EPUBParser(file_path)
            book = parser.parse()

            self.database.add_book(
                title=book.title,
                author=book.author,
                path=book.path,
                cover=book.cover,
            )

            self.load_library()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Import Error",
                f"Could not import EPUB:\n\n{error}",
            )

    def open_book(self, book):
        window = self.window()

        epub_path = book["path"]

        self.database.mark_book_opened(
            book["id"]
        )

        parser = EPUBParser(epub_path)
        real_book = parser.parse()

        window.show_reader(real_book)

    def remove_book(self, book):
        self.database.delete_book(
            book["id"]
        )

        self.load_library()

    def change_sort(self, index):
        sort_value = self.sort_combo.itemData(
            index
        )

        self.current_sort = sort_value

        self.load_library()