import cv2
import numpy

"""----------逻辑函数----------"""


def _read_local_image_to_bytes(image_path: str) -> bytes | None:
    """读取本地图片，返回 bytes 图片对象。
    :param image_path: 本地图片路径
    :return: bytes 图片对象，文件不存在或不可读时返回 None
    """
    try:
        with open(image_path, 'rb') as image_file:
            return image_file.read()
    except OSError:
        return None


def _read_local_image_to_numpy(image_path: str) -> numpy.ndarray | None:
    """读取本地图片，返回 numpy 图片对象（保留 alpha 通道）。
    :param image_path: 本地图片路径
    :return: numpy 图片对象，文件不存在、不可读或无法解码时返回 None
    """
    image_bytes = _read_local_image_to_bytes(image_path)
    if not image_bytes:
        return None
    return cv2.imdecode(numpy.frombuffer(image_bytes, dtype=numpy.uint8), -1)


"""----------调用函数----------"""


def read_local_image_to_numpy(image_path: str) -> numpy.ndarray | None:
    """读取本地图片，返回 numpy 图片对象（保留 alpha 通道）。
    :param image_path: 本地图片路径
    :return: numpy 图片对象，文件不存在、不可读或无法解码时返回 None
    """
    return _read_local_image_to_numpy(image_path)


def read_image_to_numpy(image_path: str) -> numpy.ndarray | None:
    """读取本地图片，返回 numpy 图片对象（保留 alpha 通道）。
    :param image_path: 本地图片路径
    :return: numpy 图片对象，文件不存在、不可读或无法解码时返回 None
    """
    return _read_local_image_to_numpy(image_path)


def read_local_image_to_bytes(image_path: str) -> bytes | None:
    """读取本地图片，返回 bytes 图片对象。
    :param image_path: 本地图片路径
    :return: bytes 图片对象，文件不存在或不可读时返回 None
    """
    return _read_local_image_to_bytes(image_path)


def read_image_to_bytes(image_path: str) -> bytes | None:
    """读取本地图片，返回 bytes 图片对象。
    :param image_path: 本地图片路径
    :return: bytes 图片对象，文件不存在或不可读时返回 None
    """
    return _read_local_image_to_bytes(image_path)
