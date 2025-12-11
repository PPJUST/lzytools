import os
from typing import Union, List

import filetype
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class LineEditDropFiles(QLineEdit):
    """可拖入多个文件的LineEdit，并在拖入时发送拖入的文件路径列表信号"""
    pathsDropped = Signal(List[str])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setReadOnly(True)

    def _emit_signal(self, paths: Union[list, str]):
        """发送信号"""
        if isinstance(paths, str):
            paths = [paths]
        self.pathsDropped.emit(paths)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            paths = []
            for index in range(len(urls)):
                path = urls[index].toLocalFile()
                paths.append(path)
            self._emit_signal(paths)


class LineEditCheckPathExists(LineEditDropFiles):
    """实时检查LineEdit显示的文件路径是否存在"""
    _STYLESHEET_NOT_EXISTS = 'border: 1px solid red;'
    pathNotExists = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置一个QTime，定时检查路径有效性
        self.is_exists = True
        self.timer_check = QTimer()
        self.timer_check.timeout.connect(self._check_path_exists)
        self.timer_check.setInterval(5000)  # 默认定时5秒
        self.timer_check.start()

    def set_check_interval(self, second: float):
        """设置定时检查路径有效性的时间间隔"""
        self.timer_check.setInterval(int(second * 1000))

    def set_stylesheet_not_exists(self, stylesheet: str):
        """设置路径不存在时的文本框样式"""
        self._STYLESHEET_NOT_EXISTS = stylesheet

    def _check_path_exists(self):
        """检查路径有效性"""
        path = self.text()
        if os.path.isabs(path):
            if os.path.exists(path):
                self.setStyleSheet('')
            else:
                self.setStyleSheet(self._STYLESHEET_NOT_EXISTS)
                self.pathNotExists.emit(path)
        else:
            self.setStyleSheet('')


class LabelDropFiles(QLabel):
    """可拖入多个文件的Label，并在拖入时发送拖入的文件路径列表信号"""
    pathsDropped = Signal(List[str])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setScaledContents(True)

    def _emit_signal(self, paths: Union[list, str]):
        """发送信号"""
        if isinstance(paths, str):
            paths = [paths]
        self.pathsDropped.emit(paths)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            paths = []
            for index in range(len(urls)):
                path = urls[index].toLocalFile()
                paths.append(path)
            self._emit_signal(paths)


class LabelDropFilesTip(LabelDropFiles):
    """可拖入多个文件的Label，在拖入时会进行提示，并在拖入时发送拖入的文件路径列表信号"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon_drop = ''  # 拖入时的图标
        self.icon_last = None  # 拖入前的图标

    def set_drop_icon(self, icon_path: str):
        """设置新的拖入图标"""
        self.icon_drop = ''
        if os.path.exists(icon_path):
            self.icon_drop = icon_path

    def dragEnterEvent(self, event):
        super().dragEnterEvent(event)
        if event.mimeData().hasUrls():
            event.accept()
            if self.icon_drop:
                self.icon_last = self.pixmap()
                self.setPixmap(QPixmap(self.icon_drop))  # 拖入时修改图标
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        super().dragLeaveEvent(event)
        if self.icon_drop:
            self.setPixmap(QPixmap(self.icon_last))  # 完成拖入后还原图标
            self.icon_last = None


class LabelShowDropImag(LabelDropFiles):
    """可拖入文件的Label，并将拖入图片显示在Label上，并在拖入时发送拖入的文件路径列表信号"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pathsDropped.connect(self._show_first_image)

    def _show_first_image(self, paths):
        """显示第一张图片"""
        for path in paths:
            if os.path.isfile(path) and filetype.is_image(path):
                self._show_image(path)
                return

        self._clear_image()  # 兜底

    def _show_image(self, image_path: str):
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap)

    def _clear_image(self):
        self.setPixmap(QPixmap())
