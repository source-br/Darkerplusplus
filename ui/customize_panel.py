from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                                QLabel, QPushButton, QWidget, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from pathlib import Path
from utils import translator


class CustomizeDialog(QDialog):
    def __init__(self, tool, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.setWindowTitle(f"Customize — {tool.name}")
        self.setFixedWidth(480)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
        """)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Título
        title = QLabel(f"Customize {self.tool.name}")
        title.setStyleSheet("font-size: 16px; font-weight: 600; color: #f0f0f0;")
        layout.addWidget(title)

        layout.addWidget(self._divider())
        layout.addWidget(self._build_dark_theme_section())
        layout.addWidget(self._divider())
        layout.addStretch()
        layout.addWidget(self._build_footer())

    def _build_dark_theme_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Header da seção
        header = QHBoxLayout()
        icon_lbl = QLabel()
        from utils.icons import load_icon
        icon_lbl.setPixmap(load_icon("moon", color="#7c6be0", size=18).pixmap(18, 18))
        icon_lbl.setFixedSize(18, 18)

        title = QLabel("Dark Theme")
        title.setStyleSheet("font-size: 14px; font-weight: 600; color: #f0f0f0;")

        header.addWidget(icon_lbl)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        # Descrição
        desc = QLabel(
            "Applies a dark theme to Hammer++ by replacing toolbar icons\n"
            "and enabling dark mode on the title bar."
        )
        desc.setStyleSheet("font-size: 12px; color: #666;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Status + botões
        from core.dll_patcher import is_dll_patched, get_dll_path
        dll_path = get_dll_path(self.tool.install_path)
        is_patched = is_dll_patched(dll_path) if dll_path else False

        status_row = QHBoxLayout()
        status_dot = QLabel("●")
        status_dot.setStyleSheet(f"color: {'#5ae87a' if is_patched else '#555'}; font-size: 14px;")
        status_lbl = QLabel("Applied" if is_patched else "Not applied")
        status_lbl.setStyleSheet(f"font-size: 12px; color: {'#5ae87a' if is_patched else '#555'};")

        status_row.addWidget(status_dot)
        status_row.addWidget(status_lbl)
        status_row.addStretch()
        layout.addLayout(status_row)

        # Botões apply/restore
        btn_row = QHBoxLayout()

        self.btn_apply = QPushButton("Apply Dark Theme")
        self.btn_apply.setEnabled(not is_patched)
        self.btn_apply.setCursor(Qt.PointingHandCursor)
        self.btn_apply.setStyleSheet("""
            QPushButton {
                background: #7c6be0;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                color: white;
            }
            QPushButton:hover { background: #6559c4; }
            QPushButton:disabled { background: #2a2a2a; color: #555; }
        """)
        self.btn_apply.clicked.connect(self._on_apply)

        self.btn_restore = QPushButton("Restore Original")
        self.btn_restore.setEnabled(is_patched)
        self.btn_restore.setCursor(Qt.PointingHandCursor)
        self.btn_restore.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                color: #aaa;
            }
            QPushButton:hover { background: #222; color: #e0e0e0; }
            QPushButton:disabled { color: #444; border-color: #222; }
        """)
        self.btn_restore.clicked.connect(self._on_restore)

        btn_row.addWidget(self.btn_apply)
        btn_row.addWidget(self.btn_restore)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        return widget

    def _on_apply(self):
        from PySide6.QtWidgets import QMessageBox
        from core.dll_patcher import patch_dll, get_dll_path
        from pathlib import Path

        dll_path = get_dll_path(self.tool.install_path)
        if not dll_path:
            QMessageBox.warning(self, "Hammerfy", "hammerplusplus_dll.dll não encontrada.")
            return

        assets_dir = Path(__file__).parent.parent / "assets" / "dark_icons"
        success, msg = patch_dll(dll_path, str(assets_dir))

        if success:
            QMessageBox.information(self, "Hammerfy",
                "Dark theme applied!\n\nRestart Hammer++ to see the changes.")
            self.btn_apply.setEnabled(False)
            self.btn_restore.setEnabled(True)
        else:
            QMessageBox.warning(self, "Hammerfy", f"Error: {msg}")

    def _on_restore(self):
        from PySide6.QtWidgets import QMessageBox
        from core.dll_patcher import restore_dll, get_dll_path

        dll_path = get_dll_path(self.tool.install_path)
        if not dll_path:
            QMessageBox.warning(self, "Hammerfy", "hammerplusplus_dll.dll não encontrada.")
            return

        success, msg = restore_dll(dll_path)
        if success:
            QMessageBox.information(self, "Hammerfy",
                "Original theme restored!\n\nRestart Hammer++ to see the changes.")
            self.btn_apply.setEnabled(True)
            self.btn_restore.setEnabled(False)
        else:
            QMessageBox.warning(self, "Hammerfy", f"Error: {msg}")

    def _build_footer(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addStretch()
        btn_close = QPushButton("Close")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 13px;
                color: #aaa;
            }
            QPushButton:hover { background: #222; color: #e0e0e0; }
        """)
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)
        return widget

    def _divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #242424; max-height: 1px;")
        return line