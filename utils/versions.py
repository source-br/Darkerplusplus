import json
import sys
from pathlib import Path


def _get_data_dir() -> Path:
    """Returns the directory where data files should be stored.
    When frozen (PyInstaller), uses the exe's directory (Program Files\\Hammerfy).
    When running from source, uses the project root."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent


def _versions_file() -> Path:
    return _get_data_dir() / "hammerplusplus_versions.json"


def save_version(game_id: str, build: str):
    """Saves the installed build for a game."""
    data = _load()
    data[game_id] = build
    _save(data)


def get_version(game_id: str) -> str | None:
    """Returns the installed build for a game."""
    return _load().get(game_id)


def remove_version(game_id: str):
    """Removes the version record on uninstall."""
    data = _load()
    if game_id in data:
        del data[game_id]
        _save(data)


def _load() -> dict:
    f = _versions_file()
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save(data: dict):
    _versions_file().write_text(json.dumps(data, indent=2), encoding="utf-8")