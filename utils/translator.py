import json
from pathlib import Path

LOCALES_DIR = Path(__file__).parent.parent / "locales"

_current: dict = {}
_lang: str = "en"


def load(lang: str):
    global _current, _lang
    path = LOCALES_DIR / f"{lang}.json"
    if not path.exists():
        return
    _current = json.loads(path.read_text(encoding="utf-8"))
    _lang = lang


def t(section: str, key: str, **kwargs) -> str:
    """Retorna a string traduzida. Suporta placeholders via kwargs."""
    try:
        text = _current[section][key]
        if kwargs:
            text = text.format(**kwargs)
        return text
    except (KeyError, AttributeError):
        return f"{section}.{key}"


def current_lang() -> str:
    return _lang


# Carrega inglês por padrão
load("en")