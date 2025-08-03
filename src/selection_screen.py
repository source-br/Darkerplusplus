from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QGridLayout, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path
from languages import translations, current_language

class GameSelectionInterface(QWidget):
    install_signal = pyqtSignal()

    def __init__(self, dll_manager, background_color="#333", text_color="white"):
        super().__init__()

        # Define customizable colors
        self.background_color = background_color
        self.text_color = text_color

        # Set background and text style
        self.setStyleSheet(f"background-color: {self.background_color}; color: {self.text_color};")
        self.dll_manager = dll_manager

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 25, 10, 10)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title
        header_label = QLabel(translations[current_language]["title 2"])
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

        # Subtitle
        sub_label = QLabel(translations[current_language]["subtitle 2"])
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

        # Layout for games
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(30, 25, 30, 10)
        grid_layout.setSpacing(10)

        # Update detected paths before building the interface
        self.dll_manager.find_game_folders()

        self.game_widgets = {}
        for row, game in enumerate(self.dll_manager.game_paths.keys()):
            # Create a styled button with a border around the game name
            game_button = self.create_game_button(game, game in self.dll_manager.found_game_paths)
            self.game_widgets[game] = game_button

            # Add the button to the grid layout
            grid_layout.addWidget(game_button, row // 3, row % 3)

        # Add a QSpacerItem before and after the grid to vertically center it
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        main_layout.addItem(spacer_top)
        main_layout.addLayout(grid_layout)
        main_layout.addItem(spacer_bottom)

        # Layout for the "Install" button
        install_layout = QVBoxLayout()
        install_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        # Add a spacer item to push the button down
        install_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        install_layout.addItem(install_spacer)

        # "Install" button
        install_button = QPushButton(translations[current_language]["install"])
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

        # Add the install layout to the main layout
        main_layout.addLayout(install_layout)

        self.setLayout(main_layout)

    def create_game_button(self, game, is_found):
        # Create a styled button with a border around the game name
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
        selected_dir = QFileDialog.getExistingDirectory(self, translations[current_language]["select"].format(game_name=game_name))
        if selected_dir:
            path = Path(selected_dir)
            self.dll_manager.set_user_defined_path(game_name, selected_dir)

            # Check if the selected path is valid
            if game_name in self.dll_manager.found_game_paths:
                QMessageBox.information(self, translations[current_language]["path"], translations[current_language]["path 2"].format(game_name=game_name))
                # Change the button border to green when the path is manually selected
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
                QMessageBox.warning(self, translations[current_language]["invalid"], translations[current_language]["invalid 2"])
