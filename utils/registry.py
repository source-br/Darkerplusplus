import sys

def read_value(hive, key_path: str, value_name: str) -> str | None:
    """Lê um valor do registro do Windows. Retorna None fora do Windows."""
    if sys.platform != "win32":
        return None
    try:
        import winreg
        key = winreg.OpenKey(hive, key_path)
        value, _ = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return value
    except Exception:
        return None