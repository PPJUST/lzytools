from PySide6.QtCore import QPoint, QRect, QSize, Qt, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QDialog, QRubberBand, QVBoxLayout, QWidget


class DialogScreenRegionSelect(QDialog):
    """框选屏幕区域的 Dialog"""
    SelectedRegion = Signal(int, int, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        screen_size = QGuiApplication.primaryScreen().size()
        self.setGeometry(0, 0, screen_size.width(), screen_size.height())
        self.setWindowOpacity(0.5)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget = _WidgetScreenRegionSelect(self)
        widget.SelectedRegion.connect(self.select_region)
        widget.rightClick.connect(self.close)
        layout.addWidget(widget)

    def select_region(self, rect: QRect):
        """接收框选区域并发射四元组信号"""
        self.setWindowOpacity(0)
        self.SelectedRegion.emit(rect.x(), rect.y(), rect.width(), rect.height())
        self.close()


class _WidgetScreenRegionSelect(QWidget):
    """框选控件"""
    SelectedRegion = Signal(QRect)
    rightClick = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.startPoint = None
        self.endPoint = None
        self.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPoint = event.position().toPoint()
            self.endPoint = QPoint(self.startPoint)
            self.rubberBand.setGeometry(QRect(self.startPoint, QSize()))
            self.rubberBand.show()
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightClick.emit()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.startPoint is not None:
            self.endPoint = event.position().toPoint()
            self.rubberBand.setGeometry(
                QRect(self.startPoint, self.endPoint).normalized()
            )
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.startPoint is not None:
            self.endPoint = event.position().toPoint()
            self.rubberBand.hide()
            self.take_select_area()
        super().mouseReleaseEvent(event)

    def take_select_area(self):
        """获取框选区域"""
        if self.startPoint is None or self.endPoint is None:
            return
        rect = QRect(self.startPoint, self.endPoint).normalized()
        self.SelectedRegion.emit(rect)
        self.startPoint = None
        self.endPoint = None
