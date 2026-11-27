from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QSlider, QStyle, QStyleOptionSlider


class SliderMoved(QSlider):
    """被点击移动后发送当前值的 Slider"""

    movedValue = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def _moved(self, value: int):
        """移动事件"""
        self.setValue(value)
        self._emit_signal(value)

    def _emit_signal(self, value: int):
        """发送信号"""
        self.movedValue.emit(value)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        handle_rect = self.style().subControlRect(
            QStyle.ComplexControl.CC_Slider,
            option,
            QStyle.SubControl.SC_SliderHandle,
            self,
        )
        pos = event.position().toPoint()
        if self.orientation() == Qt.Orientation.Horizontal:
            coordinate, available, handle_length = pos.x(), self.width(), handle_rect.width()
        else:
            coordinate, available, handle_length = pos.y(), self.height(), handle_rect.height()
        value = QStyle.sliderValueFromPosition(
            self.minimum(), self.maximum(), coordinate, available, handle_length
        )
        self._moved(value)
