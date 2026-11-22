from collections.abc import Hashable, Iterable
from typing import TypeVar

__all__ = ['dedup_list', 'merge_intersection_item']

_T = TypeVar('_T')
_H = TypeVar('_H', bound=Hashable)

"""----------逻辑函数----------"""


def _dedup_list(lst: list[_T]) -> tuple[list[_T], list[_T]]:
    """按首次出现顺序去重，并收集被剔除的重复项。

    可哈希元素用集合判定；不可哈希元素退化为线性比较，保持与原实现一致的 ``==`` 语义。

    :param lst: 待去重的列表
    :return: (去重后的列表, 重复项列表)
    """
    result: list[_T] = []
    removed: list[_T] = []
    seen: set[_T] = set()
    unhashable_seen: list[_T] = []

    for item in lst:
        try:
            duplicate = item in seen or any(item == u for u in unhashable_seen)
        except TypeError:  # 不可哈希元素只能逐个比较
            duplicate = item in result

        if duplicate:
            removed.append(item)
        else:
            result.append(item)
            try:
                seen.add(item)
            except TypeError:
                unhashable_seen.append(item)

    return result, removed


def _merge_intersection_item(items: Iterable[Iterable[_H]]) -> list[Iterable[_H]]:
    """合并存在交集的容器，支持列表/元组/集合等可迭代对象。

    交集具有传递性：若新容器同时与多个已有组相交，这些组会一并合并。
    通过元素到组的映射替代两两求交，平均复杂度为 O(元素总数)。

    :param items: 由容器组成的可迭代对象，容器元素需可哈希
    :return: 合并后的容器列表；单个容器保持原对象，多个容器合并为 set
    """
    groups: dict[int, set[_H]] = {}
    originals: dict[int, Iterable[_H]] = {}
    sizes: dict[int, int] = {}
    element_group: dict[_H, int] = {}
    next_id = 0

    for item in items:
        elements = set(item)
        matched = {element_group[e] for e in elements if e in element_group}

        if matched:
            target = min(matched)  # 结果保留最早组的位置
            merged = groups[target]
            for gid in matched - {target}:
                merged |= groups.pop(gid)
                del originals[gid]
                sizes[target] += sizes.pop(gid)
            merged |= elements
            sizes[target] += 1
        else:
            target = next_id
            next_id += 1
            groups[target] = set(elements)
            originals[target] = item
            sizes[target] = 1
            merged = groups[target]

        for element in merged:
            element_group[element] = target

    return [originals[gid] if sizes[gid] == 1 else groups[gid] for gid in groups]


"""----------调用函数----------"""


def dedup_list(lst: list[_T]) -> list[_T]:
    """剔除列表中的重复项，保留元素首次出现的顺序。
    :param lst: 待去重的列表
    :return: 去重后的列表
    """
    return _dedup_list(lst)[0]


def merge_intersection_item(items: Iterable[Iterable[_H]]) -> list[Iterable[_H]]:
    """合并有交集的容器，支持集合/列表/元组。
    [(1, 2), {2, 3}, (5, 6)] -> [{1, 2, 3}, (5, 6)]
    :param items: 由容器组成的可迭代对象，容器元素需可哈希
    :return: 合并后的容器列表
    """
    return _merge_intersection_item(items)
