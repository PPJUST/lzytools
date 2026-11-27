"""识别结果的数据模型。

字段采用通用的 ``code/data/time/timestamp`` 结构，文块包含
``text/score/box/end``。
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Sequence, Union

Number = Union[int, float]
Point = Sequence[Number]
Box = Sequence[Point]


@dataclass
class TextBlock:
    """一个文本块。"""

    text: str
    score: float = 0.0
    box: List[List[float]] = field(default_factory=list)
    end: str = ""

    @classmethod
    def from_dict(cls, item: Dict[str, Any]) -> "TextBlock":
        """由引擎/API 返回的字典创建文本块。"""
        box: List[List[float]] = []
        for point in item.get("box") or []:
            if len(point) < 2:
                raise ValueError(f"文本框坐标至少需要两个值: {point}")
            box.append([float(point[0]), float(point[1])])

        return cls(
            text=str(item.get("text", "") or ""),
            score=float(item.get("score", 0.0) or 0.0),
            box=box,
            end=str(item.get("end", "") or ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转为普通字典。"""
        return {
            "text": self.text,
            "score": round(self.score, 6),
            "box": [[round(x, 2), round(y, 2)] for x, y in self.box],
            "end": self.end,
        }


@dataclass
class OCRResult:
    """一次识别的完整结果。"""

    code: int
    blocks: List[TextBlock] = field(default_factory=list)
    elapsed: float = 0.0
    timestamp: float = field(default_factory=time.time)
    raw: Any = None

    @property
    def success(self) -> bool:
        return self.code == 100

    @property
    def no_text(self) -> bool:
        return self.code == 101

    @property
    def text(self) -> str:
        """按每个文本块的 end 结束符拼接全文。"""
        if not self.blocks:
            return ""
        parts: List[str] = []
        for index, block in enumerate(self.blocks):
            parts.append(block.text)
            if index < len(self.blocks) - 1:
                parts.append(block.end or "")
        return "".join(parts)

    @property
    def mean_score(self) -> float:
        """所有文本块的平均置信度。"""
        if not self.blocks:
            return 0.0
        return sum(block.score for block in self.blocks) / len(self.blocks)

    def to_dict(self, format: str = "dict") -> Dict[str, Any]:
        """转为字典。

        ``format="text"`` 时 ``data`` 为拼接后的纯文本，否则为文块列表。
        """
        if format not in ("dict", "text"):
            raise ValueError('format 只支持 "dict" 或 "text"')

        data: Any = self.text if format == "text" else [b.to_dict() for b in self.blocks]
        return {
            "code": self.code,
            "data": data,
            "score": round(self.mean_score, 6),
            "time": round(self.elapsed, 6),
            "timestamp": self.timestamp,
        }

    def save(self, path: Union[str, Path], *, format: str | None = None) -> Path:
        """保存结果。默认根据后缀选择 txt 或 json。"""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        output_format = format or ("txt" if target.suffix.lower() == ".txt" else "json")

        if output_format == "txt":
            target.write_text(self.text, encoding="utf-8")
        elif output_format == "json":
            target.write_text(
                json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        else:
            raise ValueError('format 只支持 "txt" 或 "json"')
        return target

    def __len__(self) -> int:
        return len(self.blocks)

    def __iter__(self):
        return iter(self.blocks)
