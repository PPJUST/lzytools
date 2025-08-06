import os

from ._volume import is_volume_archive_by_filename
from ..file import guess_filetype


def is_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为压缩文件
    :param filename: str，文件名（包含文件扩展名）
    :return: bool，是否为压缩包
    """
    _archive_file_extension = ['zip', 'rar', '7z', 'tar', 'gz', 'xz', 'iso']

    #  提取文件后缀名（不带.），判断一般的压缩文件
    file_extension = os.path.splitext(filename)[1].strip().strip('.').strip()
    if file_extension.lower() in _archive_file_extension:
        return True

    # 检查是否为分卷压缩文件
    if is_volume_archive_by_filename(filename):
        return True

    return False


def is_archive(filepath: str) -> bool:
    """通过文件头判断是否为压缩文件
    :param filepath: str，文件路径
    :return: bool，是否为压缩包
    """
    _archive_file_extension = ['zip', 'tar', 'rar', 'gz', '7z', 'xz']  # filetype库支持的压缩文件后缀名
    guess_type = guess_filetype(filepath)
    if guess_type and guess_type in _archive_file_extension:
        return True

    return False
