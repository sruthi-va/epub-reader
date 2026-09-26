from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QHBoxLayout,
)


class BookmarksPanel(QWidget):
    bookmark_selected = Signal(int, int)
    bookmark_deleted = Signal(int)

    def __init__(self, bookmarks, parent=None):
        super().__init__(parent)

        self.bookmarks = bookmarks

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("BOOKMARKS")
        layout.addWidget(title)

        self.bookmark_list = QListWidget()
        self.bookmark_list.itemDoubleClicked.connect(
            self.open_bookmark
        )

        layout.addWidget(self.bookmark_list)

        button_layout = QHBoxLayout()

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(
            self.delete_selected
        )

        close_button = QPushButton("Close")
        close_button.clicked.connect(
            self.close
        )

        button_layout.addWidget(delete_button)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

        self.populate_bookmarks()

    def populate_bookmarks(self):
        self.bookmark_list.clear()

        for bookmark in self.bookmarks:
            item = QListWidgetItem()

            chapter = bookmark["chapter"]
            label = bookmark["label"]

            item.setText(
                f"Chapter {chapter + 1}\n"
                f"\"{label}\""
            )

            item.setData(
                Qt.UserRole,
                bookmark,
            )

            self.bookmark_list.addItem(item)

    def open_bookmark(self, item):
        bookmark = item.data(Qt.UserRole)

        self.bookmark_selected.emit(
            bookmark["chapter"],
            bookmark["position"],
        )

    def delete_selected(self):
        item = self.bookmark_list.currentItem()

        if item is None:
            return

        bookmark = item.data(Qt.UserRole)

        self.bookmark_deleted.emit(
            bookmark["id"]
        )

        self.bookmark_list.takeItem(
            self.bookmark_list.row(item)
        )