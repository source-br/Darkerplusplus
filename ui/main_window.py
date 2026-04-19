from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame
from PySide6.QtCore import Qt
from ui.sidebar import Sidebar
from ui.topbar import Topbar
from ui.tool_grid import ToolGrid
from ui.detail_panel import DetailPanel
from models.tool import Tool, ToolStatus
from models.tool import Tool, ToolStatus
from core.steam import scan_tools
from core.hammer import open_hammer, open_folder
import sys

def _build_tools_from_scan() -> list[Tool]:
    raw = scan_tools()
    tools = []
    for t in raw:
        if t["bin_missing"]:
            status = ToolStatus.AVAILABLE
        elif t["is_installed"]:
            status = ToolStatus.INSTALLED
        else:
            status = ToolStatus.AVAILABLE

        tools.append(Tool(
            id=t["id"],
            name=t["name"],
            game=t["game"],
            engine=t["engine"],
            version_installed=t["version"] if t["is_installed"] else None,
            version_latest=None,
            install_path=t["install_path"],
            status=status,
            banner_color=t["banner_color"],
        ))
    return tools


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hammerfy")
        self.setMinimumSize(900, 600)
        self.resize(1100, 680)
        self._all_tools = _build_tools_from_scan()
        self._current_filter = "all"
        self._search_query = ""
        self._build_ui()
        self._load_tools()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.filter_changed.connect(self._on_filter)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.topbar = Topbar()
        self.topbar.search_changed.connect(self._on_search)

        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.grid = ToolGrid()
        self.grid.tool_selected.connect(self._on_tool_selected)

        self.detail = DetailPanel()
        self.grid.action_open.connect(self._on_open)
        self.grid.action_folder.connect(self._on_folder)
        self.detail.action_open.connect(self._on_open)
        self.detail.action_folder.connect(self._on_folder)

        content_layout.addWidget(self.grid)
        content_layout.addWidget(self._vline())
        content_layout.addWidget(self.detail)

        right_layout.addWidget(self._hline())
        right_layout.addWidget(self.topbar)
        right_layout.addWidget(self._hline())
        right_layout.addWidget(content)

        root.addWidget(self.sidebar)
        root.addWidget(self._vline())
        root.addWidget(right)

    def _load_tools(self):
        filtered = self._filter_tools()
        self.grid.load_tools(filtered)
        self.topbar.set_title(self._filter_title(), len(filtered))

    def _filter_tools(self):
        tools = self._all_tools

        if self._current_filter == "installed":
            tools = [t for t in tools if t.status == ToolStatus.INSTALLED]
        elif self._current_filter == "available":
            tools = [t for t in tools if t.status == ToolStatus.AVAILABLE]
        elif self._current_filter == "updates":
            tools = [t for t in tools if t.status == ToolStatus.UPDATE_AVAILABLE]

        if self._search_query:
            q = self._search_query.lower()
            tools = [t for t in tools if q in t.name.lower() or q in t.game.lower()]

        return tools

    def _filter_title(self):
        titles = {
            "all": "All tools", "installed": "Installed",
            "available": "Available", "updates": "Updates", "settings": "Settings"
        }
        return titles.get(self._current_filter, "All tools")

    def _on_filter(self, filter_id):
        self._current_filter = filter_id
        self._load_tools()

    def _on_search(self, query):
        self._search_query = query
        self._load_tools()

    def _on_tool_selected(self, tool):
        self.detail.load_tool(tool)

    def _on_open(self, tool: Tool):
        success, msg = open_hammer(tool)
        if not success:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Hammerfy", msg)

    def _on_folder(self, tool: Tool):
        success, msg = open_folder(tool)
        if not success:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Hammerfy", msg)

    def _vline(self):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("background-color: #242424; max-width: 1px;")
        return line

    def _hline(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #242424; max-height: 1px;")
        return line