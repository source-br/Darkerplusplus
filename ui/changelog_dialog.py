from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from pathlib import Path


class ChangelogDialog(QDialog):
    """Modal dialog displayed after an update to show release notes / changelog."""

    def __init__(self, version: str, notes: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Hammerfy {version} — Novidades")
        self.setFixedSize(520, 420)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self._version = version
        self._notes = notes or "Esta versão inclui melhorias gerais e correções de bugs."

        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Header with Version Badge
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        title = QLabel(f"O que há de novo na {self._version}?")
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #f0f0f0; background: transparent;")

        badge = QLabel("NOVO")
        badge.setStyleSheet("""
            font-size: 10px;
            font-weight: 700;
            color: #121212;
            background-color: #e8b84a;
            border-radius: 4px;
            padding: 2px 6px;
        """)

        header_layout.addWidget(title)
        header_layout.addWidget(badge)
        header_layout.addStretch()

        # Body - Scrollable Text Browser with Markdown rendering
        body_browser = QTextBrowser()
        body_browser.setOpenExternalLinks(True)
        body_browser.setMarkdown(self._notes)
        body_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #16161a;
                border: 1px solid #2a2a38;
                border-radius: 8px;
                padding: 14px;
                color: #d0d0d0;
                font-size: 12px;
                line-height: 1.5;
            }
            QScrollBar:vertical {
                background: #16161a;
                width: 8px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #333344;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Footer Button
        footer_layout = QHBoxLayout()
        btn_close = QPushButton("Entendido!")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setFixedHeight(36)
        btn_close.setFixedWidth(120)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #7c6be0;
                color: #ffffff;
                font-size: 13px;
                font-weight: 600;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #6c5bd0;
            }
            QPushButton:pressed {
                background-color: #5c4bc0;
            }
        """)
        btn_close.clicked.connect(self.accept)

        footer_layout.addStretch()
        footer_layout.addWidget(btn_close)

        layout.addLayout(header_layout)
        layout.addWidget(body_browser)
        layout.addLayout(footer_layout)

    def _apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #121216;
            }
        """)
