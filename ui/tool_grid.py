from PySide6.QtWidgets import QWidget, QScrollArea, QGridLayout, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from models.tool import Tool, ToolStatus
from ui.tool_card import ToolCard


class ToolGrid(QWidget):
    tool_selected = Signal(object)
    empty_clicked = Signal()
    action_open = Signal(object)
    action_folder = Signal(object)
    action_install = Signal(object)
    action_update = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cards: list[ToolCard] = []
        self._selected_id = None
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self._container = QWidget()
        self._container.mousePressEvent = self._on_container_click
        self._grid = QGridLayout(self._container)
        self._grid.setContentsMargins(16, 16, 16, 16)
        self._grid.setSpacing(10)
        self._grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        scroll.setWidget(self._container)
        outer.addWidget(scroll)

    def load_tools(self, tools: list[Tool]):
        # Limpa grid atual
        for card in self._cards:
            card.deleteLater()
        self._cards.clear()

        cols = 4
        for i, tool in enumerate(tools):
            card = ToolCard(tool)
            card.selected.connect(self._on_select)
            card.action_open.connect(self.action_open.emit)
            card.action_folder.connect(self.action_folder.emit)
            card.action_install.connect(self.action_install.emit)
            card.action_update.connect(self.action_update.emit)
            self._grid.addWidget(card, i // cols, i % cols)
            self._cards.append(card)

    def _on_select(self, tool: Tool):
        for card in self._cards:
            card.set_selected(card.tool.id == tool.id)
        self._selected_id = tool.id
        self.tool_selected.emit(tool)
    
    def _on_container_click(self, event):
        # Verifica se clicou diretamente no container, não num card filho
        child = self._container.childAt(event.pos())
        if child is None:
            self.empty_clicked.emit()