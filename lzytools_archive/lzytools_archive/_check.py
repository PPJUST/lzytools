import os

import filetype

from ._volume import is_volume_archive_by_filename

"""----------常量----------"""

# 按文件名判断时认可的压缩文件扩展名
_ARCHIVE_FILE_EXTENSION = frozenset({'zip', 'rar', '7z', 'tar', 'gz', 'xz', 'iso'})
# filetype 库能识别的压缩文件扩展名（iso 不被支持）
_ARCHIVE_FILE_EXTENSION_FILETYPE = frozenset({'zip', 'tar', '7z', 'rar', 'gz', 'xz'})

"""----------逻辑函数----------"""


def _is_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为压缩文件（含分卷压缩文件）
    :param filename: 文件名（包含文件扩展名）
    :return: 是压缩文件返回 True
    """
    # 提取不带 '.' 的扩展名，统一大小写后匹配
    file_extension = os.path.splitext(filename)[1].strip().lstrip('.').lower()
    return file_extension in _ARCHIVE_FILE_EXTENSION or is_volume_archive_by_filename(filename)


def _is_archive(filepath: str) -> bool:
    """通过文件头判断是否为压缩文件
    :param filepath: 文件路径
    :return: 是压缩文件返回 True
    """
    if not os.path.isfile(filepath):
        return False

    kind = filetype.guess(filepath)
    return kind is not None and kind.extension in _ARCHIVE_FILE_EXTENSION_FILETYPE


"""----------调用函数----------"""


def is_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为压缩文件
    :param filename: 文件名（包含文件扩展名）
    :return: 是压缩文件返回 True
    """
    return _is_archive_by_filename(filename)


def is_archive(filepath: str) -> bool:
    """通过文件头判断是否为压缩文件
    :param filepath: 文件路径
    :return: 是压缩文件返回 True
    """
    return _is_archive(filepath)
