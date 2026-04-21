from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QIcon
from ui.main_window import MainWindow
from utils import translator
from pathlib import Path
import locale
import sys
import os

class HammerfyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self._load_language()
        self._load_styles()
        self._load_icon()
        self.window = MainWindow()
        self.window.show()

    def _load_icon(self):
        icon_path = Path(__file__).parent / "assets" / "icons" / "hammerfy-icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

    def _load_language(self):
        lang_code = locale.getdefaultlocale()[0] or "en"
        if lang_code.startswith("pt"):
            translator.load("ptbr")
        else:
            translator.load("en")

    def _load_styles(self):
        style_path = os.path.join(os.path.dirname(__file__), "styles", "dark.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())