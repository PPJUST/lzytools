from PySide6.QtCore import *
from PySide6.QtWidgets import *

from ._function import set_transparent_background


class WidgetLineOpenDeleteText(QWidget):
    """控件组合，打开按钮-删除按钮-文本框"""
    signal_delete = Signal(str)
    signal_open = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.set_layout()
        self.toolButton_open = QToolButton()
        self._add_open_button()
        self.toolButton_delete = QToolButton()
        self._add_delete_button()
        self.text_label = QLabel()
        self._add_text_label()

        self.text = ''

    def set_text(self, text: str):
        """设置文本"""
        self.text_label.setText(text)
        self.text = text

    def set_tooltip(self, text: str):
        """设置文本提示"""
        self.text_label.setToolTip(text)

    def set_layout(self):
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setStretch(1, 1)

    def _open(self):
        self.signal_open.emit(self.text)

    def _delete(self):
        self.deleteLater()
        self.signal_delete.emit(self.text)

    def _add_open_button(self):
        self.toolButton_open.setText('□')
        set_transparent_background(self.toolButton_open)
        self.layout.addWidget(self.toolButton_open)
        self.toolButton_open.clicked.connect(self._open)

    def _add_delete_button(self):
        self.toolButton_delete.setText('×')
        set_transparent_background(self.toolButton_delete)
        self.layout.addWidget(self.toolButton_delete)
        self.toolButton_delete.clicked.connect(self._delete)

    def _add_text_label(self):
        self.text_label.setText('')
        self.layout.addWidget(self.text_label)


class WidgetAutoHidden(QWidget):
    """悬停时显示，离开时隐藏的Widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置计时器
        self.qtimer_hidden = QTimer()
        self.qtimer_hidden.setInterval(500)
        self.qtimer_hidden.setSingleShot(True)
        self.qtimer_hidden.timeout.connnect(self.hide)

    def set_interval(self, second: float):
        """设置延迟隐藏的时间间隔"""
        self.qtimer_hidden.setInterval(int(second * 1000))

    def enterEvent(self, event):
        super().enterEvent(event)
        self.show()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.qtimer_hidden.start()
