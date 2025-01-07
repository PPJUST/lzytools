from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class DialogScreenshot(QDialog):
    """添加全屏的半透明遮罩，实现截图操作操作"""
    signal_screenshot = Signal(bytes)

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
        widget = WidgetFrameSelect()
        widget.signal_screenshot_area.connect(self.screenshot)
        widget.rightClick.connect(self.close)
        layout.addWidget(widget)

    def screenshot(self, rect: QRect):
        # 去除遮罩
        self.setWindowOpacity(0)  # 0~1，0为完全透明
        # 截图
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
        screenshot_bytes = self.pixmap_to_bytes(screenshot)
        # 转为bytes图片对象，并发送信号
        self.signal_screenshot.emit(screenshot_bytes)

        self.close()

    @staticmethod
    def pixmap_to_bytes(pixmap: QPixmap) -> bytes:
        """将QPixmap转为bytes对象。"""
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QBuffer.WriteOnly)

        # 将 QPixmap 转为 PNG 格式保存到内存
        pixmap.save(buffer, "PNG")

        # 转换 QByteArray 为 bytes
        return byte_array.data()


class WidgetFrameSelect(QWidget):
    """在QWidget中实现截取区域的操作，发送截取区域的信号"""
    signal_screenshot_area = Signal(QRect)  # 发送截取区域QRect
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
            self.take_screenshot_area()  # 获取截取区域

    def take_screenshot_area(self):
        """获取截取区域
        注意：由于外部有半透明遮罩，所以不在该函数中直接进行截图操作"""
        rect = QRect(self.startPoint, self.endPoint).normalized()
        self.signal_screenshot_area.emit(rect)
