import os
import struct
import re
from pathlib import Path
from utils.versions import get_version

HAMMER_GAMES = {
    "GarrysMod": {
        "id": "gmod",
        "name": "Garry's Mod",
        "engine": "Source",
        "hammer_type": "Hammer++ GMod",
        "bin": r"bin",
        "exe_path": r"bin\win64\hammerplusplus.exe",
        "banner_color": "#1a2e1a",
    },
    "Team Fortress 2": {
        "id": "tf2",
        "name": "Team Fortress 2",
        "engine": "Source",
        "hammer_type": "Hammer++ TF2",
        "bin": r"bin",
        "exe_path": r"bin\x64\hammerplusplus.exe",
        "banner_color": "#3d1a08",
    },
    "Counter-Strike Source": {
        "id": "css",
        "name": "Counter-Strike: Source",
        "engine": "Source",
        "hammer_type": "Hammer++ TF2",
        "bin": r"bin",
        "exe_path": r"bin\x64\hammerplusplus.exe",
        "banner_color": "#0a1a2a",
    },
    "Day of Defeat Source": {
        "id": "dods",
        "name": "Day of Defeat: Source",
        "engine": "Source",
        "hammer_type": "Hammer++ TF2",
        "bin": r"bin",
        "exe_path": r"bin\x64\hammerplusplus.exe",
        "banner_color": "#1a1a08",
    },
    "Half-Life 2": {
        "id": "hl2",
        "name": "Half-Life 2",
        "engine": "Source",
        "hammer_type": "Hammer++ SDK SP",
        "bin": r"bin",
        "exe_path": r"bin\hammerplusplus.exe",
        "banner_color": "#0e2210",
    },
    "Left 4 Dead 2": {
        "id": "l4d2",
        "name": "Left 4 Dead 2",
        "engine": "Source",
        "hammer_type": "Hammer++ L4D2",
        "bin": r"bin",
        "exe_path": r"bin\hammerplusplus.exe",
        "banner_color": "#2a0808",
    },
    "Portal": {
        "id": "portal1",
        "name": "Portal",
        "engine": "Source",
        "hammer_type": "Hammer++ SDK SP",
        "bin": r"bin",
        "exe_path": r"bin\hammerplusplus.exe",
        "banner_color": "#0d1a2e",
    },
    "Portal 2": {
        "id": "portal2",
        "name": "Portal 2",
        "engine": "Source",
        "hammer_type": "Hammer++ Portal 2",
        "bin": r"bin",
        "exe_path": r"bin\hammerplusplus.exe",
        "banner_color": "#1a0e35",
    },
    "Source SDK Base 2013 Singleplayer": {
        "id": "sdk2013sp",
        "name": "SDK 2013 Singleplayer",
        "engine": "Source",
        "hammer_type": "Hammer++ SDK SP",
        "bin": r"bin",
        "exe_path": r"bin\hammerplusplus.exe",
        "banner_color": "#252508",
    },
    "Source SDK Base 2013 Multiplayer": {
        "id": "sdk2013mp",
        "name": "SDK 2013 Multiplayer",
        "engine": "Source",
        "hammer_type": "Hammer++ SDK MP",
        "bin": r"bin",
        "exe_path": r"bin\hammerplusplus.exe",
        "banner_color": "#1a1408",
    },
    "Counter-Strike Global Offensive": {
        "id": "csgo",
        "name": "CS: Global Offensive",
        "engine": "Source",
        "hammer_type": "Hammer++ CS:GO",
        "bin": None,
        "exe_path": None,
        "banner_color": "#0a1f2a",
    },
}


def find_steam_path() -> Path | None:
    """Localiza a pasta raiz da Steam no Windows via registro."""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        path, _ = winreg.QueryValueEx(key, "InstallPath")
        winreg.CloseKey(key)
        return Path(path)
    except Exception:
        return None


def find_library_folders(steam_path: Path) -> list[Path]:
    """Lê o libraryfolders.vdf para encontrar todas as bibliotecas Steam."""
    vdf_path = steam_path / "steamapps" / "libraryfolders.vdf"
    if not vdf_path.exists():
        return [steam_path / "steamapps"]

    libraries = [steam_path / "steamapps"]
    try:
        content = vdf_path.read_text(encoding="utf-8")
        for match in re.finditer(r'"path"\s+"([^"]+)"', content):
            lib = Path(match.group(1)) / "steamapps"
            if lib.exists() and lib not in libraries:
                libraries.append(lib)
    except Exception:
        pass

    return libraries


def find_installed_games(libraries: list[Path]) -> dict[str, Path]:
    """
    Varre as bibliotecas e retorna um dict com
    nome_do_jogo -> pasta steamapps/common/jogo
    """
    installed = {}
    for lib in libraries:
        common = lib / "common"
        if not common.exists():
            continue
        for folder in common.iterdir():
            if folder.is_dir():
                installed[folder.name] = folder
    return installed


def get_hammer_version(exe_path: Path) -> str | None:
    """Tenta extrair a versão do hammerplusplus.exe pelo cabeçalho PE."""
    try:
        import win32api
        info = win32api.GetFileVersionInfo(str(exe_path), "\\")
        ms = info["FileVersionMS"]
        ls = info["FileVersionLS"]
        return f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
    except Exception:
        return None


def scan_tools() -> list[dict]:
    """
    Função principal — escaneia o sistema e retorna lista de dicts
    com todas as ferramentas disponíveis e seu status.
    """
    steam_path = find_steam_path()
    libraries = find_library_folders(steam_path) if steam_path else []
    installed_games = find_installed_games(libraries) if libraries else {}

    tools = []
    for game_folder_name, game_info in HAMMER_GAMES.items():
        game_path = installed_games.get(game_folder_name)
        hammer_exe = None
        is_installed = False
        version = None

        if game_path and game_info["exe_path"]:
            exe_path = game_path / game_info["exe_path"]
            if exe_path.exists():
                is_installed = True
                hammer_exe = str(exe_path)
                version = get_version(game_info["id"])

        tools.append({
            "id":           game_info["id"],
            "name":         game_info["name"],
            "game":         game_folder_name,
            "engine":       game_info["engine"],
            "hammer_type": game_info["hammer_type"],
            "is_installed": is_installed,
            "install_path": hammer_exe,
            "version":      version,
            "banner_color": game_info["banner_color"],
            "bin_missing":  game_info["bin"] is None,
        })

    return tools