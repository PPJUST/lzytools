"""OCR 引擎适配层。

本库只使用本地 OCR 模型：RapidOCR（自动适配新版 ``rapidocr`` 与旧版
``rapidocr_onnxruntime``）。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from .exceptions import ConfigurationError, EngineError

RawBlock = Dict[str, Any]


def _elapsed_to_float(value: Any) -> float:
    """兼容 float 耗时与旧版 [det, cls, rec] 耗时列表。"""
    if isinstance(value, (list, tuple)):
        return sum(float(item) for item in value if isinstance(item, (int, float)))
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


class BaseEngine(ABC):
    """OCR 引擎的统一接口。"""

    name = "base"

    @abstractmethod
    def recognize(self, image: Any) -> Tuple[List[RawBlock], float]:
        """输入 RGB numpy 数组，返回 (文块列表, 引擎耗时秒)。"""

    def close(self) -> None:
        """可选的资源释放。"""


class RapidOCREngine(BaseEngine):
    """本地 RapidOCR 引擎。"""

    name = "rapid"

    def __init__(self, **engine_kwargs: Any):
        self._backend = ""
        rapid_cls = None

        try:
            from rapidocr import RapidOCR  # type: ignore

            rapid_cls = RapidOCR
            self._backend = "new"
        except ImportError:
            try:
                from rapidocr_onnxruntime import RapidOCR  # type: ignore

                rapid_cls = RapidOCR
                self._backend = "legacy"
            except ImportError as exc:
                raise EngineError(
                    "未安装本地 OCR 引擎。请安装 rapidocr>=2.0 "
                    "或旧版 rapidocr-onnxruntime>=1.4。"
                ) from exc

        try:
            self._engine = rapid_cls(**engine_kwargs)
        except Exception as exc:
            raise EngineError(f"RapidOCR 初始化失败: {exc}") from exc

    @staticmethod
    def _normalize_new(result: Any) -> Optional[Tuple[List[RawBlock], float]]:
        boxes = getattr(result, "boxes", None)
        texts = getattr(result, "txts", None)
        if boxes is None or texts is None:
            return None

        scores = getattr(result, "scores", None)
        elapsed = _elapsed_to_float(getattr(result, "elapse", 0.0))
        blocks: List[RawBlock] = []

        for index, text in enumerate(texts):
            if index >= len(boxes):
                break
            box = [[float(point[0]), float(point[1])] for point in boxes[index]]
            score = float(scores[index]) if scores is not None and index < len(scores) else 0.0
            blocks.append({"text": str(text), "score": score, "box": box})

        return blocks, elapsed

    @staticmethod
    def _normalize_legacy(result: Any) -> Optional[Tuple[List[RawBlock], float]]:
        if not isinstance(result, (tuple, list)) or len(result) < 2:
            return None

        raw, elapsed_value = result[0], result[1]
        elapsed = _elapsed_to_float(elapsed_value)
        if raw is None:
            return [], elapsed

        blocks: List[RawBlock] = []
        for row in raw:
            if len(row) < 3:
                continue
            points, text, score = row[0], row[1], row[2]
            box = [[float(point[0]), float(point[1])] for point in points]
            blocks.append({"text": str(text), "score": float(score), "box": box})
        return blocks, elapsed

    def recognize(self, image: Any) -> Tuple[List[RawBlock], float]:
        try:
            result = self._engine(image)
        except Exception as exc:
            raise EngineError(f"RapidOCR 识别失败: {exc}") from exc

        normalized = self._normalize_new(result)
        if normalized is None:
            normalized = self._normalize_legacy(result)
        if normalized is None:
            raise EngineError(f"无法解析 RapidOCR 返回结构: {type(result).__name__}")
        return normalized


def create_engine(name: str, **kwargs: Any) -> BaseEngine:
    """按名称创建本地引擎。"""
    registry = {
        "rapid": RapidOCREngine,
        "rapidocr": RapidOCREngine,
    }
    key = (name or "").lower()
    if key not in registry:
        raise ConfigurationError(
            f"未知引擎 {name!r}，可选: {', '.join(sorted(registry))}"
        )
    return registry[key](**kwargs)
