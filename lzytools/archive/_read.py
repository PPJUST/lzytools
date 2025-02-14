import zipfile
from typing import Union

import rarfile


def read_archive(archive_path: str) -> Union[zipfile.ZipFile, rarfile.RarFile, bool]:
    """读取压缩文件，并返回压缩文件对象（仅支持zip和rar）
    :param archive_path: str，压缩文件路径
    :return: 返回zip/rar对象，或正确读取文件时返回False"""
    try:
        archive = zipfile.ZipFile(archive_path)
    except zipfile.BadZipFile:
        try:
            archive = rarfile.RarFile(archive_path)
        except rarfile.NotRarFile:
            return False
    except FileNotFoundError:
        return False

    return archive


def get_infolist(archive_path: str) -> list[zipfile.ZipInfo]:
    """获取压缩文件的内部信息list（仅支持zip和rar）
    :param archive_path: str，压缩文件路径
    :return: list，zipfile/rarfile库读取的压缩文件的infolist"""
    archive = read_archive(archive_path)
    if not archive:
        raise Exception('未正确读取文件，该文件不是压缩文件或文件不存在')

    infolist = archive.infolist()  # 中文等字符会变为乱码

    archive.close()

    return infolist


def get_structure(archive_path: str) -> list:
    """获取压缩文件的内部文件结构（仅支持zip和rar）
    :param archive_path: str，压缩文件路径
    :return: list，内部文件和文件夹，按层级排序"""
    infolist = get_infolist(archive_path)
    filenames = [i.filename for i in infolist]

    return filenames


def get_real_size(archive_path: str) -> int:
    """获取一个压缩文件的内部文件大小（解压后的原始文件大小）
    :param archive_path: str，压缩文件路径
    :return: int，压缩包内部文件的实际大小（字节）"""
    total_size = 0
    infolist = get_infolist(archive_path)
    for info in infolist:
        info: Union[zipfile.ZipInfo, rarfile.RarInfo]
        total_size += info.file_size

    return total_size


def read_image(archive_path: str, image_path: str) -> bytes:
    """读取压缩文件中的指定图片，返回一个bytes图片对象
    :param archive_path: str，压缩文件路径
    :param image_path: str，压缩包内部图片路径"""
    archive = read_archive(archive_path)
    if not archive:
        raise Exception('未正确读取文件，该文件不是压缩文件或文件不存在')

    try:
        img_data = archive.read(image_path)
    except KeyError:
        raise Exception('压缩文件中不存在该文件')

    archive.close()

    return img_data
