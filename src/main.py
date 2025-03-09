import sys
import os
import ctypes
import platform
from PyQt6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from PyQt6.QtGui import QIcon, QPalette, QColor

from welcome_screen import WelcomeInterface
from selection_screen import GameSelectionInterface
from end_screen import EndScreenInterface
from dll_manager import DllManager
from theme_manager import install_and_apply_theme
from languages import translations, current_language
from utils import resource_path

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darker++")
        self.setFixedSize(800, 500)
        self.setWindowIcon(QIcon(resource_path("Resources/images/icon.png")))

        self.windows_version = self.detect_windows_version()

        self.set_application_style()
        self.set_dark_title_bar()
        self.dll_manager = DllManager()

        self.dll_manager.find_game_folders()  # Busca inicial pelos jogos
        self.welcome_screen = WelcomeInterface()
        self.game_selection_screen = GameSelectionInterface(self.dll_manager)
        self.end_screen = EndScreenInterface()

        self.addWidget(self.welcome_screen)
        self.addWidget(self.game_selection_screen)
        self.addWidget(self.end_screen)

        self.welcome_screen.continue_button.clicked.connect(self.show_game_selection)
        self.game_selection_screen.install_signal.connect(self.execute_installation)

        self.setCurrentWidget(self.welcome_screen)

    def detect_windows_version(self):
        release = platform.release()  # Obtém a versão do Windows (ex.: '10', '11')
        if release == "10":
            print("Sistema detectado: Windows 10")
            return "Windows 10"
        elif release == "11":
            print("Sistema detectado: Windows 11")
            return "Windows 11"
        else:
            print("Sistema operacional não suportado.")
            return "Desconhecido"

    def set_application_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
            }
            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QLabel {
                font-size: 18px;
                color: white;
            }
        """)

    def set_dark_title_bar(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        QApplication.setPalette(dark_palette)

    def show_game_selection(self):
        self.setCurrentWidget(self.game_selection_screen)

    def execute_installation(self):
        selected_games = self.dll_manager.found_game_paths.keys()

        if not selected_games:
            QMessageBox.warning(
                self,
                translations[current_language]["no game"],
                translations[current_language]["please select"],
            )
            return

        try:
            # Substituir DLLs
            self.dll_manager.replace_dlls()

            repository_path = ""  
            install_and_apply_theme(repository_path, self.windows_version)

            self.setCurrentWidget(self.end_screen)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Ocorreu um erro durante a instalação:\n{str(e)}"
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())
