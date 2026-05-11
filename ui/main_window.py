from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QMessageBox, QProgressDialog, QApplication)
from PySide6.QtCore import QThread, Qt, Signal as QSignal
from ui.sidebar import Sidebar, SidebarLogo
from ui.topbar import Topbar
from ui.tool_grid import ToolGrid
from ui.detail_panel import DetailPanel
from ui.settings_panel import SettingsPanel
from ui.about_panel import AboutPanel
from models.tool import Tool, ToolStatus
from core.steam import (scan_tools, SteamWatcher, find_steam_path, find_library_folders, find_installed_games, HAMMER_GAMES)
from core.hammer import open_hammer, open_folder
from core.updater import (get_latest_build, download_and_install, uninstall, CSGO_BUILD, get_tools_latest_date, download_and_install_tools)
from utils.versions import get_tools_date, save_tools_date
from utils import translator
from pathlib import Path


# ─── Tool Builder ──────────────────────────────────────────────────────────────

def _build_tools_from_scan() -> list[Tool]:
    # Scan Steam libraries and return the full tool list with statuses.
    raw    = scan_tools()
    latest = get_latest_build()
    tools  = []

    for t in raw:
        if not t["game_installed"] or t["bin_missing"]:
            status = ToolStatus.NOT_AVAILABLE
        elif t["is_installed"]:
            installed_build  = t["version"]
            effective_latest = CSGO_BUILD if t["id"] == "csgo" else latest
            is_csgo          = t["id"] == "csgo"
            # CS:GO is frozen at build 8864 — never show update available
            if (not is_csgo
                    and effective_latest
                    and installed_build
                    and installed_build != "unknown"
                    and installed_build != effective_latest):
                status = ToolStatus.UPDATE_AVAILABLE
            else:
                status = ToolStatus.INSTALLED
        else:
            status = ToolStatus.AVAILABLE

        tools.append(Tool(
            id                = t["id"],
            name              = t["name"],
            game              = t["game"],
            engine            = t["engine"],
            hammer_type       = t["hammer_type"],
            version_installed = t["version"] if t["is_installed"] else None,
            version_latest    = latest if t["is_installed"] else None,
            install_path      = t["install_path"],
            status            = status,
            banner_color      = t["banner_color"],
        ))
    return tools


# ─── Background Workers ────────────────────────────────────────────────────────

class SilentUpdateWorker(QThread):
    # Resolves 'unknown' versions for manually installed Hammer++ instances.
    finished = QSignal()

    def __init__(self, tools: list[Tool], parent=None):
        super().__init__(parent)
        self._tools = tools

    def run(self):
        build = get_latest_build()
        if not build:
            return

        for tool in self._tools:
            if tool.version_installed != "unknown" or not tool.install_path:
                continue
            install_dir = str(Path(tool.install_path).parent)
            # Silent — if it fails, version stays "unknown" and retries next launch
            download_and_install(tool.id, build, install_dir)

        self.finished.emit()


class ToolsPlusPlusWorker(QThread):
    # Keeps Tools++ up to date silently in the background.

    # Sentinel file to verify tools are actually present on disk
    SENTINEL = "vbspplusplus.exe"

    def __init__(self, tools: list[Tool], parent=None):
        super().__init__(parent)
        self._tools = tools

    def run(self):
        latest_date = get_tools_latest_date()
        if not latest_date:
            return

        saved_date = get_tools_date()

        for tool in self._tools:
            if not tool.install_path:
                continue
            install_dir   = Path(tool.install_path).parent
            tools_present = (install_dir / self.SENTINEL).exists()

            # Skip only if date matches AND files are actually present
            if saved_date == latest_date and tools_present:
                continue

            success, _ = download_and_install_tools(str(install_dir))
            if success:
                save_tools_date(latest_date)


