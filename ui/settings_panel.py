from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from utils import translator


class SettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel(translator.t("sidebar", "settings").upper())
        title.setStyleSheet("font-size: 10px; color: #555; letter-spacing: 1px;")
        layout.addWidget(title)

        layout.addSpacing(24)

        placeholder = QLabel("Settings will be available in a future update.")
        placeholder.setStyleSheet("font-size: 13px; color: #555;")
        layout.addWidget(placeholder)

        layout.addStretch()