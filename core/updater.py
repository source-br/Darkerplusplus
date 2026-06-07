import urllib.request
import urllib.error
import zipfile
import json
import shutil
from pathlib import Path
from utils.versions import save_version, remove_version


# ─── Constants ─────────────────────────────────────────────────────────────────

GITHUB_API  = "https://api.github.com/repos/ficool2/HammerPlusPlus-Website/releases/latest"
GITHUB_BASE = "https://github.com/ficool2/HammerPlusPlus-Website/releases/download"

# CS:GO build is frozen — no further updates will ever be released
CSGO_BUILD = "8864"

# Maps game_id to the zip name used in the GitHub release assets
GAME_ZIP = {
    "gmod":      "hammerplusplus_gmod",
    "tf2":       "hammerplusplus_tf2",
    "css":       "hammerplusplus_tf2",
    "dods":      "hammerplusplus_tf2",
    "hl2":       "hammerplusplus_2013sp",
    "l4d2":      "hammerplusplus_l4d2",
    "portal1":   "hammerplusplus_2013sp",
    "portal2":   "hammerplusplus_portal2",
    "sdk2013sp": "hammerplusplus_2013sp",
    "sdk2013mp": "hammerplusplus_2013mp",
    "csgo":      "hammerplusplus_csgo",
}

# Known Hammer++ files — only these are removed on uninstall, never the full game folder
HAMMER_FILES = [
    "hammerplusplus.exe",
    "hammerplusplus_dlls.dll",
    "hammerplusplus_filesystem_steam.dll",
    "hammerplusplus_settings.ini",
    "hammerplusplus_sequences.txt",
    "hammerplusplus_manifest.txt",
    "hlmvplusplus.exe",
    "hlmvplusplus.dll",
]

HAMMER_FOLDERS = [
    "hammerplusplus",
]

_HEADERS = {
    "User-Agent": "Hammerfy/0.1",
    "Accept":     "application/vnd.github+json",
}


# ─── GitHub API ────────────────────────────────────────────────────────────────

def get_latest_build() -> str | None:
    """Fetches the latest Hammer++ build tag from the GitHub releases API."""
    try:
        req = urllib.request.Request(GITHUB_API, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("tag_name")
    except Exception:
        return None


def get_download_url(game_id: str, build: str) -> str | None:
    """Builds the direct download URL for a given game and build."""
    zip_name = GAME_ZIP.get(game_id)
    if not zip_name:
        return None
    # CS:GO always uses its frozen build regardless of the latest
    actual_build = CSGO_BUILD if game_id == "csgo" else build
    return f"{GITHUB_BASE}/{actual_build}/{zip_name}_build{actual_build}.zip"


# ─── Install ───────────────────────────────────────────────────────────────────

def download_and_install(
    game_id: str,
    build: str,
    install_path: str,
    progress_callback=None,
) -> tuple[bool, str]:
    """Downloads and extracts Hammer++ into the game's bin folder.

    install_path: path to the game's bin folder (e.g. GarrysMod/bin)
    progress_callback: optional callable(downloaded_bytes, total_bytes)
    """
    url = get_download_url(game_id, build)
    if not url:
        return False, f"Jogo '{game_id}' não suportado."

    dest_folder = Path(install_path)
    if not dest_folder.exists():
        try:
            dest_folder.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return False, f"Não foi possível criar a pasta: {e}"

    zip_path = dest_folder / "hammerplusplus_temp.zip"

    # Download with optional progress reporting
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hammerfy/0.1"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            total      = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            with open(zip_path, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total)
    except urllib.error.URLError as e:
        zip_path.unlink(missing_ok=True)
        return False, f"Erro de conexão: {e}"
    except Exception as e:
        zip_path.unlink(missing_ok=True)
        return False, f"Erro ao baixar: {e}"

    # Extract — find the bin/ prefix inside the zip and merge into dest_folder
    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            members = z.namelist()

            # Locate the bin/ prefix to strip it during extraction
            # For games with bin/x64/ structure, we need to strip up to and including x64/
            bin_prefix = None
            for m in members:
                norm = m.replace("\\", "/")
                if norm.endswith("hammerplusplus.exe"):
                    bin_prefix = norm[: norm.rfind("/") + 1] if "/" in norm else ""
                    break

            # Fallback: strip up to bin/ if exe not found
            if bin_prefix is None:
                for m in members:
                    parts = Path(m.replace("\\", "/")).parts
                    if "bin" in parts:
                        idx        = list(parts).index("bin")
                        bin_prefix = "/".join(parts[:idx + 1]) + "/"
                        break

            if not bin_prefix:
                zip_path.unlink(missing_ok=True)
                return False, "Estrutura do zip não reconhecida."

            for member in members:
                norm = member.replace("\\", "/")
                if not norm.startswith(bin_prefix):
                    continue
                relative = norm[len(bin_prefix):]
                if not relative:
                    continue
                target = dest_folder / relative
                if norm.endswith("/"):
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(member) as src, open(target, "wb") as dst:
                        shutil.copyfileobj(src, dst)

    except zipfile.BadZipFile:
        zip_path.unlink(missing_ok=True)
        return False, "Arquivo baixado está corrompido."
    except Exception as e:
        zip_path.unlink(missing_ok=True)
        return False, f"Erro ao extrair: {e}"

    zip_path.unlink(missing_ok=True)

    # Save the actual installed build (CS:GO uses its frozen build, not latest)
    actual_build = CSGO_BUILD if game_id == "csgo" else build
    save_version(game_id, actual_build)

    return True, f"Hammer++ instalado em {dest_folder}"


# ─── Uninstall ─────────────────────────────────────────────────────────────────

def uninstall(install_path: str, game_id: str) -> tuple[bool, str]:
    """Removes only known Hammer++ files — never touches the full game folder."""
    folder = Path(install_path).parent
    if not folder.exists():
        return False, "Pasta não encontrada."

    removed = 0
    try:
        for fname in HAMMER_FILES:
            fpath = folder / fname
            if fpath.exists():
                fpath.unlink()
                removed += 1

        for fname in HAMMER_FOLDERS:
            fpath = folder / fname
            if fpath.exists() and fpath.is_dir():
                shutil.rmtree(fpath)
                removed += 1

    except Exception as e:
        return False, f"Erro ao remover arquivos: {e}"

    if removed == 0:
        return False, "Nenhum arquivo do Hammer++ encontrado para remover."

    remove_version(game_id)
    return True, f"{removed} itens removidos com sucesso."