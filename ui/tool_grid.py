from PySide6.QtWidgets import QWidget, QScrollArea, QGridLayout, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from models.tool import Tool
from ui.tool_card import ToolCard


class ToolGrid(QWidget):
    tool_selected  = Signal(object)
    empty_clicked  = Signal()
    action_open    = Signal(object)
    action_folder  = Signal(object)
    action_install = Signal(object)
    action_update  = Signal(object)

    MAX_COLS     = 6
    MIN_CARD_W   = 160
    MAX_CARD_W   = 220
    GRID_PADDING = 16
    GRID_SPACING = 10

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cards: list[ToolCard] = []
        self._selected_id: str | None = None
        self._build_ui()

    # ─── UI Construction ──────────────────────────────────────────────────────

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
        self._grid.setContentsMargins(
            self.GRID_PADDING, self.GRID_PADDING,
            self.GRID_PADDING, self.GRID_PADDING
        )
        self._grid.setSpacing(self.GRID_SPACING)
        self._grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        scroll.setWidget(self._container)
        outer.addWidget(scroll)
        self._scroll = scroll

    # ─── Public API ────────────────────────────────────────────────────────────

    def load_tools(self, tools: list[Tool]):
        # Destroy existing cards before rebuilding
        for card in self._cards:
            card.deleteLater()
        self._cards.clear()

        for tool in tools:
            card = ToolCard(tool)
            card.selected.connect(self._on_select)
            card.action_open.connect(self.action_open.emit)
            card.action_folder.connect(self.action_folder.emit)
            card.action_install.connect(self.action_install.emit)
            card.action_update.connect(self.action_update.emit)
            self._cards.append(card)

        self._relayout()

    # ─── Layout ────────────────────────────────────────────────────────────────

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._cards:
            self._relayout()

    def _relayout(self):
        # Detach cards from grid without destroying them
        for card in self._cards:
            self._grid.removeWidget(card)

        available  = self._scroll.viewport().width() - self.GRID_PADDING * 2
        cols       = max(1, min(self.MAX_COLS, available // self.MIN_CARD_W))
        card_w     = min(self.MAX_CARD_W, (available - (cols - 1) * self.GRID_SPACING) // cols)
        banner_h   = int(card_w / 2.14)
        card_h     = banner_h + 80

        for card in self._cards:
            card.setFixedSize(card_w, card_h)
            card.update_banner_size(card_w, banner_h)

        for i, card in enumerate(self._cards):
            self._grid.addWidget(card, i // cols, i % cols)

    # ─── Event Handlers ────────────────────────────────────────────────────────

    def _on_select(self, tool: Tool):
        for card in self._cards:
            card.set_selected(card.tool.id == tool.id)
        self._selected_id = tool.id
        self.tool_selected.emit(tool)

    def _on_container_click(self, event):
        # Emit only when clicking the background, not a card
        if self._container.childAt(event.pos()) is None:
            self.empty_clicked.emit()