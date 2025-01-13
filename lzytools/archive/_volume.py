import os.path
import re
from typing import Union

# 分卷压缩包正则
_PATTERN_7Z = r'^(.+)\.7z\.\d+$'  # test.7z.001/test.7z.002/test.7z.003
_PATTERN_RAR = r'^(.+)\.part(\d+)\.rar$'  # test.part1.rar/test.part2.rar/test.part3.rar
_PATTERN_RAR_WITHOUT_SUFFIX = r'^(.+)\.part(\d+)$'  # rar分卷文件无后缀时也能正常解压，test.part1/test.part2/test.part3
_PATTERN_ZIP = r'^(.+)\.zip$'  # zip分卷文件的第一个分卷包一般都是.zip后缀，所以.zip后缀直接视为分卷压缩文件 test.zip
_PATTERN_ZIP_VOLUME = r'^(.+)\.z\d+$'  # test.zip/test.z01/test.z02
_PATTERN_ZIP_TYPE2 = r'^(.+)\.zip\.\d+$'  # test.zip.001/test.zip.002/test.zip.003
_PATTERN_JOINED = [_PATTERN_7Z, _PATTERN_RAR, _PATTERN_RAR_WITHOUT_SUFFIX, _PATTERN_ZIP, _PATTERN_ZIP_VOLUME,
                   _PATTERN_ZIP_TYPE2]


def is_volume_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为分卷压缩文件
    :param filename: str，文件名（包含文件扩展名）"""
    for pattern in _PATTERN_JOINED:
        if re.match(pattern, filename, flags=re.I):
            return True

    return False


def guess_first_volume_archive_filename(filename: str) -> Union[str, bool]:
    """根据传入的文件名，生成分卷压缩文件的首个分卷包文件名
    :param filename: str，文件名（包含文件扩展名）
    :return: 生成的首个分卷包文件名，或未生成时False"""
    if not is_volume_archive_by_filename(filename):
        return False

    guess_filename = False

    # test.7z.001/test.7z.002/test.7z.003
    if re.match(_PATTERN_7Z, filename, flags=re.I):
        filetitle = re.match(_PATTERN_7Z, filename, flags=re.I).group(1)
        guess_filename = f'{filetitle}.7z.001'
    # test.part1.rar/test.part2.rar/test.part3.rar
    elif re.match(_PATTERN_RAR, filename, flags=re.I):
        filetitle = re.match(_PATTERN_RAR, filename, flags=re.I).group(1)
        number_length = len(re.match(_PATTERN_RAR, filename, flags=re.I).group(2))  # 处理part1.rar和part01.rar的情况
        guess_filename = f'{filetitle}.part{"1".zfill(number_length)}.rar'
    # test.part1/test.part2/test.part3
    elif re.match(_PATTERN_RAR_WITHOUT_SUFFIX, filename, flags=re.I):
        filetitle = re.match(_PATTERN_RAR_WITHOUT_SUFFIX, filename, flags=re.I).group(1)
        number_length = len(re.match(_PATTERN_RAR_WITHOUT_SUFFIX, filename, flags=re.I).group(2))
        guess_filename = f'{filetitle}.part{"1".zfill(number_length)}'
    # test.zip
    elif re.match(_PATTERN_ZIP, filename, flags=re.I):
        guess_filename = filename
    # test.zip/test.z01/test.z02
    elif re.match(_PATTERN_ZIP_VOLUME, filename, flags=re.I):
        filetitle = re.match(_PATTERN_ZIP_VOLUME, filename, flags=re.I).group(1)
        guess_filename = f'{filetitle}.zip'
    # test.zip.001/test.zip.002/test.zip.003
    elif re.match(_PATTERN_ZIP_TYPE2, filename, flags=re.I):
        filetitle = re.match(_PATTERN_ZIP_TYPE2, filename, flags=re.I).group(1)
        guess_filename = f'{filetitle}.zip.001'

    return guess_filename


def get_filetitle(filename: str) -> str:
    """根据传入的文件名，提取其不含文件扩展名的文件标题
    :param filename: str，文件名（包含文件扩展名）
    :return: 不含文件扩展名的文件标题"""
    if not is_volume_archive_by_filename(filename):
        return os.path.basename(filename)

    for pattern in _PATTERN_JOINED:
        filetitle = re.match(pattern, filename, flags=re.I).group(1)
        if filetitle:
            return filetitle
