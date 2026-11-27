from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QTimer, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QGraphicsOpacityEffect, QLabel, QMainWindow

from ._utils import set_no_frame, set_transparent_background


class TopTip(QMainWindow):
    """显示置顶并且淡入淡出文本的控件"""

    _STYLESHEET_TEXT = 'font-size: 15pt; color: blue'

    def __init__(self, text: str):
        super().__init__()
        self.label_showed = None
        self._add_label(str(text))

        self.timer_fade = QTimer(self)
        self.timer_fade.timeout.connect(self._fade_out)
        self.duration = 2  # 留存时间，秒
        self._is_fading_out = False

        self.animation = QPropertyAnimation(self)
        self._set_animation()
        self.animation.finished.connect(self._on_animation_finished)

        set_transparent_background(self)
        set_no_frame(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(self.sizeHint())

        self._show_in_center()
        self.timer_fade.start(max(1, int(self.duration * 1000)))
        self.animation.start()

    def set_duration(self, duration: float):
        """设置留存时间（秒）"""
        self.duration = duration
        self.timer_fade.start(max(1, int(float(duration) * 1000)))

    def set_stylesheet(self, stylesheet: str):
        """设置文本样式表"""
        self._STYLESHEET_TEXT = stylesheet
        if self.label_showed is not None:
            self.label_showed.setStyleSheet(stylesheet)

    def _add_label(self, text: str):
        """添加子控件"""
        label = QLabel(str(text), self)
        label.setStyleSheet(self._STYLESHEET_TEXT)
        self.setCentralWidget(label)
        self.label_showed = label

    def _show_in_center(self):
        """在屏幕中心显示"""
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        x = (screen.width() - size.width()) // 2 + screen.left()
        y = (screen.height() - size.height()) // 2 + screen.top()
        self.move(x, y)
        self.show()

    def _set_animation(self):
        """设置淡入动画"""
        opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacity_effect)
        self.animation.setTargetObject(opacity_effect)
        self.animation.setPropertyName(b'opacity')
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def _fade_out(self):
        """淡出效果"""
        if self._is_fading_out:
            return
        self._is_fading_out = True
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

    def _on_animation_finished(self):
        """只有淡出动画结束才关闭窗口，避免淡入完成就关闭"""
        if self._is_fading_out:
            self.close()
