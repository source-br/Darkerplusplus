import subprocess
import os
import sys
from pathlib import Path
from models.tool import Tool
from core.theme import is_dark_theme_applied
from core.launcher import launch_hammer_dark


def open_hammer(tool):
    if not tool.install_path:
        return False, "Hammer++ não está instalado."

    exe = Path(tool.install_path)
    if not exe.exists():
        return False, f"Executável não encontrado: {exe}"

    # Se tema escuro está ativo, usa o launcher com injeção de dark mode
    if sys.platform == "win32" and is_dark_theme_applied(tool.install_path):
        LaunchThread, _ = launch_hammer_dark(tool.install_path)
        thread = LaunchThread(tool.install_path)
        thread.start()
        return True, "Abrindo Hammer++ com dark mode..."

    # Fallback — abre normalmente
    try:
        subprocess.Popen(
            [str(exe)],
            cwd=str(exe.parent),
            creationflags=subprocess.DETACHED_PROCESS if sys.platform == "win32" else 0,
        )
        return True, "Hammer++ aberto."
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