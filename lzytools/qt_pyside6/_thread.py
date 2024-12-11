import pickle
import socket

from PySide6.QtCore import *


class ThreadListenSocket(QThread):
    """监听本地端口的子线程"""
    signal_receive_args = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.host = '127.0.0.1'  # 主机地址
        self.port = '9527'  # 端口
        self.client_limit_count = 2  # 同时连接的客户端上限

    def set_host(self, host: str):
        """设置主机地址"""
        self.host = host

    def set_port(self, port: str):
        """设置端口"""
        self.port = port

    def set_client_limit_count(self, count: int):
        """设置同时连接的客户端上限"""
        self.client_limit_count = count

    def get_host(self):
        """获取绑定的主机地址"""
        return self.host

    def get_port(self):
        """获取绑定的端口"""
        return self.port

    def get_client_limit_count(self):
        """获取同时连接的客户端上限"""
        return self.client_limit_count

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(self.client_limit_count)
        while True:
            connection, client_address = sock.accept()
            try:
                # 接收数据
                data = connection.recv(1024)
                if data:
                    args = pickle.loads(data)
                    # 打印接收到的参数
                    print(f'接收参数：{args}')
                    self.signal_receive_args.emit(args)
            finally:
                connection.close()  # 关闭连接
