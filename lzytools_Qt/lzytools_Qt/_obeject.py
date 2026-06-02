from PySide6.QtCore import QObject, Signal

"""用法示例：
# 创建自定义输出流
self.stderr_stream = ObjectEmittingStream()
# 将信号连接到界面的更新方法
self.stderr_stream.TextWritten.connect(self._show_stderr_text)
# 替换系统输出
# sys.stdout = self.stderr_stream # 可选
sys.stderr = self.stderr_stream
"""


class ObjectEmittingStream(QObject):
    """自定义输出流，用于替代 sys.stdout 或 sys.stderr
    当有内容写入时，通过信号将文本发送出去
    """
    TextWritten = Signal(str)

    _instance = None
    _is_init = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def write(self, text):
        """print 语句最终会调用这个方法"""
        if text and text.strip():
            self.TextWritten.emit(text)

    def flush(self):
        """必须实现，但可以为空"""
        pass
