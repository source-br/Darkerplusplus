import json
from pathlib import Path


SETTINGS_FILE = Path(__file__).parent.parent / "hammerfy_settings.json"

# Default values used when the settings file doesn't exist or is missing a key
DEFAULTS: dict = {
    "minimize_to_tray": True,
    "start_minimized":  False,
}


def load() -> dict:
    """Loads settings from disk, merging with defaults for any missing keys."""
    if SETTINGS_FILE.exists():
        try:
            saved = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            return {**DEFAULTS, **saved}
        except Exception:
            pass
    return dict(DEFAULTS)


def save(settings: dict):
    """Persists the full settings dict to disk."""
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")


def get(key: str):
    """Returns a single setting value by key."""
    return load().get(key, DEFAULTS.get(key))


def set_value(key: str, value):
    """Updates a single setting value and persists to disk."""
    data = load()
    data[key] = value
    save(data)