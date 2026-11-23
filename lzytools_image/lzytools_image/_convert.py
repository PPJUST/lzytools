import base64
import io
from typing import cast

import cv2
import numpy
from PIL import Image

"""----------逻辑函数----------"""


def _convert_bytes_to_numpy(bytes_image: bytes) -> numpy.ndarray:
    """将 bytes 图片对象转换为 numpy 图片对象。
    :param bytes_image: bytes 图片对象
    :return: numpy 图片对象
    """
    with Image.open(io.BytesIO(bytes_image)) as pil_image:
        return numpy.array(pil_image)


def _convert_numpy_to_bytes(numpy_image: numpy.ndarray, image_format: str = 'PNG') -> bytes:
    """将 numpy 图片对象转换为 bytes 图片对象。
    :param numpy_image: numpy 图片对象
    :param image_format: 输出图片格式，默认 PNG
    :return: bytes 图片对象
    """
    with Image.fromarray(numpy_image) as image, io.BytesIO() as bytesio_image:
        image.save(bytesio_image, format=image_format)
        return bytesio_image.getvalue()


def _convert_local_image_to_base64(image_path: str) -> str:
    """将本地图片转为 base64 值。
    :param image_path: 本地图片路径
    :return: base64 值字符串
    """
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def _convert_numpy_image_rgb_to_gray(numpy_image: numpy.ndarray) -> numpy.ndarray:
    """将 RGB 格式的 numpy 图片对象转为灰度图。
    :param numpy_image: RGB 图片对象，形状为 (H, W, 3)
    :return: 灰度图，形状为 (H, W)
    """
    return cv2.cvtColor(numpy_image, cv2.COLOR_RGB2GRAY)


def _resize_numpy_image(numpy_image: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    """缩放 numpy 图片对象至指定宽高。
    :param numpy_image: numpy 图片对象
    :param width: 新的宽度
    :param height: 新的高度
    """
    if width <= 0 or height <= 0:
        raise ValueError(f'宽高必须大于0，当前为 ({width}, {height})')
    return cv2.resize(numpy_image, dsize=(width, height))


def _resize_numpy_image_ratio(numpy_image: numpy.ndarray, ratio: float) -> numpy.ndarray:
    """按比例缩放 numpy 图片对象。
    :param numpy_image: numpy 图片对象
    :param ratio: 缩放比例，必须大于 0
    """
    if ratio <= 0:
        raise ValueError(f'缩放比例必须大于0，当前为 {ratio}')
    height, width = cast(tuple[int, int], numpy_image.shape[:2])
    new_width = max(1, int(width * ratio))
    new_height = max(1, int(height * ratio))
    return cv2.resize(numpy_image, dsize=(new_width, new_height))


"""----------调用函数----------"""


def convert_bytes_to_numpy(bytes_image: bytes) -> numpy.ndarray:
    """将 bytes 图片对象转换为 numpy 图片对象。
    :param bytes_image: bytes 图片对象
    :return: numpy 图片对象
    """
    return _convert_bytes_to_numpy(bytes_image)


def bytes_to_numpy(bytes_image: bytes) -> numpy.ndarray:
    """将 bytes 图片对象转换为 numpy 图片对象。
    :param bytes_image: bytes 图片对象
    :return: numpy 图片对象
    """
    return _convert_bytes_to_numpy(bytes_image)


def convert_numpy_to_bytes(numpy_image: numpy.ndarray, image_format: str = 'PNG') -> bytes:
    """将 numpy 图片对象转换为 bytes 图片对象。
    :param numpy_image: numpy 图片对象
    :param image_format: 输出图片格式，默认 PNG
    :return: bytes 图片对象
    """
    return _convert_numpy_to_bytes(numpy_image, image_format)


def numpy_to_bytes(numpy_image: numpy.ndarray, image_format: str = 'PNG') -> bytes:
    """将 numpy 图片对象转换为 bytes 图片对象。
    :param numpy_image: numpy 图片对象
    :param image_format: 输出图片格式，默认 PNG
    :return: bytes 图片对象
    """
    return _convert_numpy_to_bytes(numpy_image, image_format)


def convert_local_image_to_base64(image_path: str) -> str:
    """将本地图片转为 base64 值。
    :param image_path: 本地图片路径
    :return: base64 值字符串
    """
    return _convert_local_image_to_base64(image_path)


def image_to_base64(image_path: str) -> str:
    """将本地图片转为 base64 值。
    :param image_path: 本地图片路径
    :return: base64 值字符串
    """
    return _convert_local_image_to_base64(image_path)


def convert_numpy_image_rgb_to_gray(numpy_image: numpy.ndarray) -> numpy.ndarray:
    """将 RGB 格式的 numpy 图片对象转为灰度图。
    :param numpy_image: RGB 图片对象，形状为 (H, W, 3)
    :return: 灰度图，形状为 (H, W)
    """
    return _convert_numpy_image_rgb_to_gray(numpy_image)


def rgb_to_gray_numpy(numpy_image: numpy.ndarray) -> numpy.ndarray:
    """将 RGB 格式的 numpy 图片对象转为灰度图。
    :param numpy_image: RGB 图片对象，形状为 (H, W, 3)
    :return: 灰度图，形状为 (H, W)
    """
    return _convert_numpy_image_rgb_to_gray(numpy_image)


def resize_numpy_image(numpy_image: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    """缩放 numpy 图片对象至指定宽高。
    :param numpy_image: numpy 图片对象
    :param width: 新的宽度
    :param height: 新的高度
    """
    return _resize_numpy_image(numpy_image, width, height)


def resize_image_numpy(numpy_image: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    """缩放 numpy 图片对象至指定宽高。
    :param numpy_image: numpy 图片对象
    :param width: 新的宽度
    :param height: 新的高度
    """
    return _resize_numpy_image(numpy_image, width, height)


def resize_numpy_image_ratio(numpy_image: numpy.ndarray, ratio: float) -> numpy.ndarray:
    """按比例缩放 numpy 图片对象。
    :param numpy_image: numpy 图片对象
    :param ratio: 缩放比例，必须大于 0
    """
    return _resize_numpy_image_ratio(numpy_image, ratio)


def resize_image_numpy_ratio(numpy_image: numpy.ndarray, ratio: float) -> numpy.ndarray:
    """按比例缩放 numpy 图片对象。
    :param numpy_image: numpy 图片对象
    :param ratio: 缩放比例，必须大于 0
    """
    return _resize_numpy_image_ratio(numpy_image, ratio)
