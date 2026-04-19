import re
import urllib.request
import urllib.error
import zipfile
import shutil
import os
from pathlib import Path

DOWNLOAD_PAGE = "https://ficool2.github.io/HammerPlusPlus-Website/download.html"
GITHUB_BASE   = "https://github.com/ficool2/HammerPlusPlus-Website/releases/download"

CSGO_BUILD = "8864"

GAME_ZIP = {
    "gmod":      "hammerplusplus_gmod",
    "tf2":       "hammerplusplus_tf2",
    "portal"     "hammerplusplus_2013sp"   
    "portal2":   "hammerplusplus_portal2",
    "l4d2":      "hammerplusplus_l4d2",
    "css":       "hammerplusplus_tf2",
    "dods":      "hammerplusplus_tf2",
    "hl2":       "hammerplusplus_2013sp",
    "sdk2013sp": "hammerplusplus_2013sp",
    "sdk2013mp": "hammerplusplus_2013mp",
    "csgo":      "hammerplusplus_csgo",
}

def get_latest_build() -> str | None:
    """Busca o número do build mais recente na página oficial."""
    try:
        req = urllib.request.Request(
            DOWNLOAD_PAGE,
            headers={"User-Agent": "Hammerfy/0.1"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8")
        match = re.search(r"Current build version is:.*?(\d{4,})", html)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def get_download_url(game_id: str, build: str) -> str | None:
    """Monta a URL de download para um jogo e build específicos."""
    zip_name = GAME_ZIP.get(game_id)
    if not zip_name:
        return None
    actual_build = CSGO_BUILD if game_id == "csgo" else build
    return f"{GITHUB_BASE}/{actual_build}/{zip_name}_build{actual_build}.zip"

def download_and_install(
    game_id: str,
    build: str,
    install_path: str,
    progress_callback=None
) -> tuple[bool, str]:
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

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hammerfy/0.1"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            chunk_size = 8192
            with open(zip_path, "wb") as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total)

    except urllib.error.URLError as e:
        return False, f"Erro de conexão: {e}"
    except Exception as e:
        return False, f"Erro ao baixar: {e}"

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            members = z.namelist()

            # Descobre o prefixo até bin/win64/ ou bin/ dependendo do jogo
            bin_prefix = None
            for m in members:
                parts = Path(m).parts
                if "win64" in parts:
                    idx = list(parts).index("win64")
                    bin_prefix = str(Path(*parts[:idx + 1])) + "/"
                    break
                elif "bin" in parts and len(parts) >= 2:
                    idx = list(parts).index("bin")
                    bin_prefix = str(Path(*parts[:idx + 1])) + "/"

            if not bin_prefix:
                return False, "Estrutura do zip não reconhecida."

            # Extrai apenas o conteúdo dentro do bin_prefix para dest_folder
            for member in members:
                if not member.startswith(bin_prefix):
                    continue
                relative = member[len(bin_prefix):]
                if not relative:
                    continue
                target = dest_folder / relative
                if member.endswith("/"):
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
    return True, f"Hammer++ instalado em {dest_folder}"

def uninstall(install_path: str) -> tuple[bool, str]:
    folder = Path(install_path).parent

    if not folder.exists():
        return False, "Pasta não encontrada."

    hammer_files = [
        "hammerplusplus.exe",
        "hlmvplusplus.exe",
        "hlmvplusplus.dll",
        "hammerplusplus_dlls.dll",
        "hammerplusplus_filesystem_steam.dll",
        "hammerplusplus_settings.ini",
        "hammerplusplus_sequences.txt",
        "hammerplusplus_manifest.txt",
    ]

    hammer_folders = [
        "hammerplusplus",
    ]

    removed = 0
    try:
        for fname in hammer_files:
            fpath = folder / fname
            if fpath.exists():
                fpath.unlink()
                removed += 1

        for fname in hammer_folders:
            fpath = folder / fname
            if fpath.exists() and fpath.is_dir():
                shutil.rmtree(fpath)
                removed += 1

    except Exception as e:
        return False, f"Erro ao remover arquivos: {e}"

    if removed == 0:
        return False, "Nenhum arquivo do Hammer++ encontrado para remover."

    return True, f"{removed} itens removidos com sucesso."