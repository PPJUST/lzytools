import base64
from typing import Union

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

"""----------逻辑函数----------"""


def _set_transparent_background(widget: QWidget):
    """设置控件的背景色为透明色"""
    widget.setAttribute(Qt.WA_TranslucentBackground)  # 设置透明背景
    widget.setStyleSheet("background-color: transparent; border: none;")


def _set_no_frame(widget: QWidget):
    """设置控件无Windows边框"""
    widget.setWindowFlags(Qt.FramelessWindowHint)


def _convert_base64_image_to_pixmap(base64_image: Union[bytes, str]) -> QPixmap:
    """将base64图片对象转换为pixmap对象
    :param base64_image: base64字节或字符串
    :return: QPixmap对象"""
    # 解码base64字节或字符串
    byte_data = base64.b64decode(base64_image)

    # 将字节数据转换为QPixmap
    pixmap = QPixmap()
    buffer = QByteArray(byte_data)
    byte_array_device = QBuffer(buffer)
    byte_array_device.open(QBuffer.ReadOnly)
    pixmap.loadFromData(byte_array_device.data())

    return pixmap


def _convert_bytes_image_to_pixmap(bytes_image: bytes) -> QPixmap:
    """将bytes图片对象转换为pixmap对象
    :param bytes_image: bytes图片对象
    :return: QPixmap对象"""
    image = QImage()
    image.loadFromData(bytes_image)
    pixmap = QPixmap.fromImage(image)

    return pixmap


"""----------调用函数----------"""


def set_transparent_background(widget: QWidget):
    """设置控件的背景色为透明色"""
    return _set_transparent_background(widget)


def set_no_frame(widget: QWidget):
    """设置控件无Windows边框"""
    return _set_no_frame(widget)


def convert_base64_image_to_pixmap(base64_image: Union[bytes, str]) -> QPixmap:
    """将base64图片对象转换为pixmap对象
    :param base64_image: base64字节或字符串
    :return: QPixmap对象"""
    return _convert_base64_image_to_pixmap(base64_image)


def base64_to_pixmap(base64_image: Union[bytes, str]) -> QPixmap:
    """将base64图片对象转换为pixmap对象
    :param base64_image: base64字节或字符串
    :return: QPixmap对象"""
    return _convert_base64_image_to_pixmap(base64_image)


def convert_bytes_image_to_pixmap(bytes_image: bytes) -> QPixmap:
    """将bytes图片对象转换为pixmap对象
    :param bytes_image: bytes图片对象
    :return: QPixmap对象"""
    return _convert_bytes_image_to_pixmap(bytes_image)


def bytes_to_pixmap(bytes_image: bytes) -> QPixmap:
    """将bytes图片对象转换为pixmap对象
    :param bytes_image: bytes图片对象
    :return: QPixmap对象"""
    return _convert_bytes_image_to_pixmap(bytes_image)
