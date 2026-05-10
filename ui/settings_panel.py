from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                                QLabel, QCheckBox, QFrame)
from PySide6.QtCore import Qt, Signal
from utils import translator
from core.autostart import is_autostart_enabled, set_autostart
from core import tray_settings


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

        title = QLabel(translator.t("sidebar", "settings").upper())
        title.setStyleSheet("font-size: 10px; color: #555; letter-spacing: 1px;")
        layout.addWidget(title)

        layout.addSpacing(24)
        layout.addWidget(self._section("Sistema"))
        layout.addSpacing(12)
        layout.addWidget(self._build_system_options())
        layout.addStretch()
        self._building = False

    def _section(self, title):
        lbl = QLabel(title.upper())
        lbl.setStyleSheet("font-size: 10px; color: #555; letter-spacing: 1px;")
        return lbl

    def _build_system_options(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        settings = tray_settings.load()
        autostart = is_autostart_enabled()
        minimize_to_tray = settings["minimize_to_tray"]
        start_minimized = settings["start_minimized"]

        self.chk_autostart = self._checkbox(
            "Iniciar com o Windows",
            "O Hammerfy será iniciado automaticamente com o Windows.",
            autostart,
        )
        self.chk_tray = self._checkbox(
            "Minimizar para a tray",
            "Fechar a janela mantém o Hammerfy aberto em segundo plano.",
            minimize_to_tray or autostart,
        )
        self.chk_start_minimized = self._checkbox(
            "Iniciar minimizado",
            "O Hammerfy inicia sem abrir a janela.",
            start_minimized,
        )

        # Se autostart ativo, tray é obrigatório
        if autostart:
            self.chk_tray.setEnabled(False)

        self.chk_autostart.stateChanged.connect(self._on_autostart_changed)
        self.chk_tray.stateChanged.connect(self._on_tray_changed)
        self.chk_start_minimized.stateChanged.connect(self._on_start_minimized_changed)

        layout.addWidget(self.chk_autostart)
        layout.addWidget(self.chk_tray)
        layout.addWidget(self.chk_start_minimized)

        return widget

    def _checkbox(self, label: str, description: str, checked: bool) -> QCheckBox:
        chk = QCheckBox(label)
        chk.setChecked(checked)
        chk.setToolTip(description)
        chk.setStyleSheet("""
            QCheckBox {
                font-size: 12px;
                color: #c0c0c0;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #444;
                background: #1a1a1a;
            }
            QCheckBox::indicator:checked {
                background: #7c6be0;
                border-color: #7c6be0;
            }
            QCheckBox::indicator:hover {
                border-color: #7c6be0;
            }
        """)
        return chk

    def _on_autostart_changed(self, state):
        if self._building:
            return
        enabled = state == Qt.Checked
        set_autostart(enabled)
        if enabled:
            self.chk_tray.setChecked(True)
            self.chk_tray.setEnabled(False)
            tray_settings.set_value("minimize_to_tray", True)
        else:
            self.chk_tray.setEnabled(True)
        self.tray_setting_changed.emit()

    def _on_tray_changed(self, state):
        if self._building:
            return
        tray_settings.set_value("minimize_to_tray", state == Qt.Checked)
        self.tray_setting_changed.emit()

    def _on_start_minimized_changed(self, state):
        if self._building:
            return
        tray_settings.set_value("start_minimized", state == Qt.Checked)