"""
以Windows本地环境的排序规则对传入列表/传入路径的内部文件列表进行排序（主要用于排序中文）

列表排序实现方法：
1. 初始化本地环境
2. 使用冒泡排序，对比两个键的顺序，将其每个字符拆分，逐级对比
3. 返回排序后的列表

路径排序实现方法：
1. 遍历传入路径，按需提取文件或文件夹
2. 对路径中的每一个文件夹及其自身进行列表排序
3. 返回排序后的列表
"""

import locale
import os
import re
from typing import Union


def sort_list(_list: list, order_type: str = 'ASC') -> Union[list, SystemExit]:
    """排序列表
    :param _list: 需要排序的list
    :param order_type: 排序类型，'ASC' 升序或 'DESC' 降序，默认为升序
    :return: 排序后的list
    """
    # 初始化本地环境
    locale.setlocale(locale.LC_ALL, '')

    # 冒泡排序
    _list = _list.copy()
    n = len(_list)
    for i in range(n):
        for j in range(n - i - 1):
            if _is_reversal_two_key(_list[j], _list[j + 1]):
                _list[j], _list[j + 1] = _list[j + 1], _list[j]

    # 按升降序参数返回对应list
    if order_type.upper() == 'ASC':
        return _list
    elif order_type.upper() == 'DESC':
        return _list[::-1]
    else:
        raise Exception(f'排序类型错误：{order_type}')


def sort_path(_dirpath: str, order_type: str = 'ASC', filetype: str = 'both', walk_depth: int = 0) -> list:
    """排序指定文件夹中的下级文件/文件夹
    :param _dirpath: 需要排序的文件夹路径
    :param order_type: 排序类型，'ASC' 升序或 'DESC' 降序，默认为升序
    :param filetype: 需要排序的文件类型，'file' 文件或 'folder' 文件夹或 'both' 两者皆有，默认为两者皆有
    :param walk_depth: 遍历的层级深度，默认为0（排序所有下级层数的文件/文件夹）
    :return: 排序后的内部文件完整路径list
    """
    path_sorted = [_dirpath]  # 存放最终结果
    current_listdir_sorted_folder = [_dirpath]  # 当前层级中的文件夹
    current_listdir_sorted_folder_copy = current_listdir_sorted_folder.copy()  # 用于递归
    if walk_depth == 0:
        walk_depth = 100

    current_depth = 0
    while current_depth < walk_depth and current_listdir_sorted_folder:
        current_depth += 1
        for path in current_listdir_sorted_folder_copy:
            current_listdir_sorted = _sort_path_listdir(path, order_type=order_type, filetype=filetype)
            current_index = path_sorted.index(path)
            path_sorted[current_index + 1:current_index + 1] = current_listdir_sorted  # 利用切片插入列表元素（不能用insert）
            current_listdir_sorted_folder.remove(path)
            current_listdir_sorted_folder += [i for i in current_listdir_sorted if os.path.isdir(i)]
        current_listdir_sorted_folder_copy = current_listdir_sorted_folder.copy()

    # 删除一开始赋值的多余的项目
    path_sorted.remove(_dirpath)
    # 额外处理文件类型为file时的情况
    if filetype == 'file':
        path_sorted = [i for i in path_sorted if os.path.isfile(i)]

    return path_sorted


def _sort_path_listdir(dirpath: str, order_type: str = 'ASC', filetype: str = 'both') -> Union[SystemExit, list]:
    """排序指定路径中的文件/文件夹（仅第1层下级目录），并返回完整路径list
    :param dirpath: 文件夹路径
    :param order_type: 排序类型，'ASC' 升序或 'DESC' 降序
    :param filetype: 排序的文件类型，'file' 文件或 'folder' 文件夹或 'both' 两者
    :return: 排序后的完整路径list
    """
    listdir = os.listdir(dirpath)
    listdir_fullpath = [os.path.normpath(os.path.join(dirpath, i)) for i in listdir]
    listdir_fullpath_folder = [i for i in listdir_fullpath if os.path.isdir(i)]
    listdir_fullpath_file = [i for i in listdir_fullpath if os.path.isfile(i)]

    list_sorted_fullpath_folder = sort_list(listdir_fullpath_folder, order_type=order_type)
    list_sorted_fullpath_file = sort_list(listdir_fullpath_file, order_type=order_type)

    if filetype.lower() in ['both', 'file']:  # 如果排序类型是file也要返回整个list，但之后要删除folder项
        return list_sorted_fullpath_folder + list_sorted_fullpath_file
    elif filetype.lower() == 'folder':
        return list_sorted_fullpath_folder
    else:
        raise Exception(f'排序类型错误：{order_type}')


def _is_reversal_two_key(key_1: str, key_2: str):
    """排序两个键，决定是否在冒泡排序中掉转位置"""
    key_1_split = _split_key(key_1)
    key_2_split = _split_key(key_2)
    check_step = min(len(key_1_split), len(key_2_split))  # 检查步数，按最短的键的长度

    # 逐个对比两个键的每个字符，直到对比不同的字符，并返回对比结果
    for _ in range(check_step):
        split_1 = key_1_split.pop(0)
        split_2 = key_2_split.pop(0)
        if split_1 != split_2:
            splits = [split_1, split_2]
            if split_1.isdigit() and split_2.isdigit():  # 如果两个字符都是字符型数字，则按数值大小排序
                if int(split_1) == int(split_2):  # 处理特殊情况，如果两个字符转数值后相等，则需要按长度倒序排序，在Windows中00会排在0前
                    splits_sorted = sorted(splits, key=lambda x: len(x))[::-1]
                else:
                    splits_sorted = sorted(splits, key=lambda x: int(x))
            else:  # 否则按文本排序
                splits_sorted = sorted(splits, key=locale.strxfrm)
            if splits_sorted == splits:
                return False
            else:
                return True

    return False


def _split_key(key: str) -> list:
    """拆分key中的每一个字符（连续数字字符除外），返回拆分后元素组成的list"""
    pattern = r'(\d+)'  # 不需要拆分点. ，在排序时可以直接视其为字符
    split_pattern = re.split(pattern, key)

    key_split = []
    for part in split_pattern:
        if part.isdigit():
            key_split.append(part)
        else:
            key_split += list(part)

    return key_split
