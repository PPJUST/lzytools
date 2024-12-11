import os
from typing import Union


def merge_intersection_item(items: Union[list, tuple, set]) -> list:
    """合并有交集的集合/列表/元组 [(1,2),{2,3},(5,6)]->[(1,2,3),(5,6)]
    :return: 示例 [(1,2),{2,3},(5,6)]->[(1,2,3),(5,6)]"""
    merged_list = []

    for i in range(len(items)):
        set_merged = False

        for j in range(len(merged_list)):
            if set(items[i]) & set(merged_list[j]):
                merged_list[j] = set(set(items[i]) | set(merged_list[j]))
                set_merged = True
                break

        if not set_merged:
            merged_list.append(items[i])

    return merged_list


def filter_child_folder(folder_list: list) -> list:
    """过滤文件夹列表中的所有子文件夹，返回剔除子文件夹后的list"""
    child_folder = set()
    for folder in folder_list:
        # 相互比对，检查是否为当前文件夹的下级
        for other_folder in folder_list:
            # 统一路径分隔符（os.path.normpath无法实现）
            other_folder_replace = os.path.normpath(other_folder).replace('/', '\\')
            folder_replace = os.path.normpath(folder).replace('/', '\\')
            compare_path = os.path.normpath(folder + os.sep).replace('/', '\\')
            if other_folder_replace.startswith(str(compare_path)) and other_folder_replace != folder_replace:
                child_folder.add(other_folder)

    for i in child_folder:
        if i in folder_list:
            folder_list.remove(i)

    return folder_list
