from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QColor, QPainter
from utils import translator
from core.autostart import is_autostart_enabled, set_autostart
from core import tray_settings


# ─── Toggle Switch ─────────────────────────────────────────────────────────────

class ToggleSwitch(QWidget):
    """Animated toggle switch with smooth thumb sliding."""
    toggled = Signal(bool)

    def __init__(self, checked=False, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 22)
        self.setCursor(Qt.PointingHandCursor)
        self._checked = checked
        self._offset  = 18.0 if checked else 4.0

        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.InOutQuad)

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, val: bool):
        self._checked = val
        self._offset  = 18.0 if val else 4.0
        self.update()

    def setEnabled(self, val: bool):
        super().setEnabled(val)
        self.update()

    def mousePressEvent(self, event):
        if not self.isEnabled():
            return
        self._checked = not self._checked
        self._anim.stop()
        self._anim.setStartValue(self._offset)
        self._anim.setEndValue(18.0 if self._checked else 4.0)
        self._anim.start()
        self.toggled.emit(self._checked)

    def get_offset(self) -> float:
        return self._offset

    def set_offset(self, val: float):
        self._offset = val
        self.update()

    offset = Property(float, get_offset, set_offset)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        if not self.isEnabled():
            track_color = QColor("#2a2a2a")
            thumb_color = QColor("#444")
        elif self._checked:
            track_color = QColor("#7c6be0")
            thumb_color = QColor("#ffffff")
        else:
            track_color = QColor("#3a3a3a")
            thumb_color = QColor("#888888")

        p.setPen(Qt.NoPen)
        p.setBrush(track_color)
        p.drawRoundedRect(0, 3, 40, 16, 8, 8)

        p.setBrush(thumb_color)
        p.drawEllipse(int(self._offset), 1, 20, 20)


# ─── Setting Row ───────────────────────────────────────────────────────────────

class SettingRow(QWidget):
    """A labeled row with a description and a toggle switch.
    Exposes lbl and desc so the parent can update text on language change."""

    def __init__(self, label: str, description: str, checked: bool, enabled: bool = True, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(12)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        self.lbl = QLabel(label)
        self.lbl.setStyleSheet("font-size: 13px; color: #c0c0c0; background: transparent;")

        self.desc = QLabel(description)
        self.desc.setStyleSheet("font-size: 10px; color: #555; background: transparent;")

        text_col.addWidget(self.lbl)
        text_col.addWidget(self.desc)

        self.toggle = ToggleSwitch(checked=checked)
        self.toggle.setEnabled(enabled)

        layout.addLayout(text_col)
        layout.addStretch()
        layout.addWidget(self.toggle)


# ─── Settings Panel ────────────────────────────────────────────────────────────

class SettingsPanel(QWidget):
    tray_setting_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._building = False
        self._build_ui()

    def _build_ui(self):
        self._building = True
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        layout.addSpacing(24)

        self._section_lbl = self._section_label(translator.t("settings", "section_system"))
        layout.addWidget(self._section_lbl)
        layout.addSpacing(12)
        layout.addWidget(self._build_system_options())
        layout.addStretch()
        self._building = False

    def _section_label(self, text: str) -> QLabel:
        lbl = QLabel(text.upper())
        lbl.setStyleSheet("font-size: 10px; color: #555; letter-spacing: 1px;")
        return lbl

    def _build_system_options(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        settings     = tray_settings.load()
        autostart    = is_autostart_enabled()
        tray_enabled = settings.get("minimize_to_tray", True)
        start_min    = settings.get("start_minimized", False)

        self.row_autostart = SettingRow(
            translator.t("settings", "autostart_label"),
            translator.t("settings", "autostart_desc"),
            checked=autostart,
        )
        self.row_tray = SettingRow(
            translator.t("settings", "tray_label"),
            translator.t("settings", "tray_desc"),
            checked=tray_enabled or autostart,
            enabled=not autostart,
        )
        self.row_start_minimized = SettingRow(
            translator.t("settings", "start_minimized_label"),
            translator.t("settings", "start_minimized_desc"),
            checked=start_min,
        )

        self.row_autostart.toggle.toggled.connect(self._on_autostart_changed)
        self.row_tray.toggle.toggled.connect(self._on_tray_changed)
        self.row_start_minimized.toggle.toggled.connect(self._on_start_minimized_changed)

        layout.addWidget(self.row_autostart)
        layout.addWidget(self._divider())
        layout.addWidget(self.row_tray)
        layout.addWidget(self._divider())
        layout.addWidget(self.row_start_minimized)

        return widget

    def _divider(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #222; max-height: 1px;")
        return line

    def refresh_text(self):
        """Called when the UI language changes."""
        self._section_lbl.setText(translator.t("settings", "section_system").upper())
        self.row_autostart.lbl.setText(translator.t("settings", "autostart_label"))
        self.row_autostart.desc.setText(translator.t("settings", "autostart_desc"))
        self.row_tray.lbl.setText(translator.t("settings", "tray_label"))
        self.row_tray.desc.setText(translator.t("settings", "tray_desc"))
        self.row_start_minimized.lbl.setText(translator.t("settings", "start_minimized_label"))
        self.row_start_minimized.desc.setText(translator.t("settings", "start_minimized_desc"))

    # ─── Event Handlers ────────────────────────────────────────────────────────

    def _on_autostart_changed(self, enabled: bool):
        if self._building:
            return
        set_autostart(enabled)
        if enabled:
            self.row_tray.toggle.setChecked(True)
            self.row_tray.toggle.setEnabled(False)
            tray_settings.set_value("minimize_to_tray", True)
        else:
            self.row_tray.toggle.setEnabled(True)
        self.tray_setting_changed.emit()

    def _on_tray_changed(self, enabled: bool):
        if self._building:
            return
        tray_settings.set_value("minimize_to_tray", enabled)
        self.tray_setting_changed.emit()

    def _on_start_minimized_changed(self, enabled: bool):
        if self._building:
            return
        tray_settings.set_value("start_minimized", enabled)