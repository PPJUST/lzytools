from PySide6.QtCore import *
from PySide6.QtWidgets import *


class SliderMoved(QSlider):
    """移动后发送新值信号"""
    signal_moved = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def moved(self, value: int):
        """发生移动事件"""
        # 固定滑动块为新值
        self.setValue(value)
        # 发送信号
        self._emit_signal(value)

    def _emit_signal(self, value: int):
        """发送信号"""
        self.signal_moved.emit(value)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        self.moved(value)
