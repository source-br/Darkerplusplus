import sys
import winreg
from pathlib import Path
from utils.registry import read_value, write_value, delete_value


AUTOSTART_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME      = "Hammerfy"


def _get_exe_path() -> str:
    """Returns the correct executable path for the autostart registry entry.
    When frozen by PyInstaller, sys.executable is the .exe directly.
    When running from source, we build a quoted command: python main.py."""
    if getattr(sys, "frozen", False):
        # PyInstaller sets sys.frozen = True — sys.executable is the compiled .exe
        return f'"{sys.executable}"'
    return f'"{sys.executable}" "{Path(__file__).parent.parent / "main.py"}"'


def is_autostart_enabled() -> bool:
    """Returns True if Hammerfy is registered to run on Windows startup."""
    if sys.platform != "win32":
        return False
    val = read_value(winreg.HKEY_CURRENT_USER, AUTOSTART_KEY, APP_NAME)
    return val is not None


def set_autostart(enabled: bool) -> bool:
    """Adds or removes Hammerfy from the Windows startup registry key."""
    if sys.platform != "win32":
        return False
    if enabled:
        return write_value(winreg.HKEY_CURRENT_USER, AUTOSTART_KEY, APP_NAME, _get_exe_path())
    else:
        return delete_value(winreg.HKEY_CURRENT_USER, AUTOSTART_KEY, APP_NAME)