# ─── Main Window ───────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hammerfy")
        self.setMinimumSize(900, 600)
        self.resize(1280, 760)

        self._all_tools: list[Tool] = _build_tools_from_scan()
        self._current_filter = "all"

        self._build_ui()
        self._hide_detail()
        self._load_tools()
        self._start_silent_update()
        self._start_tools_update()
        self._start_steam_watcher()

    # ─── UI Construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Top row: logo + separator + topbar
        top = QWidget()
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        self.sidebar_logo = SidebarLogo()
        self.topbar       = Topbar()
        top_layout.addWidget(self.sidebar_logo)
        top_layout.addWidget(self._vline())
        top_layout.addWidget(self.topbar)

        # Content row: sidebar + separator + grid/panels + detail
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

        self._detail_divider = self._vline()

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self._vline())
        content_layout.addWidget(self.grid)
        content_layout.addWidget(self.about_panel)
        content_layout.addWidget(self.settings_panel)
        content_layout.addWidget(self._detail_divider)
        content_layout.addWidget(self.detail)

        root.addWidget(top)
        root.addWidget(self._hline())
        root.addWidget(content)

    # ─── Tool Loading ──────────────────────────────────────────────────────────

    def _load_tools(self):
        filtered = self._filter_tools()
        self.grid.load_tools(filtered)
        self.topbar.set_title(self._filter_title(), len(filtered))

    def _filter_tools(self) -> list[Tool]:
        status_map = {
            "installed": ToolStatus.INSTALLED,
            "available": ToolStatus.AVAILABLE,
            "updates":   ToolStatus.UPDATE_AVAILABLE,
        }
        if self._current_filter in status_map:
            target = status_map[self._current_filter]
            return [t for t in self._all_tools if t.status == target]
        return self._all_tools

    def _filter_title(self) -> str:
        return {
            "all":       "all_tools",
            "installed": "installed",
            "available": "available",
            "updates":   "updates",
        }.get(self._current_filter, "all_tools")

    def _refresh_tools(self):
        """Rescan and reload — keeps detail panel in sync if open."""
        self._all_tools = _build_tools_from_scan()
        self._load_tools()
        if self.detail._tool:
            updated = next((t for t in self._all_tools if t.id == self.detail._tool.id), None)
            if updated:
                self.detail.load_tool(updated)

    # ─── Panel Visibility ──────────────────────────────────────────────────────

    def _hide_detail(self):
        self.detail.setVisible(False)
        self.detail._footer.setVisible(False)
        self.detail._body.setVisible(False)
        self.detail._header.setVisible(False)
        self._detail_divider.setVisible(False)
        self._detail_divider.setMaximumWidth(0)

    def _show_detail(self):
        self.detail.setVisible(True)
        self._detail_divider.setMaximumWidth(1)
        self._detail_divider.setVisible(True)

    # ─── Event Handlers ────────────────────────────────────────────────────────

    def _on_filter(self, filter_id: str):
        self._current_filter = filter_id

        is_grid = filter_id not in ("about", "settings")
        self.grid.setVisible(is_grid)
        self.about_panel.setVisible(filter_id == "about")
        self.settings_panel.setVisible(filter_id == "settings")

        if not is_grid:
            self._hide_detail()
            self.topbar.set_title(filter_id, None)
        else:
            self._load_tools()

    def _on_tool_selected(self, tool: Tool):
        self.detail.load_tool(tool)
        self._show_detail()

    def _on_empty_click(self):
        for card in self.grid._cards:
            card.set_selected(False)
        self._hide_detail()

    def _on_open(self, tool: Tool):
        success, msg = open_hammer(tool)
        if not success:
            QMessageBox.warning(self, "Hammerfy", msg)

    def _on_folder(self, tool: Tool):
        success, msg = open_folder(tool)
        if not success:
            QMessageBox.warning(self, "Hammerfy", msg)

    def _on_install(self, tool: Tool):
        build = get_latest_build()
        if not build:
            QMessageBox.warning(self, "Hammerfy", "Não foi possível verificar a versão mais recente. Verifique sua conexão.")
            return

        steam_path = find_steam_path()
        if not steam_path:
            QMessageBox.warning(self, "Hammerfy", "Steam não encontrada.")
            return

        libs             = find_library_folders(steam_path)
        games            = find_installed_games(libs)
        game_info        = next((v for v in HAMMER_GAMES.values() if v["id"] == tool.id), None)
        game_folder_name = next((k for k, v in HAMMER_GAMES.items() if v["id"] == tool.id), None)

        if not game_folder_name or game_folder_name not in games:
            QMessageBox.warning(self, "Hammerfy", f"Jogo não encontrado.\nInstale {tool.game} primeiro.")
            return

        game_path    = games[game_folder_name]
        install_path = str(game_path / game_info["bin"])

        progress = QProgressDialog(f"Baixando Hammer++ {tool.name}...", "Cancelar", 0, 100, self)
        progress.setWindowTitle("Hammerfy")
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        def on_progress(downloaded: int, total: int):
            if total > 0:
                progress.setValue(int(downloaded / total * 100))
            QApplication.processEvents()

        success, msg = download_and_install(tool.id, build, install_path, on_progress)
        progress.close()

        if success:
            QMessageBox.information(self, "Hammerfy", "Hammer++ instalado com sucesso!")
            self._refresh_tools()
        else:
            QMessageBox.warning(self, "Hammerfy", f"Erro: {msg}")

    def _on_uninstall(self, tool: Tool):
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
            self._hide_detail()
            self._refresh_tools()
        else:
            QMessageBox.warning(self, "Hammerfy", f"Erro: {msg}")

    def _on_update(self, tool: Tool):
        self._on_install(tool)

    def _on_language(self, lang: str):
        translator.load(lang)
        self.sidebar.refresh_text()
        self.topbar.refresh_text()
        self.detail.refresh_text()
        self._load_tools()

    def _on_customize(self, tool: Tool):
        pass  # phase 3

    # ─── Background Workers ────────────────────────────────────────────────────

    def _start_silent_update(self):
        unknown = [t for t in self._all_tools if t.version_installed == "unknown"]
        if not unknown:
            return
        self._silent_worker = SilentUpdateWorker(unknown, self)
        self._silent_worker.finished.connect(self._refresh_tools, Qt.QueuedConnection)
        self._silent_worker.start()

    def _on_silent_update_done(self):
        self._refresh_tools()

    def _start_tools_update(self):
        installed = [t for t in self._all_tools if t.install_path]
        if not installed:
            return
        self._tools_worker = ToolsPlusPlusWorker(installed, self)
        self._tools_worker.start()

    # ─── Steam Watcher ─────────────────────────────────────────────────────────

    def _start_steam_watcher(self):
        steam_path = find_steam_path()
        if not steam_path:
            return
        libs = find_library_folders(steam_path)
        self._steam_watcher = SteamWatcher(self)
        self._steam_watcher.watch(libs)
        # Auto-refresh when Steam library changes (game installed/uninstalled)
        self._steam_watcher.games_changed.connect(self._refresh_tools)

    # ─── Widget Helpers ────────────────────────────────────────────────────────

    def _vline(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("background-color: #242424; max-width: 1px;")
        return line

    def _hline(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #242424; max-height: 1px;")
        return line