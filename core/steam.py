import os
import struct
import re
from pathlib import Path


HAMMER_GAMES = {
    "Half-Life 2": {
        "id": "hl2",
        "name": "Hammer++ HL2",
        "engine": "Source",
        "bin": r"Half-Life 2\bin\hammerplusplus\bin",
        "exe": "hammerplusplus.exe",
        "banner_color": "#0e2210",
    },
    "Left 4 Dead 2": {
        "id": "l4d2",
        "name": "Hammer++ L4D2",
        "engine": "Source",
        "bin": r"Left 4 Dead 2\bin\hammerplusplus\bin",
        "exe": "hammerplusplus.exe",
        "banner_color": "#2a0808",
    },
    "Team Fortress 2": {
        "id": "tf2",
        "name": "Hammer++ TF2",
        "engine": "Source",
        "bin": r"Team Fortress 2\bin\x64\hammerplusplus\bin",
        "exe": "hammerplusplus.exe",
        "banner_color": "#3d1a08",
    },
    "Portal 2": {
        "id": "portal2",
        "name": "Hammer++ Portal 2",
        "engine": "Source",
        "bin": r"Portal 2\bin\hammerplusplus\bin",
        "exe": "hammerplusplus.exe",
        "banner_color": "#1a0e35",
    },
    "GarrysMod": {
        "id": "gmod",
        "name": "Hammer++ GMod",
        "engine": "Source",
        "bin": r"GarrysMod\bin\win64\hammerplusplus\bin",
        "exe": "hammerplusplus.exe",
        "banner_color": "#1a2e1a",
    },
    "Counter-Strike Source": {
        "id": "css",
        "name": "Hammer++ CS:S",
        "engine": "Source",
        "bin": r"Counter-Strike Source\bin\x64\hammerplusplus\bin",
        "exe": "hammerplusplus.exe",
        "banner_color": "#0a1a2a",
    },
    "Day of Defeat Source": {
        "id": "dods",
        "name": "Hammer++ DoDS",
        "engine": "Source",
        "bin": r"Day of Defeat Source\bin\x64\hammerplusplus\bin",
        "exe": "hammerplusplus.exe",
        "banner_color": "#1a1a08",
    },
    "Source SDK Base 2013 Singleplayer": {
        "id": "sdk2013sp",
        "name": "Hammer++ SDK 2013 SP",
        "engine": "Source",
        "bin": r"Source SDK Base 2013 Singleplayer\bin\hammerplusplus\bin",
        "exe": "hammerplusplus.exe",
        "banner_color": "#252508",
    },
    "Source SDK Base 2013 Multiplayer": {
        "id": "sdk2013mp",
        "name": "Hammer++ SDK 2013 MP",
        "engine": "Source",
        "bin": r"Source SDK Base 2013 Multiplayer\bin\hammerplusplus\bin",
        "exe": "hammerplusplus.exe",
        "banner_color": "#1a1408",
    },
    "Counter-Strike Global Offensive": {
        "id": "csgo",
        "name": "Hammer++ CS:GO",
        "engine": "Source",
        "bin": None,
        "exe": None,
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

        if game_path and game_info["bin"] and game_info["exe"]:
            bin_path = game_path / game_info["bin"]
            exe_path = bin_path / game_info["exe"]
            if exe_path.exists():
                is_installed = True
                hammer_exe = str(exe_path)
                version = get_hammer_version(exe_path)

        tools.append({
            "id":           game_info["id"],
            "name":         game_info["name"],
            "game":         game_folder_name,
            "engine":       game_info["engine"],
            "is_installed": is_installed,
            "install_path": hammer_exe,
            "version":      version,
            "banner_color": game_info["banner_color"],
            "bin_missing":  game_info["bin"] is None,
        })

    return tools