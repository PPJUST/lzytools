from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


def set_transparent_background(widget: QWidget):
    """设置Widget的背景为透明"""
    widget.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框
    widget.setAttribute(Qt.WA_TranslucentBackground)  # 设置透明背景
    widget.setStyleSheet("background-color: transparent; border: none;")


def calculate_keep_aspect_ratio_resize(qsize_widget: QSize, qsize_pic: QSize) -> QSize:
    """计算图片显示控件上时，为了保持图片纵横比而计算的控件的新尺寸"""
    label_width = qsize_widget.width()
    label_height = qsize_widget.height()
    pic_width = qsize_pic.width()
    pic_height = qsize_pic.height()

    label_rate = label_width / label_height
    pic_rate = pic_width / pic_height

    if label_rate >= pic_rate:  # 符合则按高缩放
        resize_height = label_height
        resize_width = int(pic_width / pic_height * resize_height)
        resize_qsize = QSize(resize_width, resize_height)
    else:  # 否则按宽缩放
        resize_width = label_width
        resize_height = int(pic_height / pic_width * resize_width)
        resize_qsize = QSize(resize_width, resize_height)

    """
    后续操作示例
    pixmap = pixmap.scaled(resize_qsize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
    label.setPixmap(pixmap)
    """

    return resize_qsize
