import re
import urllib.request
import urllib.error
import zipfile
import shutil
from pathlib import Path
from utils.versions import save_version, remove_version


DOWNLOAD_PAGE = "https://ficool2.github.io/HammerPlusPlus-Website/download.html"
GITHUB_BASE   = "https://github.com/ficool2/HammerPlusPlus-Website/releases/download"

CSGO_BUILD = "8864"

GAME_ZIP = {
    "gmod":      "hammerplusplus_gmod",
    "tf2":       "hammerplusplus_tf2",
    "portal1":    "hammerplusplus_2013sp",
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
    """
    Baixa e instala o Hammer++ para um jogo.
    install_path: caminho completo até a pasta bin do jogo
                  ex: C:/Steam/steamapps/common/GarrysMod/bin/win64
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

    # Download
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
        zip_path.unlink(missing_ok=True)
        return False, f"Erro de conexão: {e}"
    except Exception as e:
        zip_path.unlink(missing_ok=True)
        return False, f"Erro ao baixar: {e}"

    # Extração — mescla conteúdo de bin/win64/ (ou bin/) com dest_folder
    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            members = z.namelist()

            # Descobre o prefixo até bin/ dentro do zip
            bin_prefix = None
            for m in members:
                parts = Path(m.replace("\\", "/")).parts
                if "bin" in parts:
                    idx = list(parts).index("bin")
                    bin_prefix = "/".join(parts[:idx + 1]) + "/"
                    break

            if not bin_prefix:
                zip_path.unlink(missing_ok=True)
                return False, "Estrutura do zip não reconhecida."

            # Copia cada arquivo do zip para dest_folder mantendo subpastas
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
    save_version(game_id, build)
    return True, f"Hammer++ instalado em {dest_folder}"


def uninstall(install_path: str, game_id: str) -> tuple[bool, str]:
    """
    Remove os arquivos do Hammer++ de uma instalação.
    Remove apenas arquivos conhecidos, não a pasta inteira do jogo.
    """
    folder = Path(install_path).parent
    if not folder.exists():
        return False, "Pasta não encontrada."

    hammer_files = [
        "hammerplusplus.exe",
        "hammerplusplus_dlls.dll",
        "hammerplusplus_filesystem_steam.dll",
        "hammerplusplus_settings.ini",
        "hammerplusplus_sequences.txt",
        "hammerplusplus_manifest.txt",
        "hlmvplusplus.exe",
        "hlmvplusplus.dll",
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

    # Descobre o game_id pelo install_path — passa como parâmetro
    remove_version(game_id)
    return True, f"{removed} itens removidos com sucesso."
