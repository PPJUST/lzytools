import io
import os

import numpy
from PIL import Image

"""----------常量----------"""

# PIL 图片格式与文件扩展名的对应关系（JPEG 的常用扩展名为 .jpg）
_FORMAT_TO_EXTENSION = {'JPEG': '.jpg'}
# numpy 图片对象不含格式信息时使用的默认扩展名
_DEFAULT_EXTENSION = '.jpg'

"""----------逻辑函数----------"""


def _get_extension(image_format: str | None) -> str:
    """将 PIL 图片格式转换为带点的文件扩展名。
    :param image_format: PIL 图片格式，如 PNG、JPEG；None 表示无格式信息
    :return: 文件扩展名，无法确定时使用 .jpg
    """
    if not image_format:
        return _DEFAULT_EXTENSION
    return _FORMAT_TO_EXTENSION.get(image_format.upper(), '.' + image_format.lower())


def _save_pil_image(image: Image.Image, dirpath: str, filetitle: str, extension: str) -> str:
    """将 PIL 图片对象保存至本地。
    :param image: PIL 图片对象
    :param dirpath: 需要保存到的目录
    :param filetitle: 保存的文件标题（不含文件扩展名）
    :param extension: 带点的文件扩展名
    :return: 保存到本地的图片路径
    """
    # 转换图像模式，防止报错 OSError: cannot write mode P as JPEG
    with image.convert('RGB') as rgb_image:
        # 清除元数据
        rgb_image.info.clear()

        # 组合保存路径并创建目录（支持多级目录）
        save_path = os.path.normpath(os.path.join(dirpath, filetitle + extension))
        os.makedirs(dirpath, exist_ok=True)

        rgb_image.save(save_path)

    return save_path


def _save_bytes_image(bytes_image: bytes, dirpath: str, filetitle: str) -> str:
    """将 bytes 图片对象保存至本地，沿用原图格式。
    :param bytes_image: bytes 图片对象
    :param dirpath: 需要保存到的目录
    :param filetitle: 保存的文件标题（不含文件扩展名）
    :return: 保存到本地的图片路径
    """
    with Image.open(io.BytesIO(bytes_image)) as image:
        # convert() 会丢失 format，需在转换前读取
        extension = _get_extension(image.format)
        return _save_pil_image(image, dirpath, filetitle, extension)


def _save_numpy_image(numpy_image: numpy.ndarray, dirpath: str, filetitle: str) -> str:
    """将 numpy 图片对象保存至本地，默认使用 jpg 格式。
    :param numpy_image: numpy 图片对象
    :param dirpath: 需要保存到的目录
    :param filetitle: 保存的文件标题（不含文件扩展名）
    :return: 保存到本地的图片路径
    """
    image = Image.fromarray(numpy.asarray(numpy_image, dtype=numpy.uint8))
    return _save_pil_image(image, dirpath, filetitle, _DEFAULT_EXTENSION)


"""----------调用函数----------"""


def save_bytes_image(bytes_image: bytes, dirpath: str, filetitle: str) -> str:
    """将 bytes 图片对象保存至本地，沿用原图格式。
    :param bytes_image: bytes 图片对象
    :param dirpath: 需要保存到的目录
    :param filetitle: 保存的文件标题（不含文件扩展名）
    :return: 保存到本地的图片路径
    """
    return _save_bytes_image(bytes_image, dirpath, filetitle)


def save_numpy_image(numpy_image: numpy.ndarray, dirpath: str, filetitle: str) -> str:
    """将 numpy 图片对象保存至本地，默认使用 jpg 格式。
    :param numpy_image: numpy 图片对象
    :param dirpath: 需要保存到的目录
    :param filetitle: 保存的文件标题（不含文件扩展名）
    :return: 保存到本地的图片路径
    """
    return _save_numpy_image(numpy_image, dirpath, filetitle)
