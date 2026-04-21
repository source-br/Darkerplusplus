from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import QUrl
from pathlib import Path
from utils import translator


LINKS = {
    "github":    "https://github.com/kenned-candido/darkerplusplus",
    "issues":    "https://github.com/kenned-candido/darkerplusplus/issues",
    "donate":    "https://ko-fi.com/",        # atualizar com link real
    "docs":      "https://github.com/kenned-candido/darkerplusplus/wiki",
}


class AboutPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        # Logo
        logo_path = Path(__file__).parent.parent / "assets" / "icons" / "hammerfy-logo.png"
        if logo_path.exists():
            logo = QLabel()
            pixmap = QPixmap(str(logo_path)).scaled(
                220, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo.setPixmap(pixmap)
            logo.setAlignment(Qt.AlignLeft)
            layout.addWidget(logo)

        layout.addSpacing(8)

        # Versão
        version = QLabel("v0.1")
        version.setStyleSheet("font-size: 13px; color: #555;")
        layout.addWidget(version)

        layout.addSpacing(32)

        # Descrição
        desc = QLabel(
            "Hammerfy is a free and open-source manager for Hammer++,\n"
            "the map editor for Valve's Source Engine games."
        )
        desc.setStyleSheet("font-size: 13px; color: #aaa; line-height: 1.6;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addSpacing(32)

        # Criador
        layout.addWidget(self._info_row("Created by", "kenned-candido"))
        layout.addWidget(self._info_row("License", "GLP-3.0"))
        layout.addWidget(self._info_row("Version", "0.1.0"))

        layout.addSpacing(32)

        # Links
        layout.addWidget(self._section_label("Links"))
        layout.addSpacing(8)
        layout.addWidget(self._link_btn("GitHub", LINKS["github"]))
        layout.addWidget(self._link_btn("Report a bug", LINKS["issues"]))
        layout.addWidget(self._link_btn("Documentation", LINKS["docs"]))
        layout.addWidget(self._link_btn("Support / Donate", LINKS["donate"]))

        layout.addStretch()

    def _section_label(self, text):
        lbl = QLabel(text.upper())
        lbl.setStyleSheet("font-size: 10px; color: #555; letter-spacing: 1px;")
        return lbl

    def _info_row(self, key, value):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 4, 0, 4)

        k = QLabel(key)
        k.setStyleSheet("font-size: 13px; color: #666;")
        k.setFixedWidth(120)

        v = QLabel(value)
        v.setStyleSheet("font-size: 13px; color: #e0e0e0;")

        layout.addWidget(k)
        layout.addWidget(v)
        layout.addStretch()
        return widget

    def _link_btn(self, text, url):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #7c6be0;
                font-size: 13px;
                text-align: left;
                padding: 4px 0;
            }
            QPushButton:hover { color: #9d8fe8; }
        """)
        btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
        return btn