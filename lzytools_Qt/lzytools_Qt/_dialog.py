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
