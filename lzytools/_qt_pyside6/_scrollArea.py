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
    MoveEvent = Signal(name='移动信号')
    AutoPlayStart = Signal(name='开始自动滚动')
    AutoPlayStop = Signal(name='停止自动滚动')

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 设置缓出动画（用于滚轮等一般滚动）
        self.animal_smooth = QPropertyAnimation()
        self.animal_smooth.setTargetObject(self)
        self.animal_smooth.setPropertyName(b"value")
        self.animal_smooth.setEasingCurve(QEasingCurve.OutQuad)  # 二次缓出
        self.animal_smooth.setDuration(400)  # 动画时间 毫秒

        # 设置线性动画（仅用于自动滚动）
        self.animal_linear = QPropertyAnimation()
        self.animal_linear.setTargetObject(self)
        self.animal_linear.setPropertyName(b"value")
        self.animal_linear.setEasingCurve(QEasingCurve.Linear)  # 二次缓出
        self.animal_linear.setDuration(400)  # 动画时间 毫秒

        # 默认动画为缓出动画
        self.animal = self.animal_smooth  # 差值动画，通过赋值不同的动画类型来改变平滑、线性状态

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
        target_value = self.value() + value
        self.scroll_to_value(target_value)

    def scroll_to_value(self, value: int):
        """滚动到指定值"""
        value = min(self.maximum(), max(self.minimum(), value))  # 防止超限
        self.MoveEvent.emit()
        self.setValue(value)

    def set_type_smooth(self):
        """设置平滑滚动"""
        self.animal.stop()
        self.animal = self.animal_smooth
        self.AutoPlayStop.emit()

    def set_type_linear(self, value: int, duration: float):
        """设置线性滚动
        :param value: int，需要滚动至的位置
        :param duration: float，滚动时间，秒"""
        self.animal.stop()
        self.animal_linear.setDuration(int(duration * 1000))
        self.animal = self.animal_linear
        self.scroll_to_value(value)
        self.AutoPlayStart.emit()

    def _set_smooth_animal_duration(self, duration: int):
        """设置缓出动画的动画时间
        :param duration: int，毫秒"""
        self.animal_smooth.stop()
        self.animal_smooth.setDuration(duration)  # 动画时间 毫秒

    def _set_linear_animal_duration(self, duration: int):
        """设置线性动画的动画时间
        :param duration: int，毫秒"""
        self.animal_linear.stop()
        self.animal_linear.setDuration(duration)  # 动画时间 毫秒

    def is_autoplay_running(self) -> bool:
        """是否正在进行自动播放"""
        # 通过判断滑动动画来判断是否正在进行自动播放
        if self.animal.easingCurve().type() == QEasingCurve.Linear:
            return True
        else:
            return False

    def mousePressEvent(self, event):
        self.set_type_smooth()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.set_type_smooth()
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.set_type_smooth()
        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        self.set_type_smooth()
        self.scroll_value(-event.angleDelta().y())
