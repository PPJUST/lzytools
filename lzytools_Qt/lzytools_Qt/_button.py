from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QToolButton


class ToolButtonRightClick(QToolButton):
    """支持右键点击信号的 ToolButton"""
    rightClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setMouseTracking(True)
        self.customContextMenuRequested.connect(self._emit_signal)

    def _emit_signal(self, *args):
        self.rightClicked.emit()
