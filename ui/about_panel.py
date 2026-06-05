from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                                QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices
from pathlib import Path
import platform
from utils import translator


# ─── Constants ─────────────────────────────────────────────────────────────────

VERSION = "0.1.0"
AUTHOR  = "kenned-candido"
LICENSE = "GPL-3.0"

LINKS = {
    "github":  "https://github.com/kenned-candido/darkerplusplus",
    "issues":  "https://github.com/kenned-candido/darkerplusplus/issues",
    "docs":    "https://github.com/kenned-candido/darkerplusplus/wiki",
    "donate":  "",
}


# ─── Helpers ───────────────────────────────────────────────────────────────────

def _get_os_name() -> str:
    """Returns a human-readable OS name for the About panel."""
    system = platform.system()
    if system == "Windows":
        build = platform.version()
        return "Windows 11" if build.startswith("10.0.2") else f"Windows {platform.release()}"
    elif system == "Linux":
        try:
            import distro
            return distro.name(pretty=True)
        except ImportError:
            pass
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        return line.split("=")[1].strip().strip('"')
        except Exception:
            pass
        return "Linux"
    elif system == "Darwin":
        return f"macOS {platform.mac_ver()[0]}"
    return system


# ─── Panel ─────────────────────────────────────────────────────────────────────

class AboutPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_left())
        root.addWidget(self._vline())
        root.addWidget(self._build_right())

    # ─── Left Column ───────────────────────────────────────────────────────────

    def _build_left(self) -> QWidget:
        widget = QWidget()
        widget.setObjectName("about_left")
        widget.setStyleSheet("QWidget#about_left { background-color: #141414; }")
        widget.setFixedWidth(340)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(48, 64, 48, 48)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        logo_path = Path(__file__).parent.parent / "assets" / "icons" / "hammerfy-logo.svg"
        if logo_path.exists():
            logo = QLabel()
            pixmap = QPixmap(str(logo_path)).scaled(200, 46, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
            logo.setStyleSheet("background: transparent;")
            layout.addWidget(logo)
        else:
            name = QLabel("Hammerfy")
            name.setStyleSheet("font-size: 22px; font-weight: 700; color: #f0f0f0; background: transparent;")
            layout.addWidget(name)

        layout.addSpacing(28)

        self._desc_lbl = QLabel(translator.t("about", "description"))
        self._desc_lbl.setStyleSheet("font-size: 13px; color: #666; background: transparent;")
        self._desc_lbl.setWordWrap(True)
        layout.addWidget(self._desc_lbl)
        layout.addStretch()

        return widget

    # ─── Right Column ──────────────────────────────────────────────────────────

    def _build_right(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        # Info section
        self._section_info_lbl = self._section_label(translator.t("about", "section_info"))
        layout.addWidget(self._section_info_lbl)
        layout.addSpacing(12)

        # Store info row label widgets for refresh_text
        self._info_created_key, self._info_created_val = self._info_row(translator.t("about", "created_by"), AUTHOR)
        self._info_version_key, _                      = self._info_row(translator.t("about", "version"),    VERSION)
        self._info_license_key, _                      = self._info_row(translator.t("about", "license"),    LICENSE)
        self._info_platform_key, _                     = self._info_row(translator.t("about", "platform"),   _get_os_name())

        for key_lbl, val_lbl in [
            (self._info_created_key,  self._info_created_val),
            (self._info_version_key,  None),
            (self._info_license_key,  None),
            (self._info_platform_key, None),
        ]:
            row = self._make_row_widget(key_lbl, self._get_val_for_key(key_lbl))
            layout.addWidget(row)
            layout.addWidget(self._hline())

        layout.addSpacing(40)

        # Links section
        self._section_links_lbl = self._section_label(translator.t("about", "section_links"))
        layout.addWidget(self._section_links_lbl)
        layout.addSpacing(16)

        for title_key, url in [
            ("github_title",  LINKS["github"]),
            ("bug_title",     LINKS["issues"]),
            ("docs_title",    LINKS["docs"]),
            ("donate_title",  LINKS["donate"]),
        ]:
            layout.addWidget(self._link_card(translator.t("about", title_key), url))
            layout.addSpacing(8)

        layout.addStretch()
        return widget

    # ─── Public API ────────────────────────────────────────────────────────────

    def refresh_text(self):
        """Called when the UI language changes."""
        self._desc_lbl.setText(translator.t("about", "description"))
        self._section_info_lbl.setText(translator.t("about", "section_info").upper())
        self._section_links_lbl.setText(translator.t("about", "section_links").upper())
        self._info_created_key.setText(translator.t("about", "created_by"))
        self._info_version_key.setText(translator.t("about", "version"))
        self._info_license_key.setText(translator.t("about", "license"))
        self._info_platform_key.setText(translator.t("about", "platform"))

    # ─── Widget Builders ───────────────────────────────────────────────────────

    def _section_label(self, text: str) -> QLabel:
        lbl = QLabel(text.upper())
        lbl.setStyleSheet("font-size: 10px; color: #555; letter-spacing: 1.5px; background: transparent;")
        return lbl

    def _info_row(self, key: str, value: str) -> tuple[QLabel, QLabel]:
        """Returns (key_label, value_label) for external refresh access."""
        k = QLabel(key)
        k.setStyleSheet("font-size: 13px; color: #555; background: transparent;")
        k.setFixedWidth(110)

        v = QLabel(value)
        v.setStyleSheet("font-size: 13px; color: #e0e0e0; background: transparent;")

        return k, v

    def _get_val_for_key(self, key_lbl: QLabel) -> QLabel:
        """Helper to retrieve the matching value label for a key label."""
        mapping = {
            self._info_created_key:  QLabel(AUTHOR),
            self._info_version_key:  QLabel(VERSION),
            self._info_license_key:  QLabel(LICENSE),
            self._info_platform_key: QLabel(_get_os_name()),
        }
        lbl = mapping.get(key_lbl, QLabel(""))
        lbl.setStyleSheet("font-size: 13px; color: #e0e0e0; background: transparent;")
        return lbl

    def _make_row_widget(self, key_lbl: QLabel, val_lbl: QLabel) -> QWidget:
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.addWidget(key_lbl)
        layout.addWidget(val_lbl)
        layout.addStretch()
        return widget

    def _link_card(self, title: str, url: str) -> QPushButton:
        """Link card without subtitle — cleaner look."""
        btn = QPushButton()
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(48)
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

        t = QLabel(title)
        t.setStyleSheet("font-size: 13px; color: #e0e0e0; background: transparent;")
        t.setAlignment(Qt.AlignVCenter)

        arrow = QLabel("→")
        arrow.setStyleSheet("font-size: 14px; color: #444; background: transparent;")
        arrow.setAlignment(Qt.AlignVCenter)

        inner.addWidget(t)
        inner.addStretch()
        inner.addWidget(arrow)

        btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
        return btn

    def _vline(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("background-color: #242424; max-width: 1px;")
        return line

    def _hline(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #1e1e1e; max-height: 1px; margin: 0px;")
        return line