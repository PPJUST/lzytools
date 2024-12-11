import pickle
import socket


def send_data_to_socket(data, host: str, port: str):
    """向本地端口传递数据（使用socket）
    :param data: 任意类型的数据
    :param host: str，主机地址
    :param port: str，端口"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)

    try:
        # 发送数据
        serialized_data = pickle.dumps(data)  # 用pickle序列化，传递更多类型的数据
        sock.sendall(serialized_data)
    finally:
        # 关闭连接
        sock.close()
