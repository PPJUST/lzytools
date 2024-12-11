import os


def split_path(path: str):
    """拆分路径为父目录路径，文件名（不含文件扩展名），文件扩展名
    :param path: str，需要拆分的路径
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


def reverse_path(path: str) -> str:
    """反转路径字符串，从后往前排列目录层级
    :param path: str，路径
    :return: str，重组后的路径字符串
    """
    path = os.path.normpath(path)
    _split_path = path.split('\\')
    path_reversed = ' \\ '.join(_split_path[::-1])
    path_reversed = os.path.normpath(path_reversed)
    return path_reversed
