from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ._function import set_transparent_background


class DialogGifPlayer(QDialog):
    """播放GIF动画的QDialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        set_transparent_background(self)

        # 添加label
        self.label_gif = QLabel('GIF PLAYER')
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label_gif)

        # 添加动画对象
        self.gif = None

    def set_gif(self, gif: str):
        """设置gif
        :param gif: str，gif文件路径"""
        self.gif = QMovie(gif)
        self.label_gif.setMovie(self.gif)

    def play(self):
        self.gif.start()
        self.show()

    def stop(self):
        self.gif.stop()
        self.close()
