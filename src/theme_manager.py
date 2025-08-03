import shutil
import subprocess
from pathlib import Path
from utils import resource_path

def install_and_apply_theme(repository_path, windows_version):
    # Define the theme folder and files based on Windows version
    theme_folder = Path(resource_path("Resources")) / "themes"

    if windows_version == "Windows 10":
        theme_file = theme_folder / "Aerodark10.theme"
        msstyles_folder = theme_folder / "Aerodark10"
    elif windows_version == "Windows 11":
        theme_file = theme_folder / "Aerodark11.theme"
        msstyles_folder = theme_folder / "Aerodark11"
    else:
        print("Windows version not supported.")
        return

    windows_theme_folder = Path("C:\\Windows\\Resources\\Themes")

    # Check if the theme file exists
    if theme_file.exists():
        try:
            # Copy the theme file to the Windows theme folder
            shutil.copy2(theme_file, windows_theme_folder)
            print(f"Theme file ({theme_file.name}) copied successfully.")

            # Copy the msstyles folder to the Windows theme folder
            destination_msstyles_folder = windows_theme_folder / msstyles_folder.name
            if msstyles_folder.exists():
                if destination_msstyles_folder.exists():
                    shutil.rmtree(destination_msstyles_folder)
                shutil.copytree(msstyles_folder, destination_msstyles_folder)
                print(f"Theme folder ({msstyles_folder.name}) copied successfully.")
            else:
                print("Theme folder not found in the repository.")

            # Execute the theme to apply it
            execute_theme(windows_version)

        except Exception as e:
            # Handle errors during theme file copying
            print(f"Error copying theme files: {e}")
    else:
        # Handle missing theme file in the repository
        print("Theme file not found in the repository.")

def execute_theme(windows_version):
    # Execute the theme file to apply the theme
    try:
        windows_theme_folder = Path("C:\\Windows\\Resources\\Themes")
        theme_file = f"Aerodark10.theme" if windows_version == "Windows 10" else "Aerodark11.theme"
        theme_path = str(windows_theme_folder / theme_file)

        if Path(theme_path).exists():
            # Run the theme file using subprocess
            subprocess.run(["start", "", theme_path], shell=True, check=True)
            print(f".theme file ({theme_file}) executed to apply the theme.")
        else:
            # Handle missing theme file in the system folder
            print("Theme file not found in the system folder.")
    except Exception as e:
        # Handle errors during theme execution
        print(f"Error executing theme file: {e}")
