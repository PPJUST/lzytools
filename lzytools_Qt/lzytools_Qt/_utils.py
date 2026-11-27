import base64
from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget

"""----------逻辑函数----------"""


def _set_transparent_background(widget: QWidget):
    """设置控件的背景色为透明色"""
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    widget.setStyleSheet('background-color: transparent; border: none;')


def _set_no_frame(widget: QWidget):
    """设置控件无 Windows 边框，保留原有窗口标志"""
    widget.setWindowFlags(widget.windowFlags() | Qt.WindowType.FramelessWindowHint)


def _convert_base64_image_to_pixmap(base64_image: Union[bytes, str]) -> QPixmap:
    """将 base64 图片对象转换为 pixmap 对象
    :param base64_image: base64 字节或字符串
    :return: QPixmap 对象"""
    byte_data = base64.b64decode(base64_image)
    pixmap = QPixmap()
    pixmap.loadFromData(byte_data)
    return pixmap


def _convert_bytes_image_to_pixmap(bytes_image: bytes) -> QPixmap:
    """将 bytes 图片对象转换为 pixmap 对象
    :param bytes_image: bytes 图片对象
    :return: QPixmap 对象"""
    pixmap = QPixmap()
    pixmap.loadFromData(bytes_image)
    return pixmap


"""----------调用函数----------"""


def set_transparent_background(widget: QWidget):
    """设置控件的背景色为透明色"""
    return _set_transparent_background(widget)


def set_no_frame(widget: QWidget):
    """设置控件无 Windows 边框"""
    return _set_no_frame(widget)


def convert_base64_image_to_pixmap(base64_image: Union[bytes, str]) -> QPixmap:
    """将 base64 图片对象转换为 pixmap 对象"""
    return _convert_base64_image_to_pixmap(base64_image)


def base64_to_pixmap(base64_image: Union[bytes, str]) -> QPixmap:
    """convert_base64_image_to_pixmap 的别名"""
    return _convert_base64_image_to_pixmap(base64_image)


def convert_bytes_image_to_pixmap(bytes_image: bytes) -> QPixmap:
    """将 bytes 图片对象转换为 pixmap 对象"""
    return _convert_bytes_image_to_pixmap(bytes_image)


def bytes_to_pixmap(bytes_image: bytes) -> QPixmap:
    """convert_bytes_image_to_pixmap 的别名"""
    return _convert_bytes_image_to_pixmap(bytes_image)
