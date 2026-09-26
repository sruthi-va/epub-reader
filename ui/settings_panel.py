from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QSlider,
    QButtonGroup,
    QRadioButton,
)


class SettingsPanel(QWidget):
    settings_changed = Signal()

    def __init__(self, settings, parent=None):
        super().__init__(parent)

        self.settings = settings

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("READER SETTINGS")
        layout.addWidget(title)

        # -------------------------
        # Font family
        # -------------------------

        layout.addWidget(QLabel("Font family"))

        self.font_combo = QComboBox()

        self.font_combo.addItems([
            "Georgia",
            "Arial",
            "Times New Roman",
            "Verdana",
            "Courier New",
        ])

        self.font_combo.setCurrentText(
            self.settings.font_family
        )

        self.font_combo.currentTextChanged.connect(
            self.change_font
        )

        layout.addWidget(self.font_combo)

        # -------------------------
        # Font size
        # -------------------------

        layout.addWidget(QLabel("Font size"))

        size_layout = QHBoxLayout()

        minus_button = QPushButton("−")
        minus_button.clicked.connect(
            self.decrease_font_size
        )

        self.size_label = QLabel(
            str(self.settings.font_size)
        )

        self.size_label.setMinimumWidth(40)

        plus_button = QPushButton("+")
        plus_button.clicked.connect(
            self.increase_font_size
        )

        size_layout.addWidget(minus_button)
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(plus_button)

        layout.addLayout(size_layout)

        # -------------------------
        # Line spacing
        # -------------------------

        layout.addWidget(QLabel("Line spacing"))

        self.spacing_slider = QSlider()

        self.spacing_slider.setOrientation(
            Qt.Horizontal
        )

        self.spacing_slider.setMinimum(10)
        self.spacing_slider.setMaximum(25)
        self.spacing_slider.setValue(
            int(self.settings.line_spacing * 10)
        )

        self.spacing_slider.valueChanged.connect(
            self.change_line_spacing
        )

        layout.addWidget(self.spacing_slider)

        # -------------------------
        # Text width
        # -------------------------

        layout.addWidget(QLabel("Text width"))

        self.width_slider = QSlider()

        self.width_slider.setOrientation(
            Qt.Horizontal
        )

        self.width_slider.setMinimum(500)
        self.width_slider.setMaximum(1000)
        self.width_slider.setValue(
            self.settings.text_width
        )

        self.width_slider.valueChanged.connect(
            self.change_text_width
        )

        layout.addWidget(self.width_slider)

        # -------------------------
        # Theme
        # -------------------------

        layout.addWidget(QLabel("Theme"))

        self.theme_group = QButtonGroup(self)

        light = QRadioButton("Light")
        sepia = QRadioButton("Sepia")
        dark = QRadioButton("Dark")

        self.theme_group.addButton(light)
        self.theme_group.addButton(sepia)
        self.theme_group.addButton(dark)

        light.clicked.connect(
            lambda: self.change_theme("light")
        )

        sepia.clicked.connect(
            lambda: self.change_theme("sepia")
        )

        dark.clicked.connect(
            lambda: self.change_theme("dark")
        )

        layout.addWidget(light)
        layout.addWidget(sepia)
        layout.addWidget(dark)

        if self.settings.theme == "light":
            light.setChecked(True)
        elif self.settings.theme == "sepia":
            sepia.setChecked(True)
        else:
            dark.setChecked(True)

        layout.addStretch()

    def change_font(self, font):
        self.settings.font_family = font
        self.settings_changed.emit()

    def decrease_font_size(self):
        if self.settings.font_size > 10:
            self.settings.font_size -= 1

            self.size_label.setText(
                str(self.settings.font_size)
            )

            self.settings_changed.emit()

    def increase_font_size(self):
        if self.settings.font_size < 40:
            self.settings.font_size += 1

            self.size_label.setText(
                str(self.settings.font_size)
            )

            self.settings_changed.emit()

    def change_line_spacing(self, value):
        self.settings.line_spacing = value / 10
        self.settings_changed.emit()

    def change_text_width(self, value):
        self.settings.text_width = value
        self.settings_changed.emit()

    def change_theme(self, theme):
        self.settings.theme = theme
        self.settings_changed.emit()