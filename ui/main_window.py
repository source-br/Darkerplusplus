from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame
from PySide6.QtCore import Qt
from ui.sidebar import Sidebar
from ui.topbar import Topbar
from ui.tool_grid import ToolGrid
from ui.detail_panel import DetailPanel
from models.tool import Tool, ToolStatus


MOCK_TOOLS = [
    Tool("tf2",      "Hammer++ TF2",              "Team Fortress 2",           "Source", "2024.11", "2024.11", "/fake/path", ToolStatus.INSTALLED,       "#3d1a08"),
    Tool("gmod",     "Hammer++ GMod",             "Garry's Mod",               "Source", "2024.11", "2024.11", "/fake/path", ToolStatus.INSTALLED,       "#1a2e1a"),
    Tool("portal2",  "Hammer++ Portal 2",         "Portal 2",                  "Source", None,      "2024.10", None,         ToolStatus.AVAILABLE,       "#1a0e35"),
    Tool("l4d2",     "Hammer++ L4D2",             "Left 4 Dead 2",             "Source", "2024.09", "2024.09", "/fake/path", ToolStatus.INSTALLED,       "#2a0808"),
    Tool("css",      "Hammer++ CS:S",             "Counter-Strike: Source",    "Source", None,      "2024.10", None,         ToolStatus.AVAILABLE,       "#0a1a2a"),
    Tool("dods",     "Hammer++ DoDS",             "Day of Defeat: Source",     "Source", None,      "2024.10", None,         ToolStatus.AVAILABLE,       "#1a1a08"),
    Tool("hl2",      "Hammer++ HL2",              "Half-Life 2",               "Source", None,      "2024.10", None,         ToolStatus.AVAILABLE,       "#0e2210"),
    Tool("sdk2013sp","Hammer++ SDK 2013 SP",      "Source SDK 2013 SP",        "Source", "2024.08", "2024.11", "/fake/path", ToolStatus.UPDATE_AVAILABLE,"#252508"),
    Tool("sdk2013mp","Hammer++ SDK 2013 MP",      "Source SDK 2013 MP",        "Source", None,      "2024.10", None,         ToolStatus.AVAILABLE,       "#1a1408"),
    Tool("csgo",     "Hammer++ CS:GO",            "Counter-Strike: Global Offensive", "Source", None, "2024.10", None,      ToolStatus.AVAILABLE,       "#0a1f2a"),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hammerfy")
        self.setMinimumSize(900, 600)
        self.resize(1100, 680)
        self._all_tools = MOCK_TOOLS
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