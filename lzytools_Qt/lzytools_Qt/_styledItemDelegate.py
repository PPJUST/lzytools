from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class StyledItemDelegateImage(QStyledItemDelegate):
    """用于在QStandardItem中显示自适应大小的图像的项目视图委托QStyledItemDelegate
    注意：图片数据需在保存在QStandardItem的UserRole属性中"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        # 获取QStandardItem中的图片数据
        pixmap = index.data(Qt.UserRole)
        if not pixmap:
            raise Exception('错误，图片数据需在保存在QStandardItem的UserRole属性中')

        # 创建绘制工具
        item_rect = option.rect
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)

        # 缩放图片以适应QStandardItem
        scaled_pixmap = pixmap.scaled(QSize(item_rect.width(), item_rect.height()),
                                      Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # 在QStandardItem上绘制图片
        painter.drawPixmap(item_rect.x() + (item_rect.width() - scaled_pixmap.width()) / 2,
                           item_rect.y() + (item_rect.height() - scaled_pixmap.height()) / 2,
                           scaled_pixmap.width(), scaled_pixmap.height(), scaled_pixmap)
