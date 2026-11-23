import imagehash
from PIL import Image

from ._hash import _convert_numpy_hash_to_str

"""----------逻辑函数----------"""


def _is_pure_color_image(image_path: str, threshold: float = 0.9) -> bool:
    """判断图片是否为纯色图片。
    :param image_path: 本地图片路径
    :param threshold: 判断阈值，0~1
    :return: 是否为纯色图片，图片损坏或无法打开时返回 False
    """
    try:
        with Image.open(image_path) as image, image.convert('L') as gray_image:
            # 计算均值哈希，hash_size=16 共 256 位
            ahash = imagehash.average_hash(gray_image, hash_size=16)
    except OSError:
        # 图片损坏时会抛出 OSError: image file is truncated
        return False

    hash_str = _convert_numpy_hash_to_str(ahash)
    if not hash_str:
        return False

    proportion = hash_str.count('0') / len(hash_str)
    return proportion > threshold or proportion < (1 - threshold)


"""----------调用函数----------"""


def is_pure_color_image(image_path: str, threshold: float = 0.9) -> bool:
    """判断图片是否为纯色图片。
    :param image_path: 本地图片路径
    :param threshold: 判断阈值，0~1
    :return: 是否为纯色图片，图片损坏或无法打开时返回 False
    """
    return _is_pure_color_image(image_path, threshold)
