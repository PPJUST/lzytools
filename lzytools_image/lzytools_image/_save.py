import io
import os

import numpy
from PIL import Image

"""----------逻辑函数----------"""


def _save_bytes_image(bytes_image: bytes, dirpath: str, filetitle: str) -> str:
    """将一个bytes图片对象保存至本地
    :param bytes_image: bytes图片对象
    :param dirpath: 需要保存到的目录
    :param filetitle: 保存的文件标题（不含文件扩展名）
    :return: 保存到本地的图片路径"""
    image = Image.open(io.BytesIO(bytes_image))

    # 清除元数据
    image.info.clear()

    # 转换图像模式，防止报错OSError: cannot write mode P as JPEG
    image = image.convert('RGB')

    # 提取文件扩展名
    file_extension = image.format  # 文件扩展名带.

    # 如果未提取到文件后缀，则使用jpg格式
    if not file_extension:
        file_extension = '.jpg'

    # 组合保存路径
    filename = filetitle + file_extension
    save_path = os.path.normpath(os.path.join(dirpath, filename))

    # 保存到本地
    if not os.path.exists(dirpath):
        os.mkdir(save_path)
    image.save(save_path)
    image.close()

    return save_path


def _save_numpy_image(numpy_image: numpy.ndarray, dirpath: str, filetitle: str) -> str:
    """将一个numpy图片对象保存至本地
    :param numpy_image: numpy图片对象
    :param dirpath: 需要保存到的目录
    :param filetitle: 保存的文件标题（不含文件扩展名）
    :return: 保存到本地的图片路径"""
    # 转换为uint8类型
    numpy_image = numpy_image.astype(numpy.uint8)

    # 转换为Pillow图像对象
    image = Image.fromarray(numpy_image)

    # 清除元数据
    image.info.clear()

    # 转换图像模式，防止报错OSError: cannot write mode P as JPEG
    image = image.convert('RGB')

    # 提取文件扩展名
    file_extension = image.format  # 文件扩展名带.

    # 如果未提取到文件后缀，则使用jpg格式
    if not file_extension:
        file_extension = '.jpg'

    # 组合保存路径
    filename = filetitle + file_extension
    save_path = os.path.normpath(os.path.join(dirpath, filename))

    # 保存到本地
    if not os.path.exists(dirpath):
        os.mkdir(save_path)
    image.save(save_path)
    image.close()

    return save_path


"""----------调用函数----------"""


def save_bytes_image(bytes_image: bytes, dirpath: str, filetitle: str) -> str:
    """将一个bytes图片对象保存至本地
    :param bytes_image: bytes图片对象
    :param dirpath: 需要保存到的目录
    :param filetitle: 保存的文件标题（不含文件扩展名）
    :return: 保存到本地的图片路径"""
    return _save_bytes_image(bytes_image, dirpath, filetitle)


def save_numpy_image(numpy_image: numpy.ndarray, dirpath: str, filetitle: str) -> str:
    """将一个numpy图片对象保存至本地
    :param numpy_image: numpy图片对象
    :param dirpath: 需要保存到的目录
    :param filetitle: 保存的文件标题（不含文件扩展名）
    :return: 保存到本地的图片路径"""
    return _save_numpy_image(numpy_image, dirpath, filetitle)
