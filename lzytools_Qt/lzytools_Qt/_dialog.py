from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ._utils import set_transparent_background, set_no_frame


class DialogPlayGif(QDialog):
    """置顶播放Gif的Dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)

        set_transparent_background(self)
        set_no_frame(self)

        # 添加label
        self.label_gif = QLabel('GIF PLAYER')
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label_gif)

        # 添加动画对象
        self.gif = None

    def set_gif(self, gif_path: str):
        """设置gif
        :param gif_path: Gif文件路径"""
        self.gif = QMovie(gif_path)
        self.label_gif.setMovie(self.gif)

    def play(self):
        self.gif.start()
        self.show()

    def stop(self):
        self.gif.stop()
        self.close()


class DialogImages(QDialog):
    """显示图片的Dialog，可以左右切页，图片自适应大小（支持放大/缩小）"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # 添加一个显示文本的label
        self.label_info = QLabel()
        self.layout.addWidget(self.label_info)

        # 图片显示Label - 基础设置
        self.label_image = QLabel('Image')
        self.label_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_image.setAlignment(Qt.AlignCenter)  # 图片居中
        self.label_image.setScaledContents(False)  # 禁用自动拉伸
        self.layout.addWidget(self.label_image, stretch=1)

        # 页码布局
        self.layout_pages = QHBoxLayout()
        self.layout_pages.addStretch(1)
        self.label_current_page = QLabel('Current')
        self.label_1 = QLabel('/')
        self.label_pages_count = QLabel('Count')
        self.layout_pages.addWidget(self.label_current_page)
        self.layout_pages.addWidget(self.label_1)
        self.layout_pages.addWidget(self.label_pages_count)
        self.layout_pages.addStretch(1)
        self.layout.addLayout(self.layout_pages)

        # 切页按钮
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

        # 变量优化：分离原始图片和显示用图片
        self.current_page = 0
        self.pages_count = 0
        self.original_pixmaps = []  # 存储原始未缩放的图片（关键！）

    def add_page(self, image_path: str):
        """新增图片页（存储原始图片）"""
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():  # 校验图片是否有效
            self.pages_count += 1
            self.label_pages_count.setText(str(self.pages_count))
            self.original_pixmaps.append(pixmap)  # 只存原始图片

    def _previous_page(self):
        """切换到上一页"""
        if self.pages_count == 0:
            return
        self.current_page -= 1
        if self.current_page < 1:
            self.current_page = self.pages_count
        self._show_image()

    def _next_page(self):
        """切换到下一页"""
        if self.pages_count == 0:
            return
        self.current_page += 1
        if self.current_page > self.pages_count:
            self.current_page = 1
        self._show_image()

    def _show_image(self):
        """显示当前页（始终基于原始图片缩放）"""
        if self.pages_count == 0 or self.current_page - 1 >= len(self.original_pixmaps):
            self.label_image.setText('No Image')
            return

        self.label_current_page.setText(str(self.current_page))
        # 核心修复：取原始图片，而非缩放后的图片
        original_pixmap = self.original_pixmaps[self.current_page - 1]
        # 获取Label的可用尺寸（减去边距，避免超出边界）
        label_rect = self.label_image.contentsRect()
        # 按比例缩放：始终基于原始图片，支持放大/缩小
        scaled_pixmap = original_pixmap.scaled(
            label_rect.size(),
            Qt.KeepAspectRatio,  # 保持宽高比
            Qt.SmoothTransformation  # 平滑缩放（更清晰）
        )
        self.label_image.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        """窗口大小变化时，重新缩放图片（关键：基于原始图）"""
        super().resizeEvent(event)
        if self.current_page > 0 and self.pages_count > 0:
            self._show_image()  # 重新渲染，用原始图适配新尺寸

    def exec(self):
        """启动对话框"""
        if self.pages_count > 0:
            self.current_page = 1
            self._show_image()
        super().exec()