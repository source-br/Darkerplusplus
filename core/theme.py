import shutil
import re
from pathlib import Path


DARK_THEME = {
    # Base colors
    "White":              "220 220 220 255",
    "OffWhite":           "180 180 180 255",
    "DullWhite":          "150 150 150 255",
    "Orange":             "124 107 224 255",   # accent roxo do Hammerfy
    "TransparentBlack":   "0 0 0 180",
    "Black":              "0 0 0 255",
    "Blank":              "0 0 0 0",

    # UI structure
    "GameDarkBrown":              "24 24 24 255",
    "GameDarkBrownTransparent":   "24 24 24 210",
    "GameTanBright":              "60 60 65 255",
    "GameTanLight":               "50 50 55 255",
    "GameTanMedium":              "40 40 45 255",
    "GameTanLightDark":           "35 35 40 120",
    "GameOrangeBright":           "124 107 224 255",   # accent

    # Text
    "GameTextBright":             "220 220 225 255",
    "GameTextLight":              "180 180 185 255",
    "GameTextMedium":             "130 130 135 255",
    "GameTextMediumDark":         "90 90 95 255",
    "GameTextDull":               "100 100 105 255",

    # Lists and selection
    "QuickListBGDeselected":      "30 30 33 255",
    "QuickListBGSelected":        "50 50 55 200",
    "ControlBG":                  "32 32 36 255",
    "ControlDarkBG":              "26 26 30 255",
    "WindowBG":                   "20 20 23 255",
    "SelectionBG":                "60 55 100 255",
    "SelectionBG2":               "45 42 75 255",
    "ListBG":                     "18 18 21 255",

    # Steam achievement colors reused
    "AchievementsLightGrey":      "55 55 60 255",
    "AchievementsDarkGrey":       "35 35 38 255",
    "AchievementsInactiveFG":     "100 100 105 255",
    "SteamLightGreen":            "100 180 80 255",
}


def _parse_res(content: str) -> dict:
    """Extrai as cores atuais do .res como dict nome->valor."""
    colors = {}
    in_colors = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped == "Colors":
            in_colors = True
        elif in_colors and stripped == "{":
            continue
        elif in_colors and stripped == "}":
            in_colors = False
        elif in_colors:
            match = re.match(r'"([^"]+)"\s+"([^"]+)"', stripped)
            if match:
                colors[match.group(1)] = match.group(2)
    return colors


def _apply_colors(content: str, new_colors: dict) -> str:
    """Substitui os valores de cor no .res."""
    def replace_color(match):
        name = match.group(1)
        if name in new_colors:
            return f'"{name}"\t\t\t"{new_colors[name]}"'
        return match.group(0)

    return re.sub(r'"([^"]+)"\s+"(\d+ \d+ \d+ \d+)"', replace_color, content)


def apply_dark_theme(hammer_install_path: str) -> tuple[bool, str]:
    """
    Aplica o tema escuro ao Hammer++ editando o .res.
    Faz backup do original antes de modificar.
    """
    base = Path(hammer_install_path).parent
    res_path = base / "hammerplusplus" / "resource" / "hammerplusplus_scheme.res"

    if not res_path.exists():
        return False, f"Arquivo não encontrado: {res_path}"

    backup_path = res_path.with_suffix(".res.backup")

    try:
        # Backup do original se ainda não existe
        if not backup_path.exists():
            shutil.copy2(res_path, backup_path)

        content = res_path.read_text(encoding="utf-8", errors="ignore")
        modified = _apply_colors(content, DARK_THEME)
        res_path.write_text(modified, encoding="utf-8")

        return True, "Tema escuro aplicado com sucesso."
    except Exception as e:
        return False, f"Erro ao aplicar tema: {e}"


def restore_original_theme(hammer_install_path: str) -> tuple[bool, str]:
    """Restaura o tema original do backup."""
    base = Path(hammer_install_path).parent
    res_path = base / "hammerplusplus" / "resource" / "hammerplusplus_scheme.res"
    backup_path = res_path.with_suffix(".res.backup")

    if not backup_path.exists():
        return False, "Backup não encontrado. Tema original não pode ser restaurado."

    try:
        shutil.copy2(backup_path, res_path)
        return True, "Tema original restaurado."
    except Exception as e:
        return False, f"Erro ao restaurar tema: {e}"


def is_dark_theme_applied(hammer_install_path: str) -> bool:
    """Verifica se o tema escuro já está aplicado."""
    base = Path(hammer_install_path).parent
    backup_path = base / "hammerplusplus" / "resource" / "hammerplusplus_scheme.res.backup"
    return backup_path.exists()