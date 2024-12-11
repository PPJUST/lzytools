from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ToolButtonRightClick(QToolButton):
    """支持右键点击信号的QToolButton"""
    rightClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setMouseTracking(True)
        self.customContextMenuRequested.connect(self._emit_signal)

    def _emit_signal(self):
        self.rightClicked.emit()
