from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QStyledItemDelegate


class StyledItemDelegateImage(QStyledItemDelegate):
    """在视图项中绘制等比缩放的图片。

    图片数据需保存在 QStandardItem 的 UserRole 属性中；
    数据缺失或无效时回退到默认绘制。
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        pixmap = index.data(Qt.ItemDataRole.UserRole)
        if not isinstance(pixmap, QPixmap) or pixmap.isNull():
            super().paint(painter, option, index)
            return

        item_rect = option.rect
        if item_rect.isEmpty():
            return

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        scaled_pixmap = pixmap.scaled(
            QSize(item_rect.width(), item_rect.height()),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        x = item_rect.x() + (item_rect.width() - scaled_pixmap.width()) // 2
        y = item_rect.y() + (item_rect.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)
