import shutil
import subprocess
from pathlib import Path

def install_and_apply_theme(repository_path, windows_version):
    theme_folder = Path(repository_path) / "Resources" / "themes"

    if windows_version == "Windows 10":
        theme_file = theme_folder / "Aerodark10.theme"
        msstyles_folder = theme_folder / "Aerodark10"
    elif windows_version == "Windows 11":
        theme_file = theme_folder / "Aerodark11.theme"
        msstyles_folder = theme_folder / "Aerodark11"
    else:
        print("Versão do Windows não suportada.")
        return

    windows_theme_folder = Path("C:\\Windows\\Resources\\Themes")

    if theme_file.exists():
        try:
            shutil.copy2(theme_file, windows_theme_folder)
            print(f"Arquivo do tema ({theme_file.name}) copiado com sucesso.")

            destination_msstyles_folder = windows_theme_folder / msstyles_folder.name
            if msstyles_folder.exists():
                if destination_msstyles_folder.exists():
                    shutil.rmtree(destination_msstyles_folder)
                shutil.copytree(msstyles_folder, destination_msstyles_folder)
                print(f"Pasta do tema ({msstyles_folder.name}) copiada com sucesso.")
            else:
                print("Pasta do tema não encontrada no repositório.")

            execute_theme(windows_version)

        except Exception as e:
            print(f"Erro ao copiar os arquivos do tema: {e}")
    else:
        print("Arquivo do tema não encontrado no repositório.")

def execute_theme(windows_version):
    try:
        windows_theme_folder = Path("C:\\Windows\\Resources\\Themes")
        theme_file = f"Aerodark10.theme" if windows_version == "Windows 10" else "Aerodark11.theme"
        theme_path = str(windows_theme_folder / theme_file)

        if Path(theme_path).exists():
            subprocess.run(["start", "", theme_path], shell=True, check=True)
            print(f"Arquivo .theme ({theme_file}) executado para aplicar o tema.")
        else:
            print("Arquivo do tema não encontrado na pasta do sistema.")
    except Exception as e:
        print(f"Erro ao executar o arquivo do tema: {e}")
        