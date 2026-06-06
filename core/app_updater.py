import urllib.request
import json
import sys
import subprocess
import os
from pathlib import Path


RELEASES_API = "https://api.github.com/repos/kenned-candido/hammerfy/releases/latest"
_HEADERS     = {"User-Agent": "Hammerfy/0.1", "Accept": "application/vnd.github+json"}

# Version defined at build time by PyInstaller via hammerfy.spec
CURRENT_VERSION = os.environ.get("HAMMERFY_VERSION", "dev")

def get_latest_release() -> dict | None:
    """Fetches the latest release info from GitHub."""
    try:
        req = urllib.request.Request(RELEASES_API, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def check_for_update() -> tuple[bool, str, str]:
    """Returns (has_update, latest_version, download_url)."""
    release = get_latest_release()
    if not release:
        return False, "", ""

    latest  = release.get("tag_name", "")
    if latest == CURRENT_VERSION:
        return False, latest, ""

    # Find the Setup installer asset
    for asset in release.get("assets", []):
        if "Setup" in asset["name"] and asset["name"].endswith(".exe"):
            return True, latest, asset["browser_download_url"]

    return False, latest, ""


def download_and_run_installer(url: str, version: str) -> bool:
    """Downloads the installer and launches it, then exits the app."""
    try:
        dest = Path.home() / "Downloads" / f"Hammerfy-Setup-{version}.exe"
        req  = urllib.request.Request(url, headers={"User-Agent": "Hammerfy/0.1"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.write_bytes(resp.read())

        # Launch installer and exit — installer will restart the app if user chooses
        subprocess.Popen([str(dest)])
        return True
    except Exception:
        return False