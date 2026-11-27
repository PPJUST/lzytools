import os
from typing import Union

import filetype
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QLineEdit


def _as_path_list(paths: Union[list, str]) -> list:
    """把拖入的单个路径或路径列表统一转换为列表。"""
    if isinstance(paths, str):
        return [paths]
    return list(paths)


class LineEditDropFiles(QLineEdit):
    """可拖入多个文件的 LineEdit，并在拖入时发送文件路径列表信号"""
    pathsDropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setReadOnly(True)

    def _emit_signal(self, paths: Union[list, str]):
        """发送信号"""
        self.pathsDropped.emit(_as_path_list(paths))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self._emit_signal([url.toLocalFile() for url in urls])
        else:
            super().dropEvent(event)


class LineEditCheckPathExists(LineEditDropFiles):
    """实时检查 LineEdit 显示的文件路径是否存在"""
    _STYLESHEET_NOT_EXISTS = 'border: 1px solid red;'
    pathNotExists = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_exists = True
        self.timer_check = QTimer(self)
        self.timer_check.timeout.connect(self._check_path_exists)
        self.set_check_interval(5)
        self.timer_check.start()

    def set_check_interval(self, second: float):
        """设置定时检查路径有效性的时间间隔（秒）"""
        self.timer_check.setInterval(max(1, int(float(second) * 1000)))

    def set_stylesheet_not_exists(self, stylesheet: str):
        """设置路径不存在时的文本框样式"""
        self._STYLESHEET_NOT_EXISTS = stylesheet

    def _check_path_exists(self):
        """检查路径有效性"""
        path = self.text()
        if not os.path.isabs(path):
            self.is_exists = True
            self.setStyleSheet('')
            return

        self.is_exists = os.path.exists(path)
        if self.is_exists:
            self.setStyleSheet('')
        else:
            self.setStyleSheet(self._STYLESHEET_NOT_EXISTS)
            self.pathNotExists.emit(path)


class LabelDropFiles(QLabel):
    """可拖入多个文件的 Label，并在拖入时发送文件路径列表信号"""
    pathsDropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setScaledContents(True)

    def _emit_signal(self, paths: Union[list, str]):
        """发送信号"""
        self.pathsDropped.emit(_as_path_list(paths))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self._emit_signal([url.toLocalFile() for url in urls])
        else:
            super().dropEvent(event)


class LabelDropFilesTip(LabelDropFiles):
    """可拖入多个文件的 Label，拖入时会切换提示图标并发送路径列表信号"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon_drop = ''  # 拖入时的图标
        self.icon_last = None  # 拖入前的图标

    def set_drop_icon(self, icon_path: str):
        """设置新的拖入图标"""
        self.icon_drop = ''
        if icon_path and os.path.exists(icon_path):
            self.icon_drop = icon_path

    def dragEnterEvent(self, event):
        if not event.mimeData().hasUrls():
            event.ignore()
            return
        super().dragEnterEvent(event)
        if self.icon_drop and self.icon_last is None:
            self.icon_last = self.pixmap()
            self.setPixmap(QPixmap(self.icon_drop))

    def dragLeaveEvent(self, event):
        super().dragLeaveEvent(event)
        if self.icon_drop and self.icon_last is not None:
            self.setPixmap(self.icon_last)
            self.icon_last = None


class LabelShowDropImag(LabelDropFiles):
    """可拖入文件的 Label，并将拖入的第一张图片显示出来"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pathsDropped.connect(self._show_first_image)

    def _show_first_image(self, paths):
        """显示第一张图片"""
        for path in paths:
            if os.path.isfile(path) and filetype.is_image(path):
                self._show_image(path)
                return

        self._clear_image()

    def _show_image(self, image_path: str):
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap)

    def _clear_image(self):
        self.setPixmap(QPixmap())
