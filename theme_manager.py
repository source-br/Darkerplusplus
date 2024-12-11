import shutil
import subprocess
from pathlib import Path

def install_and_apply_theme(repository_path):
    # Instala e aplica automaticamente o tema padrão, copiando também os arquivos de suporte necessários.
    theme_folder = Path(repository_path) / "Data" / "themes"
    theme_file = theme_folder / "Dark_1.theme"  # Arquivo principal do tema
    msstyles_folder = theme_folder / "Dark"
    windows_theme_folder = Path("C:\\Windows\\Resources\\Themes")

    # Verifica se o tema existe e tenta copiá-lo
    if theme_file.exists():
        try:
            # Copia o arquivo .theme
            shutil.copy2(theme_file, windows_theme_folder)
            print("Arquivo do tema copiado com sucesso.")

            # Copia a pasta do tema (com .msstyles e subpastas)
            destination_msstyles_folder = windows_theme_folder / "Dark"
            if msstyles_folder.exists():
                if destination_msstyles_folder.exists():
                    shutil.rmtree(destination_msstyles_folder)  # Remove a pasta anterior, se existir
                shutil.copytree(msstyles_folder, destination_msstyles_folder)
                print("Pasta do tema copiada com sucesso.")
            else:
                print("Pasta do tema não encontrada no repositório.")

            # Executa o arquivo .theme para aplicar o tema
            execute_theme()

        except Exception as e:
            print(f"Erro ao copiar os arquivos do tema: {e}")
    else:
        print("Arquivo do tema não encontrado no repositório.")

def execute_theme():
    try:
        windows_theme_folder = Path("C:\\Windows\\Resources\\Themes")
        theme_path = str(windows_theme_folder / "Dark_1.theme")
        if Path(theme_path).exists():
            # Usa subprocess para executar o arquivo .theme
            subprocess.run(["start", "", theme_path], shell=True, check=True)
            print("Arquivo .theme executado para aplicar o tema.")
        else:
            print("Arquivo do tema não encontrado na pasta do sistema.")
    except Exception as e:
        print(f"Erro ao executar o arquivo do tema: {e}")
