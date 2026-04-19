from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                                QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt, Signal
from models.tool import Tool, ToolStatus


class DetailPanel(QWidget):
    action_open = Signal(object)
    action_folder = Signal(object)
    action_install = Signal(object)
    action_update = Signal(object)
    action_uninstall = Signal(object)
    action_customize = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setObjectName("detail_panel")
        self._tool = None
        self._build_ui()
        self._footer.setVisible(False)
        self._body.setVisible(False)
        self._header.setVisible(False)

    def _build_ui(self):
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._header = self._build_header()
        self._body = self._build_body()
        self._footer = self._build_footer()

        self._layout.addWidget(self._header)
        self._layout.addWidget(self._divider())
        self._layout.addWidget(self._body)
        self._layout.addStretch()
        self._layout.addWidget(self._divider())
        self._layout.addWidget(self._footer)

    def _build_header(self):
        widget = QWidget()
        widget.setObjectName("detail_header")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        self.banner = QLabel()
        self.banner.setFixedHeight(80)
        self.banner.setAlignment(Qt.AlignCenter)
        self.banner.setStyleSheet("border-radius: 6px; font-size: 28px; font-weight: 700; color: rgba(255,255,255,0.85);")

        self.lbl_name = QLabel()
        self.lbl_name.setStyleSheet("font-size: 14px; font-weight: 600; color: #f0f0f0;")

        self.lbl_status = QLabel()
        self.lbl_status.setStyleSheet("font-size: 11px; color: #555;")

        layout.addWidget(self.banner)
        layout.addWidget(self.lbl_name)
        layout.addWidget(self.lbl_status)

        return widget

    def _build_body(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        self._info_section = self._section("Info")
        self._path_section = self._section("Path")
        self._custom_section = self._section("Customization")

        layout.addWidget(self._info_section)
        layout.addWidget(self._path_section)
        layout.addWidget(self._custom_section)

        return widget

    def _build_footer(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        self.btn_open     = self._action_btn("▶  Open")
        self.btn_folder   = self._action_btn("📁  Open folder")
        self.btn_customize= self._action_btn("⚙  Customize")
        self.btn_install  = self._action_btn("⬇  Install", accent=True)
        self.btn_update   = self._action_btn("⬆  Update", accent=True)
        self.btn_uninstall= self._action_btn("🗑  Uninstall", danger=True)

        for btn in [self.btn_open, self.btn_folder, self.btn_customize,
                    self.btn_install, self.btn_update, self.btn_uninstall]:
            layout.addWidget(btn)

        self.btn_open.clicked.connect(lambda: self.action_open.emit(self._tool))
        self.btn_folder.clicked.connect(lambda: self.action_folder.emit(self._tool))
        self.btn_customize.clicked.connect(lambda: self.action_customize.emit(self._tool))
        self.btn_install.clicked.connect(lambda: self.action_install.emit(self._tool))
        self.btn_update.clicked.connect(lambda: self.action_update.emit(self._tool))
        self.btn_uninstall.clicked.connect(lambda: self.action_uninstall.emit(self._tool))

        return widget

    def load_tool(self, tool: Tool):
        self._tool = tool
        self._footer.setVisible(True)
        self._body.setVisible(True)
        self._header.setVisible(True)


        self.banner.setText(tool.id.upper())
        self.banner.setStyleSheet(f"""
            background-color: {tool.banner_color};
            border-radius: 6px;
            font-size: 28px;
            font-weight: 700;
            color: rgba(255,255,255,0.85);
        """)
        self.lbl_name.setText(tool.name)

        status_map = {
            ToolStatus.INSTALLED:        ("● Installed",       "#5ae87a"),
            ToolStatus.UPDATE_AVAILABLE: ("● Update available","#e8b84a"),
            ToolStatus.AVAILABLE:        ("○ Not installed",   "#555"),
        }
        text, color = status_map[tool.status]
        self.lbl_status.setText(f'<span style="color:{color};">{text}</span> · {tool.engine}')

        self._refresh_info(tool)
        self._refresh_buttons(tool)

    def _refresh_info(self, tool: Tool):
        layout = self._info_section.layout()
        self._clear_layout(layout)

        rows = [
            ("Version",   tool.version_installed or tool.version_latest or "—"),
            ("Engine",    tool.engine),
            ("Game",      tool.game),
        ]

        # Popula seção PATH
        path_layout = self._path_section.layout()
        self._clear_layout(path_layout)
        if tool.install_path:
            lbl = QLabel(tool.install_path)
            lbl.setStyleSheet("font-size: 10px; color: #555;")
            lbl.setWordWrap(True)
            path_layout.addWidget(lbl)

        for key, val in rows:
            layout.addWidget(self._row(key, val))

    def _refresh_buttons(self, tool: Tool):
        is_installed = tool.status == ToolStatus.INSTALLED
        has_update   = tool.status == ToolStatus.UPDATE_AVAILABLE
        is_available = tool.status == ToolStatus.AVAILABLE

        self.btn_open.setVisible(is_installed)
        self.btn_folder.setVisible(is_installed or has_update)
        self.btn_customize.setVisible(is_installed)
        self.btn_install.setVisible(is_available)
        self.btn_update.setVisible(has_update)
        self.btn_uninstall.setVisible(is_installed or has_update)

    def _section(self, title):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        lbl = QLabel(title.upper())
        lbl.setStyleSheet("font-size: 10px; color: #555; letter-spacing: 1px;")
        layout.addWidget(lbl)

        return widget

    def _row(self, key, val):
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

    def _action_btn(self, text, accent=False, danger=False):
        btn = QPushButton(text)
        btn.setFixedHeight(30)
        btn.setCursor(Qt.PointingHandCursor)

        if accent:
            btn.setStyleSheet("""
                QPushButton { background: #e05c20; border: none; border-radius: 6px; font-size: 12px; color: white; }
                QPushButton:hover { background: #c94e17; }
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

    def _divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #2a2a2a; max-height: 1px;")
        return line

    def _clear_layout(self, layout):
        while layout.count() > 1:
            item = layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()