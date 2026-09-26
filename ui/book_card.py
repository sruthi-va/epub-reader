from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QPushButton,
)


class BookCard(QFrame):
    clicked = Signal(object)
    remove_clicked = Signal(object)

    def __init__(self, book):
        super().__init__()

        self.book = book

        self.setFixedSize(160, 310)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        # Cover
        self.cover = QLabel("COVER")
        self.cover.setFixedSize(140, 200)
        self.cover.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # Title
        title = QLabel(book["title"])
        title.setObjectName("bookTitle")
        title.setWordWrap(True)
        title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        # Author
        author = QLabel(book["author"])
        author.setObjectName("bookAuthor")
        author.setWordWrap(True)
        author.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        # Remove button
        remove_button = QPushButton("REMOVE")
        remove_button.setObjectName("removeBookButton")
        remove_button.clicked.connect(
            self.remove_book
        )

        layout.addWidget(self.cover)

        layout.addSpacing(8)
        layout.addWidget(title)

        layout.addSpacing(2)
        layout.addWidget(author)

        layout.addSpacing(8)
        layout.addWidget(remove_button)

        self.setStyleSheet("""
            QFrame {
                background-color: #161620;
                border: 1px solid #252533;
                border-radius: 8px;
            }

            QFrame:hover {
                border: 1px solid #3f3f5c;
            }

            QLabel {
                background: transparent;
                border: none;
            }

            QPushButton {
                background-color: #1c1c28;
                border: 1px solid #303040;
                border-radius: 4px;

                color: #aaaabd;
                padding: 3px;
            }

            QPushButton:hover {
                background-color: #27273a;
                border: 1px solid #6666aa;
                color: #ffffff;
            }

            QPushButton:pressed {
                background-color: #303047;
            }
        """)

        # Cover hover effect
        self.cover.setStyleSheet("""
            QLabel {
                background-color: #303040;
                border: 1px solid #44445a;
                border-radius: 8px;
            }

            QLabel:hover {
                border: 1px solid #6666aa;
            }
        """)

    def remove_book(self):
        self.remove_clicked.emit(self.book)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.book)

        super().mousePressEvent(event)