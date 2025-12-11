from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ._utils import set_transparent_background, set_no_frame


class TopTip(QMainWindow):
    """显示置顶并且淡入淡出文本的控件"""
    _STYLESHEET_TEXT = 'font-size: 15pt; color: blue'

    def __init__(self, text: str):
        super().__init__()
        # 添加显示文字的子控件
        self.label_showed = None
        self._add_label(str(text))

        # 设置定时器
        self.timer_fade = QTimer(self)
        self.timer_fade.timeout.connect(self._fade_out)
        self.duration: int = 2  # 留存时间，秒
        self.timer_fade.start(self.duration * 1000)

        # 设置淡入淡出动画
        self.animation = QPropertyAnimation()
        self._set_animation()

        # 设置透明属性
        set_transparent_background(self)

        # 设置无边框
        set_no_frame(self)

        # 设置置顶显示
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # 更新控件大小（需要在添加子控件后更新）
        self.setFixedSize(self.sizeHint())

        # 显示
        self._show_in_center()
        self.animation.start()

    def set_duration(self, duration: int):
        """设置留存时间（秒）"""
        self.duration = duration
        self.timer_fade.start(self.duration * 1000)

    def set_stylesheet(self, stylesheet: str):
        """设置文本样式表"""
        self._STYLESHEET_TEXT = stylesheet

    def _add_label(self, text: str):
        """添加子控件"""
        label = QLabel(str(text))
        label.setStyleSheet(self._STYLESHEET_TEXT)
        self.setCentralWidget(label)

    def _show_in_center(self):
        """在屏幕中心显示"""
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = int((screen.width() - size.width()) / 2)
        y = int((screen.height() - size.height()) / 2)
        print(x, y)
        self.move(x, y)

        self.show()

    def _set_animation(self):
        """设置动画"""
        opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacity_effect)
        self.animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

    def _fade_out(self):
        """淡出效果"""
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.close)

        self.animation.start()
