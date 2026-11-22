import os
import shutil
import subprocess
import time

import natsort
import send2trash

from ._filename import create_nodup_filename_standard_digital_suffix
from ._filepath import split_path
from ._info import get_first_multi_file_dirpath

"""----------常量----------"""

# Windows 下移动/重命名被占用文件时，等待后重试的间隔（秒）
_OPERATION_RETRY_DELAY = 0.2

"""----------逻辑函数----------"""


def _normalize_path_key(path: str) -> str:
    """生成用于路径比较的标准化键（统一绝对路径与大小写）"""
    return os.path.normcase(os.path.abspath(os.path.normpath(path)))


def _move_with_retry(src: str, dst: str) -> None:
    """移动文件/文件夹；遇到 Windows 权限竞争时等待后重试一次"""
    try:
        _ = shutil.move(src, dst)
    except PermissionError:
        time.sleep(_OPERATION_RETRY_DELAY)
        _ = shutil.move(src, dst)


def _delete(path: str, send_to_trash: bool = False) -> bool:
    """删除指定的文件/文件夹
    :param path: 需要删除的路径
    :param send_to_trash: 是否删除至回收站
    :return: 是否成功删除"""
    if not os.path.lexists(path):
        return False
    try:
        if send_to_trash:
            send2trash.send2trash(path)
        elif os.path.islink(path) or os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
        return True
    except Exception as e:  # 例如 PermissionError：文件被占用
        print(f'删除失败：{path}，{e}')
        return False


def _find_empty_folder(dirpath: str) -> list[str]:
    """搜索指定文件夹中的空文件夹（及其自身）
    :param dirpath: 文件夹路径
    :return: 搜索到的空文件夹路径（自然排序）"""
    if not os.path.isdir(dirpath):
        return []

    empty_folders: set[str] = set()
    result: list[str] = []
    # topdown=False 保证子目录先于父目录处理，父目录只需判断子目录是否均为空
    for current_dir, dirnames, filenames in os.walk(dirpath, topdown=False):
        child_dirpaths = {
            os.path.normpath(os.path.join(current_dir, name))
            for name in dirnames
        }
        if not filenames and child_dirpaths <= empty_folders:
            normalized = os.path.normpath(current_dir)
            empty_folders.add(normalized)
            result.append(normalized)

    return natsort.os_sorted(result)


def _delete_empty_folder(dirpath: str, send_to_trash: bool = True) -> list[str]:
    """删除指定文件夹中的空文件夹（及其自身）
    :param dirpath: 文件夹路径
    :param send_to_trash: 是否删除至回收站
    :return: 删除的文件夹路径"""
    remove_func = send2trash.send2trash if send_to_trash else os.rmdir
    deleted_paths: list[str] = []
    for empty_folder in _find_empty_folder(dirpath):
        if not os.path.exists(empty_folder):
            continue
        try:
            remove_func(empty_folder)
            deleted_paths.append(empty_folder)
        except Exception as e:
            print(f'删除空文件夹失败：{empty_folder}，{e}')
    return deleted_paths


def _set_hidden_attrib(path: str, is_hidden: bool = False) -> bool:
    """设置文件/文件夹的隐藏属性
    :param path: 文件/文件夹路径
    :param is_hidden: 是否隐藏文件/文件夹
    :return: 操作后是否显示（True 为显示，False 为隐藏）"""
    if os.name != 'nt':
        raise NotImplementedError('设置隐藏属性仅支持 Windows 系统')

    cmd = ['attrib', '+h' if is_hidden else '-h', path]
    result = subprocess.run(cmd, capture_output=True, text=True,
                            encoding='utf-8', errors='replace')
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        print(f'设置隐藏属性失败：{path}，{detail}')
    return not is_hidden


def _release_nesting_folder(check_path: str, target_dirpath: str) -> str:
    """解除套娃文件夹，将最深一级的非单层文件/文件夹移动至指定文件夹
    :param check_path: 需要检查的路径
    :param target_dirpath: 移动的目标文件夹
    :return: 最终移动后的路径
    :raises Exception: 路径不存在或目标路径不是文件夹
    :raises RuntimeError: 移动失败"""
    if not os.path.exists(check_path):
        raise Exception(f'路径不存在：{check_path}')

    if not os.path.exists(target_dirpath):
        os.makedirs(target_dirpath)
    if not os.path.isdir(target_dirpath):
        raise Exception(f'传入文件夹参数错误，【{target_dirpath}】不是文件夹路径')

    # 传入文件时直接移动该文件；传入文件夹时取最深一级非单层文件夹
    need_move_path = (check_path if os.path.isfile(check_path)
                      else get_first_multi_file_dirpath(check_path))

    if _normalize_path_key(need_move_path) == _normalize_path_key(target_dirpath):
        return os.path.normpath(need_move_path)

    _, filetitle, file_extension = split_path(need_move_path)
    nodup_filename = create_nodup_filename_standard_digital_suffix(
        filetitle, target_dirpath, file_extension
    )
    final_path = os.path.normpath(os.path.join(target_dirpath, nodup_filename))

    # 直接移动到最终无重复路径，无需先重命名为随机名称
    try:
        _move_with_retry(need_move_path, final_path)
    except OSError as e:
        raise RuntimeError(f'移动失败：{need_move_path} -> {final_path}') from e

    _ = _delete_empty_folder(check_path)  # 清理原路径中可能残留的空文件夹
    return final_path


"""----------调用函数----------"""


def delete(path: str, send_to_trash: bool = False) -> bool:
    """删除指定的文件/文件夹
    :param path: 需要删除的路径
    :param send_to_trash: 是否删除至回收站
    :return: 是否成功删除"""
    return _delete(path, send_to_trash)


def find_empty_folder(dirpath: str) -> list[str]:
    """搜索指定文件夹中的空文件夹（及其自身）
    :param dirpath: 文件夹路径
    :return: 搜索到的空文件夹路径"""
    return _find_empty_folder(dirpath)


def delete_empty_folder(dirpath: str, send_to_trash: bool = True) -> list[str]:
    """删除指定文件夹中的空文件夹（及其自身）
    :param dirpath: 文件夹路径
    :param send_to_trash: 是否删除至回收站
    :return: 删除的文件夹路径"""
    return _delete_empty_folder(dirpath, send_to_trash)


def set_hidden_attrib(path: str, is_hidden: bool = False) -> bool:
    """设置文件/文件夹的隐藏属性
    :param path: 文件/文件夹路径
    :param is_hidden: 是否隐藏文件/文件夹
    :return: True为显示，False为隐藏"""
    return _set_hidden_attrib(path, is_hidden)


def release_nesting_folder(check_path: str, target_dirpath: str) -> str:
    """解除套娃文件夹，将最深一级的非单层文件/文件夹移动至指定文件夹
    :param check_path: 需要检查的路径
    :param target_dirpath: 移动的目标文件夹
    :return: 最终移动后的路径"""
    return _release_nesting_folder(check_path, target_dirpath)
