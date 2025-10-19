import base64
import io

import cv2
import numpy
from PIL import Image


def bytes_to_numpy(bytes_image: bytes) -> numpy.ndarray:
    """将bytes图片对象转换为numpy图片对象
    :param bytes_image: bytes图片对象
    :return: numpy图片对象"""
    bytesio_image = io.BytesIO(bytes_image)  # 转为BytesIO对象
    pil_image = Image.open(bytesio_image)  # 转PIL.Image
    numpy_image = numpy.array(pil_image)  # 转NumPy数组
    pil_image.close()

    return numpy_image


def numpy_to_bytes(numpy_image: numpy.ndarray) -> bytes:
    """将numpy图片对象转换为bytes图片对象
    :param numpy_image: numpy图片对象
    :return: bytes图片对象"""
    image = Image.fromarray(numpy_image)  # 换为PIL Image对象
    bytes_image = io.BytesIO()  # 转为BytesIO对象
    image.save(bytes_image, format=image.format)
    bytes_image = bytes_image.getvalue()
    image.close()

    return bytes_image


def resize_image_numpy(image: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    """缩放numpy图片对象至指定宽高
    :param image: numpy图片对象
    :param width: int，新的宽度
    :param height: int，新的高度"""
    image_ = cv2.resize(image, dsize=(width, height))
    return image_


def resize_image_numpy_ratio(image: numpy.ndarray, ratio: float) -> numpy.ndarray:
    """按比例缩放numpy图片对象
    :param image: numpy图片对象
    :param ratio: float，缩放比例（>0）"""
    width, height = image.size
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    image_ = cv2.resize(image, dsize=(new_width, new_height))
    return image_


def rgb_to_gray_numpy(image: numpy.ndarray) -> numpy.ndarray:
    """将numpy图片对象转为灰度图"""
    image_ = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image_


def image_to_base64(image_path: str) -> str:
    """本地图片转为base64图片
    :param image_path: str，本地图片路径
    :return: bytes，base64字符串"""
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_str = base64.b64encode(image_data).decode('utf-8')
    return base64_str
