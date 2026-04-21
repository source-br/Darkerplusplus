from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                                QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt, Signal, QSize
from models.tool import Tool, ToolStatus
from pathlib import Path
from PySide6.QtGui import QPixmap
from utils.icons import load_icon
from utils import translator

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

        self._info_section = self._section(translator.t("detail", "info"))
        self._path_section = self._section(translator.t("detail", "path"))
        self._custom_section = self._section(translator.t("detail", "customization"))

        layout.addWidget(self._info_section)
        layout.addWidget(self._path_section)
        layout.addWidget(self._custom_section)

        return widget

    def _build_footer(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        self.btn_open      = self._action_btn(translator.t("detail", "open"),        icon_name="play",        accent=True)
        self.btn_folder    = self._action_btn(translator.t("detail", "open_folder"), icon_name="folder-open")
        self.btn_customize = self._action_btn(translator.t("detail", "customize"),   icon_name="settings")
        self.btn_install   = self._action_btn(translator.t("detail", "install"),     icon_name="download",    accent=True)
        self.btn_update    = self._action_btn(translator.t("detail", "update"),      icon_name="refresh-cw",  accent=True)
        self.btn_uninstall = self._action_btn(translator.t("detail", "uninstall"),   icon_name="trash-2",     danger=True)

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

        banner_path = Path(__file__).parent.parent / "assets" / "banners" / f"{tool.id}.png"
        if banner_path.exists():
            pixmap = QPixmap(str(banner_path))
            self.banner.setPixmap(pixmap)
            self.banner.setScaledContents(True)
            self.banner.setText("")
            self.banner.setStyleSheet("border-radius: 8px;")
            self.banner.setFixedHeight(100)
        else:
            self.banner.setPixmap(QPixmap())
            self.banner.setText(tool.id.upper())
            self.banner.setStyleSheet(f"""
                background-color: {self._tool.banner_color};
                border-radius: 8px;
                font-size: 28px;
                font-weight: 700;
                color: rgba(255,255,255,0.85);
            """)
        self.lbl_name.setText(tool.name)

        status_map = {
            ToolStatus.INSTALLED:        ("● Installed",       "#5ae87a"),
            ToolStatus.UPDATE_AVAILABLE: ("● Update available","#e8b84a"),
            ToolStatus.AVAILABLE:        ("○ Not installed",   "#555"),
            ToolStatus.NOT_AVAILABLE:    ("○ Game not installed", "#444"),
        }
        text, color = status_map[tool.status]
        self.lbl_status.setText(f'<span style="color:{color};">{text}</span> · {tool.engine}')

        self._refresh_info(tool)
        self._refresh_buttons(tool)

    def _refresh_info(self, tool: Tool):
        layout = self._info_section.layout()
        self._clear_layout(layout)

        version_text = tool.version_installed or "—"  # adiciona essa linha

        rows = [
            (translator.t("detail", "version"), version_text),
            (translator.t("detail", "engine"),  tool.engine),
            (translator.t("detail", "game"),    tool.game),
            (translator.t("detail", "hammer"),   tool.hammer_type),
        ]

        # Popula seção PATH
        path_layout = self._path_section.layout()
        self._clear_layout(path_layout)
        if tool.install_path:
            lbl = QLabel()
            lbl.setStyleSheet("font-size: 10px; color: #555;")
            lbl.setWordWrap(True)
            lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            # Quebra apenas nas barras do path
            path_display = tool.install_path.replace("\\", "\\\u200b")
            lbl.setText(path_display)
            lbl.setToolTip(tool.install_path)
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

    def refresh_text(self):
        self.btn_open.setText(translator.t("detail", "open"))
        self.btn_folder.setText(translator.t("detail", "open_folder"))
        self.btn_customize.setText(translator.t("detail", "customize"))
        self.btn_install.setText(translator.t("detail", "install"))
        self.btn_update.setText(translator.t("detail", "update"))
        self.btn_uninstall.setText(translator.t("detail", "uninstall"))

        # Atualiza títulos das seções
        for widget, key in zip(
            [self._info_section, self._path_section, self._custom_section],
            ["info", "path", "customization"]
        ):
            label = widget.layout().itemAt(0).widget()
            if label:
                label.setText(translator.t("detail", key).upper())

        # Rerenderiza info se tiver tool carregada
        if self._tool:
            self._refresh_info(self._tool)

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

    def _action_btn(self, text, icon_name=None, accent=False, danger=False):
        btn = QPushButton(text)
        btn.setFixedHeight(30)
        btn.setCursor(Qt.PointingHandCursor)

        if icon_name:
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