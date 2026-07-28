import urllib.request
import json
import sys
import subprocess
import os
from pathlib import Path


from core.version import get_version

RELEASES_LATEST_API = "https://api.github.com/repos/kenned-candido/hammerfy/releases/latest"
RELEASES_LIST_API   = "https://api.github.com/repos/kenned-candido/hammerfy/releases"
_HEADERS            = {"User-Agent": "Hammerfy/0.1", "Accept": "application/vnd.github+json"}


def get_latest_release(include_beta: bool = True) -> dict | None:
    """Fetches the latest release info from GitHub.
    If include_beta is True, fetches all releases and returns the newest one (including pre-releases).
    If False, fetches only official stable releases via /releases/latest."""
    try:
        url = RELEASES_LIST_API if include_beta else RELEASES_LATEST_API
        req = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if include_beta and isinstance(data, list):
                return data[0] if data else None
            return data if isinstance(data, dict) else None
    except Exception:
        return None


def check_for_update(include_beta: bool = True) -> tuple[bool, str, str, str]:
    """Returns (has_update, latest_version, download_url, release_body)."""
    release = get_latest_release(include_beta=include_beta)
    if not release:
        return False, "", "", ""

    latest  = release.get("tag_name", "").strip()
    body    = release.get("body", "").strip()
    current = get_version().strip()

    if current.lower() == "dev":
        return False, latest, "", body

    latest_norm  = latest.lstrip("vV").strip()
    current_norm = current.lstrip("vV").strip()

    if latest_norm == current_norm:
        return False, latest, "", body

    # Find the Setup installer asset
    for asset in release.get("assets", []):
        if "Setup" in asset["name"] and asset["name"].endswith(".exe"):
            return True, latest, asset["browser_download_url"], body

    return False, latest, "", body


def download_and_run_installer(url: str, version: str, progress_callback=None) -> bool:
    """Downloads the installer with progress callback and launches it with silent flags."""
    try:
        dest = Path.home() / "Downloads" / f"Hammerfy-Setup-{version}.exe"
        req  = urllib.request.Request(url, headers={"User-Agent": "Hammerfy/0.1"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            chunk_size = 64 * 1024
            with open(dest, "wb") as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0 and progress_callback:
                        pct = int(downloaded / total * 100)
                        progress_callback(pct)

        # Clean PyInstaller environment variables to prevent child installer / new app
        # from inheriting the old instance's temporary _MEIPASS folder and failing with 'Failed to load Python DLL'.
        env = os.environ.copy()
        meipass = getattr(sys, "_MEIPASS", None)
        env.pop("_MEIPASS", None)
        env.pop("_MEIPASS2", None)

        if meipass and "PATH" in env:
            paths = env["PATH"].split(os.pathsep)
            paths = [p for p in paths if p.rstrip("\\/") != meipass.rstrip("\\/")]
            env["PATH"] = os.pathsep.join(paths)

        # Launch installer with flags to run automatically and handle running application files
        subprocess.Popen([str(dest), "/SILENT", "/CLOSEAPPLICATIONS"], env=env)
        return True
    except Exception:
        return False


def cleanup_downloaded_installers():
    """Removes leftover Hammerfy-Setup-*.exe installers from Downloads folder."""
    try:
        downloads = Path.home() / "Downloads"
        if downloads.exists():
            for installer in downloads.glob("Hammerfy-Setup-*.exe"):
                try:
                    installer.unlink()
                except Exception:
                    pass
    except Exception:
        pass