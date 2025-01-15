import os
import shutil
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox, QApplication

class DllManager:
    def __init__(self):
        self.default_drives = ["C:\\", "D:\\", "E:\\", "K:\\"]  # Discos padrão para busca
        self.dll_folder = Path("Resources/Tools/dll")  # Repositório de DLLs
        self.game_paths = {
            "Half-Life 2": r"Half-Life 2\bin\hammerplusplus\bin",
            "Left 4 Dead 2": r"Left 4 Dead 2\bin\hammerplusplus\bin",
            "Team Fortress 2": r"Team Fortress 2\bin\hammerplusplus\bin",
            "Portal 2": r"Portal 2\bin\hammerplusplus\bin",
            "Garry's Mod": r"GarrysMod\bin\win64\hammerplusplus\bin",
            "Counter Strike Source": r"Counter-Strike Source\bin\hammerplusplus\bin",
            "Day of Defeat Source": r"Day of Defeat Source\bin\hammerplusplus\bin",
            "Source SDK Base 2013 Singleplayer": r"Source SDK Base 2013 Singleplayer\bin\hammerplusplus\bin",
            "Source SDK Base 2013 Multiplayer": r"Source SDK Base 2013 Multiplayer\bin\hammerplusplus\bin",
        }
        self.found_game_paths = {}

    def find_game_folders(self):
        # Busca os jogos nos discos padrão e atualiza os caminhos encontrados.
        self.found_game_paths.clear()  # Limpa os caminhos encontrados anteriormente

        for drive in self.default_drives:
            for game, relative_path in self.game_paths.items():
                # Regras especiais para o disco C
                if drive == "C:\\":
                    full_path = Path(drive) / "Program Files (x86)\\Steam\\steamapps\\common" / relative_path
                else:
                    full_path = Path(drive) / relative_path

                if full_path.exists() and full_path.is_dir():
                    self.found_game_paths[game] = str(full_path)
                    print(f"Encontrado: {game} em {full_path}")  # Log de depuração

    def set_user_defined_path(self, game, custom_path):
        # Define o caminho personalizado para o jogo especificado.
        custom_path = Path(custom_path)

        try:
            if not custom_path.exists():
                raise FileNotFoundError(f"O caminho especificado não existe: {custom_path}")

            # Verificar se a pasta do Hammer++ está presente
            hammer_path = self.find_hammer_path(game, custom_path)
            if hammer_path:
                self.found_game_paths[game] = str(hammer_path)
                print(f"Caminho personalizado definido para {game}: {hammer_path}")
            else:
                raise FileNotFoundError(
                    f"O caminho do Hammer++ não foi encontrado dentro da pasta do jogo selecionado: {custom_path}"
                )
        except FileNotFoundError as fnf_error:
            self.show_error_popup("Erro de Caminho", str(fnf_error))
        except Exception as e:
            self.show_error_popup("Erro Desconhecido", str(e))

    def find_hammer_path(self, game, custom_path):
        # Tenta encontrar o caminho do Hammer++ dentro da pasta do jogo.
        if game == "Garry's Mod":
            # Para o GMod, o caminho esperado inclui a pasta 'win64'
            possible_path = custom_path / "bin" / "win64" / "hammerplusplus" / "bin"
            if possible_path.exists() and possible_path.is_dir():
                return possible_path
        else:
            # Para os outros jogos, o caminho esperado é diretamente na pasta 'bin'
            possible_path = custom_path / "bin" / "hammerplusplus" / "bin"
            if possible_path.exists() and possible_path.is_dir():
                return possible_path
        return None

    def replace_dlls(self):
        # Substitui as DLLs nas pastas dos jogos encontrados.
        for game, folder_path in self.found_game_paths.items():
            source_dll = self.dll_folder / game / "hammerplusplus_dll.dll"
            target_dll = Path(folder_path) / "hammerplusplus_dll.dll"

            if source_dll.exists() and target_dll.parent.exists():
                try:
                    print(f"Tentando substituir DLL de {game} para {target_dll}")
                    shutil.copy2(source_dll, target_dll)
                    print(f"Substituído com sucesso: {target_dll}")
                except Exception as e:
                    print(f"Erro ao substituir DLL para {game}: {e}")
            else:
                if not source_dll.exists():
                    print(f"Arquivo DLL de origem não encontrado: {source_dll}")
                if not target_dll.parent.exists():
                    print(f"Pasta de destino não encontrada: {target_dll.parent}")

    @staticmethod
    def show_error_popup(title, message):
        # Exibe um pop-up de erro com o título e mensagem especificados.
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        QMessageBox.critical(None, title, message)
        # O programa continua rodando para permitir novas tentativas.


# Exemplo de uso
if __name__ == "__main__":
    manager = DllManager()
    manager.find_game_folders()  # Procura pastas dos jogos nos discos padrão

    # Exemplo de caminho personalizado
    while True:
        try:
            # Simula o usuário escolhendo a pasta do jogo
            user_input = input("Digite o caminho personalizado ou 'sair' para encerrar: ")
            if user_input.lower() == "sair":
                break
            manager.set_user_defined_path("Garry's Mod", user_input)  # Define o caminho personalizado para o GMod
        except Exception as e:
            print(f"Erro ao definir o caminho: {e}")

    manager.replace_dlls()  # Substitui as DLLs encontradas
