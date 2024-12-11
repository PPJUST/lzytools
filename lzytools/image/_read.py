import os
from typing import Union

import cv2
import numpy


def read_image_to_numpy(image_path: str) -> numpy.ndarray:
    """读取本地图片，返回numpy图片对象
    :param image_path: 图片路径
    :return: numpy图片对象"""
    image_numpy = cv2.imdecode(numpy.fromfile(image_path, dtype=numpy.uint8), -1)

    return image_numpy


def read_image_to_bytes(image_path: str) -> bytes:
    """读取本地图片，返回bytes图片对象
    :param image_path: 图片路径
    :return: bytes图片对象"""
    if os.path.exists(image_path):
        with open(image_path, 'rb') as file:
            image_bytes = file.read()
    else:
        image_bytes = rb''

    return image_bytes


def read_image(image_path: str, type_: str = 'bytes') -> Union[bytes, numpy.ndarray]:
    """读取本地图片，返回bytes图片对象
    :param image_path: 图片路径
    :param type_: 返回的数据类型，'bytes'/'numpy'
    :return: bytes/numpy图片对象"""
    _TYPE = ['bytes', 'numpy']
    if type_.lower() not in _TYPE:
        raise Exception('读取类型输入错误')

    if type_.lower() == 'bytes':
        img = read_image_to_bytes(image_path)
    else:
        img = read_image_to_numpy(image_path)

    return img
