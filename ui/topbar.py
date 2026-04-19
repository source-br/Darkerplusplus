from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt, Signal


class Topbar(QWidget):
    search_changed = Signal(str)
    view_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.setObjectName("topbar")
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(10)

        self.title_label = QLabel("All tools")
        self.title_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #f0f0f0;")

        self.count_label = QLabel("")
        self.count_label.setStyleSheet("font-size: 12px; color: #555;")

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search tools...")
        self.search.setFixedWidth(180)
        self.search.setFixedHeight(30)
        self.search.textChanged.connect(self.search_changed.emit)

        self.btn_grid = QPushButton("Grid")
        self.btn_list = QPushButton("List")
        for btn in [self.btn_grid, self.btn_list]:
            btn.setFixedHeight(28)
            btn.setFixedWidth(48)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: 1px solid #2a2a2a;
                    border-radius: 5px;
                    font-size: 11px;
                    color: #666;
                }
                QPushButton:checked {
                    background: #2a2a2a;
                    color: #ccc;
                    border-color: #333;
                }
                QPushButton:hover { color: #aaa; }
            """)

        self.btn_grid.setChecked(True)
        self.btn_grid.clicked.connect(lambda: self._on_view("grid"))
        self.btn_list.clicked.connect(lambda: self._on_view("list"))

        layout.addWidget(self.title_label)
        layout.addWidget(self.count_label)
        layout.addStretch()
        layout.addWidget(self.search)
        layout.addWidget(self.btn_grid)
        layout.addWidget(self.btn_list)

    def set_title(self, title, count=None):
        self.title_label.setText(title)
        self.count_label.setText(f"{count} available" if count is not None else "")

    def _on_view(self, mode):
        self.btn_grid.setChecked(mode == "grid")
        self.btn_list.setChecked(mode == "list")
        self.view_changed.emit(mode)