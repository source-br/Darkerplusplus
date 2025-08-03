import os
import shutil
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox, QApplication
from utils import resource_path

class DllManager:
    def __init__(self):
        self.default_drives = ["C:\\", "D:\\", "E:\\", "K:\\"]  # Default drives for search
        self.dll_folder = Path(resource_path("Resources\Tools\dll"))  # DLL repository
        self.game_paths = {
            "Half-Life 2": r"Half-Life 2\bin\hammerplusplus\bin",
            "Left 4 Dead 2": r"Left 4 Dead 2\bin\hammerplusplus\bin",
            "Team Fortress 2": r"Team Fortress 2\bin\x64\hammerplusplus\bin",
            "Portal 2": r"Portal 2\bin\hammerplusplus\bin",
            "Garry's Mod": r"GarrysMod\bin\win64\hammerplusplus\bin",
            "Counter Strike Source": r"Counter-Strike Source\bin\x64\hammerplusplus\bin",
            "Day of Defeat Source": r"Day of Defeat Source\bin\x64\hammerplusplus\bin",
            "Source SDK Base 2013 Singleplayer": r"Source SDK Base 2013 Singleplayer\bin\hammerplusplus\bin",
            "Source SDK Base 2013 Multiplayer": r"Source SDK Base 2013 Multiplayer\bin\hammerplusplus\bin",
        }
        self.found_game_paths = {}

    def find_game_folders(self):
        # Searches for games in the default drives and updates the found paths.
        self.found_game_paths.clear()  # Clears previously found paths

        for drive in self.default_drives:
            for game, relative_path in self.game_paths.items():
                # Special rules for drive C
                if drive == "C:\\":
                    full_path = Path(drive) / "Program Files (x86)\\Steam\\steamapps\\common" / relative_path
                else:
                    full_path = Path(drive) / relative_path

                if full_path.exists() and full_path.is_dir():
                    self.found_game_paths[game] = str(full_path)
                    print(f"Encontrado: {game} em {full_path}")  # Debug log

    def set_user_defined_path(self, game, custom_path):
        # Sets a custom path for the specified game.
        custom_path = Path(custom_path)

        try:
            if not custom_path.exists():
                raise FileNotFoundError(f"The specified path does not exist: {custom_path}")

            # Check if the Hammer++ folder is present
            hammer_path = self.find_hammer_path(game, custom_path)
            if hammer_path:
                self.found_game_paths[game] = str(hammer_path)
                print(f"Custom path set for {game}: {hammer_path}")
            else:
                raise FileNotFoundError(
                    f"The Hammer++ path was not found inside the selected game folder: {custom_path}"
                )
        except FileNotFoundError as fnf_error:
            self.show_error_popup("Path Error", str(fnf_error))
        except Exception as e:
            self.show_error_popup("Unknown Error", str(e))

    def find_hammer_path(self, game, custom_path):
        # Attempts to find the Hammer++ path inside the game folder.
        if game == "Garry's Mod":
            possible_path = custom_path / "bin" / "win64" / "hammerplusplus" / "bin"
        elif game in ["Day of Defeat Source", "Team Fortress 2", "Counter Strike Source"]:
            possible_path = custom_path / "bin" / "x64" / "hammerplusplus" / "bin"
        else:
            possible_path = custom_path / "bin" / "hammerplusplus" / "bin"

        if possible_path.exists() and possible_path.is_dir():
            return possible_path
        return None

    def replace_dlls(self):
        # Replaces the DLLs in the found game folders.
        for game, folder_path in self.found_game_paths.items():
            source_dll = self.dll_folder / game / "hammerplusplus_dll.dll"
            target_dll = Path(folder_path) / "hammerplusplus_dll.dll"

            if source_dll.exists() and target_dll.parent.exists():
                try:
                    print(f"Attempting to replace DLL for {game} to {target_dll}")
                    shutil.copy2(source_dll, target_dll)
                    print(f"Successfully replaced: {target_dll}")
                except Exception as e:
                    print(f"Error replacing DLL for {game}: {e}")
            else:
                if not source_dll.exists():
                    print(f"Source DLL file not found: {source_dll}")
                if not target_dll.parent.exists():
                    print(f"Target folder not found: {target_dll.parent}")

    @staticmethod
    def show_error_popup(title, message):
        # Displays an error popup with the specified title and message.
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        QMessageBox.critical(None, title, message)
        # The program continues running to allow new attempts.


# Usage example
if __name__ == "__main__":
    manager = DllManager()
    manager.find_game_folders()  # Searches for game folders in the default drives

    # Example of custom path
    while True:
        try:
            # Simulates the user choosing the game folder
            user_input = input("Digite o caminho personalizado ou 'sair' para encerrar: ")
            if user_input.lower() == "sair":
                break
            manager.set_user_defined_path("Garry's Mod", user_input)  # Sets the custom path for GMod
        except Exception as e:
            print(f"Erro ao definir o caminho: {e}")

    manager.replace_dlls()  # Replaces the found DLLs
