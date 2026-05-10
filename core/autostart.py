import sys
from pathlib import Path

AUTOSTART_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "Hammerfy"


def _get_exe_path() -> str:
    if getattr(sys, "frozen", False):
        return sys.executable
    return f'"{sys.executable}" "{Path(__file__).parent.parent / "main.py"}"'


def is_autostart_enabled() -> bool:
    from utils.registry import read_value
    import winreg
    val = read_value(winreg.HKEY_CURRENT_USER, AUTOSTART_KEY, APP_NAME)
    return val is not None


def set_autostart(enabled: bool) -> bool:
    import winreg
    from utils.registry import write_value, delete_value
    if enabled:
        return write_value(winreg.HKEY_CURRENT_USER, AUTOSTART_KEY, APP_NAME, _get_exe_path())
    else:
        return delete_value(winreg.HKEY_CURRENT_USER, AUTOSTART_KEY, APP_NAME)