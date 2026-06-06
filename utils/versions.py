import json
from pathlib import Path

VERSIONS_FILE = Path(__file__).parent.parent / "hammerplusplus_versions.json"

def save_version(game_id: str, build: str):
    """Salva o build instalado para um jogo."""
    data = _load()
    data[game_id] = build
    _save(data)

def get_version(game_id: str) -> str | None:
    """Retorna o build instalado para um jogo."""
    return _load().get(game_id)

def remove_version(game_id: str):
    """Remove o registro de versão ao desinstalar."""
    data = _load()
    if game_id in data:
        del data[game_id]
        _save(data)

def _load() -> dict:
    if VERSIONS_FILE.exists():
        try:
            return json.loads(VERSIONS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def _save(data: dict):
    VERSIONS_FILE.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

def get_tools_date() -> str | None:
    """Retorna a data de instalação das Tools++."""
    return _load().get("_tools_date")

def save_tools_date(date: str):
    """Salva a data de atualização das Tools++."""
    data = _load()
    data["_tools_date"] = date
    _save(data)
