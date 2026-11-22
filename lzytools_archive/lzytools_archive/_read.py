import os
import zipfile
from typing import cast

import rarfile

"""----------常量----------"""

# 压缩文件内部信息条目类型（rarfile 无类型存根，此处显式标注）
_ArchiveInfo = zipfile.ZipInfo | rarfile.RarInfo
# 无法读取压缩文件时的统一提示
_READ_ARCHIVE_ERROR = '未正确读取文件，该文件不是压缩文件或文件不存在'

"""----------逻辑函数----------"""


def _read_archive(archive_path: str) -> zipfile.ZipFile | rarfile.RarFile | None:
    """读取压缩文件，并返回压缩文件对象（仅支持 zip 和 rar）
    :param archive_path: 压缩文件路径
    :return: zip/rar 对象，读取失败时返回 None（由调用方负责关闭）
    """
    if not os.path.isfile(archive_path):
        return None

    try:
        return zipfile.ZipFile(archive_path)
    except zipfile.BadZipFile:
        pass  # 不是 zip，继续尝试按 rar 读取
    except OSError:
        return None

    try:
        return rarfile.RarFile(archive_path)
    except (rarfile.Error, OSError):
        return None


def _get_infolist(archive_path: str) -> list[_ArchiveInfo]:
    """获取压缩文件的内部信息列表（仅支持 zip 和 rar）
    :param archive_path: 压缩文件路径
    :return: zipfile/rarfile 库读取的内部信息列表（非 UTF-8 编码的压缩包中中文名可能乱码）
    :raises ValueError: 文件不是压缩文件或不存在
    """
    archive = _read_archive(archive_path)
    if archive is None:
        raise ValueError(_READ_ARCHIVE_ERROR)

    with archive:
        return cast(list[_ArchiveInfo], archive.infolist())


def _get_structure(archive_path: str) -> list[str]:
    """获取压缩文件的内部文件结构（仅支持 zip 和 rar）
    :param archive_path: 压缩文件路径
    :return: 内部文件和文件夹路径列表
    """
    return [info.filename for info in _get_infolist(archive_path)]


def _get_real_size(archive_path: str) -> int:
    """获取压缩文件的内部文件大小（解压后的原始总大小）
    :param archive_path: 压缩文件路径
    :return: 压缩包内部文件的实际总大小（字节）
    """
    return sum(info.file_size for info in _get_infolist(archive_path))


def _read_image(archive_path: str, image_path: str) -> bytes:
    """读取压缩文件中的指定图片，返回 bytes 图片对象
    :param archive_path: 压缩文件路径
    :param image_path: 压缩包内部图片路径
    :return: 图片字节数据
    :raises ValueError: 文件不是压缩文件或不存在
    :raises KeyError: 压缩文件中不存在指定文件
    """
    # zipfile 仅支持 '/' 作为路径分隔符
    image_path = image_path.replace('\\', '/')

    archive = _read_archive(archive_path)
    if archive is None:
        raise ValueError(_READ_ARCHIVE_ERROR)

    with archive:
        try:
            return archive.read(image_path)
        except KeyError as e:
            raise KeyError(f'压缩文件中不存在该文件：{image_path}') from e


"""----------调用函数----------"""


def read_archive(archive_path: str) -> zipfile.ZipFile | rarfile.RarFile | None:
    """读取压缩文件，并返回压缩文件对象（仅支持 zip 和 rar）
    :param archive_path: 压缩文件路径
    :return: zip/rar 对象，读取失败时返回 None（由调用方负责关闭）
    """
    return _read_archive(archive_path)


def get_infolist(archive_path: str) -> list[_ArchiveInfo]:
    """获取压缩文件的内部信息列表（仅支持 zip 和 rar）
    :param archive_path: 压缩文件路径
    :return: zipfile/rarfile 库读取的内部信息列表（非 UTF-8 编码的压缩包中中文名可能乱码）
    """
    return _get_infolist(archive_path)


def get_structure(archive_path: str) -> list[str]:
    """获取压缩文件的内部文件结构（仅支持 zip 和 rar）
    :param archive_path: 压缩文件路径
    :return: 内部文件和文件夹路径列表
    """
    return _get_structure(archive_path)


def get_real_size(archive_path: str) -> int:
    """获取压缩文件的内部文件大小（解压后的原始总大小）
    :param archive_path: 压缩文件路径
    :return: 压缩包内部文件的实际总大小（字节）
    """
    return _get_real_size(archive_path)


def read_image(archive_path: str, image_path: str) -> bytes:
    """读取压缩文件中的指定图片，返回 bytes 图片对象
    :param archive_path: 压缩文件路径
    :param image_path: 压缩包内部图片路径
    :return: 图片字节数据
    """
    return _read_image(archive_path, image_path)
