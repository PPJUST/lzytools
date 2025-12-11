import base64
import io

import cv2
import numpy
from PIL import Image

"""----------逻辑函数----------"""


def _convert_bytes_to_numpy(bytes_image: bytes) -> numpy.ndarray:
    """将bytes图片对象转换为numpy图片对象
    :param bytes_image: bytes图片对象
    :return: numpy图片对象"""
    bytesio_image = io.BytesIO(bytes_image)  # 转为BytesIO对象
    pil_image = Image.open(bytesio_image)  # 转PIL.Image
    numpy_image = numpy.array(pil_image)  # 转NumPy数组
    pil_image.close()

    return numpy_image


def _convert_numpy_to_bytes(numpy_image: numpy.ndarray) -> bytes:
    """将numpy图片对象转换为bytes图片对象
    :param numpy_image: numpy图片对象
    :return: bytes图片对象"""
    image = Image.fromarray(numpy_image)  # 换为PIL Image对象
    bytes_image = io.BytesIO()  # 转为BytesIO对象
    image.save(bytes_image, format=image.format)
    bytes_image = bytes_image.getvalue()
    image.close()

    return bytes_image


def _convert_local_image_to_base64(image_path: str) -> str:
    """将本地图片转为base64值
    :param image_path: 本地图片路径
    :return: base64值字符串"""
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_str = base64.b64encode(image_data).decode('utf-8')
    return base64_str


def _convert_numpy_image_rgb_to_gray(numpy_image: numpy.ndarray) -> numpy.ndarray:
    """转换numpy图片对象的色度，将其转为灰度图"""
    image_ = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2GRAY)
    return image_


def _resize_numpy_image(numpy_image: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    """缩放numpy图片对象至指定宽高
    :param numpy_image: numpy图片对象
    :param width: 新的宽度
    :param height: 新的高度"""
    image_ = cv2.resize(numpy_image, dsize=(width, height))
    return image_


def _resize_numpy_image_ratio(numpy_image: numpy.ndarray, ratio: float) -> numpy.ndarray:
    """按比例缩放numpy图片对象
    :param numpy_image: numpy图片对象
    :param ratio: 缩放比例（大于0）"""
    width, height = numpy_image.size
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    image_ = cv2.resize(numpy_image, dsize=(new_width, new_height))
    return image_


"""----------调用函数----------"""


def convert_bytes_to_numpy(bytes_image: bytes) -> numpy.ndarray:
    """将bytes图片对象转换为numpy图片对象
    :param bytes_image: bytes图片对象
    :return: numpy图片对象"""
    return _convert_bytes_to_numpy(bytes_image)


def bytes_to_numpy(bytes_image: bytes) -> numpy.ndarray:
    """将bytes图片对象转换为numpy图片对象
    :param bytes_image: bytes图片对象
    :return: numpy图片对象"""
    return _convert_bytes_to_numpy(bytes_image)


def convert_numpy_to_bytes(numpy_image: numpy.ndarray) -> bytes:
    """将numpy图片对象转换为bytes图片对象
    :param numpy_image: numpy图片对象
    :return: bytes图片对象"""
    return _convert_numpy_to_bytes(numpy_image)


def numpy_to_bytes(numpy_image: numpy.ndarray) -> bytes:
    """将numpy图片对象转换为bytes图片对象
    :param numpy_image: numpy图片对象
    :return: bytes图片对象"""
    return _convert_numpy_to_bytes(numpy_image)


def convert_local_image_to_base64(image_path: str) -> str:
    """将本地图片转为base64值
    :param image_path: 本地图片路径
    :return: base64值字符串"""
    return _convert_local_image_to_base64(image_path)


def image_to_base64(image_path: str) -> str:
    """将本地图片转为base64值
    :param image_path: 本地图片路径
    :return: base64值字符串"""
    return _convert_local_image_to_base64(image_path)


def convert_numpy_image_rgb_to_gray(numpy_image: numpy.ndarray) -> numpy.ndarray:
    """转换numpy图片对象的色度，将其转为灰度图"""
    return _convert_numpy_image_rgb_to_gray(numpy_image)


def rgb_to_gray_numpy(numpy_image: numpy.ndarray) -> numpy.ndarray:
    """转换numpy图片对象的色度，将其转为灰度图"""
    return _convert_numpy_image_rgb_to_gray(numpy_image)


def resize_numpy_image(numpy_image: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    """缩放numpy图片对象至指定宽高
    :param numpy_image: numpy图片对象
    :param width: 新的宽度
    :param height: 新的高度"""
    return _resize_numpy_image(numpy_image, width, height)


def resize_image_numpy(numpy_image: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    """缩放numpy图片对象至指定宽高
    :param numpy_image: numpy图片对象
    :param width: 新的宽度
    :param height: 新的高度"""
    return _resize_numpy_image(numpy_image, width, height)


def resize_numpy_image_ratio(numpy_image: numpy.ndarray, ratio: float) -> numpy.ndarray:
    """按比例缩放numpy图片对象
    :param numpy_image: numpy图片对象
    :param ratio: 缩放比例（大于0）"""
    return _resize_numpy_image_ratio(numpy_image, ratio)


def resize_image_numpy_ratio(numpy_image: numpy.ndarray, ratio: float) -> numpy.ndarray:
    """按比例缩放numpy图片对象
    :param numpy_image: numpy图片对象
    :param ratio: 缩放比例（大于0）"""
    return _resize_numpy_image_ratio(numpy_image, ratio)
