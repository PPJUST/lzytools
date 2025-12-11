from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ._widget import WidgetLineOpenDeleteText


class ListWidgetFileList(QListWidget):
    """拖入文件/文件夹并显示在列表控件中，附带基础功能"""
    signal_update_list = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.paths = []

    def _add_items(self, paths: list):
        """新增行项目"""
        for path in paths:
            if path not in self.paths:
                self.paths.append(path)

        self._refresh()

    def _refresh(self):
        """刷新项目"""
        self.clear()
        for path in self.paths:
            # 创建子控件
            item = QListWidgetItem()
            item_widget = WidgetLineOpenDeleteText()
            item_widget.set_text(path)
            item_widget.signal_delete.connect(self._delete_item)
            # 插入子控件
            end_index = self.count()
            self.insertItem(end_index + 1, item)
            self.setItemWidget(item, item_widget)

        # 发送更新后的list
        self.signal_update_list.emit(self.paths)

    def _delete_item(self, deleted_path):
        """删除行项目"""
        # 删除变量中的对应数据
        if deleted_path in self.paths:
            self.paths.remove(deleted_path)
        # 刷新
        self._refresh()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            paths = [url.toLocalFile() for url in urls]
            self._add_items(paths)
