from dataclasses import dataclass
from enum import Enum

class ToolStatus(Enum):
    INSTALLED = "installed"
    AVAILABLE = "available"
    UPDATE_AVAILABLE = "update_available"

@dataclass
class Tool:
    id: str                  # ex: "tf2", "cs2", "l4d2"
    name: str                # ex: "Hammer++ TF2"
    game: str                # ex: "Team Fortress 2"
    engine: str              # ex: "Source", "Source 2"
    hammer_type: str
    version_installed: str | None
    version_latest: str | None
    install_path: str | None
    status: ToolStatus
    banner_color: str        # cor hex para o banner do card