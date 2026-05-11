from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap
from pathlib import Path
from models.tool import Tool, ToolStatus
from utils.icons import load_icon
from utils import translator


class DetailPanel(QWidget):
    action_open      = Signal(object)
    action_folder    = Signal(object)
    action_install   = Signal(object)
    action_update    = Signal(object)
    action_uninstall = Signal(object)
    action_customize = Signal(object)  # reserved for phase 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setObjectName("detail_panel")
        self._tool: Tool | None = None
        self._build_ui()
        self._set_visible(False)

    # ─── UI Construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._header = self._build_header()
        self._body   = self._build_body()
        self._footer = self._build_footer()

        layout.addWidget(self._header)
        layout.addWidget(self._divider())
        layout.addWidget(self._body)
        layout.addStretch()
        layout.addWidget(self._divider())
        layout.addWidget(self._footer)

    def _build_header(self) -> QWidget:
        widget = QWidget()
        widget.setObjectName("detail_header")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        self.banner = QLabel()
        self.banner.setFixedHeight(80)
        self.banner.setAlignment(Qt.AlignCenter)
        self.banner.setStyleSheet("border-radius: 6px; font-size: 28px; font-weight: 700; color: rgba(255,255,255,0.85);")

        self.lbl_name   = QLabel()
        self.lbl_name.setStyleSheet("font-size: 14px; font-weight: 600; color: #f0f0f0;")

        self.lbl_status = QLabel()
        self.lbl_status.setStyleSheet("font-size: 11px; color: #555;")

        layout.addWidget(self.banner)
        layout.addWidget(self.lbl_name)
        layout.addWidget(self.lbl_status)
        return widget

    def _build_body(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        self._info_section = self._section(translator.t("detail", "info"))
        self._path_section = self._section(translator.t("detail", "path"))

        layout.addWidget(self._info_section)
        layout.addWidget(self._path_section)
        return widget

    def _build_footer(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        self.btn_open      = self._action_btn(translator.t("detail", "open"),        "play",       accent=True)
        self.btn_folder    = self._action_btn(translator.t("detail", "open_folder"), "folder-open")
        self.btn_install   = self._action_btn(translator.t("detail", "install"),     "download",   accent=True)
        self.btn_update    = self._action_btn(translator.t("detail", "update"),      "refresh-cw", accent=True)
        self.btn_uninstall = self._action_btn(translator.t("detail", "uninstall"),   "trash-2",    danger=True)
        # btn_customize hidden until phase 3

        for btn in [self.btn_open, self.btn_folder,
                    self.btn_install, self.btn_update, self.btn_uninstall]:
            layout.addWidget(btn)

        self.btn_open.clicked.connect(lambda: self.action_open.emit(self._tool))
        self.btn_folder.clicked.connect(lambda: self.action_folder.emit(self._tool))
        self.btn_install.clicked.connect(lambda: self.action_install.emit(self._tool))
        self.btn_update.clicked.connect(lambda: self.action_update.emit(self._tool))
        self.btn_uninstall.clicked.connect(lambda: self.action_uninstall.emit(self._tool))

        return widget

    # ─── Public API ────────────────────────────────────────────────────────────

    def load_tool(self, tool: Tool):
        self._tool = tool
        self._set_visible(True)
        self._refresh_banner(tool)
        self._refresh_status(tool)
        self._refresh_info(tool)
        self._refresh_buttons(tool)

    def refresh_text(self):
        """Called when the UI language changes."""
        self.btn_open.setText(translator.t("detail", "open"))
        self.btn_folder.setText(translator.t("detail", "open_folder"))
        self.btn_install.setText(translator.t("detail", "install"))
        self.btn_update.setText(translator.t("detail", "update"))
        self.btn_uninstall.setText(translator.t("detail", "uninstall"))

        for section, key in [(self._info_section, "info"), (self._path_section, "path")]:
            lbl = section.layout().itemAt(0).widget()
            if lbl:
                lbl.setText(translator.t("detail", key).upper())

        if self._tool:
            self._refresh_info(self._tool)

    # ─── Internal Refresh ──────────────────────────────────────────────────────

    def _refresh_banner(self, tool: Tool):
        banner_path = Path(__file__).parent.parent / "assets" / "banners" / f"{tool.id}.png"
        if banner_path.exists():
            self.banner.setPixmap(QPixmap(str(banner_path)))
            self.banner.setScaledContents(True)
            self.banner.setText("")
            self.banner.setStyleSheet("border-radius: 8px;")
            self.banner.setFixedHeight(100)
        else:
            self.banner.setPixmap(QPixmap())
            self.banner.setText(tool.id.upper())
            self.banner.setStyleSheet(f"""
                background-color: {tool.banner_color};
                border-radius: 8px;
                font-size: 28px; font-weight: 700;
                color: rgba(255,255,255,0.85);
            """)
        self.lbl_name.setText(tool.name)

    def _refresh_status(self, tool: Tool):
        status_map = {
            ToolStatus.INSTALLED:        ("● Installed",          "#5ae87a"),
            ToolStatus.UPDATE_AVAILABLE: ("● Update available",   "#e8b84a"),
            ToolStatus.AVAILABLE:        ("○ Not installed",      "#555"),
            ToolStatus.NOT_AVAILABLE:    ("○ Game not installed", "#444"),
        }
        text, color = status_map[tool.status]
        self.lbl_status.setText(f'<span style="color:{color};">{text}</span> · {tool.engine}')

    def _refresh_info(self, tool: Tool):
        # Rebuild info rows
        info_layout = self._info_section.layout()
        self._clear_layout(info_layout)

        version_text = "—" if tool.version_installed in (None, "unknown") else tool.version_installed
        row_version  = self._row(translator.t("detail", "version"), version_text)
        if tool.version_installed == "unknown":
            row_version.setToolTip("Unknown version — reinstall via Hammerfy to track updates")

        for w in [
            row_version,
            self._row(translator.t("detail", "engine"), tool.engine),
            self._row(translator.t("detail", "game"),   tool.game),
            self._row(translator.t("detail", "hammer"), tool.hammer_type),
        ]:
            info_layout.addWidget(w)

        # Rebuild path section
        path_layout = self._path_section.layout()
        self._clear_layout(path_layout)
        if tool.install_path:
            lbl = QLabel()
            lbl.setStyleSheet("font-size: 10px; color: #555;")
            lbl.setWordWrap(True)
            lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            # Zero-width space after backslashes allows the path to wrap naturally
            lbl.setText(tool.install_path.replace("\\", "\\\u200b"))
            lbl.setToolTip(tool.install_path)
            path_layout.addWidget(lbl)

    def _refresh_buttons(self, tool: Tool):
        is_installed = tool.status == ToolStatus.INSTALLED
        has_update   = tool.status == ToolStatus.UPDATE_AVAILABLE
        is_available = tool.status == ToolStatus.AVAILABLE

        self.btn_open.setVisible(is_installed)
        self.btn_folder.setVisible(is_installed or has_update)
        self.btn_install.setVisible(is_available)
        self.btn_update.setVisible(has_update)
        self.btn_uninstall.setVisible(is_installed or has_update)

    def _set_visible(self, visible: bool):
        """Show or hide all three panel sections at once."""
        self._header.setVisible(visible)
        self._body.setVisible(visible)
        self._footer.setVisible(visible)

    # ─── Widget Builders ───────────────────────────────────────────────────────

    def _section(self, title: str) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        lbl = QLabel(title.upper())
        lbl.setStyleSheet("font-size: 10px; color: #555; letter-spacing: 1px;")
        layout.addWidget(lbl)
        return widget

    def _row(self, key: str, val: str) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        k = QLabel(key)
        k.setStyleSheet("font-size: 11px; color: #666;")

        v = QLabel(val)
        v.setStyleSheet("font-size: 11px; color: #aaa;")
        v.setWordWrap(True)
        v.setAlignment(Qt.AlignRight)

        layout.addWidget(k)
        layout.addStretch()
        layout.addWidget(v)
        return widget

    def _action_btn(self, text: str, icon_name: str, accent=False, danger=False) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(30)
        btn.setCursor(Qt.PointingHandCursor)

        color = "white" if accent else ("#e84a4a" if danger else "#aaa")
        btn.setIcon(load_icon(icon_name, color=color, size=14))
        btn.setIconSize(QSize(14, 14))

        if accent:
            btn.setStyleSheet("""
                QPushButton { background: #7c6be0; border: none; border-radius: 6px; font-size: 12px; color: white; }
                QPushButton:hover { background: #6559c4; }
            """)
        elif danger:
            btn.setStyleSheet("""
                QPushButton { background: transparent; border: 1px solid #3a1a1a; border-radius: 6px; font-size: 12px; color: #e84a4a; }
                QPushButton:hover { background: #2a1010; }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton { background: transparent; border: 1px solid #2a2a2a; border-radius: 6px; font-size: 12px; color: #aaa; }
                QPushButton:hover { background: #222; color: #e0e0e0; }
            """)
        return btn

    def _divider(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #2a2a2a; max-height: 1px;")
        return line

    def _clear_layout(self, layout):
        # Remove all widgets except the first (section title label)
        while layout.count() > 1:
            item = layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()