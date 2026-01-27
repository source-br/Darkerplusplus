import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from src.app.windows.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
