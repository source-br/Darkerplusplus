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

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search tools...")
        self.search.setFixedWidth(180)
        self.search.setFixedHeight(30)
        self.search.textChanged.connect(self.search_changed.emit)

        self.btn_lang = QPushButton("EN")
        self.btn_lang.setObjectName("topbar_btn")
        self.btn_lang.setFixedSize(38, 30)
        self.btn_lang.setCursor(Qt.PointingHandCursor)
        self.btn_lang.setToolTip("Toggle language")
        self.btn_lang.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #2a2a2a;
                border-radius: 6px;
                font-size: 11px;
                color: #aaa;
            }
            QPushButton:hover { background: #222; color: #e0e0e0; }
        """)
        self.btn_lang.clicked.connect(self._on_language)

        layout.addWidget(self.title_label)
        layout.addWidget(self.count_label)
        layout.addStretch()
        layout.addWidget(self.search)
        layout.addWidget(self.btn_lang)

    def set_title(self, title, count=None):
        self.title_label.setText(title)
        self.count_label.setText(f"{count} available" if count is not None else "")

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