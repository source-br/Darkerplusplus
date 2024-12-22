import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from PyQt6.QtGui import QIcon, QPalette, QColor

from welcome_screen import WelcomeInterface
from selection_screen import GameSelectionInterface
from end_screen import EndScreenInterface
from dll_manager import DllManager
from theme_manager import install_and_apply_theme, execute_theme
from languages import translations, current_language

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darker++")
        self.setFixedSize(800, 500)
        self.setWindowIcon(QIcon("Data/imagens/icon.png"))

        # Definindo o estilo global para todo o aplicativo
        self.set_application_style()

        # Ajustando a barra de título do Windows para preto
        self.set_dark_title_bar()
        self.dll_manager = DllManager()

        # Inicializando as interfaces
        self.dll_manager.find_game_folders()  # Busca inicial pelos jogos
        self.welcome_screen = WelcomeInterface()
        self.game_selection_screen = GameSelectionInterface(self.dll_manager)
        self.end_screen = EndScreenInterface()  # Adicionando a tela de agradecimento

        # Adicionando telas ao QStackedWidget
        self.addWidget(self.welcome_screen)
        self.addWidget(self.game_selection_screen)
        self.addWidget(self.end_screen)

        # Conectando botões para navegação
        self.welcome_screen.continue_button.clicked.connect(self.show_game_selection)
        self.game_selection_screen.install_signal.connect(self.execute_installation)

        # Exibindo a tela inicial
        self.setCurrentWidget(self.welcome_screen)

    def set_application_style(self):
        # Estilo global para todos os widgets do aplicativo
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
        # Configurando uma paleta escura para a barra de título
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))  # Cor da barra de título
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))  # Texto do título
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
            # Substituir DLLs usando o DllManager
            self.dll_manager.replace_dlls()

            # Copiar e aplicar o tema
            repository_path = ""  # Substitua pelo caminho correto do repositório
            install_and_apply_theme(repository_path)

            # Exibir a tela de agradecimento após a instalação
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
