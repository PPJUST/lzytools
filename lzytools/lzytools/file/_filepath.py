import os
import subprocess
from pathlib import Path

import natsort

"""----------逻辑函数----------"""


def _split_path(path: str) -> tuple[str, str, str]:
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
    normalized = os.path.normpath(path)
    return os.sep.join(normalized.split(os.sep)[::-1])


def _get_parent_dirpaths(path: str) -> list[str]:
    """获取传入路径的所有上级目录路径
    :param path: 文件/文件夹路径
    :return: 所有上级目录列表，层级越高，顺序越前"""
    parents = Path(os.path.normpath(path)).parents
    return [os.path.normpath(str(parent)) for parent in reversed(list(parents))]


def _get_parent_dirpath(filepath: str, parent_level: int = 1):
    """获取传入路径的第n层父目录
    :param filepath: 文件路径
    :param parent_level: 父目录层级，1 表示直接父目录，超出层级时返回根目录"""
    parents = list(Path(os.path.normpath(filepath)).parents)
    if not parents:  # 根目录本身没有上级目录
        return os.path.normpath(filepath)
    index = min(max(parent_level, 1), len(parents)) - 1
    return os.path.normpath(str(parents[index]))


def _remove_subpaths(paths: list[str]) -> list[str]:
    """剔除传入路径列表中的子路径，仅保留最上级路径"""
    normalized = [os.path.normpath(path) for path in paths]
    result: list[str] = []
    for path in natsort.os_sorted(set(normalized)):
        # 若已有结果中的某条路径是当前路径的上级，则当前路径为子路径
        if any(_is_subpath(parent, path)
               and os.path.normcase(parent) != os.path.normcase(path)
               for parent in result):
            continue
        result.append(path)

    return result


def _is_subpath(parent_path: str, child_path: str) -> bool:
    """判断一个路径是否为另一个路径的子路径"""
    # 统一大小写后再比较，避免 Windows 下因盘符或目录大小写不一致误判
    parent = os.path.normcase(os.path.abspath(os.path.normpath(parent_path)))
    child = os.path.normcase(os.path.abspath(os.path.normpath(child_path)))

    try:
        return os.path.commonpath([parent, child]) == parent
    except ValueError:  # 不同盘符等无法计算公共路径的情况
        return False


def _copy_file_to_clipboard(file_path: str):
    """调用PowerShell命令复制文件到剪切板"""
    # 以参数列表传递路径，避免路径中的引号、特殊字符导致命令注入或解析失败
    cmd = ['powershell', '-NoProfile', '-NonInteractive', '-Command',
           'Set-Clipboard -LiteralPath $args[0]', os.path.abspath(file_path)]
    _ = subprocess.run(cmd, check=True)


def _open_parent_and_select(path: str):
    """打开父目录并选中文件"""
    abs_path = os.path.abspath(path)
    _ = subprocess.Popen(['explorer', '/select,', abs_path])


"""----------调用函数----------"""


def split_path(path: str) -> tuple[str, str, str]:
    """拆分路径为父目录路径，文件名（不含文件扩展名），文件扩展名
    :param path: 需要拆分的路径
    :return: 父目录路径，文件名（不含文件扩展名），文件扩展名"""
    return _split_path(path)


def reverse_path(path: str) -> str:
    """反转路径层级，从后往前排列目录层级
    :param path: 需要反转的路径
    :return: 反转后的路径
    """
    return _reverse_path(path)


def get_parent_dirpaths(path: str) -> list[str]:
    """获取传入路径的所有上级目录路径
    :param path: 文件/文件夹路径
    :return: 所有上级目录列表，层级越高，顺序越前"""
    return _get_parent_dirpaths(path)


def get_parent_dirpath(filepath: str, parent_level: int = 1):
    """获取传入路径的第n层父目录
    :param filepath: 文件路径
    :param parent_level: 父目录层级"""
    return _get_parent_dirpath(filepath, parent_level)


def remove_subpaths(paths: list[str]) -> list[str]:
    """剔除传入路径列表中的子路径，仅保留最上级路径"""
    return _remove_subpaths(paths)


def is_subpath(parent_path: str, child_path: str) -> bool:
    """判断一个路径是否为另一个路径的子路径"""
    return _is_subpath(parent_path, child_path)


def copy_file_to_clipboard(file_path: str):
    """调用PowerShell命令复制文件到剪切板"""
    return _copy_file_to_clipboard(file_path)


def open_parent_and_select(path: str):
    """打开父目录并选中文件"""
    return _open_parent_and_select(path)
