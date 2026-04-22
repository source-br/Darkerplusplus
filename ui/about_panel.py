from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                                QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices
from pathlib import Path
import platform


LINKS = {
    "github":  "https://github.com/kenned-candido/darkerplusplus",
    "issues":  "https://github.com/kenned-candido/darkerplusplus/issues",
    "donate":  "https://ko-fi.com/",
    "docs":    "https://github.com/kenned-candido/darkerplusplus/wiki",
}

VERSION = "0.1.0"
AUTHOR  = "kenned-candido"
LICENSE = "GPL-3.0"


def get_os_name() -> str:
    system = platform.system()
    release = platform.release()
    if system == "Windows":
        version = platform.version()
        if "11" in version or int(release) >= 11 if release.isdigit() else False:
            return "Windows 11"
        return f"Windows {release}"
    elif system == "Linux":
        try:
            import distro
            return f"{distro.name()} {distro.version()}"
        except ImportError:
            return f"Linux {platform.release()}"
    elif system == "Darwin":
        return f"macOS {platform.mac_ver()[0]}"
    return system


class AboutPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_left())

        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("background-color: #242424; max-width: 1px;")
        root.addWidget(line)

        root.addWidget(self._build_right())

    def _build_left(self):
        widget = QWidget()
        widget.setObjectName("about_left")
        widget.setStyleSheet("QWidget#about_left { background-color: #141414; }")
        widget.setFixedWidth(340)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(48, 64, 48, 48)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        # Logo
        logo_path = Path(__file__).parent.parent / "assets" / "icons" / "hammerfy-logo.png"
        if logo_path.exists():
            logo = QLabel()
            pixmap = QPixmap(str(logo_path)).scaled(
                200, 46, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo.setPixmap(pixmap)
            logo.setStyleSheet("background: transparent;")
            layout.addWidget(logo)
        else:
            name = QLabel("Hammerfy")
            name.setStyleSheet("font-size: 22px; font-weight: 700; color: #f0f0f0; background: transparent;")
            layout.addWidget(name)

        layout.addSpacing(10)

        version = QLabel(f"v{VERSION}")
        version.setStyleSheet("font-size: 12px; color: #555; background: transparent;")
        layout.addWidget(version)

        layout.addSpacing(28)

        desc = QLabel(
            "A free and open-source manager\n"
            "for Hammer++, the map editor\n"
            "for Valve's Source Engine games."
        )
        desc.setStyleSheet("font-size: 13px; color: #666; background: transparent;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addStretch()

        badge = QLabel("Free & Open Source")
        badge.setStyleSheet("""
            background-color: #1a1a2e;
            color: #7c6be0;
            border: 1px solid #2a2a4a;
            border-radius: 4px;
            font-size: 11px;
            padding: 4px 10px;
        """)
        badge.setFixedHeight(26)
        badge.setFixedWidth(140)
        layout.addWidget(badge)

        return widget

    def _build_right(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(self._section_label("Info"))
        layout.addSpacing(12)
        layout.addWidget(self._info_row("Created by", AUTHOR))
        layout.addWidget(self._divider())
        layout.addWidget(self._info_row("Version", VERSION))
        layout.addWidget(self._divider())
        layout.addWidget(self._info_row("License", LICENSE))
        layout.addWidget(self._divider())
        layout.addWidget(self._info_row("Platform", get_os_name()))

        layout.addSpacing(40)

        layout.addWidget(self._section_label("Links"))
        layout.addSpacing(16)

        links = [
            ("GitHub",          "View source code and releases", LINKS["github"]),
            ("Report a bug",    "Open an issue on GitHub",       LINKS["issues"]),
            ("Documentation",   "Guides and wiki",               LINKS["docs"]),
            ("Support / Donate","Support the project on Ko-fi",  LINKS["donate"]),
        ]

        for title, subtitle, url in links:
            layout.addWidget(self._link_card(title, subtitle, url))
            layout.addSpacing(8)

        layout.addStretch()
        return widget

    def _section_label(self, text):
        lbl = QLabel(text.upper())
        lbl.setStyleSheet("font-size: 10px; color: #555; letter-spacing: 1.5px; background: transparent;")
        return lbl

    def _divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #1e1e1e; max-height: 1px; margin: 0px;")
        return line

    def _info_row(self, key, value):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 10)

        k = QLabel(key)
        k.setStyleSheet("font-size: 13px; color: #555; background: transparent;")
        k.setFixedWidth(110)

        v = QLabel(value)
        v.setStyleSheet("font-size: 13px; color: #e0e0e0; background: transparent;")

        layout.addWidget(k)
        layout.addWidget(v)
        layout.addStretch()
        return widget

    def _link_card(self, title, subtitle, url):
        btn = QPushButton()
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(58)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #181818;
                border: 1px solid #242424;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1e1a2e;
                border-color: #7c6be0;
            }
        """)

        inner = QHBoxLayout(btn)
        inner.setContentsMargins(16, 0, 16, 0)
        inner.setSpacing(0)

        text_col = QVBoxLayout()
        text_col.setSpacing(3)
        text_col.setAlignment(Qt.AlignVCenter)

        t = QLabel(title)
        t.setStyleSheet("font-size: 13px; color: #e0e0e0; background: transparent;")
        t.setAlignment(Qt.AlignVCenter)

        s = QLabel(subtitle)
        s.setStyleSheet("font-size: 11px; color: #555; background: transparent;")
        s.setAlignment(Qt.AlignVCenter)

        text_col.addWidget(t)
        text_col.addWidget(s)

        arrow = QLabel("→")
        arrow.setStyleSheet("font-size: 14px; color: #444; background: transparent;")
        arrow.setAlignment(Qt.AlignVCenter)

        inner.addLayout(text_col)
        inner.addStretch()
        inner.addWidget(arrow)

        btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
        return btn