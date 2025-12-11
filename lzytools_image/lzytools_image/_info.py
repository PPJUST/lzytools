import io
import zipfile
from typing import Union

import lzytools_archive  # 0.0.1
import rarfile
from PIL import Image

"""----------逻辑函数----------"""


def _get_image_size(image_path: str) -> tuple[int, int]:
    """获取图片的宽高
    :param image_path: 本地图片路径
    :return: (宽, 高)"""
    image = Image.open(image_path)
    size = image.size
    image.close()
    return size


def _get_image_filesize_in_archive(archive_path: str, image_path: str) -> int:
    """获取压缩文件中指定图片的文件大小（字节）
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return:图片的文件大小（字节）"""
    infolist = lzytools_archive.get_infolist(archive_path)
    for info in infolist:
        info: Union[zipfile.ZipInfo, rarfile.RarInfo]
        path = info.filename
        if image_path.lower() == path.lower():
            size = info.file_size
            return size

    return 0  # 兜底


def _get_image_size_in_archive(archive_path: str, image_path: str) -> tuple[int, int]:
    """获取压缩文件中指定图片的尺寸
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return: (宽, 高)"""
    image_bytes = lzytools_archive.read_image(archive_path, image_path)
    image_stream = io.BytesIO(image_bytes)
    image_pil = Image.open(image_stream)
    size = image_pil.size
    image_pil.close()
    return size


"""----------调用函数----------"""


def get_image_size(image_path: str) -> tuple[int, int]:
    """获取图片的宽高
    :param image_path: 本地图片路径
    :return: (宽, 高)"""
    return _get_image_size(image_path)


def get_image_filesize_in_archive(archive_path: str, image_path: str) -> int:
    """获取压缩文件中指定图片的文件大小（字节）
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return:图片的文件大小（字节）"""
    return _get_image_filesize_in_archive(archive_path, image_path)


def get_image_filesize_from_archive(archive_path: str, image_path: str) -> int:
    """获取压缩文件中指定图片的文件大小（字节）
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return:图片的文件大小（字节）"""
    return _get_image_filesize_in_archive(archive_path, image_path)


def get_image_size_in_archive(archive_path: str, image_path: str) -> tuple[int, int]:
    """获取压缩文件中指定图片的尺寸
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return: (宽, 高)"""
    return _get_image_size_in_archive(archive_path, image_path)


def get_image_size_from_archive(archive_path: str, image_path: str) -> tuple[int, int]:
    """获取压缩文件中指定图片的尺寸
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return: (宽, 高)"""
    return _get_image_size_in_archive(archive_path, image_path)
