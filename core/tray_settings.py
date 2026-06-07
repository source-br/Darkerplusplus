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


def _settings_file() -> Path:
    return _get_data_dir() / "hammerfy_settings.json"


DEFAULTS: dict = {
    "minimize_to_tray": True,
    "start_minimized":  False,
    "language":         "",
}


def load() -> dict:
    """Loads settings from disk, merging with defaults for any missing keys."""
    f = _settings_file()
    if f.exists():
        try:
            saved = json.loads(f.read_text(encoding="utf-8"))
            return {**DEFAULTS, **saved}
        except Exception:
            pass
    return dict(DEFAULTS)


def save(settings: dict):
    """Persists the full settings dict to disk."""
    _settings_file().write_text(json.dumps(settings, indent=2), encoding="utf-8")


def get(key: str):
    """Returns a single setting value by key."""
    return load().get(key, DEFAULTS.get(key))


def set_value(key: str, value):
    """Updates a single setting value and persists to disk."""
    data = load()
    data[key] = value
    save(data)