from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame
from PySide6.QtCore import Qt
from ui.sidebar import Sidebar
from ui.topbar import Topbar
from ui.tool_grid import ToolGrid
from ui.detail_panel import DetailPanel
from ui.sidebar import Sidebar, SidebarLogo
from ui.settings_panel import SettingsPanel
from ui.about_panel import AboutPanel
from models.tool import Tool, ToolStatus
from core.steam import scan_tools
from core.hammer import open_hammer, open_folder
from core.updater import get_latest_build, download_and_install, uninstall
from utils.versions import get_version
from utils import translator

import sys

def _build_tools_from_scan() -> list[Tool]:
    raw = scan_tools()
    latest = get_latest_build()
    tools = []
    for t in raw:
        if not t["game_installed"] or t["bin_missing"]:
            status = ToolStatus.NOT_AVAILABLE
        elif t["is_installed"]:
            installed_build = t["version"]
            if latest and installed_build and installed_build != latest:
                status = ToolStatus.UPDATE_AVAILABLE
            else:
                status = ToolStatus.INSTALLED
        else:
            status = ToolStatus.AVAILABLE

        tools.append(Tool(
            id=t["id"],
            name=t["name"],
            game=t["game"],
            engine=t["engine"],
            hammer_type=t["hammer_type"],
            version_installed=t["version"] if t["is_installed"] else None,
            version_latest=latest if t["is_installed"] else None,
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
        self.resize(1280, 760)
        self._all_tools = _build_tools_from_scan()
        self._current_filter = "all"
        self._search_query = ""
        self._build_ui()
        self._load_tools()

    from ui.sidebar import Sidebar, SidebarLogo

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Topo: logo + linha vertical + topbar
        top = QWidget()
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        self.sidebar_logo = SidebarLogo()
        self.topbar = Topbar()

        top_layout.addWidget(self.sidebar_logo)
        top_layout.addWidget(self._vline())
        top_layout.addWidget(self.topbar)

        # Linha horizontal atravessa tudo
        hline = self._hline()

        # Conteúdo: sidebar nav + linha vertical + grid + detail
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.filter_changed.connect(self._on_filter)

        self.grid = ToolGrid()
        self.grid.tool_selected.connect(self._on_tool_selected)
        self.grid.empty_clicked.connect(self._on_empty_click)
        self.grid.action_open.connect(self._on_open)
        self.grid.action_folder.connect(self._on_folder)
        self.grid.action_install.connect(self._on_install)
        self.grid.action_update.connect(self._on_update)

        self.settings_panel = SettingsPanel()
        self.settings_panel.setVisible(False)

        self.about_panel = AboutPanel()
        self.about_panel.setVisible(False)

        self.detail = DetailPanel()
        self.detail.setFixedWidth(240)
        self.detail.action_open.connect(self._on_open)
        self.detail.action_folder.connect(self._on_folder)
        self.detail.action_install.connect(self._on_install)
        self.detail.action_update.connect(self._on_update)
        self.detail.action_uninstall.connect(self._on_uninstall)
        self.detail.action_customize.connect(self._on_customize)

        self.detail._footer.setVisible(False)
        self.detail._body.setVisible(False)
        self.detail._header.setVisible(False)

        self._detail_divider = self._vline()
        self._detail_divider.setVisible(False)
        self._detail_divider.setMaximumWidth(0)

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self._vline())
        content_layout.addWidget(self.grid)
        content_layout.addWidget(self.about_panel)
        content_layout.addWidget(self.settings_panel)
        content_layout.addWidget(self._detail_divider)
        content_layout.addWidget(self.detail)

        root.addWidget(top)
        root.addWidget(hline)
        root.addWidget(content)

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

        return tools

    def _filter_title(self):
        keys = {
            "all":      "all_tools",
            "installed":"installed",
            "available":"available",
            "updates":  "updates",
            "settings": "settings",
        }
        return keys.get(self._current_filter, "all_tools")

    def _on_filter(self, filter_id):
        self._current_filter = filter_id
        if filter_id == "about":
            self.grid.setVisible(False)
            self.about_panel.setVisible(True)
            self.settings_panel.setVisible(False)
            self.detail.setVisible(False)
            self._detail_divider.setVisible(False)
            self._detail_divider.setMaximumWidth(0)
            self.detail._header.setVisible(False)
            self.detail._body.setVisible(False)
            self.detail._footer.setVisible(False)
            self.topbar.set_title("about", None)
        elif filter_id == "settings":
            self.grid.setVisible(False)
            self.about_panel.setVisible(False)
            self.settings_panel.setVisible(True)
            self.detail.setVisible(False)
            self._detail_divider.setVisible(False)
            self._detail_divider.setMaximumWidth(0)
            self.detail._header.setVisible(False)
            self.detail._body.setVisible(False)
            self.detail._footer.setVisible(False)
            self.topbar.set_title("settings", None)
        else:
            self.grid.setVisible(True)
            self.about_panel.setVisible(False)
            self.settings_panel.setVisible(False)
            self.detail.setVisible(False)
            self._load_tools()
            if self.detail._header.isVisible():
                self._detail_divider.setVisible(True)

    def _on_search(self, query):
        self._search_query = query
        self._load_tools()

    def _on_tool_selected(self, tool):
        self.detail.load_tool(tool)
        self.detail.setVisible(True)
        self._detail_divider.setMaximumWidth(1)
        self._detail_divider.setVisible(True)

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
        top = QWidget()
        top.setFixedHeight(48)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #242424; max-height: 1px;")
        return line

    def _on_install(self, tool: Tool):
        from PySide6.QtWidgets import QMessageBox, QProgressDialog
        from PySide6.QtCore import Qt

        build = get_latest_build()
        if not build:
            QMessageBox.warning(self, "Hammerfy", "Não foi possível verificar a versão mais recente. Verifique sua conexão.")
            return

        # Descobre o caminho de instalação pelo steam.py
        from core.steam import HAMMER_GAMES, find_steam_path, find_library_folders, find_installed_games
        steam_path = find_steam_path()
        if not steam_path:
            QMessageBox.warning(self, "Hammerfy", "Steam não encontrada.")
            return

        libs = find_library_folders(steam_path)
        games = find_installed_games(libs)

        game_info = next((v for v in HAMMER_GAMES.values() if v["id"] == tool.id), None)
        game_folder_name = next((k for k, v in HAMMER_GAMES.items() if v["id"] == tool.id), None)

        if not game_folder_name or game_folder_name not in games:
            QMessageBox.warning(self, "Hammerfy", f"Jogo não encontrado na biblioteca Steam.\nInstale {tool.game} primeiro.")
            return

        game_path = games[game_folder_name]
        install_path = str(game_path / game_info["bin"])

        progress = QProgressDialog(f"Baixando Hammer++ {tool.name}...", "Cancelar", 0, 100, self)
        progress.setWindowTitle("Hammerfy")
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        def on_progress(downloaded, total):
            if total > 0:
                progress.setValue(int(downloaded / total * 100))
            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()

        success, msg = download_and_install(tool.id, build, install_path, on_progress)
        progress.close()

        if success:
            QMessageBox.information(self, "Hammerfy", f"Hammer++ instalado com sucesso!")
            self._all_tools = _build_tools_from_scan()
            self._load_tools()
            if self.detail._header.isVisible() and self.detail._tool and self.detail._tool.id == tool.id:
                updated_tool = next((t for t in self._all_tools if t.id == tool.id), None)
                if updated_tool:
                    self.detail.load_tool(updated_tool)
        else:
            QMessageBox.warning(self, "Hammerfy", f"Erro: {msg}")

    def _on_uninstall(self, tool: Tool):
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, "Hammerfy",
            f"Desinstalar {tool.name}?\nEssa ação não pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        success, msg = uninstall(tool.install_path, tool.id)
        if success:
            QMessageBox.information(self, "Hammerfy", "Hammer++ desinstalado com sucesso.")
            self._all_tools = _build_tools_from_scan()
            self._load_tools()
        else:
            QMessageBox.warning(self, "Hammerfy", f"Erro: {msg}")

    def _on_update(self, tool: Tool):
        self._on_install(tool)

    def _on_empty_click(self):
        for card in self.grid._cards:
            card.set_selected(False)
        self.detail.setVisible(False)
        self.detail._footer.setVisible(False)
        self.detail._body.setVisible(False)
        self.detail._header.setVisible(False)
        self._detail_divider.setVisible(False)
        self._detail_divider.setMaximumWidth(0)

    def _on_language(self, lang):
        translator.load(lang)
        self._refresh_ui_text()

    def _refresh_ui_text(self):
        self.sidebar.refresh_text()
        self.topbar.refresh_text()
        self.detail.refresh_text()
        self._load_tools()

    def _on_customize(self, tool: Tool):
        pass  # implementar na fase 3