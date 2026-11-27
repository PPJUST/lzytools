"""lzytools_OCR 的主调用入口。"""

from __future__ import annotations

import time
from typing import Any, Iterable, List, Optional, Union

from .engines import BaseEngine, create_engine
from .exceptions import ConfigurationError
from .image import ImageSource, base64_to_numpy, to_numpy
from .models import OCRResult, TextBlock
from .tbpu import process_blocks

PARSERS = (
    "none",
    "multi_para",
    "multi_line",
    "multi_none",
    "single_para",
    "single_line",
    "single_none",
    "single_code",
)


class OCR:
    """一个简单的 OCR 调用封装。

    示例::

        from lzytools_OCR import OCR

        ocr = OCR()
        result = ocr.recognize("demo.png")
        print(result.text)
    """

    def __init__(
        self,
        engine: Union[str, BaseEngine, None] = None,
        *,
        parser: str = "multi_para",
        limit_side_len: int = 960,
        ignore_area: Optional[List[Any]] = None,
    ):
        if isinstance(engine, str):
            engine = create_engine(engine)
        elif engine is None:
            engine = create_engine("rapid")
        elif not callable(getattr(engine, "recognize", None)):
            raise ConfigurationError("engine 必须实现 recognize(image) 方法")

        if parser not in PARSERS:
            raise ConfigurationError(f"未知排版解析方案 {parser!r}，可选: {', '.join(PARSERS)}")

        self.engine = engine
        self.parser = parser
        self.limit_side_len = limit_side_len
        self.ignore_area = ignore_area

    def recognize(
        self,
        source: ImageSource,
        *,
        parser: Optional[str] = None,
        ignore_area: Optional[List[Any]] = None,
        limit_side_len: Optional[int] = None,
    ) -> OCRResult:
        """识别一张图片，返回 :class:`OCRResult`。"""
        limit = self.limit_side_len if limit_side_len is None else limit_side_len
        image = to_numpy(source, limit or 0)
        return self._run(image, parser=parser, ignore_area=ignore_area)

    def recognize_text(
        self,
        source: ImageSource,
        *,
        parser: Optional[str] = None,
        ignore_area: Optional[List[Any]] = None,
        limit_side_len: Optional[int] = None,
    ) -> str:
        """识别一张图片，只返回拼接后的文本。"""
        return self.recognize(
            source,
            parser=parser,
            ignore_area=ignore_area,
            limit_side_len=limit_side_len,
        ).text

    def recognize_base64(
        self,
        data: str,
        *,
        parser: Optional[str] = None,
        ignore_area: Optional[List[Any]] = None,
        limit_side_len: Optional[int] = None,
    ) -> OCRResult:
        """识别 base64 编码的图片。"""
        limit = self.limit_side_len if limit_side_len is None else limit_side_len
        image = base64_to_numpy(data, limit or 0)
        return self._run(image, parser=parser, ignore_area=ignore_area)

    def recognize_many(self, sources: Iterable[ImageSource]) -> List[OCRResult]:
        """批量识别，顺序与输入一致。"""
        return [self.recognize(source) for source in sources]

    def _run(
        self,
        image: Any,
        *,
        parser: Optional[str],
        ignore_area: Optional[List[Any]],
    ) -> OCRResult:
        wall_start = time.time()
        perf_start = time.perf_counter()
        raw_blocks, engine_elapsed = self.engine.recognize(image)
        elapsed = engine_elapsed if engine_elapsed > 0 else time.perf_counter() - perf_start

        selected_parser = parser or self.parser
        if selected_parser not in PARSERS:
            raise ConfigurationError(
                f"未知排版解析方案 {selected_parser!r}，可选: {', '.join(PARSERS)}"
            )

        selected_area = self.ignore_area if ignore_area is None else ignore_area
        blocks_dict = process_blocks(raw_blocks or [], selected_parser, selected_area)
        blocks = [TextBlock.from_dict(block) for block in blocks_dict if block.get("text")]
        code = 100 if blocks else 101

        return OCRResult(
            code=code,
            blocks=blocks,
            elapsed=elapsed,
            timestamp=wall_start,
            raw=raw_blocks,
        )

    def close(self) -> None:
        close = getattr(self.engine, "close", None)
        if callable(close):
            close()

    def __call__(self, source: ImageSource) -> str:
        return self.recognize_text(source)

    def __enter__(self) -> "OCR":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
