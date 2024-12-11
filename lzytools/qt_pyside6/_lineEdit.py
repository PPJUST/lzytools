import os
from typing import Union

import filetype
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ._function import calculate_keep_aspect_ratio_resize


class LineEditDropFiles(QLineEdit):
    """支持拖入多个文件/文件夹的文本框，设置文本为拖入的路径，并发送信号传递拖入路径的list"""

    signal_path_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setReadOnly(True)
        self.setPlaceholderText('拖入文件到此处...')

        self.path_dropped = []

    def update_paths(self, paths: list):
        """更新路径
        :param paths: list，包含完整路径的列表"""
        # 列表去重
        paths = list(dict.fromkeys(paths))
        # 重置参数
        self.path_dropped = paths
        # 更新文本
        self._update_text(paths)
        # 发送信号
        self._emit_signal(paths)

    def _update_text(self, paths: Union[list, str]):
        """更新文本"""
        if isinstance(paths, str):
            paths = [paths]
        self.setText(';'.join(paths))
        self.setToolTip('/n'.join(paths))

    def _emit_signal(self, paths: Union[list, str]):
        """发送信号"""
        if isinstance(paths, str):
            paths = [paths]
        self.signal_path_dropped.emit(paths)

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
            self.update_paths(paths)


class LineEditDropFile(LineEditDropFiles):
    """支持拖入单个文件/文件夹的文本框，设置文本为拖入的路径，并发送信号传递拖入路径的list
    新增功能：定时检查路径有效性"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置一个QTime，定时检查路径有效性
        self.is_exists = True
        self.stylesheet_not_exists = 'border: 1px solid red;'
        self.qtimer_check_path_exists = QTimer()
        self.qtimer_check_path_exists.timeout.connect(self._check_path_exists)
        self.qtimer_check_path_exists.setInterval(5000)  # 默认定时5秒
        self.qtimer_check_path_exists.start()

    def update_paths(self, paths: list):
        """更新路径
        :param paths: list，包含完整路径的列表"""
        # 提取首个路径
        path = paths[0]
        # 重置参数
        self.path_dropped = path
        # 更新文本
        self._update_text(path)
        # 发送信号
        self._emit_signal(path)

    def set_check_interval(self, second: float):
        """设置定时检查路径有效性的时间间隔"""
        self.qtimer_check_path_exists.setInterval(int(second * 1000))

    def set_stylesheet_not_exists(self, stylesheet: str):
        """设置路径不存在时的文本框样式"""
        self.stylesheet_not_exists = stylesheet

    def _check_path_exists(self):
        """检查路径有效性"""
        if self.path_dropped:
            if os.path.exists(self.path_dropped):
                self.is_exists = True
                self.setStyleSheet('')
            else:
                self.is_exists = False
                self.setStyleSheet(self.stylesheet_not_exists)
        else:
            self.is_exists = False


class LabelDropFiles(QLabel):
    """支持拖入多个文件/文件夹的标签控件，并发送信号传递拖入路径的list"""

    signal_path_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setScaledContents(True)

        self.path_dropped = []

    def update_paths(self, paths: list):
        """更新路径
        :param paths: list，包含完整路径的列表"""
        # 列表去重
        paths = list(dict.fromkeys(paths))
        # 重置参数
        self.path_dropped = paths
        # 发送信号
        self._emit_signal(paths)

    def _emit_signal(self, paths: Union[list, str]):
        """发送信号"""
        if isinstance(paths, str):
            paths = [paths]
        self.signal_path_dropped.emit(paths)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            paths = [url.toLocalFile() for url in urls]
            self.update_paths(paths)


class LabelDropFilesTip(LabelDropFiles):
    """支持拖入多个文件/文件夹的标签控件，并发送信号传递拖入路径的list
    新增功能：拖入时会提示"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon_drop = ''  # 拖入时的图标
        self.icon_last = None  # 拖入前的图标

    def set_drop_icon(self, icon_path: str):
        """拖入图标路径"""
        self.icon_drop = ''
        if os.path.exists(icon_path):
            self.icon_drop = icon_path

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            if self.icon_drop:
                self.icon_last = self.pixmap()
                self.setPixmap(QPixmap(self.icon_drop))  # 拖入时修改图标
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        if self.icon_drop:
            self.setPixmap(QPixmap(self.icon_last))  # 完成拖入后变回原图标
            self.icon_last = None


class LabelDropImageShow(LabelDropFiles):
    """拖入单个图片文件并显示"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def update_paths(self, paths: list):
        """更新路径
        :param paths: list，包含完整路径的列表"""
        # 提取首个路径并进行检查
        path = paths[0]
        self.path_dropped = ''
        if os.path.isfile(path) and filetype.is_image(path):
            self.path_dropped = path

        # 显示图片
        if self.path_dropped:
            self._show_image(self.path_dropped)
        else:
            self._clear_image()

        # 发送信号
        self._emit_signal(paths)

    def _show_image(self, image_path: str):
        pixmap = QPixmap(image_path)
        resize = calculate_keep_aspect_ratio_resize(self.size(), pixmap.size())
        pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
        self.setPixmap(pixmap)

    def _clear_image(self):
        self.setPixmap(QPixmap())
