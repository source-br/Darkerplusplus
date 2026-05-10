from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtCore import QTimer
from ui.main_window import MainWindow
from utils import translator
from core import tray_settings
from pathlib import Path
import locale
import sys
import os


class HammerfyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)  # não sai ao fechar janela
        self._load_language()
        self._load_styles()
        self._load_icon()
        self.window = MainWindow()
        self._setup_tray()
        self._apply_start_behavior()
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
            self._icon = QIcon(str(icon_path))
            self.setWindowIcon(self._icon)
        else:
            self._icon = QIcon()

    def _setup_tray(self):
        self._tray = QSystemTrayIcon(self._icon, self)
        self._tray.setToolTip("Hammerfy")

        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #1e1e1e;
                border: 1px solid #2a2a2a;
                color: #c0c0c0;
                font-size: 12px;
                padding: 4px;
            }
            QMenu::item { padding: 6px 20px; border-radius: 4px; }
            QMenu::item:selected { background-color: #2a2a3a; color: white; }
            QMenu::separator { height: 1px; background: #2a2a2a; margin: 4px 0; }
        """)

        action_open = menu.addAction("Abrir Hammerfy")
        action_open.triggered.connect(self._show_window)
        menu.addSeparator()
        action_quit = menu.addAction("Sair")
        action_quit.triggered.connect(self._quit)

        self._tray.setContextMenu(menu)
        self._tray.activated.connect(self._on_tray_activated)

        # Conecta settings panel para atualizar comportamento ao mudar
        self.window.settings_panel.tray_setting_changed.connect(self._update_tray_visibility)
        self._update_tray_visibility()

        # Intercepta o closeEvent da janela
        self.window.closeEvent = self._on_window_close

    def _update_tray_visibility(self):
        settings = tray_settings.load()
        if settings["minimize_to_tray"] or tray_settings.get("minimize_to_tray"):
            self._tray.show()
        else:
            # Tray fica visível apenas se minimize_to_tray estiver ativo
            from core.autostart import is_autostart_enabled
            if is_autostart_enabled():
                self._tray.show()
            else:
                self._tray.hide()

    def _apply_start_behavior(self):
        settings = tray_settings.load()
        if settings.get("start_minimized") and settings.get("minimize_to_tray"):
            self._tray.show()
            # não mostra a janela
        else:
            self.window.show()

    def _on_window_close(self, event):
        settings = tray_settings.load()
        from core.autostart import is_autostart_enabled
        if settings.get("minimize_to_tray") or is_autostart_enabled():
            event.ignore()
            self.window.hide()
            self._tray.show()
        else:
            event.accept()
            self._quit()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self._show_window()

    def _show_window(self):
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def _quit(self):
        self._tray.hide()
        self.quit()

    def _start_update_checker(self):
        self._update_timer = QTimer()
        self._update_timer.setInterval(24 * 60 * 60 * 1000)
        self._update_timer.timeout.connect(self._check_updates)
        self._update_timer.start()

    def _check_updates(self):
        from ui.main_window import _build_tools_from_scan
        self.window._all_tools = _build_tools_from_scan()
        self.window._load_tools()