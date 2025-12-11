from typing import Union, Tuple

"""----------逻辑函数----------"""


def _dedup_list(lst: list) -> Tuple[list, list]:
    """"剔除列表中的重复项"""
    list_filter = []  # 去重后的列表
    list_removed = []  # 被去重元素
    for i in lst:
        if i not in list_filter:
            list_filter.append(i)
        else:
            list_removed.append(i)
    return list_filter, list_removed


def _merge_intersection_item(items: Union[list, tuple, set]) -> list:
    """合并有交集的容器，支持集合/列表/元组
    [(1, 2), {2, 3}, (5, 6)]->[(1, 2, 3), (5, 6)]"""
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


"""----------调用函数----------"""


def dedup_list(lst: list) -> list:
    """"剔除列表中的重复项"""
    return _dedup_list(lst)[0]


def merge_intersection_item(items: Union[list, tuple, set]) -> list:
    """合并有交集的容器，支持集合/列表/元组
    [(1, 2), {2, 3}, (5, 6)]->[(1, 2, 3), (5, 6)]"""
    return _merge_intersection_item(items)
