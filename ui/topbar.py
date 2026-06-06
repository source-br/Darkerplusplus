from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from utils import translator


class Topbar(QWidget):
    search_changed   = Signal(str)
    language_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.setObjectName("topbar")
        self._current_lang = "en"
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(10)

        self.title_label = QLabel("All tools")
        self.title_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #f0f0f0;")

        self.count_label = QLabel("")
        self.count_label.setStyleSheet("font-size: 12px; color: #555;")

        layout.addWidget(self.title_label)
        layout.addWidget(self.count_label)
        layout.addStretch()

    def set_title(self, title_key: str, count: int | None = None):
        self.title_label.setText(translator.t("sidebar", title_key))
        if count is not None:
            self.count_label.setText(translator.t("topbar", "available_count", count=count))
        else:
            self.count_label.setText("")

    def refresh_text(self):
        """Called when the UI language changes."""
        pass