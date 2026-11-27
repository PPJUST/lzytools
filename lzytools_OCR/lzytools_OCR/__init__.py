"""lzytools_OCR：个人使用的轻量 Python OCR 库。"""

from .engines import BaseEngine, RapidOCREngine, create_engine
from .exceptions import (
    ConfigurationError,
    EngineError,
    LzytoolsOcrError,
    UnsupportedSourceError,
)
from .models import OCRResult, TextBlock
from .ocr import OCR

__version__ = "0.1.0"

__all__ = [
    "BaseEngine",
    "ConfigurationError",
    "EngineError",
    "LzytoolsOcrError",
    "OCR",
    "OCRResult",
    "RapidOCREngine",
    "TextBlock",
    "UnsupportedSourceError",
    "create_engine",
]
