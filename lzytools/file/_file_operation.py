import os
import shutil
import subprocess
import time

import send2trash

from ._filename import create_nodup_filename_standard_digital_suffix
from ._filepath import split_path
from ._info import get_first_multi_file_dirpath
from ..general import create_random_string


def delete(path: str, send_to_trash: bool = False) -> bool:
    """删除指定的文件/文件夹
    :param path: str，需要删除的路径
    :param send_to_trash: bool，是否删除至回收站
    :return: bool，是否成功删除"""
    if os.path.exists(path):
        try:
            if send_to_trash:
                send2trash.send2trash(path)
            else:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
            return True  # 成功执行删除操作的返回True
        except Exception as e:  # 报错PermissionError:文件被占用
            print(f'报错提示：{e}')
            return False
    return False


def delete_empty_folder(dirpath: str, send_to_trash: bool = True):
    """删除指定文件夹中的空文件夹（及其自身）
    :param dirpath: str，文件夹路径
    :param send_to_trash: bool，是否删除至回收站
    """
    _dirpaths = []

    # 提取所有文件夹路径
    for _dirpath, dirnames, filenames in os.walk(dirpath):
        _dirpaths.append(_dirpath)

    _dirpaths.insert(0, dirpath)  # 将其自身放于首位

    # 从后往前逐级删除
    for child_dirpath in _dirpaths[::-1]:
        if not os.listdir(child_dirpath):
            if send_to_trash:
                send2trash.send2trash(child_dirpath)
            else:
                os.rmdir(child_dirpath)


def set_hidden_attrib(path: str, is_hidden: bool = False) -> bool:
    """设置文件/文件及的隐藏属性
    :param path: str，文件/文件夹路径
    :param is_hidden: bool，是否隐藏文件/文件夹
    :return: bool，True为显示，False为隐藏"""
    if is_hidden:
        subprocess.run(['attrib', '+h', path])
        return False
    else:
        subprocess.run(['attrib', '-h', path])
        return True


def release_nesting_folder(check_path: str, target_dirpath: str) -> str:
    """解除套娃文件夹，将最深一级的非单层文件/文件夹移动至指定文件夹
    :param check_path: str，需要检查的路径
    :param target_dirpath: str，移动的目标文件夹
    :return: str，最终移动后的路径
    """
    if not os.path.exists(check_path):
        raise Exception('路径不存在')

    # 如果目标文件夹不存在，则新建该文件夹
    if not os.path.exists(target_dirpath):
        os.makedirs(target_dirpath)

    if not os.path.isdir(target_dirpath):
        raise Exception(f'传入文件夹参数错误，【{target_dirpath}】不是文件夹路径')

    # 提取需要移动的路径（如果传参是文件，则直接为该路径，如果传参是文件夹，则为最深一级非单层文件夹
    if os.path.isfile(check_path):
        need_move_path = check_path
    else:
        need_move_path = get_first_multi_file_dirpath(check_path)

    # 检查需要移动的路径是否和目标文件夹一致，如果一致，则不需要进行移动
    if need_move_path == target_dirpath:
        return need_move_path

    # 提取原始文件名，生成目标文件夹下无重复的文件夹名
    parent_dirpath, filetitle, file_extension = split_path(need_move_path)
    nodup_filename = create_nodup_filename_standard_digital_suffix(filetitle, target_dirpath, file_extension)

    # 移动前先重命名
    move_path_renamed = need_move_path
    _origin_filename = f'{filetitle}.{file_extension.strip(".")}'
    if nodup_filename == _origin_filename:  # 如果该文件名与原文件名一致，则不需要进行重命名
        pass
    else:  # 否则，先重命名为随机文件名（防止同目录存在重复文件名）
        _random_filename = f'{create_random_string()}.{create_random_string(4)}'
        _path_with_random_filename = os.path.normpath(os.path.join(parent_dirpath, _random_filename))
        move_path_renamed = _path_with_random_filename
        # 重命名时会遇到权限问题导致报错
        try:
            os.rename(need_move_path, _path_with_random_filename)
        except PermissionError:  # PermissionError: [WinError 5] 拒绝访问。尝试等待0.2秒后再次重命名
            time.sleep(0.2)
            try:
                os.rename(need_move_path, _path_with_random_filename)
            except Exception as e:
                raise e

    # 再进行移动
    try:
        shutil.move(move_path_renamed, target_dirpath)
    except OSError:  # OSError: [WinError 145] 目录不是空的。原始文件夹下有残留文件夹，如果为空则尝试直接删除
        delete_empty_folder(move_path_renamed)

    # 拼接最终路径
    final_path = os.path.normpath(os.path.join(target_dirpath, nodup_filename))
    delete_empty_folder(check_path)  # 如果原始文件夹为空，则直接删除

    return final_path
