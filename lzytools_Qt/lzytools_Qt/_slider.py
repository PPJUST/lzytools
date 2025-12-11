from PySide6.QtCore import *
from PySide6.QtWidgets import *


class SliderMoved(QSlider):
    """被移动后发送当前值的Slider"""
    movedValue = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def _moved(self, value: int):
        """移动事件"""
        # 固定滑动块为新值
        self.setValue(value)
        # 发送信号
        self._emit_signal(value)

    def _emit_signal(self, value: int):
        """发送信号"""
        self.movedValue.emit(value)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        self._moved(value)
