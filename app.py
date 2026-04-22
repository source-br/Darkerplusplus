from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtCore import QTimer
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
        self._start_update_checker()

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

    def _load_icon(self):
        icon_path = Path(__file__).parent / "assets" / "icons" / "hammerfy-icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

    def _start_update_checker(self):
        """Checa updates a cada 24 horas em background."""
        self._update_timer = QTimer()
        self._update_timer.setInterval(24 * 60 * 60 * 1000)  # 24h em ms
        self._update_timer.timeout.connect(self._check_updates)
        self._update_timer.start()

    def _check_updates(self):
        self.window._all_tools = self.window._build_tools_from_scan()
        self.window._load_tools()