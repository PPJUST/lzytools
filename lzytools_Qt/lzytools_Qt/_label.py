from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class LabelHiddenOverLengthText(QLabel):
    """文本框，自动隐藏长文本的Label（abcd->a...）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_origin = ''

    def setText(self, text):
        super().setText(text)
        self.text_origin = text
        self._check_length()

    def _check_length(self):
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
        self._check_length()


class LabelHoverInfo(QLabel):
    """能够自动隐藏的悬浮显示信息的Label，用于显示提示信息"""
    _STYLESHEET_TEXT = 'color: blue;'
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
            self.setStyleSheet(self._STYLESHEET_TEXT)
            self.setWordWrap(True)
            self.hide()
            self.raise_()  # 置顶

            self.duration: float = 1  # 显示时长，秒
            self.position: str = 'LB'  # 显示位置，RT/RB/LT/LB

            # 设置定时器
            self.timer_hidden = QTimer()
            self.timer_hidden.setSingleShot(True)
            self.timer_hidden.timeout.connect(self.hide)

    def set_duration(self, duration: float):
        """设置显示时长（秒）"""
        self.duration = duration

    def set_position(self, position: str):
        """设置显示的位置
        :param position: RT/RB/LT/LB"""
        if position.upper() not in ['RT', 'RB', 'LT', 'LB']:
            raise Exception('参数错误，请选择RT/RB/LT/LB')
        self.position = position.upper()

    def _show(self, text: str):
        """显示Label"""
        self.setText(text)
        self._reset_position()
        self.show()
        self.timer_hidden.start(int(self.duration * 1000))

    def _reset_position(self):
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


class LabelShowImage(QLabel):
    """用于显示图片的Label"""

    def __init__(self, image_path: str = None):
        """:param image_path: 本地图片路径"""
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.pixmap_original = None
        if image_path:
            self.pixmap_original = QPixmap(image_path)

    def set_image(self, image_path: str = None):
        """设置图片"""
        self.pixmap_original = QPixmap(image_path)
        self._update_image_size()

    def set_bytes_image(self, bytes_image: bytes):
        """设置bytes图片"""
        self.pixmap_original = QPixmap()
        self.pixmap_original.loadFromData(bytes_image, format=None)
        self._update_image_size()

    def _update_image_size(self):
        """更新图片尺寸"""
        if self.pixmap_original and not self.pixmap_original.isNull():
            scaled_pixmap = self.pixmap_original.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        self._update_image_size()
        super().resizeEvent(event)
