"""图片输入归一化：路径 / 字节 / base64 / PIL / numpy 统一转为 RGB numpy 数组。"""

from __future__ import annotations

import base64
import binascii
import io
from pathlib import Path
from typing import Union

import numpy as np
from PIL import Image, ImageOps

from .exceptions import UnsupportedSourceError

ImageSource = Union[str, Path, bytes, bytearray, memoryview, Image.Image, np.ndarray]

_RESAMPLING = getattr(Image, "Resampling", Image).LANCZOS


def _limit_side(image: Image.Image, limit_side_len: int | float) -> Image.Image:
    if limit_side_len and limit_side_len > 0 and max(image.size) > limit_side_len:
        image = image.copy()
        image.thumbnail((int(limit_side_len), int(limit_side_len)), _RESAMPLING)
    return image


def _ndarray_to_pil(array: np.ndarray) -> Image.Image:
    array = np.asarray(array)
    if array.ndim == 2:
        return Image.fromarray(array)
    if array.ndim == 3:
        if array.shape[2] == 1:
            return Image.fromarray(array[:, :, 0])
        if array.shape[2] == 3:
            return Image.fromarray(array)
        if array.shape[2] == 4:
            return Image.fromarray(array).convert("RGB")
    raise UnsupportedSourceError(f"不支持的 numpy 图片形状: {array.shape}")


def to_numpy(source: ImageSource, limit_side_len: int | float = 0) -> np.ndarray:
    """将支持的图片来源转成 RGB numpy 数组。"""
    if isinstance(source, np.ndarray):
        pil = _ndarray_to_pil(source)
    elif isinstance(source, Image.Image):
        pil = source
    elif isinstance(source, (bytes, bytearray, memoryview)):
        try:
            pil = Image.open(io.BytesIO(bytes(source)))
        except Exception as exc:
            raise UnsupportedSourceError(f"无法从字节流解析图片: {exc}") from exc
    elif isinstance(source, (str, Path)):
        path = Path(source)
        if not path.is_file():
            raise UnsupportedSourceError(f"图片路径不存在或不是文件: {path}")
        try:
            pil = Image.open(path)
        except Exception as exc:
            raise UnsupportedSourceError(f"无法打开图片 {path}: {exc}") from exc
    else:
        raise UnsupportedSourceError(
            "输入需为图片路径、bytes、base64、PIL.Image 或 numpy.ndarray，"
            f"当前类型: {type(source).__name__}"
        )

    try:
        pil = ImageOps.exif_transpose(pil).convert("RGB")
        pil = _limit_side(pil, limit_side_len)
        return np.asarray(pil)
    except Exception as exc:
        raise UnsupportedSourceError(f"图片预处理失败: {exc}") from exc


def base64_to_numpy(data: str, limit_side_len: int | float = 0) -> np.ndarray:
    """将 base64 图片字符串转成 RGB numpy 数组，兼容 data URI 前缀。"""
    if not isinstance(data, str):
        raise UnsupportedSourceError("base64 图片必须是字符串")
    if data.startswith("data:"):
        data = data.split(",", 1)[-1]
    try:
        raw = base64.b64decode(data, validate=False)
    except (binascii.Error, ValueError) as exc:
        raise UnsupportedSourceError(f"base64 解码失败: {exc}") from exc
    if not raw:
        raise UnsupportedSourceError("base64 图片内容为空")
    return to_numpy(raw, limit_side_len)
