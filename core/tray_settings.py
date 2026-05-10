import json
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent.parent / "hammerfy_settings.json"

DEFAULTS = {
    "minimize_to_tray": True,
    "start_minimized": False,
}

def load() -> dict:
    if SETTINGS_FILE.exists():
        try:
            return {**DEFAULTS, **json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))}
        except Exception:
            pass
    return dict(DEFAULTS)

def save(settings: dict):
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")

def get(key: str):
    return load().get(key, DEFAULTS.get(key))

def set_value(key: str, value):
    data = load()
    data[key] = value
    save(data)