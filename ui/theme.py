APP_STYLESHEET = """
/* ================================
   GLOBAL
   ================================ */

QWidget {
    background-color: #101018;
    color: #e8e8f0;
    font-family: Arial;
    font-size: 14px;
}

QLabel#pageTitle {
    color: #f0f0f8;
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 2px;
}

/* ================================
   MAIN WINDOW
   ================================ */

QMainWindow {
    background-color: #101018;
}


/* ================================
   LABELS
   ================================ */

QLabel {
    color: #e8e8f0;
    background: transparent;
}


/* ================================
   BUTTONS
   ================================ */

QPushButton {
    background-color: #1c1c28;
    color: #e8e8f0;

    border: 1px solid #38384a;
    border-radius: 6px;

    padding: 7px 12px;
}

QPushButton:hover {
    background-color: #27273a;
    border: 1px solid #6666aa;
}

QPushButton#addBookButton {
    background-color: #26263a;
    border: 1px solid #55557a;
    color: #f0f0ff;
}

QPushButton#addBookButton:hover {
    background-color: #33334d;
    border: 1px solid #7777aa;
}

QListWidget#contentsList {
    background-color: #12121a;
    border: none;
    border-right: 1px solid #292938;
    border-radius: 0px;
}

QLabel#pageSubtitle {
    color: #66667d;
    font-size: 10px;
    font-weight: bold;
}

QFrame#pageDivider {
    color: #292938;
    background-color: #292938;
    max-height: 1px;
}

QLabel#bookTitle {
    color: #eeeeF5;
    font-size: 13px;
    font-weight: bold;
}

QLabel#bookAuthor {
    color: #77778d;
    font-size: 11px;
}

QPushButton#removeButton {
    background-color: transparent;
    border: none;
    color: #555565;
    font-size: 10px;
    padding: 2px;
}

QPushButton#removeButton:hover {
    background-color: #241c28;
    border: none;
    color: #b88aa8;
}

QWidget#settingsPanel {
    background-color: #161620;
}

QFrame#readerToolbar {
    background-color: #14141d;
    border-bottom: 1px solid #292938;
}

QLabel#readerTitle {
    color: #e8e8f0;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#backButton {
    background-color: transparent;
    border: none;
    color: #88889d;
    font-size: 18px;
    padding: 4px 8px;
}

QPushButton#backButton:hover {
    background-color: #222231;
    color: #ffffff;
}

QListWidget#contentsList {
    background-color: #12121a;
    border: none;
    border-right: 1px solid #292938;
    border-radius: 0px;

    padding: 12px 8px;
}

QListWidget#contentsList::item {
    color: #77778d;
    padding: 9px 8px;
    border-radius: 4px;
}

QListWidget#contentsList::item:hover {
    background-color: #1e1e2b;
    color: #c8c8d8;
}

QListWidget#contentsList::item:selected {
    background-color: #28283b;
    color: #ffffff;

    border-left: 2px solid #6666aa;
}

QPushButton#chapterNavigation {
    background-color: transparent;
    border: none;
    color: #77778d;
    padding: 6px 10px;
}

QPushButton#chapterNavigation:hover {
    color: #eeeeF5;
    background-color: #1c1c28;
}

QPushButton#chapterNavigation:disabled {
    color: #3f3f4d;
    background-color: transparent;
}

QLabel#panelTitle {
    color: #eeeeF5;
    font-size: 16px;
    font-weight: bold;
}

QLabel#statusLabel {
    color: #454557;
    font-size: 9px;
}

QSlider::groove:horizontal {
    height: 4px;
    background: #292938;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    width: 12px;
    margin: -4px 0;
    background: #6666aa;
    border-radius: 6px;
}

QWidget {
    selection-background-color: #303047;
    selection-color: #ffffff;
}

QLineEdit {
    background-color: #161620;
    color: #e8e8f0;

    border: 1px solid #38384a;
    border-radius: 5px;

    padding: 7px;
}

QLineEdit:focus {
    border: 1px solid #6666aa;
}

QPushButton:pressed {
    background-color: #303047;
}

QPushButton:disabled {
    color: #555565;
    background-color: #15151d;
    border: 1px solid #252532;
}


/* ================================
   COMBO BOX
   ================================ */

QComboBox {
    background-color: #1c1c28;
    color: #e8e8f0;

    border: 1px solid #38384a;
    border-radius: 6px;

    padding: 7px 10px;
}

QComboBox:hover {
    border: 1px solid #6666aa;
}

QComboBox::drop-down {
    border: none;
    width: 28px;
}

QComboBox QAbstractItemView {
    background-color: #1c1c28;
    color: #e8e8f0;

    border: 1px solid #38384a;
    selection-background-color: #303047;
}


/* ================================
   LISTS
   ================================ */

QListWidget {
    background-color: #15151f;
    color: #dcdce8;

    border: 1px solid #2d2d3c;
    border-radius: 6px;

    padding: 5px;
}

QListWidget::item {
    padding: 8px;
    border-radius: 4px;
}

QListWidget::item:hover {
    background-color: #1e1e2b;
}

QListWidget::item:selected {
    background-color: #28283b;
    color: #ffffff;

    border-left: 2px solid #6666aa;
}


/* ================================
   SCROLL AREAS
   ================================ */

QScrollArea {
    background-color: #101018;
    border: none;
}


/* ================================
   SCROLLBARS
   ================================ */

QScrollBar:vertical {
    background: #101018;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #38384a;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #6666aa;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: #101018;
    height: 10px;
}

QScrollBar::handle:horizontal {
    background: #38384a;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background: #6666aa;
}


/* ================================
   FRAMES
   ================================ */

QFrame {
    background-color: transparent;
}
"""