import os

import filetype

from ._volume import is_volume_archive_by_filename

_ARCHIVE_FILE_EXTENSION = ['zip', 'rar', '7z', 'tar', 'gz', 'xz', 'iso']
_ARCHIVE_FILE_EXTENSION_FILETYPE = ['zip', 'tar', '7z', 'rar', 'gz', 'xz']  # filetype库支持的压缩文件后缀名

"""----------逻辑函数----------"""


def _is_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为压缩文件
    :param filename: 文件名（包含文件扩展名）
    """
    #  提取文件后缀名（不带.），判断一般的压缩文件
    file_extension = os.path.splitext(filename)[1].strip().strip('.').strip()
    if file_extension.lower() in _ARCHIVE_FILE_EXTENSION:
        return True

    # 检查是否为分卷压缩文件
    if is_volume_archive_by_filename(filename):
        return True

    return False


def _is_archive(filepath: str) -> bool:
    """通过文件头判断是否为压缩文件
    :param filepath: 文件路径
    """
    kind = filetype.guess(filepath)
    if kind is None:
        return False

    guess_type = kind.extension

    if guess_type and guess_type in _ARCHIVE_FILE_EXTENSION_FILETYPE:
        return True

    return False


"""----------调用函数----------"""


def is_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为压缩文件
    :param filename: 文件名（包含文件扩展名）
    """
    return _is_archive_by_filename(filename)


def is_archive(filepath: str) -> bool:
    """通过文件头判断是否为压缩文件
    :param filepath: 文件路径
    """
    return _is_archive(filepath)
