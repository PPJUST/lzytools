import io

import lzytools_archive
from PIL import Image

"""----------逻辑函数----------"""


def _get_image_size(image_path: str) -> tuple[int, int]:
    """获取图片的宽高。
    :param image_path: 本地图片路径
    :return: (宽, 高)
    """
    with Image.open(image_path) as image:
        return image.size


def _get_image_filesize_in_archive(archive_path: str, image_path: str) -> int:
    """获取压缩文件中指定图片的文件大小（字节）。
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return: 图片的文件大小（字节），未找到时返回 0
    """
    # zipfile 仅支持 '/' 作为路径分隔符
    image_path = image_path.replace('\\', '/').lower()
    infolist = lzytools_archive.get_infolist(archive_path)
    return next((info.file_size for info in infolist if info.filename.lower() == image_path), 0)


def _get_image_size_in_archive(archive_path: str, image_path: str) -> tuple[int, int]:
    """获取压缩文件中指定图片的尺寸。
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return: (宽, 高)
    """
    image_bytes = lzytools_archive.read_image(archive_path, image_path)
    with io.BytesIO(image_bytes) as image_stream, Image.open(image_stream) as image:
        return image.size


"""----------调用函数----------"""


def get_image_size(image_path: str) -> tuple[int, int]:
    """获取图片的宽高。
    :param image_path: 本地图片路径
    :return: (宽, 高)
    """
    return _get_image_size(image_path)


def get_image_filesize_in_archive(archive_path: str, image_path: str) -> int:
    """获取压缩文件中指定图片的文件大小（字节）。
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return: 图片的文件大小（字节），未找到时返回 0
    """
    return _get_image_filesize_in_archive(archive_path, image_path)


def get_image_filesize_from_archive(archive_path: str, image_path: str) -> int:
    """获取压缩文件中指定图片的文件大小（字节）。
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return: 图片的文件大小（字节），未找到时返回 0
    """
    return _get_image_filesize_in_archive(archive_path, image_path)


def get_image_size_in_archive(archive_path: str, image_path: str) -> tuple[int, int]:
    """获取压缩文件中指定图片的尺寸。
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return: (宽, 高)
    """
    return _get_image_size_in_archive(archive_path, image_path)


def get_image_size_from_archive(archive_path: str, image_path: str) -> tuple[int, int]:
    """获取压缩文件中指定图片的尺寸。
    :param archive_path: 压缩文件路径
    :param image_path: 压缩文件内部图片路径
    :return: (宽, 高)
    """
    return _get_image_size_in_archive(archive_path, image_path)
