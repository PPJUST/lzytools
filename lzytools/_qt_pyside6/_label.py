from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class LabelImageAutoSize(QLabel):
    """自适应大小显示图片"""

    def __init__(self, image_path: str = None):
        """:param image_path: str，图片路径"""
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pixmap = None
        if image_path:
            self.pixmap = QPixmap(image_path)

    def set_image(self, image_path: str = None):
        """设置图片"""
        self.pixmap = QPixmap(image_path)
        self.update_image_size()

    def update_image_size(self):
        """更新图片尺寸"""
        if not self.pixmap.isNull():
            scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        self.update_image_size()
        super().resizeEvent(event)


class LabelHiddenOverLengthText(QLabel):
    """文本框控件，自动隐藏长文本（abcd->a...）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_origin = ''

    def setText(self, text):
        super().setText(text)
        self.text_origin = text
        self.check_over_length_text()

    def check_over_length_text(self):
        """检查文本是否超限"""
        # 获取字体度量
        font_metrics = self.fontMetrics()
        label_width = self.width()

        # 检查文本是否超出label宽度
        if font_metrics.horizontalAdvance(self.text_origin) > label_width:
            elided_text = font_metrics.elidedText(self.text_origin, Qt.ElideRight, label_width)
            self.setText(elided_text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.check_over_length_text()


class LabelHoverInfo(QLabel):
    """自动隐藏的悬浮在控件左下角的label（用于显示提示信息）"""

    _instance = None
    _is_init = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if not self._is_init:
            super().__init__(parent)
            self._is_init = True

            self.setMouseTracking(True)
            self.setStyleSheet("color: blue;")
            self.setWordWrap(True)
            self.hide()
            self.raise_()  # 置顶

            self.duration = 1  # 显示时长，秒
            self.position = 'LB'  # 显示位置，RT/RB/LT/LB

            # 设置定时器
            self.timer_hidden = QTimer()
            self.timer_hidden.setSingleShot(True)
            self.timer_hidden.timeout.connect(self.hide)

    def set_duration(self, duration: float):
        """设置显示时长，秒"""
        self.duration = duration

    def set_position(self, position: str):
        """设置显示位置
        :param position: str，RT/RB/LT/LB"""
        if position.upper() not in ['RT', 'RB', 'LT', 'LB']:
            raise Exception('参数错误，请选择RT/RB/LT/LB')
        self.position = position.upper()

    def _show(self, text: str):
        """显示信息"""
        self.setText(text)
        self.reset_position()
        self.show()
        self.timer_hidden.start(self.duration * 1000)

    def reset_position(self):
        """重设坐标轴位置"""
        width, height = self.sizeHint()
        parent_width, parent_height = self.parent().size()

        if self.position == 'LT':  # LT左上角
            self.setGeometry(0, 0, width, height)
        elif self.position == 'LB':  # LB左下角
            self.setGeometry(0, parent_height - height, width, height)
        elif self.position == 'RT':  # RT右上角
            self.setGeometry(parent_width - width, 0, width, height)
        elif self.position == 'RB':  # RB右下角
            self.setGeometry(parent_width - width, parent_height - height, width, height)
