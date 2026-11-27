"""文块后处理（tbpu）。

引擎先返回零散的 ``{"text", "score", "box"}`` 文块，再经过忽略区域和
排版解析，为每个文块补充 ``end`` 结束符。多栏方案采用基于列间距的
轻量启发式实现。
"""

from __future__ import annotations

import unicodedata
from statistics import median
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from .exceptions import ConfigurationError

Block = Dict[str, Any]
BBox = Tuple[float, float, float, float]

_CJK_RANGES = (
    (0x4E00, 0x9FFF),
    (0x3040, 0x30FF),
    (0x1100, 0x11FF),
    (0x3130, 0x318F),
    (0xAC00, 0xD7AF),
    (0x3000, 0x303F),
    (0xFE30, 0xFE4F),
    (0xFF00, 0xFFEF),
)


def _is_cjk(character: str) -> bool:
    code = ord(character)
    return any(start <= code <= end for start, end in _CJK_RANGES)


def word_separator(left: str, right: str) -> str:
    """根据前后字符决定两个文本块之间是否需要空格。"""
    if not left or not right:
        return ""
    if _is_cjk(left) and _is_cjk(right):
        return ""
    if left == "-":
        return ""
    if unicodedata.category(right).startswith("P"):
        return ""
    return " "


def _copy_blocks(blocks: Iterable[Dict[str, Any]]) -> List[Block]:
    """复制并规范化文块，跳过空文本。"""
    result: List[Block] = []
    for raw in blocks:
        text = str(raw.get("text", "") or "")
        if not text.strip():
            continue

        box: List[List[float]] = []
        for point in raw.get("box") or []:
            if len(point) < 2:
                raise ConfigurationError(f"文本框坐标至少需要两个值: {point}")
            box.append([float(point[0]), float(point[1])])

        result.append(
            {
                "text": text,
                "score": float(raw.get("score", 0.0) or 0.0),
                "box": box,
                "end": str(raw.get("end", "") or ""),
            }
        )
    return result


def _bbox(block: Block) -> BBox:
    box = block["box"]
    xs = [point[0] for point in box]
    ys = [point[1] for point in box]
    return min(xs), min(ys), max(xs), max(ys)


def _normalize_area(area: Sequence[Any]) -> Tuple[float, float, float, float]:
    """把 ``[[x1,y1],[x2,y2]]``、四点框或平铺四元组统一成边界框。"""
    try:
        if len(area) == 4 and all(isinstance(v, (int, float)) for v in area):
            x1, y1, x2, y2 = area
        elif len(area) == 2:
            x1, y1 = area[0][0], area[0][1]
            x2, y2 = area[1][0], area[1][1]
        elif len(area) >= 4:
            x1, y1 = area[0][0], area[0][1]
            x2, y2 = area[2][0], area[2][1]
        else:
            raise ValueError("区域格式无法识别")
        return (
            min(float(x1), float(x2)),
            min(float(y1), float(y2)),
            max(float(x1), float(x2)),
            max(float(y1), float(y2)),
        )
    except Exception as exc:
        raise ConfigurationError(
            "忽略区域格式应为 [[x1,y1],[x2,y2]]，当前值不合法: "
            f"{area}"
        ) from exc


def apply_ignore_area(blocks: List[Block], areas: Sequence[Sequence[Any]]) -> List[Block]:
    """删除完全落在任意忽略区域内的文本块。"""
    normalized = [_normalize_area(area) for area in areas]
    result: List[Block] = []
    for block in blocks:
        left, top, right, bottom = _bbox(block)
        ignored = any(
            ax1 <= left and ay1 <= top and ax2 >= right and ay2 >= bottom
            for ax1, ay1, ax2, ay2 in normalized
        )
        if not ignored:
            result.append(block)
    return result


