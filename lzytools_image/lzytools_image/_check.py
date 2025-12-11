import imagehash
from PIL import Image

from ._hash import _convert_numpy_hash_to_str

"""----------逻辑函数----------"""


def _is_pure_color_image(image_path: str, threshold: float = 0.9) -> bool:
    """是否为纯色图片
    :param image_path: 本地图片路径
    :param threshold: 判断阈值，0~1"""
    try:
        image_pil = Image.open(image_path)
        image_pil = image_pil.convert('L')  # 转灰度图
    except OSError:  # 如果图片损坏，会抛出异常OSError: image file is truncated (4 bytes not processed)
        return False

    dhash = imagehash.average_hash(image_pil, hash_size=16)
    image_pil.close()
    hash_str = _convert_numpy_hash_to_str(dhash)

    proportion = hash_str.count('0') / len(hash_str)
    if proportion > threshold or proportion < (1 - threshold):
        return True
    else:
        return False


"""----------调用函数----------"""


def is_pure_color_image(image_path: str, threshold: float = 0.9) -> bool:
    """是否为纯色图片
    :param image_path: 本地图片路径
    :param threshold: 判断阈值，0~1"""
    return _is_pure_color_image(image_path, threshold)
