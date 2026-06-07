from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, QThread, Signal as QSignal
from ui.main_window import MainWindow
from utils import translator
from core import tray_settings
from core.autostart import is_autostart_enabled
from pathlib import Path
import locale
import sys
import os


# ─── App Update Worker ─────────────────────────────────────────────────────────

class AppUpdateWorker(QThread):
    """Checks GitHub Releases for a new Hammerfy version in the background."""
    update_available = QSignal(str, str)  # (latest_version, download_url)

    def run(self):
        from core.app_updater import check_for_update
        has_update, version, url = check_for_update()
        if has_update and url:
            self.update_available.emit(version, url)


# ─── Application ───────────────────────────────────────────────────────────────

class HammerfyApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)
        self._load_language()
        self._load_styles()
        self._load_icon()
        self.window = MainWindow()
        self._setup_tray()
        self._apply_start_behavior()
        self._start_update_checker()

    # ─── Initialization ────────────────────────────────────────────────────────

    def _load_language(self):
        """Loads saved language preference, falls back to OS detection, then English."""
        from core import tray_settings
        saved_lang = tray_settings.get("language")
        if saved_lang:
            translator.load(saved_lang)
            return
        # Auto-detect from OS locale
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
        icon_path = Path(__file__).parent / "assets" / "icons" / "hammerfy-icon.svg"
        if icon_path.exists():
            self._icon = QIcon(str(icon_path))
            self.setWindowIcon(self._icon)
        else:
            self._icon = QIcon()

    # ─── System Tray ───────────────────────────────────────────────────────────

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
        self._tray.show()

        # Intercept window close to minimize to tray instead of quitting
        self.window.closeEvent = self._on_window_close

        # Connect settings panel language change signal
        self.window.settings_panel.language_changed.connect(self.window._on_language)

    def _apply_start_behavior(self):
        settings = tray_settings.load()
        if settings.get("start_minimized") and settings.get("minimize_to_tray"):
            pass  # stay in tray, don't show window
        else:
            self.window.show()

    def _on_window_close(self, event):
        settings = tray_settings.load()
        if settings.get("minimize_to_tray") or is_autostart_enabled():
            event.ignore()
            self.window.hide()
        else:
            event.accept()
            self._quit()

    def _on_tray_activated(self, reason):
        if reason in (QSystemTrayIcon.DoubleClick, QSystemTrayIcon.Trigger):
            self._show_window()

    def _show_window(self):
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def _quit(self):
        self._tray.hide()
        self.quit()

    # ─── App Update Checker ────────────────────────────────────────────────────

    def _start_update_checker(self):
        """Checks for a new Hammerfy version once at startup and every 24h."""
        self._run_update_check()

        self._update_timer = QTimer()
        self._update_timer.setInterval(24 * 60 * 60 * 1000)
        self._update_timer.timeout.connect(self._run_update_check)
        self._update_timer.start()

    def _run_update_check(self):
        self._app_update_worker = AppUpdateWorker()
        self._app_update_worker.update_available.connect(self._on_update_available)
        self._app_update_worker.start()

    def _on_update_available(self, version: str, url: str):
        reply = QMessageBox.question(
            self.window,
            "Atualização disponível",
            f"Uma nova versão do Hammerfy está disponível: {version}\n\nDeseja baixar e instalar agora?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        from core.app_updater import download_and_run_installer
        success = download_and_run_installer(url, version)
        if success:
            # Installer is running — quit the app so it can replace the exe
            self._quit()
        else:
            QMessageBox.warning(
                self.window,
                "Hammerfy",
                "Não foi possível baixar a atualização. Verifique sua conexão."
            )