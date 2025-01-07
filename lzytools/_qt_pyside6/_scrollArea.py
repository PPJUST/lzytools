from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ScrollAreaSmooth(QScrollArea):
    """平滑滚动的scrollArea"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.move_direction = 'v'  # 移动方向，v纵向h横向
        # 替换滚动条
        self.scrollbar_h = ScrollBarSmooth(self)
        self.scrollbar_v = ScrollBarSmooth(self)
        self.scrollbar_h.setOrientation(Qt.Horizontal)
        self.scrollbar_v.setOrientation(Qt.Vertical)
        self.setVerticalScrollBar(self.scrollbar_v)
        self.setHorizontalScrollBar(self.scrollbar_h)

    def set_move_direction(self, direction: str):
        """设置移动方向
        :param direction: str，v/纵向/h/横向"""
        if direction.lower() not in ['v', '纵向', 'h', '横向']:
            raise Exception(f'参数错误：{direction}')
        if direction.lower() in ['v', '纵向']:
            self.move_direction = 'v'
        elif direction.lower() in ['h', '横向']:
            self.move_direction = 'h'

    def wheelEvent(self, arg__1: QWheelEvent):
        if self.move_direction == 'v':
            self.scrollbar_v.scroll_value(-arg__1.angleDelta().y())
        elif self.move_direction == 'h':
            self.scrollbar_h.scroll_value(-arg__1.angleDelta().y())


class ScrollBarSmooth(QScrollBar):
    """实现平滑滚动的滚动条（在起点终点之间插值）"""
    MoveEvent = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 设置插值动画
        self.animal = QPropertyAnimation()
        self.animal.setTargetObject(self)
        self.animal.setPropertyName(b"value")
        self.set_scroll_type_smooth()  # 设置滚动动画曲线
        self.set_animal_duration(400)  # 设置滚动动画时间，用于控制滚动速度

    def setValue(self, value: int):
        if value == self.value():
            return

        # 停止动画
        self.animal.stop()

        # 重新开始动画
        self.MoveEvent.emit()
        self.animal.setStartValue(self.value())
        self.animal.setEndValue(value)
        self.animal.start()

    def scroll_value(self, value: int):
        """滚动指定距离"""
        value += self.value()
        value = min(self.maximum(), max(self.minimum(), value))  # 防止超限
        self.MoveEvent.emit()
        self.setValue(value)

    def _scroll_to_value(self, value: int):
        """滚动到指定位置"""
        value = min(self.maximum(), max(self.minimum(), value))  # 防止超限
        self.MoveEvent.emit()
        self.setValue(value)

    def set_animal_duration(self, duration: int):
        """设置动画时间
        :param duration: int，毫秒"""
        self.animal.stop()
        self.animal.setDuration(duration)  # 动画时间 毫秒

    def set_scroll_type_liner(self):
        """设置线性滚动"""
        self.animal.stop()
        self.animal.setEasingCurve(QEasingCurve.Linear)

    def set_scroll_type_smooth(self):
        """设置平滑滚动"""
        self.animal.stop()
        self.animal.setEasingCurve(QEasingCurve.OutQuad)

    def mousePressEvent(self, event):
        self.animal.stop()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.animal.stop()
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.animal.stop()
        super().mouseMoveEvent(event)
