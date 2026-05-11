from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap
from pathlib import Path
from models.tool import Tool, ToolStatus
from utils.icons import load_icon
from utils import translator


class ToolCard(QWidget):
    selected       = Signal(object)
    action_open    = Signal(object)
    action_folder  = Signal(object)
    action_install = Signal(object)
    action_update  = Signal(object)

    def __init__(self, tool: Tool, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.setFixedSize(165, 165)
        self.setCursor(Qt.PointingHandCursor)
        self._is_selected = False
        self._build_ui()
        self._apply_style()

    # ─── UI Construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 8)
        layout.setSpacing(6)

        self._banner_container = self._build_banner()

        version_text = "—" if self.tool.version_installed in (None, "unknown") else self.tool.version_installed

        self.lbl_name = QLabel(self.tool.name)
        self.lbl_name.setWordWrap(True)
        self.lbl_name.setStyleSheet("font-size: 11px; font-weight: 600; color: #e0e0e0;")

        self.lbl_version = QLabel(f"{version_text} · {self.tool.engine}")
        self.lbl_version.setStyleSheet("font-size: 10px; color: #555;")

        layout.addWidget(self._banner_container)
        layout.addWidget(self.lbl_name)
        layout.addWidget(self.lbl_version)
        layout.addWidget(self._build_actions())

    def _build_banner(self) -> QWidget:
        outer = QWidget()
        outer.setFixedHeight(95)
        self._banner_widget = outer

        banner_path = Path(__file__).parent.parent / "assets" / "banners" / f"{self.tool.id}.png"

        if banner_path.exists():
            self._banner_pixmap_orig = QPixmap(str(banner_path))
            self._banner_img = QLabel(outer)
            self._banner_img.setScaledContents(True)
            self._banner_img.setPixmap(self._banner_pixmap_orig)
            self._banner_img.setGeometry(0, 0, 165, 95)
            outer.setFixedWidth(165)
        else:
            self._banner_pixmap_orig = None
            self._banner_img = None
            outer.setStyleSheet(f"background-color: {self.tool.banner_color}; border-radius: 8px;")
            text = self.tool.id.upper()
            font_size = 14 if len(text) > 4 else 20
            lbl = QLabel(text, outer)
            lbl.setStyleSheet(f"font-size: {font_size}px; font-weight: 700; color: rgba(255,255,255,0.85);")
            lbl.move(8, 30)

        # Status badge overlaid on the top-right of the banner
        badge = self._build_status_badge()
        badge.setParent(outer)
        badge.move(0, 6)
        self._status_badge = badge

        return outer

    def _build_status_badge(self) -> QLabel:
        # (bg, fg, border) per status
        status_style = {
            ToolStatus.INSTALLED:        ("#1a3a1a", "#5ae87a", "#2a5a2a"),
            ToolStatus.UPDATE_AVAILABLE: ("#3a2a0a", "#e8b84a", "#5a4a1a"),
            ToolStatus.AVAILABLE:        ("#1a1a2a", "#666",    "#2a2a3a"),
            ToolStatus.NOT_AVAILABLE:    ("#1a1a1a", "#444",    "#222"),
        }
        status_key = {
            ToolStatus.INSTALLED:        "installed",
            ToolStatus.UPDATE_AVAILABLE: "update_available",
            ToolStatus.AVAILABLE:        "available",
            ToolStatus.NOT_AVAILABLE:    "not_available",
        }
        bg, fg, border = status_style[self.tool.status]
        badge = QLabel(translator.t("status", status_key[self.tool.status]))
        badge.setFixedHeight(16)
        badge.setStyleSheet(f"""
            background-color: {bg};
            color: {fg};
            border: 1px solid {border};
            border-radius: 3px;
            font-size: 9px;
            font-weight: 600;
            padding: 0px 5px;
        """)
        return badge

    def _build_actions(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        if self.tool.status == ToolStatus.INSTALLED:
            btn_open = self._btn(translator.t("card", "open"), primary=True)
            btn_open.clicked.connect(lambda: self.action_open.emit(self.tool))
            btn_folder = self._icon_btn("folder-open")
            btn_folder.clicked.connect(lambda: self.action_folder.emit(self.tool))
            # btn_settings hidden until phase 3
            layout.addWidget(btn_open)
            layout.addWidget(btn_folder)

        elif self.tool.status == ToolStatus.UPDATE_AVAILABLE:
            btn_update = self._btn(translator.t("card", "update"), accent="#8a6200")
            btn_update.clicked.connect(lambda: self.action_update.emit(self.tool))
            btn_folder = self._icon_btn("folder-open")
            btn_folder.clicked.connect(lambda: self.action_folder.emit(self.tool))
            layout.addWidget(btn_update)
            layout.addWidget(btn_folder)

        elif self.tool.status == ToolStatus.NOT_AVAILABLE:
            btn = self._btn(translator.t("status", "not_available"), muted=True)
            btn.setEnabled(False)
            layout.addWidget(btn)

        else:  # AVAILABLE
            btn_install = self._btn(translator.t("card", "install"), muted=True)
            btn_install.clicked.connect(lambda: self.action_install.emit(self.tool))
            layout.addWidget(btn_install)

        return widget

    # ─── Button Helpers ────────────────────────────────────────────────────────

    def _btn(self, text: str, primary=False, muted=False, accent: str | None = None) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(24)
        btn.setCursor(Qt.PointingHandCursor)

        if primary:
            btn.setStyleSheet("""
                QPushButton {
                    background: #7c6be0; border: none; border-radius: 5px;
                    font-size: 11px; color: white; padding: 0 8px;
                }
                QPushButton:hover { background: #6559c4; }
            """)
        elif muted:
            btn.setStyleSheet("""
                QPushButton {
                    background: #2a2a2a; border: 1px solid #444; border-radius: 5px;
                    font-size: 11px; color: #aaa; padding: 0 8px;
                }
                QPushButton:hover { background: #333; }
            """)
        elif accent:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {accent}; border: none; border-radius: 5px;
                    font-size: 11px; color: white; padding: 0 8px;
                }}
                QPushButton:hover {{ background: #6a4a00; }}
            """)
        return btn

    def _icon_btn(self, icon_name: str) -> QPushButton:
        """Small square icon-only button."""
        btn = QPushButton()
        btn.setFixedSize(36, 24)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setIcon(load_icon(icon_name, color="#666", size=14))
        btn.setIconSize(QSize(14, 14))
        btn.setStyleSheet("""
            QPushButton {
                background: transparent; border: 1px solid #333;
                border-radius: 5px; color: #666;
            }
            QPushButton:hover { background: #222; color: #aaa; }
        """)
        return btn

    # ─── State & Style ─────────────────────────────────────────────────────────

    def set_selected(self, selected: bool):
        self._is_selected = selected
        self._apply_style()

    def _apply_style(self):
        if self._is_selected:
            self.setStyleSheet("""
                ToolCard {
                    background: #1e1a2e;
                    border: 1px solid #7c6be0;
                    border-radius: 10px;
                }
            """)
        else:
            self.setStyleSheet("""
                ToolCard {
                    background: #1e1e1e;
                    border: 1px solid #2a2a2a;
                    border-radius: 10px;
                }
                ToolCard:hover {
                    background: #242424;
                    border-color: #333;
                }
            """)

    def mousePressEvent(self, event):
        self.selected.emit(self.tool)
        super().mousePressEvent(event)

    # ─── Layout Updates ────────────────────────────────────────────────────────

    def update_banner_size(self, card_width: int, banner_height: int):
        self._banner_widget.setFixedHeight(banner_height)
        self._banner_widget.setFixedWidth(card_width)

        if self._banner_img:
            self._banner_img.setGeometry(0, 0, card_width, banner_height)

        if hasattr(self, "_status_badge"):
            badge_w = self._status_badge.sizeHint().width()
            self._status_badge.move(card_width - badge_w - 6, 6)