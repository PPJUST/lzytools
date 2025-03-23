import re
from typing import Union

from lzytools.file._check import is_dup_filename

# WINDOWS系统文件命名规则：文件和文件夹不能命名为“.”或“..”，也不能包含以下任何字符: \ / : * ? " < > |
_ILLEGAL_CHARACTERS = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']


def is_legal_filename(filename: str) -> bool:
    """检查文件名是否符合Windows的文件命名规范
    :param filename: str，仅文件名（不含文件扩展名和文件父路径）
    """
    # 检查.（强制文件名不能以.开头）
    if filename[0] == '.':
        return False

    # 检查非法字符
    for key in _ILLEGAL_CHARACTERS:
        if key in filename:
            return False

    return True


def replace_illegal_filename(filename: str, replace_str: str = '') -> Union[str, bool]:
    """替换文件名中的非法字符串
    :param filename: str，仅文件名（不含文件扩展名和文件父路径）
    :param replace_str: str，用于替换的新字符
    """
    # 检查用于替换的字符是否属于非法字符
    if replace_str in _ILLEGAL_CHARACTERS:
        raise Exception(f'替换字符非法：{replace_str}')

    # 替换非法字符
    for word in _ILLEGAL_CHARACTERS:
        filename = filename.replace(word, replace_str)

    # 替换.（强制文件名不能以.开头）
    while filename[0] == '.':
        filename = filename[1:]

    filename = filename.strip()
    if not filename:
        raise Exception(f'结果文件名非法：{filename}')

    return filename


def remove_suffix(filetitle: str, suffix: str = None) -> str:
    """提取无后缀的文件名（剔除（1）等后缀和自定义后缀）
    :param filetitle: str，文件名（不包含文件扩展名）
    :param suffix: str，自定义的后缀（若存在）
    :return: str，提取出的无后缀的文件名（不包含文件扩展名）"""
    # 剔除(1)等后缀
    filetitle = re.sub(r'\s*\(\d+\)\s*$', '', filetitle)
    # 剔除（1）等后缀
    filetitle = re.sub(r'\s*（\d+）\s*$', '', filetitle)
    # 剔除自定义后缀+数字的组合
    if suffix:
        filetitle = re.sub(rf'\s*{suffix}\s*\d+\s*$', '', filetitle)

    return filetitle.strip()


def create_nodup_filename_standard_digital_suffix(filetitle: str, check_dirpath: str,
                                                  filename_extension: str = None) -> str:
    """生成指定路径对应的文件在目标文件夹中非重复的文件名（统一数字后缀的文件名，(1)（1）等后缀）
    :param filetitle: str，文件名（不包含文件扩展名）
    :param filename_extension: str，文件扩展名（如果检查的文件名是文件的文件名，则必须使用该参数）
    :param check_dirpath: str，目标文件夹路径
    :return: str，非重复的文件名（包含文件扩展名）"""
    # 组合文件名
    if filename_extension.strip():
        filename = f'{filetitle}.{filename_extension.strip()}'  # 假设为文件的文件名
    else:
        filename = filetitle  # 假设为文件夹的文件名

    # 剔除后缀
    filetitle_filter = remove_suffix(filetitle)

    if filetitle_filter == filetitle:
        return filename
    else:
        # 检查重复文件名
        if is_dup_filename(filename, check_dirpath):
            # 生成无重复的文件名，按照Windows重复文件名规则，一直循环后缀编号累加，直到不存在重复文件名
            count = 1
            while True:
                # 组合文件名
                if filename_extension.strip():
                    filename = f'{filetitle} ({count}).{filename_extension.strip()}'  # 假设为文件的文件名
                else:
                    filename = f'{filetitle} ({count})'  # 假设为文件夹的文件名

                # 检查
                if is_dup_filename(filename, check_dirpath):
                    count += 1
                else:
                    break

        return filename


def create_nodup_filename_custom_suffix(filetitle: str, check_dirpath: str, add_suffix: str,
                                        filename_extension: str = None) -> str:
    """生成指定路径对应的文件在目标文件夹中非重复的文件名（可指定目标文件名）
    :param filetitle: str，文件名（不包含文件扩展名）
    :param filename_extension: str，文件扩展名（如果检查的文件名是文件的文件名，则必须使用该参数）
    :param check_dirpath: str，目标文件夹路径
    :param add_suffix: 存在重复文件名时在文件名后添加的后缀
    :return: str，非重复的文件名（包含文件扩展名）"""
    # 剔除原始后缀
    filetitle = remove_suffix(filetitle, add_suffix)

    # 组合文件名
    if filename_extension.strip():
        filename = f'{filetitle}.{filename_extension.strip()}'  # 假设为文件的文件名
    else:
        filename = filetitle  # 假设为文件夹的文件名

    # 检查重复文件名
    if is_dup_filename(filename, check_dirpath):
        # 生成无重复的文件名，一直循环后缀编号累加，直到不存在重复文件名
        count = 1
        while True:
            # 组合文件名
            if filename_extension.strip():
                filename = f'{filetitle}{add_suffix}{count}.{filename_extension.strip()}'  # 假设为文件的文件名
            else:
                filename = f'{filetitle}{add_suffix}{count}'  # 假设为文件夹的文件名

            # 检查
            if is_dup_filename(filename, check_dirpath):
                count += 1
            else:
                break

    return filename