def _group_lines(blocks: List[Block]) -> List[List[Block]]:
    """按高度、垂直中心位置把文本块聚成行。"""
    items = [(block, _bbox(block)) for block in blocks if block["text"]]
    if not items:
        return []
    items.sort(key=lambda item: (item[1][1], item[1][0]))

    used = [False] * len(items)
    lines: List[List[Block]] = []

    for index, (block, (_, top, _, bottom)) in enumerate(items):
        if used[index]:
            continue
        used[index] = True
        height = max(1.0, bottom - top)
        center = (top + bottom) / 2
        line = [block]

        for other_index in range(index + 1, len(items)):
            if used[other_index]:
                continue
            other, (_, other_top, _, other_bottom) = items[other_index]
            other_height = max(1.0, other_bottom - other_top)
            other_center = (other_top + other_bottom) / 2

            if abs(center - other_center) > max(height, other_height) * 0.6:
                continue
            if abs(height - other_height) > max(height, other_height) * 0.8:
                continue

            used[other_index] = True
            line.append(other)

        line.sort(key=lambda item: _bbox(item)[0])
        lines.append(line)

    lines.sort(key=lambda line: min(_bbox(block)[1] for block in line))
    return lines


def _set_line_ends(lines: List[List[Block]], *, code_mode: bool = False) -> None:
    """设置同一行内相邻文块的结束符，行末默认换行。"""
    for line in lines:
        for index, block in enumerate(line):
            if index == len(line) - 1:
                block["end"] = "\n"
                continue

            next_block = line[index + 1]
            _, _, right, bottom = _bbox(block)
            next_left, _, _, _ = _bbox(next_block)
            height = max(1.0, bottom - _bbox(block)[1])
            gap = next_left - right

            if gap > height * (0.3 if code_mode else 1.2):
                block["end"] = " "
            else:
                block["end"] = word_separator(block["text"][-1], next_block["text"][0])


def _apply_single(blocks: List[Block], mode: str) -> List[Block]:
    out = _copy_blocks(blocks)
    if mode == "none":
        for block in out:
            block["end"] = "\n"
        return out

    if mode not in ("single_line", "single_none", "single_para", "single_code"):
        for block in out:
            block["end"] = "\n"
        return out

    lines = _group_lines(out)
    if not lines:
        return out
    _set_line_ends(lines, code_mode=(mode == "single_code"))

    ordered = [block for line in lines for block in line]

    if mode == "single_none":
        for index, block in enumerate(ordered[:-1]):
            if block["end"] == "\n":
                block["end"] = word_separator(block["text"][-1], ordered[index + 1]["text"][0])
        ordered[-1]["end"] = ""
    elif mode == "single_para":
        for index, line in enumerate(lines[:-1]):
            last = line[-1]
            next_first = lines[index + 1][0]
            _, top, _, bottom = _bbox(last)
            _, next_top, _, _ = _bbox(next_first)
            height = max(1.0, bottom - top)
            if next_top - bottom > height * 1.2:
                last["end"] = "\n\n"

    return ordered


def _group_columns(blocks: List[Block]) -> List[List[Block]]:
    """用列间距做轻量分栏。"""
    items = [(block, _bbox(block)) for block in blocks if block["text"]]
    if not items:
        return []

    heights = [max(1.0, box[3] - box[1]) for _, box in items]
    gap_threshold = median(heights) * 1.8
    items.sort(key=lambda item: item[1][0])

    columns: List[List[Block]] = []
    current: List[Block] = []
    right_edge: float | None = None

    for block, (left, _, right, _) in items:
        if current and right_edge is not None and left > right_edge + gap_threshold:
            columns.append(current)
            current = []
            right_edge = None
        current.append(block)
        right_edge = right if right_edge is None else max(right_edge, right)

    if current:
        columns.append(current)

    columns.sort(key=lambda column: min(_bbox(block)[0] for block in column))
    return columns


def _apply_multi(blocks: List[Block], suffix: str) -> List[Block]:
    if suffix not in ("line", "none", "para"):
        suffix = "line"
    result: List[Block] = []
    for column in _group_columns(blocks):
        result.extend(_apply_single(column, f"single_{suffix}"))
    return result


def process_blocks(
    blocks: Iterable[Dict[str, Any]],
    parser: str = "none",
    ignore_area: Sequence[Sequence[Any]] | None = None,
) -> List[Block]:
    """执行忽略区域与排版解析，返回新的文块列表。"""
    out = _copy_blocks(blocks)
    if ignore_area:
        out = apply_ignore_area(out, ignore_area)

    parser = (parser or "none").lower()
    if parser.startswith("multi_"):
        return _apply_multi(out, parser[len("multi_") :])
    return _apply_single(out, parser)
