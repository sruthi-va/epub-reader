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
from reader.database import Database
from reader.settings import ReaderSettings
from reader.style import apply_reader_style
from ui.settings_panel import SettingsPanel
from PySide6.QtGui import QShortcut, QKeySequence
from ui.bookmarks_panel import BookmarksPanel

class ReaderPage(QWidget):
    def __init__(self, book, parent=None):
        super().__init__(parent)

        self.current_book = book
        self.current_chapter = 0
        self.current_position = 0

        self.settings = ReaderSettings()

        self.database = Database()

        self.book_id = self.database.add_book(
            title=self.current_book.title,
            author=self.current_book.author,
            path=self.current_book.path,
            cover=self.current_book.cover,
        )

        self.setup_ui()
        self.populate_contents()

        progress = self.database.get_progress(
            self.book_id
        )

        if progress is not None:
            self.current_chapter = progress["chapter"]
            self.current_position = progress["position"]

        self.load_chapter(self.current_chapter)

        self.bookmarks_panel = None
        self.bookmark_shortcut = QShortcut(
            QKeySequence("Ctrl+B"),
            self,
        )

        self.bookmark_shortcut.activated.connect(
            self.add_bookmark
        )

        

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        #-------------------------
        # Settings panel
        #-------------------------
        self.settings_panel = SettingsPanel(
            self.settings
        )

        self.settings_panel.setWindowTitle(
            "Reader Settings"
        )

        self.settings_panel.setMinimumWidth(300)

        self.settings_panel.settings_changed.connect(
            self.refresh_chapter
        )

        self.settings_panel.hide()

        # -------------------------
        # Top toolbar
        # -------------------------

        toolbar = QHBoxLayout()

        back_button = QPushButton("←")
        back_button.clicked.connect(self.go_back)

        title_label = QLabel(self.current_book.title)

        bookmarks_button = QPushButton("🔖")
        bookmarks_button.clicked.connect(
            self.show_bookmarks
        )

        settings_button = QPushButton("⚙")
        settings_button.clicked.connect(
            self.toggle_settings
        )

        toolbar.addWidget(back_button)
        toolbar.addWidget(title_label)
        toolbar.addStretch()
        toolbar.addWidget(bookmarks_button)
        toolbar.addWidget(settings_button)

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

        self.database.save_progress(
            book_id=self.book_id,
            chapter=self.current_chapter,
            position=self.current_position,
        )

        chapter = self.current_book.chapters[index]

        styled_content = apply_reader_style(
            chapter.content,
            self.settings,
        )

        self.web_view.setHtml(styled_content)

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

    def refresh_chapter(self):
        self.load_chapter(
            self.current_chapter
        )

    def toggle_settings(self):
        self.settings_panel.setVisible(
            not self.settings_panel.isVisible()
        )

    def get_current_position(self, callback):
        self.web_view.page().runJavaScript(
            "window.scrollY",
            callback,
        )

    def add_bookmark(self):
        def save_bookmark(position):
            if position is None:
                position = 0

            position = int(position)

            self.web_view.page().runJavaScript(
                """
                (() => {
                    const element = document.elementFromPoint(
                        window.innerWidth / 2,
                        100
                    );

                    return element
                        ? element.innerText
                        : "";
                })();
                """,
                lambda label: self.finish_bookmark(
                    position,
                    label,
                ),
            )

        self.get_current_position(save_bookmark)

    def finish_bookmark(self, position, label):
        if not label:
            label = "Current location"

        label = label.strip().replace(
            "\n",
            " ",
        )

        if len(label) > 80:
            label = label[:80] + "..."

        self.database.add_bookmark(
            self.book_id,
            self.current_chapter,
            position,
            label,
        )

        self.show_bookmarks()

    def show_bookmarks(self):
        bookmarks = self.database.get_bookmarks(
            self.book_id
        )

        if self.bookmarks_panel is not None:
            self.bookmarks_panel.close()

        self.bookmarks_panel = BookmarksPanel(
            bookmarks
        )

        self.bookmarks_panel.setWindowTitle(
            "Bookmarks"
        )

        self.bookmarks_panel.setMinimumSize(
            400,
            500,
        )

        self.bookmarks_panel.bookmark_selected.connect(
            self.go_to_bookmark
        )

        self.bookmarks_panel.bookmark_deleted.connect(
            self.delete_bookmark
        )

        self.bookmarks_panel.show()

    def go_to_bookmark(self, chapter, position):
        self.current_chapter = chapter

        self.update_navigation_buttons()
        self.contents.setCurrentRow(chapter)

        chapter_data = self.current_book.chapters[chapter]

        styled_content = apply_reader_style(
            chapter_data.content,
            self.settings,
        )

        self.bookmark_position = position

        try:
            self.web_view.loadFinished.disconnect(
                self.restore_bookmark_position
            )
        except RuntimeError:
            pass

        self.web_view.loadFinished.connect(
            self.restore_bookmark_position
        )

        self.web_view.setHtml(styled_content)

        self.database.save_progress(
            self.book_id,
            chapter,
            position,
        )

        if self.bookmarks_panel is not None:
            self.bookmarks_panel.close()


    def restore_bookmark_position(self, success):
        if not success:
            return

        position = self.bookmark_position

        self.web_view.page().runJavaScript(
            f"window.scrollTo(0, {position});"
        )

        try:
            self.web_view.loadFinished.disconnect(
                self.restore_bookmark_position
            )
        except RuntimeError:
            pass

    def delete_bookmark(self, bookmark_id):
        self.database.delete_bookmark(
            bookmark_id
        )

