from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from ui.main_window import MainWindow
import sys
import os

class HammerfyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self._load_styles()
        self.window = MainWindow()
        self.window.show()

    def _load_styles(self):
        style_path = os.path.join(os.path.dirname(__file__), "styles", "dark.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())