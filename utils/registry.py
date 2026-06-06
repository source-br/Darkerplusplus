import sys

def read_value(hive, key_path: str, value_name: str) -> str | None:
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

def write_value(hive, key_path: str, value_name: str, value: str) -> bool:
    if sys.platform != "win32":
        return False
    try:
        import winreg
        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)
        return True
    except Exception:
        return False

def delete_value(hive, key_path: str, value_name: str) -> bool:
    if sys.platform != "win32":
        return False
    try:
        import winreg
        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, value_name)
        winreg.CloseKey(key)
        return True
    except Exception:
        return False