from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QDialog
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from languages import translations, current_language
from utils import resource_path

class PopupWindow(QDialog):
    def __init__(self, background_color="#333", text_color="white"):
        super().__init__()

        # Define customizable colors
        self.background_color = background_color
        self.text_color = text_color

        # Set background and text style
        self.setStyleSheet(f"background-color: {self.background_color}; color: {self.text_color};")

        # Main layout of the popup
        popup_layout = QVBoxLayout()
        popup_layout.setContentsMargins(10, 10, 10, 10)
        popup_layout.setSpacing(10)
        popup_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Centered icon
        icon_label = QLabel()
        icon = QIcon(resource_path("Resources/images/SVG/dialog-warning.svg")) # Replace with your icon path
        icon_label.setPixmap(icon.pixmap(60, 60))  # Adjust icon size
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        popup_layout.addWidget(icon_label)

        # Title below the icon
        title_label = QLabel(translations[current_language]["atention"])
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {self.text_color};
                background: none;
                border: none;
            }}
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        popup_layout.addWidget(title_label)

        # Content paragraph
        content_label = QLabel(translations[current_language]["info"])
        content_label.setStyleSheet(f"""    
            QLabel {{
                font-size: 14px;
                color: {self.text_color};
                background: none;
                border: none;
                margin-top: 10px;
            }}
        """)
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        popup_layout.addWidget(content_label)

        # Layout for the button
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)  # Set small margins for the button
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # "Continue" button
        continue_button = QPushButton(translations[current_language]["continue"])
        continue_button.setStyleSheet(f"""
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
        continue_button.clicked.connect(self.accept)  # Close the popup when clicked
        button_layout.addWidget(continue_button)

        popup_layout.addLayout(button_layout)

        # Set the layout and window properties
        self.setLayout(popup_layout)
        self.setWindowTitle(translations[current_language]["atention"])
        self.setWindowIcon(QIcon(resource_path("Resources/images/SVG/dialog-warning.svg")))
        self.setFixedSize(300, 300)
        
class WelcomeInterface(QWidget):
    def __init__(self, background_color="#333", text_color="white"):
        super().__init__()

        # Define customizable colors
        self.background_color = background_color
        self.text_color = text_color

        # Set background and text style
        self.setStyleSheet(f"background-color: {self.background_color}; color: {self.text_color};")

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 25, 0, 0)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title
        welcome_label = QLabel(translations[current_language]["title 1"])
        welcome_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {self.text_color};
                background: none;
                border: none;
            }}
        """)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(welcome_label)

        # Subtitle
        subtitle_label = QLabel(translations[current_language]["subtitle 1"])
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                color: {self.text_color};
                background: none;
                border: none;
            }}
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)

        # Image
        image_label = QLabel()
        pixmap = QPixmap(resource_path("Resources/images/dazai.png"))
        pixmap = pixmap.scaled(900, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("margin: 0; padding: 0; background: none; ")
        main_layout.addWidget(image_label)

        # "Continue" button
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)  # Set small margins for the button
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.continue_button = QPushButton(translations[current_language]["continue"])
        self.continue_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #444;
                color: {self.text_color};
                padding: 10px 20px;
                border-radius: 15px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #555;
            }}
        """)
        self.continue_button.clicked.connect(self.open_popup)
        button_layout.addWidget(self.continue_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def open_popup(self):
        # Display the popup modally
        self.popup = PopupWindow(background_color=self.background_color, text_color=self.text_color)
        self.popup.exec()  # Displays the popup modally
