from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class BookCard(QFrame):
    clicked = Signal(object)

    def __init__(self, book):
        super().__init__()

        self.book = book

        self.setFixedWidth(160)

        layout = QVBoxLayout()

        cover = QLabel("COVER")
        cover.setFixedSize(140, 200)
        cover.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title = QLabel(book.title)
        title.setWordWrap(True)

        author = QLabel(book.author)
        author.setWordWrap(True)

        layout.addWidget(cover)
        layout.addWidget(title)
        layout.addWidget(author)

        self.setStyleSheet("""
            QFrame {
                background-color: #1c1c28;
                border: 1px solid #303040;
                border-radius: 8px;
            }

            QFrame:hover {
                border: 1px solid #6666aa;
            }

            QLabel {
                border: none;
            }
        """)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.book)

        super().mousePressEvent(event)