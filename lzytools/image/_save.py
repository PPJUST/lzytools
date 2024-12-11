import io
import os
from typing import Union

import numpy
from PIL import Image


def save_bytes_image(bytes_image: bytes, dirpath: str, filename: str) -> str:
    """将一个bytes图片对象保存至本地
    :param bytes_image: bytes，bytes图片对象
    :param dirpath: str，保存至该目录下
    :param filename: str，保存的文件名（不含文件扩展名）
    :return: str，保存的本地图片路径"""
    image = Image.open(io.BytesIO(bytes_image))

    # 转换图像模式，防止报错OSError: cannot write mode P as JPEG
    image = image.convert('RGB')

    # 提取文件后缀
    file_extension = image.format  # 备忘录 找一个读取bytes图片后缀的方法

    # 组合保存路径
    save_path = os.path.normpath(os.path.join(dirpath, filename + file_extension))

    # 保存到本地
    if not os.path.exists(dirpath):
        os.mkdir(save_path)
    image.save(save_path)

    return save_path


def save_numpy_image(numpy_image: numpy.ndarray, dirpath: str, filename: str) -> str:
    """将一个numpy图片对象保存至本地
    :param numpy_image: numpy.ndarray，numpy图片对象
    :param dirpath: str，保存至该目录下
    :param filename: str，保存的文件名（不含文件扩展名）
    :return: str，保存的本地图片路径"""
    # 转换为uint8类型
    numpy_image = numpy_image.astype(numpy.uint8)

    # 转换为Pillow图像对象
    image = Image.fromarray(numpy_image)

    # 提取文件后缀
    file_extension = image.format

    # 组合保存路径
    save_path = os.path.normpath(os.path.join(dirpath, filename + file_extension))

    # 保存到本地
    if not os.path.exists(dirpath):
        os.mkdir(save_path)
    image.save(save_path)

    return save_path


def save_local(image: Union[bytes, numpy.ndarray], dirpath: str, filename: str) -> str:
    """将一个bytes/numpy图片对象保存至本地
    :param image: bytes/numpy图片对象
    :param dirpath: str，保存至该目录下
    :param filename: str，保存的文件名（不含文件扩展名）
    :return: str，保存的本地图片路径"""
    if isinstance(image, bytes):
        return save_bytes_image(image, dirpath, filename)
    elif isinstance(image, numpy.ndarray):
        return save_numpy_image(image, dirpath, filename)
    else:
        raise Exception(f'不支持的图片类型：{type(image)}')
