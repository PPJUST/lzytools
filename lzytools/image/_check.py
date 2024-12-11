import imagehash
from PIL import Image

from ._similar import numpy_hash_to_str


def is_pure_color_image(image_path: str) -> bool:
    """是否为纯色图片
    :param image_path: str，图片路径"""
    # 考虑到库的大小，通过计算图片Hash值的方法来判断是否为纯色图片（不使用opencv库，该库太大）
    try:
        image_pil = Image.open(image_path)
        image_pil = image_pil.convert('L')  # 转灰度图
    except OSError:  # 如果图片损坏，会抛出异常OSError: image file is truncated (4 bytes not processed)
        return False

    dhash = imagehash.average_hash(image_pil, hash_size=16)
    hash_str = numpy_hash_to_str(dhash)

    if hash_str.count('0') == len(hash_str):
        return True
    else:
        return False
