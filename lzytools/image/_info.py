import io
import zipfile
from typing import Union

import rarfile
from PIL import Image

from ..archive import get_infolist, read_image


def get_image_size(image_path: str):
    """获取图片的宽高
    :param image_path: str，本地图片路径"""
    image = Image.open(image_path)
    size = image.size
    return size


def get_image_filesize_from_archive(archive_path: str, image_path: str) -> int:
    """获取压缩文件中指定图片的文件大小（字节）
    :param archive_path: str，压缩文件路径
    :param image_path: str，压缩包内部图片路径
     :return: int，压缩文件中指定图片的文件大小（字节）"""
    infolist = get_infolist(archive_path)
    for info in infolist:
        info: Union[zipfile.ZipInfo, rarfile.RarInfo]
        path = info.filename
        if image_path.lower() == path.lower():
            size = info.file_size
            return size

    return 0  # 兜底


def get_image_size_from_archive(archive_path: str, image_path: str) -> tuple[int, int]:
    """获取压缩文件中指定图片的尺寸
    :param archive_path: str，压缩文件路径
    :param image_path: str，压缩包内部图片路径
     :return: tuple，(宽, 高）"""
    image_bytes = read_image(archive_path, image_path)
    image_stream = io.BytesIO(image_bytes)
    image_pil = Image.open(image_stream)
    size = image_pil.size
    return size
