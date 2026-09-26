from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EPUB Reader")
        self.resize(1000, 700)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        library_title = QLabel("MY LIBRARY")
        library_button = QPushButton("Library")
        favorites_button = QPushButton("Favorites")
        settings_button = QPushButton("Settings")

        sidebar_layout.addWidget(library_title)
        sidebar_layout.addWidget(library_button)
        sidebar_layout.addWidget(favorites_button)
        sidebar_layout.addWidget(settings_button)
        sidebar_layout.addStretch()

        sidebar.setLayout(sidebar_layout)

        # Main content
        content = QWidget()
        content_layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to your EPUB Reader")

        description_label = QLabel(
            "Your books will appear here."
        )

        add_button = QPushButton("Add Your First Book")

        add_button.clicked.connect(
            lambda: description_label.setText(
                "Your library is empty. Add an EPUB to get started!"
            )
        )

        content_layout.addStretch()
        content_layout.addWidget(welcome_label)
        content_layout.addWidget(description_label)
        content_layout.addWidget(add_button)
        content_layout.addStretch()

        content.setLayout(content_layout)

        # Main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content, 1)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)