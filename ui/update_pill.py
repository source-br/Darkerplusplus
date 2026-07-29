from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from utils.icons import load_icon
from utils import translator


class UpdatePillWidget(QWidget):
    """Pill-shaped update widget shown at the bottom of the sidebar.
    Displays yellow border on update notification, and interactive progress fill during download."""

    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        self.setCursor(Qt.PointingHandCursor)
        self._version = ""
        self._download_url = ""
        self._release_body = ""
        self._progress = 0  # 0 to 100
        self._is_downloading = False

        self._build_ui()
        self.setVisible(False)

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(6)

        self._icon_lbl = QLabel()
        self._icon_lbl.setFixedSize(16, 16)
        self._icon_lbl.setStyleSheet("background: transparent;")

        self._text_lbl = QLabel()
        self._text_lbl.setStyleSheet("font-size: 11px; font-weight: 600; color: #f0f0f0; background: transparent;")

        layout.addWidget(self._icon_lbl)
        layout.addWidget(self._text_lbl)
        layout.addStretch()

        self._update_icon()

    def _update_icon(self):
        icon_name = "download" if self._is_downloading else "circle-arrow-up"
        pix = load_icon(icon_name, color="#7c6be0", size=16).pixmap(16, 16)
        self._icon_lbl.setPixmap(pix)

    def set_update_info(self, version: str, download_url: str, release_body: str):
        self._version = version
        self._download_url = download_url
        self._release_body = release_body
        self._is_downloading = False
        self._progress = 0
        self._update_icon()
        self.refresh_text()
        self.setVisible(True)
        self.update()

    def set_progress(self, percentage: int):
        self._is_downloading = True
        self._progress = max(0, min(100, percentage))
        self._update_icon()
        self.refresh_text()
        self.update()

    def refresh_text(self):
        """Refreshes pill text on UI language change."""
        if not self._version:
            return
        if self._is_downloading:
            self._text_lbl.setText(translator.t("sidebar", "update_pill_downloading", pct=self._progress))
        else:
            ver = self._version if self._version.startswith("v") or self._version.startswith("V") else f"v{self._version}"
            self._text_lbl.setText(translator.t("sidebar", "update_pill", version=ver))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self._is_downloading and self.isVisible():
            self.clicked.emit()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        # Background color — transparent to match sidebar background
        bg_color = QColor(0, 0, 0, 0)
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 10, 10)

        # Progress fill overlay when downloading
        if self._is_downloading and self._progress > 0:
            fill_width = int(rect.width() * (self._progress / 100.0))
            fill_rect = rect.adjusted(0, 0, 0, 0)
            fill_rect.setWidth(fill_width)

            progress_color = QColor(124, 107, 224, 90)  # Semi-transparent brand purple #7c6be0
            painter.setBrush(QBrush(progress_color))
            painter.drawRoundedRect(fill_rect, 10, 10)

        # Border styling (brand purple border #7c6be0)
        border_pen = QPen(QColor("#7c6be0"), 1.5)
        painter.setPen(border_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 9, 9)
