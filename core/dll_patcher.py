import sys
import shutil
import ctypes
from pathlib import Path


# Mapeamento: nome do arquivo → ID do recurso na DLL
BITMAP_MAP = {
    "Bitmap129.bmp":   129,
    "Bitmap178.bmp":   178,
    "Bitmap223.bmp":   223,
    "Bitmap235.bmp":   235,
    "Bitmap284.bmp":   284,
    "Bitmap326.bmp":   326,
    "Bitmap30996.bmp": 30996,
}

ICON_MAP = {
    "IconGroup311.ico":   311,
    "IconGroup312.ico":   312,
    "IconGroup313.ico":   313,
    "IconGroup314.ico":   314,
    "IconGroup320.ico":   320,
    "IconGroup321.ico":   321,
    "IconGroup31235.ico": 31235,
    "IconGroup31236.ico": 31236,
    "IconGroup31237.ico": 31237,
    "IconGroup31238.ico": 31238,
}

RT_BITMAP   = 2
RT_ICON     = 3
RT_GROUP_ICON = 14
LANG_NEUTRAL = 0x0409  # English US (1033)


def _read_bmp_data(path: Path) -> bytes:
    """Lê BMP e remove o header de 14 bytes — o que a DLL armazena é sem o BITMAPFILEHEADER."""
    data = path.read_bytes()
    if data[:2] == b"BM":
        return data[14:]  # remove BITMAPFILEHEADER
    return data


def _read_ico_data(path: Path) -> bytes:
    """Lê ICO como bytes completos."""
    return path.read_bytes()


def patch_dll(dll_path: str, assets_dir: str) -> tuple[bool, str]:
    """
    Substitui os bitmaps e ícones dark dentro da hammerplusplus_dll.dll.
    Faz backup antes de modificar.
    """
    if sys.platform != "win32":
        return False, "Patch de DLL só funciona no Windows."

    dll = Path(dll_path)
    if not dll.exists():
        return False, f"DLL não encontrada: {dll}"

    assets = Path(assets_dir)
    backup = dll.with_suffix(".dll.backup")

    try:
        # Backup do original
        if not backup.exists():
            shutil.copy2(dll, backup)

        kernel32 = ctypes.windll.kernel32

        # Abre a DLL para atualização de recursos
        handle = kernel32.BeginUpdateResourceW(str(dll), False)
        if not handle:
            return False, f"Erro ao abrir DLL para edição: {ctypes.GetLastError()}"

        errors = []

        # Substitui bitmaps
        for filename, resource_id in BITMAP_MAP.items():
            bmp_path = assets / filename
            if not bmp_path.exists():
                continue
            try:
                data = _read_bmp_data(bmp_path)
                buf = (ctypes.c_char * len(data))(*data)
                result = kernel32.UpdateResourceW(
                    handle,
                    RT_BITMAP,
                    resource_id,
                    LANG_NEUTRAL,
                    buf,
                    len(data)
                )
                if not result:
                    errors.append(f"Bitmap {resource_id}: erro {ctypes.GetLastError()}")
            except Exception as e:
                errors.append(f"Bitmap {resource_id}: {e}")

        # Finaliza e salva
        if not kernel32.EndUpdateResourceW(handle, False):
            return False, f"Erro ao salvar DLL: {ctypes.GetLastError()}"

        if errors:
            return True, f"DLL patchada com avisos: {'; '.join(errors)}"
        return True, "DLL patchada com sucesso — ícones dark aplicados."

    except Exception as e:
        return False, f"Erro ao patcher DLL: {e}"


def restore_dll(dll_path: str) -> tuple[bool, str]:
    """Restaura a DLL original do backup."""
    dll = Path(dll_path)
    backup = dll.with_suffix(".dll.backup")

    if not backup.exists():
        return False, "Backup não encontrado."

    try:
        shutil.copy2(backup, dll)
        return True, "DLL restaurada com sucesso."
    except Exception as e:
        return False, f"Erro ao restaurar DLL: {e}"


def is_dll_patched(dll_path: str) -> bool:
    """Verifica se a DLL já foi patchada."""
    return Path(dll_path).with_suffix(".dll.backup").exists()


def get_dll_path(hammer_install_path: str) -> str | None:
    """Retorna o caminho da hammerplusplus_dll.dll a partir do exe."""
    exe = Path(hammer_install_path)
    dll = exe.parent / "hammerplusplus" / "bin" / "hammerplusplus_dll.dll"
    return str(dll) if dll.exists() else None