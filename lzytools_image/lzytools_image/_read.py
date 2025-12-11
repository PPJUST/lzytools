import os
from typing import Union

import cv2
import numpy

"""----------逻辑函数----------"""


def _read_local_image_to_numpy(image_path: str) -> Union[numpy.ndarray, None]:
    """读取本地图片，返回numpy对象
    :param image_path: 本地图片路径
    :return: numpy对象"""
    if os.path.exists(image_path):
        image_numpy = cv2.imdecode(numpy.fromfile(image_path, dtype=numpy.uint8), -1)
        return image_numpy
    else:
        return None


def _read_local_image_to_bytes(image_path: str) -> Union[bytes, None]:
    """读取本地图片，返回bytes对象
    :param image_path: 本地图片路径
    :return: bytes对象"""
    if os.path.exists(image_path):
        with open(image_path, 'rb') as file:
            image_bytes = file.read()
            return image_bytes
    else:
        return None


"""----------调用函数----------"""


def read_local_image_to_numpy(image_path: str) -> Union[numpy.ndarray, None]:
    """读取本地图片，返回numpy对象
    :param image_path: 本地图片路径
    :return: numpy对象"""
    return _read_local_image_to_numpy(image_path)


def read_image_to_numpy(image_path: str) -> Union[numpy.ndarray, None]:
    """读取本地图片，返回numpy对象
    :param image_path: 本地图片路径
    :return: numpy对象"""
    return _read_local_image_to_numpy(image_path)


def read_local_image_to_bytes(image_path: str) -> Union[bytes, None]:
    """读取本地图片，返回bytes对象
    :param image_path: 本地图片路径
    :return: bytes对象"""
    return _read_local_image_to_bytes(image_path)


def read_image_to_bytes(image_path: str) -> Union[bytes, None]:
    """读取本地图片，返回bytes对象
    :param image_path: 本地图片路径
    :return: bytes对象"""
    return _read_local_image_to_bytes(image_path)
