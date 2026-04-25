import sys
import subprocess
import time
import ctypes
from pathlib import Path


def _find_hammer_hwnd(exe_name: str, timeout: int = 10) -> int | None:
    """Aguarda o Hammer++ abrir e retorna o HWND da janela principal."""
    if sys.platform != "win32":
        return None

    user32 = ctypes.windll.user32
    start = time.time()

    while time.time() - start < timeout:
        hwnd = user32.FindWindowW(None, None)
        # Enumera todas as janelas abertas
        found = []

        def enum_callback(hwnd, lparam):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                title = buf.value
                if "Hammer++" in title or "hammerplusplus" in title.lower():
                    found.append(hwnd)
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        callback = WNDENUMPROC(enum_callback)
        user32.EnumWindows(callback, 0)

        if found:
            return found[0]

        time.sleep(0.5)

    return None


def _apply_dark_mode_to_hwnd(hwnd: int):
    """Aplica modo escuro na barra de título e controles Win32."""
    if sys.platform != "win32":
        return

    try:
        # Escurece a barra de título via DWM
        dwmapi = ctypes.windll.dwmapi
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = ctypes.c_int(1)
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )

        # Ativa modo escuro nos controles via uxtheme funções não documentadas
        uxtheme = ctypes.windll.LoadLibrary("uxtheme.dll")

        # SetPreferredAppMode (ordinal 135) — ativa AllowDark globalmente
        set_preferred_app_mode = ctypes.WINFUNCTYPE(
            ctypes.c_int, ctypes.c_int
        )(("", uxtheme), ((1, "mode"),))

        try:
            _fn = ctypes.cast(
                ctypes.windll.kernel32.GetProcAddress(
                    ctypes.windll.kernel32.LoadLibraryW("uxtheme.dll"),
                    ctypes.c_char_p(135)
                ),
                ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
            )
            _fn(2)  # 2 = ForceDark
        except Exception:
            pass

        # AllowDarkModeForWindow (ordinal 133)
        try:
            _allow = ctypes.cast(
                ctypes.windll.kernel32.GetProcAddress(
                    ctypes.windll.kernel32.LoadLibraryW("uxtheme.dll"),
                    ctypes.c_char_p(133)
                ),
                ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_bool)
            )
            _allow(hwnd, True)
        except Exception:
            pass

        # SetWindowTheme — aplica DarkMode_Explorer nos controles filhos
        uxtheme_std = ctypes.windll.uxtheme
        uxtheme_std.SetWindowTheme(hwnd, "DarkMode_Explorer", None)

        # Força redraw
        user32 = ctypes.windll.user32
        user32.SendMessageW(hwnd, 0x0031, 0, 0)  # WM_THEMECHANGED
        user32.InvalidateRect(hwnd, None, True)

    except Exception as e:
        print(f"[Hammerfy] Erro ao aplicar dark mode: {e}")


def launch_hammer_dark(install_path: str) -> tuple[bool, str]:
    """
    Abre o Hammer++ e aplica dark mode na janela.
    Roda em thread separada para não travar a UI.
    """
    from PySide6.QtCore import QThread, Signal

    class LaunchThread(QThread):
        done = Signal(bool, str)

        def __init__(self, path):
            super().__init__()
            self.path = path

        def run(self):
            try:
                exe = Path(self.path)
                proc = subprocess.Popen(
                    [str(exe)],
                    cwd=str(exe.parent),
                    creationflags=subprocess.DETACHED_PROCESS
                )

                hwnd = _find_hammer_hwnd("hammerplusplus.exe", timeout=15)
                if hwnd:
                    time.sleep(0.5)  # aguarda janela renderizar
                    _apply_dark_mode_to_hwnd(hwnd)
                    self.done.emit(True, "Hammer++ aberto com dark mode.")
                else:
                    self.done.emit(True, "Hammer++ aberto (dark mode não aplicado).")
            except Exception as e:
                self.done.emit(False, str(e))

    return LaunchThread, None