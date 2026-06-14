import subprocess
import os
import sys
from pathlib import Path
from models.tool import Tool


def open_hammer(tool: Tool) -> tuple[bool, str]:
    """Opens the Hammer++ executable for the given tool."""
    if not tool.install_path:
        return False, "Hammer++ não está instalado."

    exe = Path(tool.install_path)
    if not exe.exists():
        return False, f"Executável não encontrado: {exe}"

    bin_dir = exe.parent
    if (bin_dir / "hammerplusplus").exists():
        cwd = bin_dir
    elif (bin_dir.parent / "hammerplusplus").exists():
        cwd = bin_dir.parent
    else:
        cwd = bin_dir

    try:
        kwargs = {"cwd": str(cwd)}

        # Debugging aid: write a small pre-launch check file next to the exe
        try:
            dbg = exe.parent / "hammerfy_launch_debug.txt"
            with open(dbg, "w", encoding="utf-8") as f:
                f.write(f"exe={exe}\n")
                f.write(f"cwd={cwd}\n")
                f.write("exists_exe=" + str(exe.exists()) + "\n")
                f.write("listing=\n")
                for p in sorted([str(x) for x in exe.parent.iterdir()]):
                    f.write(p + "\n")
                # try to detect common hammer dlls
                for dll in ("hammerplusplus_dlls.dll", "hammerplusplus_filesystem_steam.dll"):
                    f.write(dll + ": " + str((exe.parent / dll).exists()) + "\n")
        except Exception:
            pass

        if sys.platform == "win32":
            # CREATE_NEW_PROCESS_GROUP allows Hammer++ to spawn child compiler
            # processes (vbsp, vvis, vrad) correctly without inheriting our handles
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
            kwargs["close_fds"]     = True

        subprocess.Popen([str(exe)], **kwargs)
        return True, "Hammer++ aberto com sucesso."
    except Exception as e:
        return False, f"Erro ao abrir: {e}"


def open_folder(tool: Tool) -> tuple[bool, str]:
    """Opens the Hammer++ installation folder in the system file explorer."""
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