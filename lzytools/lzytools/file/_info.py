import os
from typing import Union

import filetype
import win32com.client  # pywin32
from natsort import natsort

"""----------逻辑函数----------"""


def _get_size(path: str) -> int:
    """获取指定文件/文件夹的总大小（字节byte）
    :param path: 文件/文件夹路径
    :return: 总大小（字节byte）"""
    if not os.path.exists(path):
        raise Exception(f'路径不存在：{path}')

    if os.path.isdir(path):
        return _get_dir_size(path)
    elif os.path.isfile(path):
        return os.path.getsize(path)
    else:
        return 0


def _get_dir_size(dirpath: str) -> int:
    """获取指定文件夹的总大小（字节byte）
    :param dirpath: 文件夹路径
    :return: 总大小（字节byte）"""
    _folder_size = 0
    for _dirpath, dirnames, filenames in os.walk(dirpath):
        for item in filenames:
            filepath = os.path.join(_dirpath, item)
            _folder_size += os.path.getsize(filepath)

    return _folder_size


def _get_files_in_dir(dirpath: str) -> list:
    """获取文件夹中所有文件的路径
    :param dirpath: 文件夹路径"""
    files = []
    for _dirpath, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            filepath_join = os.path.normpath(os.path.join(_dirpath, filename))
            files.append(filepath_join)

    return files


def _get_files_in_paths(paths: list) -> list:
    """提取输入路径列表中所有文件路径"""
    # 删除路径中的子路径
    paths = remove_subpaths(paths)

    # 提取路径中的文件
    files = set()
    for path in paths:
        if os.path.isfile(path):
            files.add(path)
        elif os.path.isdir(path):
            child_files = get_files_in_dir(path)
            files.update(child_files)

    files = natsort.os_sorted(files)
    return files


def _get_folders_in_dir(dirpath: str) -> list:
    """获取文件夹中所有文件夹的路径
    :param dirpath: 文件夹路径"""
    folders = []
    for _dirpath, dirnames, filenames in os.walk(dirpath):
        for dirname in dirnames:
            filepath_join = os.path.normpath(os.path.join(_dirpath, dirname))
            folders.append(filepath_join)

    return folders


def _guess_filetype(path) -> Union[str, None]:
    """判断文件类型
    :param path: 文件路径"""
    if not os.path.isfile(path):
        return None

    kind = filetype.guess(path)
    if kind is None:
        return None

    type_ = kind.extension
    if type_:
        return type_
    else:
        return None


def _get_first_multi_file_dirpath(dirpath: str) -> str:
    """找出文件夹中首个含多个下级文件/文件夹的文件夹路径（用于解除套娃文件夹）
    :param dirpath: 需要检查的文件夹路径
    :return: 首个含多个下级文件/文件夹的文件夹路径
    """
    if not os.path.exists(dirpath):
        raise Exception("传入路径不存在")
    if not os.path.isdir(dirpath):
        raise Exception("传入路径不是文件夹")

    child_paths = os.listdir(dirpath)
    # 没有对空文件夹进行进一步检查
    if len(child_paths) == 1:  # 文件夹下级只有一个文件/文件夹
        child_path = os.path.normpath(os.path.join(dirpath, child_paths[0]))
        if os.path.isfile(child_path):  # 如果是文件，则直接返回结果
            return child_path
        else:  # 如果是文件夹，则递归
            return _get_first_multi_file_dirpath(child_path)
    else:
        return dirpath


def _get_shortcut_target_path(shortcut_path: str) -> str:
    """获取快捷方式指向的路径
    :param shortcut_path: 快捷方式路径
    :return: 快捷方式指向的路径"""
    try:
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        return shortcut.Targetpath
    except Exception as e:
        raise f'报错提示：{e}'


"""----------调用函数----------"""


def get_size(path: str) -> int:
    """获取指定文件/文件夹的总大小（字节byte）
    :param path: 文件/文件夹路径
    :return: 总大小（字节byte）"""
    return _get_size(path)


def get_dir_size(dirpath: str) -> int:
    """获取指定文件夹的总大小（字节byte）
    :param dirpath: 文件夹路径
    :return: 总大小（字节byte）"""
    return _get_dir_size(dirpath)


def get_files_in_dir(dirpath: str) -> list:
    """获取文件夹中所有文件的路径
    :param dirpath: 文件夹路径"""
    return _get_files_in_dir(dirpath)


def get_files_in_paths(paths: list) -> list:
    """提取输入路径列表中所有文件路径"""
    return _get_files_in_paths(paths)


def get_folders_in_dir(dirpath: str) -> list:
    """获取文件夹中所有文件夹的路径
    :param dirpath: 文件夹路径"""
    return _get_folders_in_dir(dirpath)


def guess_filetype(path) -> Union[str, None]:
    """判断文件类型
    :param path: 文件路径"""
    return _guess_filetype(path)


def get_first_multi_file_dirpath(dirpath: str) -> str:
    """找出文件夹中首个含多个下级文件/文件夹的文件夹路径（用于解除套娃文件夹）
    :param dirpath: 需要检查的文件夹路径
    :return: 首个含多个下级文件/文件夹的文件夹路径
    """
    return _get_first_multi_file_dirpath(dirpath)


def get_shortcut_target_path(shortcut_path: str) -> str:
    """获取快捷方式指向的路径
    :param shortcut_path: 快捷方式路径
    :return: 快捷方式指向的路径"""
    return _get_shortcut_target_path(shortcut_path)
