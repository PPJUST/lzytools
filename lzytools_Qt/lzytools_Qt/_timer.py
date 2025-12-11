from PySide6.QtCore import *


class QtimerSingleShot(QTimer):
    """单次触发的Timer（单例）"""
    _instance = None
    _is_init = False
    timeStart = Signal()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if not self._is_init:
            super().__init__(parent)
            self._is_init = True
        self.setSingleShot(True)  # 设置为单次触发

    def start(self):
        super().start()
        self.timeStart.emit()
