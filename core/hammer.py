import subprocess
import os
import sys
from pathlib import Path
from models.tool import Tool


def open_hammer(tool: Tool) -> tuple[bool, str]:
    """Abre o executável do Hammer++."""
    if not tool.install_path:
        return False, "Hammer++ não está instalado."

    exe = Path(tool.install_path)
    if not exe.exists():
        return False, f"Executável não encontrado: {exe}"

    try:
        subprocess.Popen(
            [str(exe)],
            cwd=str(exe.parent),
            creationflags=subprocess.DETACHED_PROCESS if sys.platform == "win32" else 0,
        )
        return True, "Hammer++ aberto com sucesso."
    except Exception as e:
        return False, f"Erro ao abrir: {e}"


def open_folder(tool: Tool) -> tuple[bool, str]:
    """Abre a pasta de instalação do Hammer++ no explorador de arquivos."""
    if not tool.install_path:
        return False, "Hammer++ não está instalado."

    folder = Path(tool.install_path).parent
    if not folder.exists():
        return False, f"Pasta não encontrada: {folder}"

    try:
        if sys.platform == "win32":
            os.startfile(str(folder))
        elif sys.platform == "linux":
            subprocess.Popen(["xdg-open", str(folder)])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(folder)])
        return True, "Pasta aberta."
    except Exception as e:
        return False, f"Erro ao abrir pasta: {e}"