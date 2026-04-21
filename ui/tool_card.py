from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from models.tool import Tool, ToolStatus
from pathlib import Path
from utils.icons import load_icon
from PySide6.QtCore import QSize
from utils import translator


class ToolCard(QWidget):
    selected = Signal(object)
    action_open = Signal(object)
    action_folder = Signal(object)
    action_install = Signal(object)
    action_update = Signal(object)

    def __init__(self, tool: Tool, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.setFixedSize(165, 165)
        self.setCursor(Qt.PointingHandCursor)
        self._is_selected = False
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        self._banner_container = self._build_banner()
        layout.addWidget(self._banner_container)

        self.lbl_name = QLabel(self.tool.name)
        self.lbl_name.setObjectName("card_name")
        self.lbl_name.setWordWrap(True)
        self.lbl_name.setStyleSheet("font-size: 11px; font-weight: 600; color: #e0e0e0;")

        version_text = self.tool.version_installed or "—"
        self.lbl_version = QLabel(f"{version_text} · {self.tool.engine}")
        self.lbl_version.setObjectName("card_version")
        self.lbl_version.setStyleSheet("font-size: 10px; color: #555;")

        layout.addWidget(self.lbl_name)
        layout.addWidget(self.lbl_version)
        layout.addStretch()
        layout.addWidget(self._build_actions())

    def _build_banner(self):
        banner = QWidget()
        banner.setFixedHeight(95)
        banner.setObjectName("card_banner")
        banner.setStyleSheet("border-radius: 8px;")
        self._banner_widget = banner

        b_layout = QHBoxLayout(banner)
        b_layout.setContentsMargins(0, 0, 0, 0)

        # Tenta carregar imagem do jogo
        banner_path = Path(__file__).parent.parent / "assets" / "banners" / f"{self.tool.id}.png"
        if banner_path.exists():
            from PySide6.QtGui import QPixmap
            img = QLabel()
            img.setFixedSize(165, 75)
            img.setAlignment(Qt.AlignCenter)
            pixmap = QPixmap(str(banner_path)).scaled(
                165, 75,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            img.setPixmap(pixmap)
            img.setFixedSize(165, 95)
            img.setStyleSheet(f"background-color: {self.tool.banner_color}; border-radius: 5px;")
            self._banner_img = img
            b_layout.addWidget(img)
        else:
            self._banner_img = None
            banner.setStyleSheet(f"background-color: {self.tool.banner_color}; border-radius: 5px;")
            text = self.tool.id.upper()
            font_size = 14 if len(text) > 4 else 20
            label = QLabel(text)
            label.setStyleSheet(f"font-size: {font_size}px; font-weight: 700; color: rgba(255,255,255,0.85);")
            b_layout.addWidget(label)

        # Badge de status sempre por cima
        status_badge = self._build_status_badge()
        b_layout.addStretch()
        b_layout.addWidget(status_badge, alignment=Qt.AlignTop | Qt.AlignRight)

        return banner

    def _build_status_badge(self):
        badge = QLabel()
        badge.setFixedHeight(16)

        status_keys = {
            ToolStatus.INSTALLED:        ("status", "installed",       "#1a3a1a", "#5ae87a", "#2a5a2a"),
            ToolStatus.UPDATE_AVAILABLE: ("status", "update_available","#3a2a0a", "#e8b84a", "#5a4a1a"),
            ToolStatus.AVAILABLE:        ("status", "available",       "#1a1a2a", "#666",    "#2a2a3a"),
        }

        section, key, bg, fg, border = status_keys[self.tool.status]
        text = translator.t(section, key)
        badge.setText(text)
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

    def _build_actions(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        if self.tool.status == ToolStatus.INSTALLED:
            btn_main = self._btn(translator.t("card", "open"), primary=True)
            btn_main.clicked.connect(lambda: self.action_open.emit(self.tool))
            btn_folder = self._btn("", icon=True, icon_name="folder-open")
            btn_folder.clicked.connect(lambda: self.action_folder.emit(self.tool))
            btn_settings = self._btn("", icon=True, icon_name="settings")
            layout.addWidget(btn_main)
            layout.addWidget(btn_folder)
            layout.addWidget(btn_settings)

        elif self.tool.status == ToolStatus.UPDATE_AVAILABLE:
            btn_main = self._btn(translator.t("card", "update"), accent="#8a6200")
            btn_main.clicked.connect(lambda: self.action_update.emit(self.tool))
            btn_folder = self._btn("...", icon=True)
            btn_folder.clicked.connect(lambda: self.action_folder.emit(self.tool))
            layout.addWidget(btn_main)
            layout.addWidget(btn_folder)

        else:
            btn_main = self._btn(translator.t("card", "install"), muted=True)
            btn_main.clicked.connect(lambda: self.action_install.emit(self.tool))
            layout.addWidget(btn_main)

        return widget

    def _btn(self, text, primary=False, icon=False, muted=False, accent=None, icon_name=None):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)

        if icon_name:
            color = "white" if primary else "#666"
            btn.setIcon(load_icon(icon_name, color=color, size=14))
            btn.setIconSize(QSize(14, 14))

        if icon:
            btn.setFixedSize(36, 24)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: 1px solid #333;
                    border-radius: 5px;
                    font-size: 10px;
                    color: #666;
                }
                QPushButton:hover { background: #222; color: #aaa; }
            """)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: 1px solid #333;
                    border-radius: 5px;
                    font-size: 11px;
                    color: #666;
                }
                QPushButton:hover { background: #222; color: #aaa; }
            """)
        elif primary:
            btn.setFixedHeight(24)
            btn.setSizePolicy(btn.sizePolicy().horizontalPolicy(), btn.sizePolicy().verticalPolicy())
            btn.setStyleSheet("""
                QPushButton {
                    background: #7c6be0;
                    border: none;
                    border-radius: 5px;
                    font-size: 11px;
                    color: white;
                    padding: 0 8px;
                }
                QPushButton:hover { background: #6559c4; }
            """)
        elif muted:
            btn.setFixedHeight(24)
            btn.setStyleSheet("""
                QPushButton {
                    background: #2a2a2a;
                    border: 1px solid #444;
                    border-radius: 5px;
                    font-size: 11px;
                    color: #aaa;
                    padding: 0 8px;
                }
                QPushButton:hover { background: #333; }
            """)
        elif accent:
            btn.setFixedHeight(24)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {accent};
                    border: none;
                    border-radius: 5px;
                    font-size: 11px;
                    color: white;
                    padding: 0 8px;
                }}
                QPushButton:hover {{ background: #6a4a00; }}
            """)

        return btn

    def set_selected(self, selected: bool):
        self._is_selected = selected
        self._apply_style()

    def _apply_style(self):
        if self._is_selected:
            self.setStyleSheet("""
                ToolCard {
                    background: #271e17;
                    border: 1px solid #7c6be0;
                    border-radius: 8px;
                }
            """)
        else:
            self.setStyleSheet("""
                ToolCard {
                    background: #222;
                    border: 1px solid #2a2a2a;
                    border-radius: 8px;
                }
                ToolCard:hover {
                    background: #272727;
                    border-color: #333;
                }
            """)

    def mousePressEvent(self, event):
        self.selected.emit(self.tool)
        super().mousePressEvent(event)

    def update_banner_size(self, card_width: int, banner_height: int):
        """Atualiza o tamanho do banner dinamicamente."""
        self._banner_widget.setFixedHeight(banner_height)
        if hasattr(self, '_banner_img') and self._banner_img:
            from pathlib import Path
            from PySide6.QtGui import QPixmap
            banner_path = Path(__file__).parent.parent / "assets" / "banners" / f"{self.tool.id}.png"
            if banner_path.exists():
                pixmap = QPixmap(str(banner_path)).scaled(
                    card_width, banner_height,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self._banner_img.setPixmap(pixmap)
                self._banner_img.setFixedSize(card_width, banner_height)