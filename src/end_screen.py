from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPainter, QPixmap
from languages import translations, current_language

class EndScreenInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #333; color: white;")

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 25, 0, 0)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Renderizando a imagem SVG
        self.svg_renderer = QSvgRenderer("Resources/images/SVG/done-icon.svg")
        self.svg_pixmap = QPixmap(100, 100)
        self.svg_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(self.svg_pixmap)
        self.svg_renderer.render(painter)
        painter.end()

        # Imagem SVG (ícone de sucesso) em QPixmap
        image_label = QLabel()
        image_label.setPixmap(self.svg_pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("margin: 0; padding: 0; background: none; ")
        main_layout.addWidget(image_label)

        # Título
        title_label = QLabel(translations[current_language]["title 3"])
        title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: white;
                background: none;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Subtítulo
        subtitle_label = QLabel(translations[current_language]["subtitle 3"])
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: white;
                background: none;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)

        # Botão de fechar
        self.close_button = QPushButton(translations[current_language]["close"])
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                padding: 10px 20px;
                border-radius: 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.close_button.clicked.connect(self.close_application)
        main_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def close_application(self):
        QApplication.quit()
