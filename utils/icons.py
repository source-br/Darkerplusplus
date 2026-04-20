from pathlib import Path
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QSize
from PySide6.QtSvg import QSvgRenderer


ICONS_DIR = Path(__file__).parent.parent / "assets" / "icons"


def load_icon(name: str, color: str = "#aaaaaa", size: int = 16) -> QIcon:
    """Carrega um SVG como QIcon com a cor especificada."""
    path = ICONS_DIR / f"{name}.svg"
    if not path.exists():
        return QIcon()

    svg_content = path.read_text(encoding="utf-8")

    # Substitui a cor do stroke/fill pelo color desejado
    svg_content = svg_content.replace('stroke="currentColor"', f'stroke="{color}"')
    svg_content = svg_content.replace('fill="currentColor"', f'fill="{color}"')

    renderer = QSvgRenderer(svg_content.encode("utf-8"))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)