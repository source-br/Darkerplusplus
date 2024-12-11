from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QGridLayout, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path

class GameSelectionInterface(QWidget):
    install_signal = pyqtSignal()

    def __init__(self, dll_manager, background_color="#333", text_color="white"):
        super().__init__()

        # Definir cores personalizáveis
        self.background_color = background_color
        self.text_color = text_color

        # Definir o estilo de fundo e texto
        self.setStyleSheet(f"background-color: {self.background_color}; color: {self.text_color};")
        self.dll_manager = dll_manager

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 25, 10, 10)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Título
        header_label = QLabel("JOGOS ENCONTRADOS")
        header_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {self.text_color};
                background: none;
                border: none;
            }}
        """)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        # Subtítulo
        sub_label = QLabel("Clique no jogo para selecionar sua pasta manualmente")
        sub_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                color: {self.text_color};
                background: none;
                border: none;
            }}
        """)
        sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(sub_label)

        # Layout para os jogos
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(30, 25, 30, 10)
        grid_layout.setSpacing(10)

        # Atualizar os caminhos detectados antes de construir a interface
        self.dll_manager.find_game_folders()

        self.game_widgets = {}
        for row, game in enumerate(self.dll_manager.game_paths.keys()):
            # Criar o botão estilizado com borda ao redor do nome do jogo
            game_button = self.create_game_button(game, game in self.dll_manager.found_game_paths)
            self.game_widgets[game] = game_button

            # Adicionar o botão ao layout de grade
            grid_layout.addWidget(game_button, row // 3, row % 3)

        # Adiciona um QSpacerItem antes e depois do grid para centralizar verticalmente
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        main_layout.addItem(spacer_top)
        main_layout.addLayout(grid_layout)
        main_layout.addItem(spacer_bottom)

        # Layout para o botão "Instalar"
        install_layout = QVBoxLayout()
        install_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        # Adiciona um item de espaço para empurrar o botão para baixo
        install_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        install_layout.addItem(install_spacer)

        # Botão "Instalar"
        install_button = QPushButton("Instalar")
        install_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #3584e4;
                color: {self.text_color};
                padding: 10px 20px;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #3584e4;
            }}
        """)
        install_button.clicked.connect(self.on_install_clicked)
        install_layout.addWidget(install_button)

        # Adicionar o layout de instalação ao layout principal
        main_layout.addLayout(install_layout)

        self.setLayout(main_layout)

    def create_game_button(self, game, is_found):
        # Cria um botão estilizado com borda ao redor do nome do jogo
        button = QPushButton(game)
        button.setStyleSheet(f"""
            QPushButton {{
                background: {self.background_color};
                border: 2px solid {'#4CAF50' if is_found else '#555'};
                color: {self.text_color};
                font-size: 14px;
                padding: 10px 15px;
                border-radius: 15px;
            }}
            QPushButton:hover {{
                border-color: {'#66BB6A' if is_found else '#777'};
                cursor: pointer;
            }}
        """)
        button.clicked.connect(lambda: self.select_game_path(game, button))
        return button

    def on_install_clicked(self):
        self.install_signal.emit()

    def select_game_path(self, game_name, button):
        selected_dir = QFileDialog.getExistingDirectory(self, f"Selecione o diretório do {game_name}")
        if selected_dir:
            path = Path(selected_dir)
            self.dll_manager.set_user_defined_path(game_name, selected_dir)

            # Verificar se o caminho selecionado é válido
            if game_name in self.dll_manager.found_game_paths:
                QMessageBox.information(self, "Caminho Atualizado", f"Caminho para {game_name} atualizado com sucesso.")
                # Alterar a borda do botão para verde quando o caminho é selecionado manualmente
                button.setStyleSheet(f"""
                    QPushButton {{
                        background: {self.background_color};
                        border: 2px solid #4CAF50;
                        color: {self.text_color};
                        font-size: 14px;
                        padding: 10px 15px;
                        border-radius: 15px;
                    }}
                    QPushButton:hover {{
                        border-color: #66BB6A;
                        cursor: pointer;
                    }}
                """)
            else:
                QMessageBox.warning(self, "Caminho Inválido", "O caminho selecionado não contém o jogo esperado.")
