from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt, Signal, QSize
from utils.icons import load_icon
from utils import translator


class Topbar(QWidget):
    search_changed = Signal(str)
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

    def set_title(self, title_key, count=None):
        self.title_label.setText(translator.t("sidebar", title_key))
        if count is not None:
            self.count_label.setText(translator.t("topbar", "available_count", count=count))
        else:
            self.count_label.setText("")

    def _on_language(self):
        self._current_lang = "ptbr" if self._current_lang == "en" else "en"
        self.btn_lang.setText("PT" if self._current_lang == "ptbr" else "EN")
        self.language_changed.emit(self._current_lang)

    def refresh_text(self):
        self.search.setPlaceholderText(translator.t("topbar", "search_placeholder"))
        if self._current_lang == "ptbr":
            self.btn_lang.setText("PT")
        else:
            self.btn_lang.setText("EN")