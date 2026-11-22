import pickle
import socket

"""----------逻辑函数----------"""


def _send_data_to_socket(data: object, host: str, port: int | str, timeout: float = 5.0) -> None:
    """向指定主机和端口传递数据（使用 socket）

    :param data: 任意可 pickle 序列化的数据
    :param host: str，主机地址
    :param port: int 或 str，端口号
    :param timeout: float，连接和发送的超时时间（秒）
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, int(port)))
        sock.sendall(pickle.dumps(data))


"""----------调用函数----------"""


def send_data_to_socket(data: object, host: str, port: int | str, timeout: float = 5.0) -> None:
    """向指定主机和端口传递数据（使用 socket）

    :param data: 任意可 pickle 序列化的数据
    :param host: str，主机地址
    :param port: int 或 str，端口号
    :param timeout: float，连接和发送的超时时间（秒）
    """
    _send_data_to_socket(data, host, port, timeout)
