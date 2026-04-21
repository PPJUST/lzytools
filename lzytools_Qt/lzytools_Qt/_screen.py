from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class DialogScreenRegionSelect(QDialog):
    """框选屏幕区域的Dialog"""
    SelectedRegion = Signal(int, int, int, int, name='左上角x轴坐标，左上角y轴坐标，宽度，高度')

    def __init__(self):
        super().__init__()
        # 设置无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 设置置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 设置为全屏大小
        screen_geometry = QGuiApplication.primaryScreen().size()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.setGeometry(0, 0, screen_width, screen_height)
        # 设置半透明
        self.setWindowOpacity(0.5)  # 0~1，0为完全透明

        # 添加框选控件
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget = _WidgetScreenRegionSelect()
        widget.SelectedRegion.connect(self.select_region)
        widget.rightClick.connect(self.close)
        layout.addWidget(widget)

    def select_region(self, rect: QRect):
        # 去除遮罩
        self.setWindowOpacity(0)  # 0~1，0为完全透明

        # 提取框选区域
        x = rect.x()
        y = rect.y()
        width = rect.width()
        height = rect.height()

        self.SelectedRegion.emit(x, y, width, height)

        self.close()


class _WidgetScreenRegionSelect(QWidget):
    """框选控件"""
    SelectedRegion = Signal(QRect)  # 发送截取区域QRect
    rightClick = Signal()  # 右键信号

    def __init__(self):
        super().__init__()
        # 初始化变量
        self.startPoint = None  # 截取起始点
        self.endPoint = None  # 截取终止点
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)  # 橡皮筋控件（蚂蚁线）

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # 左键
            self.startPoint = event.pos()
            self.rubberBand.setGeometry(QRect(self.startPoint, QSize()))
            self.rubberBand.show()
        elif event.button() == Qt.RightButton:  # 右键
            self.rightClick.emit()

    def mouseMoveEvent(self, event):
        if self.startPoint:
            self.endPoint = event.pos()
            self.rubberBand.setGeometry(QRect(self.startPoint, self.endPoint).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.startPoint:
            self.endPoint = event.pos()
            self.rubberBand.hide()
            self.take_select_area()  # 获取截取区域

    def take_select_area(self):
        """获取框选区域"""
        rect = QRect(self.startPoint, self.endPoint).normalized()
        self.SelectedRegion.emit(rect)
