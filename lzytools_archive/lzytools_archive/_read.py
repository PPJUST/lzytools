import zipfile
from typing import Union

import rarfile

"""----------逻辑函数----------"""


def _read_archive(archive_path: str) -> Union[zipfile.ZipFile, rarfile.RarFile, None]:
    """读取压缩文件，并返回压缩文件对象（仅支持zip和rar）
    :param archive_path: 压缩文件路径
    :return: 返回zip/rar对象，未成功读取时返回None"""
    try:
        archive = zipfile.ZipFile(archive_path)
    except zipfile.BadZipFile:
        try:
            archive = rarfile.RarFile(archive_path)
        except rarfile.NotRarFile:
            return None
    except FileNotFoundError:
        return None

    return archive


def _get_infolist(archive_path: str) -> list[zipfile.ZipInfo]:
    """获取压缩文件的内部信息list（仅支持zip和rar）
    :param archive_path: 压缩文件路径
    :return: zipfile/rarfile库读取的压缩文件的infolist"""
    archive = _read_archive(archive_path)
    if not archive:
        raise Exception('未正确读取文件，该文件不是压缩文件或文件不存在')

    infolist = archive.infolist()  # 中文等字符会变为乱码

    archive.close()

    return infolist


def _get_structure(archive_path: str) -> list:
    """获取压缩文件的内部文件结构（仅支持zip和rar）
    :param archive_path: 压缩文件路径
    :return: 内部文件和文件夹，按层级排序"""
    infolist = _get_infolist(archive_path)
    filenames = [i.filename for i in infolist]

    return filenames


def _get_real_size(archive_path: str) -> int:
    """获取一个压缩文件的内部文件大小（解压后的原始文件大小）
    :param archive_path: 压缩文件路径
    :return: 压缩包内部文件的实际大小（字节）"""
    total_size = 0
    infolist = _get_infolist(archive_path)
    for info in infolist:
        info: Union[zipfile.ZipInfo, rarfile.RarInfo]
        total_size += info.file_size

    return total_size


def _read_image(archive_path: str, image_path: str) -> bytes:
    """读取压缩文件中的指定图片，返回一个bytes图片对象
    :param archive_path: 压缩文件路径
    :param image_path: 压缩包内部图片路径"""
    # 由于zipfile仅支持/路径分隔符，而不支持\，所以需要将\都替换为/
    image_path = image_path.replace('\\', '/')
    archive = _read_archive(archive_path)
    if not archive:
        raise Exception('未正确读取文件，该文件不是压缩文件或文件不存在')

    try:
        img_data = archive.read(image_path)
    except KeyError:
        raise Exception('压缩文件中不存在该文件')

    archive.close()

    return img_data


"""----------调用函数----------"""


def read_archive(archive_path: str) -> Union[zipfile.ZipFile, rarfile.RarFile, None]:
    """读取压缩文件，并返回压缩文件对象（仅支持zip和rar）
    :param archive_path: 压缩文件路径
    :return: 返回zip/rar对象，未成功读取时返回None"""
    return _read_archive(archive_path)


def get_infolist(archive_path: str) -> list[zipfile.ZipInfo]:
    """获取压缩文件的内部信息list（仅支持zip和rar）
    :param archive_path: 压缩文件路径
    :return: zipfile/rarfile库读取的压缩文件的infolist"""
    return _get_infolist(archive_path)


def get_structure(archive_path: str) -> list:
    """获取压缩文件的内部文件结构（仅支持zip和rar）
    :param archive_path: 压缩文件路径
    :return: 内部文件和文件夹，按层级排序"""
    return _get_structure(archive_path)


def get_real_size(archive_path: str) -> int:
    """获取一个压缩文件的内部文件大小（解压后的原始文件大小）
    :param archive_path: 压缩文件路径
    :return: 压缩包内部文件的实际大小（字节）"""
    return _get_real_size(archive_path)


def read_image(archive_path: str, image_path: str) -> bytes:
    """读取压缩文件中的指定图片，返回一个bytes图片对象
    :param archive_path: 压缩文件路径
    :param image_path: 压缩包内部图片路径"""
    return _read_image(archive_path, image_path)
