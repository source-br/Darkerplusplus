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
        # Set the main window properties
        self.setWindowTitle("Hammerfy")
        self.setFixedSize(800, 500)
        self.setWindowIcon(QIcon(resource_path("Resources/images/icon.png")))

        # Detect the Windows version
        self.windows_version = self.detect_windows_version()

        # Set the application style and title bar
        self.set_application_style()
        self.set_dark_title_bar()

        # Initialize the DLL manager
        self.dll_manager = DllManager()

        self.dll_manager.find_game_folders()  # Initial search for games
        # Create and add screens to the stacked widget
        self.welcome_screen = WelcomeInterface()
        self.game_selection_screen = GameSelectionInterface(self.dll_manager)
        self.end_screen = EndScreenInterface()

        self.addWidget(self.welcome_screen)
        self.addWidget(self.game_selection_screen)
        self.addWidget(self.end_screen)

        # Connect signals and set the initial screen
        self.welcome_screen.continue_button.clicked.connect(self.show_game_selection)
        self.game_selection_screen.install_signal.connect(self.execute_installation)

        self.setCurrentWidget(self.welcome_screen)

    def detect_windows_version(self):
        # Detect the Windows version (e.g., '10', '11')
        release = platform.release()  # Obtains the Windows version (e.g., '10', '11')
        if release == "10":
            print("Detected system: Windows 10")
            return "Windows 10"
        elif release == "11":
            print("Detected system: Windows 11")
            return "Windows 11"
        else:
            print("Unsupported operating system.")
            return "Unknown"

    def set_application_style(self):
        # Set the application-wide stylesheet
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
        # Set the dark title bar palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        QApplication.setPalette(dark_palette)

    def show_game_selection(self):
        # Switch to the game selection screen
        self.setCurrentWidget(self.game_selection_screen)

    def execute_installation(self):
        # Execute the installation process
        selected_games = self.dll_manager.found_game_paths.keys()

        if not selected_games:
            QMessageBox.warning(
                self,
                translations[current_language]["no game"],
                translations[current_language]["please select"],
            )
            return

        try:
            # Replace DLLs
            self.dll_manager.replace_dlls()

            repository_path = ""  
            install_and_apply_theme(repository_path, self.windows_version)

            self.setCurrentWidget(self.end_screen)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred during installation:\n{str(e)}"
            )

if __name__ == "__main__":
    # Initialize and run the application
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())
