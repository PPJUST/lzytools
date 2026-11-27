from PySide6.QtCore import QTimer, Signal


class QtimerSingleShot(QTimer):
    """单次触发的 Timer（单例），start() 用法与 QTimer 一致"""

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
        self.setSingleShot(True)

    def start(self, msec=None):
        """启动定时器；可传入毫秒数，兼容 QTimer.start(int)"""
        if msec is not None:
            self.setInterval(int(msec))
        super().start()
        self.timeStart.emit()
