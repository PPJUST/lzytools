from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QGuiApplication, QPixmap
from PySide6.QtWidgets import QLabel, QSizePolicy


class LabelHiddenOverLengthText(QLabel):
    """自动省略超长文本的 Label（abcd -> a...），始终保留原始文本。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_origin = ''

    def setText(self, text):
        self.text_origin = '' if text is None else str(text)
        super().setText(self.text_origin)
        self._check_length()

    def _check_length(self):
        """按当前宽度重绘文本；基于原文缩放，窗口放大后可恢复完整文本。"""
        if not self.text_origin:
            return
        width = self.width()
        if width <= 0:
            return
        metrics = self.fontMetrics()
        if metrics.horizontalAdvance(self.text_origin) > width:
            elided = metrics.elidedText(
                self.text_origin, Qt.TextElideMode.ElideRight, width
            )
            super().setText(elided)
        else:
            super().setText(self.text_origin)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._check_length()


class LabelHoverInfo(QLabel):
    """悬浮提示 Label（单例）：可设置显示时长与位置。"""
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
            self.raise_()

            self.duration: float = 1  # 显示时长，秒
            self.position: str = 'LB'  # 显示位置，RT/RB/LT/LB

            self.timer_hidden = QTimer(self)
            self.timer_hidden.setSingleShot(True)
            self.timer_hidden.timeout.connect(self.hide)
        elif parent is not None and parent is not self.parent():
            self.setParent(parent)

    def set_duration(self, duration: float):
        """设置显示时长（秒）"""
        self.duration = max(0.0, float(duration))

    def set_position(self, position: str):
        """设置显示的位置
        :param position: RT/RB/LT/LB"""
        position = str(position).upper()
        if position not in ('RT', 'RB', 'LT', 'LB'):
            raise ValueError('参数错误，请选择 RT/RB/LT/LB')
        self.position = position

    def show_info(self, text: str):
        """在父控件的指定角落显示提示文本。"""
        self._show(text)

    def _show(self, text: str):
        self.setText(str(text))
        self._reset_position()
        self.show()
        self.raise_()
        self.timer_hidden.start(max(1, int(self.duration * 1000)))

    def _reset_position(self):
        hint = self.sizeHint()
        width, height = hint.width(), hint.height()
        parent = self.parent()
        if parent is not None:
            parent_size = parent.size()
        else:
            parent_size = QGuiApplication.primaryScreen().availableGeometry().size()
        parent_width, parent_height = parent_size.width(), parent_size.height()

        if self.position == 'LT':
            self.setGeometry(0, 0, width, height)
        elif self.position == 'LB':
            self.setGeometry(0, parent_height - height, width, height)
        elif self.position == 'RT':
            self.setGeometry(parent_width - width, 0, width, height)
        elif self.position == 'RB':
            self.setGeometry(parent_width - width, parent_height - height, width, height)


class LabelShowImage(QLabel):
    """用于显示图片的 Label，图片按 Label 尺寸等比缩放。"""

    def __init__(self, image_path: str = None, parent=None):
        """:param image_path: 本地图片路径"""
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.pixmap_original = None
        if image_path:
            self.set_image(image_path)

    def set_image(self, image_path: str = None):
        """设置图片；传入空值时清除当前图片。"""
        if not image_path:
            self.pixmap_original = None
            self.clear()
            return
        self.pixmap_original = QPixmap(image_path)
        self._update_image_size()

    def set_bytes_image(self, bytes_image: bytes):
        """设置 bytes 图片"""
        self.pixmap_original = QPixmap()
        self.pixmap_original.loadFromData(bytes_image)
        self._update_image_size()

    def _update_image_size(self):
        """更新图片尺寸"""
        if self.pixmap_original is None or self.pixmap_original.isNull():
            self.clear()
            return
        size = self.size()
        if size.isEmpty():
            return
        scaled = self.pixmap_original.scaled(
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_image_size()
