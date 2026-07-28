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


def check_for_update(include_beta: bool = True) -> tuple[bool, str, str]:
    """Returns (has_update, latest_version, download_url)."""
    release = get_latest_release(include_beta=include_beta)
    if not release:
        return False, "", ""

    latest  = release.get("tag_name", "").strip()
    current = get_version().strip()

    if current.lower() == "dev":
        return False, latest, ""

    latest_norm  = latest.lstrip("vV").strip()
    current_norm = current.lstrip("vV").strip()

    if latest_norm == current_norm:
        return False, latest, ""

    # Find the Setup installer asset
    for asset in release.get("assets", []):
        if "Setup" in asset["name"] and asset["name"].endswith(".exe"):
            return True, latest, asset["browser_download_url"]

    return False, latest, ""


def download_and_run_installer(url: str, version: str) -> bool:
    """Downloads the installer and launches it with silent flags, allowing automatic installation."""
    try:
        dest = Path.home() / "Downloads" / f"Hammerfy-Setup-{version}.exe"
        req  = urllib.request.Request(url, headers={"User-Agent": "Hammerfy/0.1"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.write_bytes(resp.read())

        # Launch installer with flags to run automatically and handle running application files
        subprocess.Popen([str(dest), "/SILENT", "/CLOSEAPPLICATIONS"])
        return True
    except Exception:
        return False