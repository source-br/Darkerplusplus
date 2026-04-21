from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal
from utils import translator
from pathlib import Path


class SidebarLogo(QWidget):
    """Apenas o logo — fica na topbar area."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(210)
        self.setFixedHeight(48)
        self.setObjectName("logo_area")
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(0)

        logo_path = Path(__file__).parent.parent / "assets" / "icons" / "hammerfy-logo.png"
        if logo_path.exists():
            from PySide6.QtGui import QPixmap
            img = QLabel()
            pixmap = QPixmap(str(logo_path)).scaled(
                160, 36,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            img.setPixmap(pixmap)
            img.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            layout.addWidget(img)
        else:
            name = QLabel("Hammerfy")
            name.setObjectName("logo_text")
            name.setStyleSheet("font-size: 15px; font-weight: 600; color: #f0f0f0;")
            layout.addWidget(name)

        layout.addStretch()
        version = QLabel("v0.1")
        version.setStyleSheet("font-size: 10px; color: #555;")
        layout.addWidget(version)


class Sidebar(QWidget):
    """Apenas a navegação — fica na área de conteúdo."""
    filter_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(210)
        self.setObjectName("sidebar")
        self._active_filter = "all"
        self._buttons = {}
        self._section_labels = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._build_nav())
        layout.addStretch()

    def _build_nav(self):
        nav = QWidget()
        layout = QVBoxLayout(nav)
        layout.setContentsMargins(8, 12, 8, 12)
        layout.setSpacing(2)

        layout.addWidget(self._nav_label(translator.t("sidebar", "library")))
        layout.addWidget(self._nav_btn("all",       translator.t("sidebar", "all_tools"),  "#7c6be0"))
        layout.addWidget(self._nav_btn("installed", translator.t("sidebar", "installed"),  "#3c9e3c"))
        layout.addWidget(self._nav_btn("available", translator.t("sidebar", "available"),  "#444"))
        layout.addWidget(self._nav_btn("updates",   translator.t("sidebar", "updates"),    "#e8b84a"))

        layout.addSpacing(8)
        layout.addWidget(self._nav_label(translator.t("sidebar", "system")))
        layout.addWidget(self._nav_btn("settings",  translator.t("sidebar", "settings"),   "#444"))

        return nav

    def _nav_label(self, text):
        label = QLabel(text.upper())
        label.setStyleSheet("font-size: 10px; color: #555; letter-spacing: 1px; padding: 4px 8px;")
        self._section_labels.append(label)
        return label

    def _nav_btn(self, filter_id, text, dot_color):
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setObjectName(f"nav_btn_{filter_id}")
        btn.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(btn)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        dot = QLabel()
        dot.setFixedSize(6, 6)
        dot.setStyleSheet(f"background-color: {dot_color}; border-radius: 3px;")

        label = QLabel(text)
        label.setStyleSheet("font-size: 13px;")

        layout.addWidget(dot)
        layout.addWidget(label)
        layout.addStretch()

        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 6px;
                text-align: left;
                color: #888;
            }
            QPushButton:hover { background: #222; color: #ccc; }
            QPushButton:checked { background: #2a2a2a; color: #f0f0f0; }
        """)

        btn.clicked.connect(lambda: self._on_filter(filter_id))
        self._buttons[filter_id] = btn

        if filter_id == "all":
            btn.setChecked(True)

        return btn

    def _on_filter(self, filter_id):
        for btn in self._buttons.values():
            btn.setChecked(False)
        self._buttons[filter_id].setChecked(True)
        self._active_filter = filter_id
        self.filter_changed.emit(filter_id)

    def refresh_text(self):
        keys = ["library", "system"]
        for i, label in enumerate(self._section_labels):
            if i < len(keys):
                label.setText(translator.t("sidebar", keys[i]).upper())

        labels = {
            "all":       translator.t("sidebar", "all_tools"),
            "installed": translator.t("sidebar", "installed"),
            "available": translator.t("sidebar", "available"),
            "updates":   translator.t("sidebar", "updates"),
            "settings":  translator.t("sidebar", "settings"),
        }
        for filter_id, btn in self._buttons.items():
            if filter_id in labels:
                for child in btn.findChildren(QLabel):
                    child.setText(labels[filter_id])