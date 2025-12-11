import os
from typing import Tuple

import natsort

"""----------逻辑函数----------"""


def _split_path(path: str) -> Tuple[str, str, str]:
    """拆分路径为父目录路径，文件名（不含文件扩展名），文件扩展名
    :param path: 需要拆分的路径
    :return: 父目录路径，文件名（不含文件扩展名），文件扩展名"""
    if os.path.isfile(path):
        _temp_path, file_extension = os.path.splitext(path)
        parent_dirpath, filetitle = os.path.split(_temp_path)
    elif os.path.isdir(path):
        file_extension = ''
        parent_dirpath, filetitle = os.path.split(path)
    else:
        raise Exception('非法路径')

    return parent_dirpath, filetitle, file_extension


def _reverse_path(path: str) -> str:
    """反转路径层级，从后往前排列目录层级
    :param path: 需要反转的路径
    :return: 反转后的路径
    """
    path = os.path.normpath(path)
    _split_path = path.split('\\')
    path_reversed = ' \\ '.join(_split_path[::-1])
    path_reversed = os.path.normpath(path_reversed)
    return path_reversed


def _get_parent_dirpaths(path: str) -> list:
    """获取传入路径的所有上级目录路径
    :param path: 文件/文件夹路径
    :return: 所有上级目录列表，层级越高，顺序越前"""
    parent_dirs = []

    while True:
        parent_dirpath, filename = os.path.split(path)
        if filename:
            parent_dirs.append(parent_dirpath)
        else:
            break

        path = parent_dirpath

    # 反转列表顺序，使得越上级目录排在越前面
    parent_dirs = parent_dirs[::-1]

    return parent_dirs


def _remove_subpaths(paths: list):
    """剔除传入路径列表中的子路径，仅保留最上级路径"""
    paths = [os.path.normpath(path) for path in paths]
    paths = natsort.os_sorted(paths)  # 排序路径
    subpaths = []
    for path in paths:
        paths_split_parents = _get_parent_dirpaths(path)
        # 判断其父路径是否与原始列表存在交集，如果存在则说明其是子路径
        _s1 = set(paths)
        _s2 = set(paths_split_parents)
        if _s1 & _s2:
            subpaths.append(path)

    return [i for i in paths if i not in subpaths]


def _is_subpath(parent_path: str, child_path: str) -> bool:
    """判断一个路径是否为另一个路径的子路径"""
    # 获取绝对路径并规范化
    parent = os.path.abspath(os.path.normpath(parent_path))
    child = os.path.abspath(os.path.normpath(child_path))

    # 比较公共前缀
    common_prefix = os.path.commonpath([parent, child])
    return common_prefix == parent


"""----------调用函数----------"""


def split_path(path: str) -> Tuple[str, str, str]:
    """拆分路径为父目录路径，文件名（不含文件扩展名），文件扩展名
    :param path: 需要拆分的路径
    :return: 父目录路径，文件名（不含文件扩展名），文件扩展名"""
    return split_path(path)


def reverse_path(path: str) -> str:
    """反转路径层级，从后往前排列目录层级
    :param path: 需要反转的路径
    :return: 反转后的路径
    """
    return _reverse_path(path)


def get_parent_dirpaths(path: str) -> list:
    """获取传入路径的所有上级目录路径
    :param path: 文件/文件夹路径
    :return: 所有上级目录列表，层级越高，顺序越前"""
    return _get_parent_dirpaths(path)


def remove_subpaths(paths: list):
    """剔除传入路径列表中的子路径，仅保留最上级路径"""
    return _remove_subpaths(paths)


def is_subpath(parent_path: str, child_path: str) -> bool:
    """判断一个路径是否为另一个路径的子路径"""
    return _is_subpath(parent_path, child_path)
