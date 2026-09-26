from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QScrollArea,
)

from library.sample_books import SAMPLE_BOOKS
from ui.book_card import BookCard
from PySide6.QtCore import Qt

class LibraryPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Toolbar
        toolbar = QHBoxLayout()

        title = QLabel("MY LIBRARY")

        add_button = QPushButton("+ Add Book")

        add_button.clicked.connect(
            self.add_book_clicked
        )

        toolbar.addWidget(title)
        toolbar.addStretch()
        toolbar.addWidget(add_button)

        # Section title
        recently_added = QLabel("Recently Added")

        # Book grid
        book_grid = QGridLayout()

        for index, book in enumerate(SAMPLE_BOOKS):

            card = BookCard(book)

            row = index // 3
            column = index % 3

            book_grid.addWidget(
                card,
                row,
                column,
            )

        book_container = QWidget()
        book_container.setLayout(book_grid)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(book_container)

        main_layout.addLayout(toolbar)
        main_layout.addWidget(recently_added)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def show_empty_state(self):
        empty_label = QLabel(
            "Your library is empty.\n\n"
            "Add an EPUB to start reading."
        )

        empty_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

    def add_book_clicked(self):
        print("Add Book clicked!")