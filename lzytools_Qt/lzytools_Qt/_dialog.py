from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie, QPixmap
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout

from ._utils import set_no_frame, set_transparent_background


class DialogPlayGif(QDialog):
    """置顶播放 GIF 的 Dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)

        set_transparent_background(self)
        set_no_frame(self)

        self.label_gif = QLabel('GIF PLAYER')
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label_gif)

        self.gif = None

    def set_gif(self, gif_path: str):
        """设置 gif
        :param gif_path: Gif文件路径"""
        old_gif = self.gif
        self.gif = QMovie(gif_path, parent=self)
        self.label_gif.setMovie(self.gif)
        if old_gif is not None:
            old_gif.stop()
            old_gif.deleteLater()

    def play(self):
        if self.gif is None:
            raise RuntimeError('请先调用 set_gif() 设置 GIF 文件')
        self.gif.start()
        self.show()

    def stop(self):
        if self.gif is not None:
            self.gif.stop()
        self.close()


class DialogImages(QDialog):
    """显示图片的 Dialog，可以左右切页，图片自适应大小"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.label_info = QLabel()
        self.layout.addWidget(self.label_info)

        self.label_image = QLabel('Image')
        self.label_image.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setScaledContents(False)
        self.layout.addWidget(self.label_image, stretch=1)

        self.layout_pages = QHBoxLayout()
        self.layout_pages.addStretch(1)
        self.label_current_page = QLabel('Current')
        self.label_1 = QLabel('/')
        self.label_pages_count = QLabel('Count')
        for label in (self.label_current_page, self.label_1, self.label_pages_count):
            self.layout_pages.addWidget(label)
        self.layout_pages.addStretch(1)
        self.layout.addLayout(self.layout_pages)

        self.layout_turn = QHBoxLayout()
        self.layout_turn.addStretch(1)
        self.button_previous = QPushButton('<')
        self.button_previous.clicked.connect(self._previous_page)
        self.button_next = QPushButton('>')
        self.button_next.clicked.connect(self._next_page)
        self.layout_turn.addWidget(self.button_previous)
        self.layout_turn.addWidget(self.button_next)
        self.layout_turn.addStretch(1)
        self.layout.addLayout(self.layout_turn)

        self.current_page = 0
        self.pages_count = 0
        self.original_pixmaps = []  # 存储原始图片 pixmap 对象

    def add_page(self, image_path: str):
        """新增图片页"""
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return False
        self.original_pixmaps.append(pixmap)
        self.pages_count = len(self.original_pixmaps)
        self.label_pages_count.setText(str(self.pages_count))
        return True

    def _previous_page(self):
        """切换到上一页"""
        if self.pages_count == 0:
            return
        self.current_page = self.current_page - 1 or self.pages_count
        self._show_image()

    def _next_page(self):
        """切换到下一页"""
        if self.pages_count == 0:
            return
        self.current_page = self.current_page % self.pages_count + 1
        self._show_image()

    def _show_image(self):
        """显示当前页"""
        if not (1 <= self.current_page <= self.pages_count):
            self.label_image.setText('No Image')
            return

        self.label_current_page.setText(str(self.current_page))
        label_size = self.label_image.contentsRect().size()
        if label_size.isEmpty():
            return
        original_pixmap = self.original_pixmaps[self.current_page - 1]
        scaled_pixmap = original_pixmap.scaled(
            label_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.label_image.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        """窗口大小变化时，重新缩放图片"""
        super().resizeEvent(event)
        if self.current_page > 0 and self.pages_count > 0:
            self._show_image()

    def exec(self):
        """启动对话框并返回对话框结果"""
        if self.pages_count > 0:
            self.current_page = 1
            self._show_image()
        return super().exec()
