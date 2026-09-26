import sys

from PySide6.QtWidgets import QApplication

from app.window import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget {
            font-family: Arial;
            font-size: 14px;
        }

        QPushButton {
            padding: 10px;
        }
    """)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()