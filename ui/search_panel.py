from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return " ".join(self.text)

class SearchPanel(QWidget):
    result_selected = Signal(int)

    def __init__(self, chapters, parent=None):
        super().__init__(parent)

        self.chapters = chapters

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("SEARCH")
        layout.addWidget(title)

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search..."
        )

        self.search_input.returnPressed.connect(
            self.search
        )

        search_button = QPushButton("🔍")
        search_button.clicked.connect(
            self.search
        )

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        layout.addLayout(search_layout)

        self.result_count = QLabel(
            "0 results"
        )
        layout.addWidget(self.result_count)

        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(
            self.open_result
        )

        layout.addWidget(self.results_list)

        close_button = QPushButton("Close")
        close_button.clicked.connect(
            self.close
        )

        layout.addWidget(close_button)

        self.search_input.setFocus()

    def search(self):
        query = self.search_input.text().strip()

        self.results_list.clear()

        if not query:
            self.result_count.setText("0 results")
            return

        query_lower = query.lower()

        result_count = 0

        for index, chapter in enumerate(
            self.chapters
        ):
            extractor = TextExtractor()
            extractor.feed(chapter.content)

            text = extractor.get_text()

            if query_lower not in text.lower():
                continue

            snippet = self.create_snippet(
                text,
                query,
            )

            item = QListWidgetItem()

            item.setText(
                f"Chapter {index + 1}\n"
                f"\"{snippet}\""
            )

            item.setData(
                Qt.UserRole,
                index,
            )

            self.results_list.addItem(item)

            result_count += 1

        self.result_count.setText(
            f"{result_count} results"
        )

    def create_snippet(self, text, query):
        text_lower = text.lower()
        query_lower = query.lower()

        position = text_lower.find(
            query_lower
        )

        if position == -1:
            return ""

        start = max(
            0,
            position - 50,
        )

        end = min(
            len(text),
            position + len(query) + 80,
        )

        snippet = text[start:end]

        snippet = snippet.replace(
            "\n",
            " ",
        )

        return snippet.strip()

    def open_result(self, item):
        chapter_index = item.data(
            Qt.UserRole
        )

        self.result_selected.emit(
            chapter_index
        )