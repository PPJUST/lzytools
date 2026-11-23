from typing import Literal

import imagehash
import numpy
from PIL import Image

HASH_TYPE = Literal['ahash', 'phash', 'dhash', 'all']

"""----------逻辑函数----------"""


def _calc_hash(pillow_image: Image.Image, hash_type: HASH_TYPE = 'ahash', hash_size: int = 8) -> dict[str, str | None]:
    """计算图片的 3 种图片 Hash 值。
    :param pillow_image: PIL 图片对象
    :param hash_type: 需要计算的 hash 类型，ahash/phash/dhash/all
    :param hash_size: 计算图片的边长，最终 hash 值长度为边长的平方
    :return: {'ahash': None, 'phash': None, 'dhash': None}
    """
    result: dict[str, str | None] = {'ahash': None, 'phash': None, 'dhash': None}
    hash_type_lower = hash_type.lower()

    if hash_type_lower in ('all', 'ahash'):
        # 均值哈希
        result['ahash'] = _convert_numpy_hash_to_str(imagehash.average_hash(pillow_image, hash_size=hash_size))

    if hash_type_lower in ('all', 'phash'):
        # 感知哈希
        result['phash'] = _convert_numpy_hash_to_str(imagehash.phash(pillow_image, hash_size=hash_size))

    if hash_type_lower in ('all', 'dhash'):
        # 差异哈希
        result['dhash'] = _convert_numpy_hash_to_str(imagehash.dhash(pillow_image, hash_size=hash_size))

    return result


def _convert_numpy_hash_to_str(numpy_hash: numpy.ndarray | imagehash.ImageHash | None) -> str | None:
    """将 numpy 数组形式的图片 Hash 值转换为由 01 组成的字符串。
    :param numpy_hash: numpy 数组形式的图片 Hash 值（imagehash 对象）
    :return: 由 01 组成的字符串，空值时返回 None
    """
    if numpy_hash is None:
        return None
    hash_array = numpy.asarray(
        numpy_hash.hash if isinstance(numpy_hash, imagehash.ImageHash) else numpy_hash
    )
    if hash_array.size == 0:
        return None

    return ''.join('1' if col else '0' for row in hash_array for col in row)


def _calc_hamming_distance(hash_1: str, hash_2: str) -> bool | int:
    """计算两个由 01 组成的字符串形式的图片 Hash 值之间的汉明距离。
    :param hash_1: 字符串形式的 hash 值
    :param hash_2: 字符串形式的 hash 值
    :return: 汉明距离，位数不一致时返回 False
    """
    if len(hash_1) != len(hash_2):  # 位数不同时，无法进行比较
        return False

    return sum(ch1 != ch2 for ch1, ch2 in zip(hash_1, hash_2))


def _calc_hash_similar(hash_1: str, hash_2: str) -> bool | float:
    """计算两个由 01 组成的字符串形式的图片 Hash 值之间的相似度。
    :param hash_1: 字符串形式的 hash 值
    :param hash_2: 字符串形式的 hash 值
    :return: 相似度（0~1），位数不一致时返回 False
    """
    if len(hash_1) != len(hash_2):  # 位数不同时，无法进行比较
        return False

    hash_int1 = int(hash_1, 2)
    hash_int2 = int(hash_2, 2)
    # 使用异或操作计算差异位数
    diff_bits = bin(hash_int1 ^ hash_int2).count('1')

    return 1 - diff_bits / len(hash_1)


"""----------调用函数----------"""


def calc_hash(pillow_image: Image.Image, hash_type: HASH_TYPE = 'ahash', hash_size: int = 8) -> dict[str, str | None]:
    """计算图片的 3 种图片 Hash 值。
    :param pillow_image: PIL 图片对象
    :param hash_type: 需要计算的 hash 类型，ahash/phash/dhash/all
    :param hash_size: 计算图片的边长，最终 hash 值为边长的平方
    :return: {'ahash': None, 'phash': None, 'dhash': None}
    """
    return _calc_hash(pillow_image, hash_type, hash_size)


def convert_numpy_hash_to_str(numpy_hash: numpy.ndarray | imagehash.ImageHash | None) -> str | None:
    """将 numpy 数组形式的图片 Hash 值转换为由 01 组成的字符串。
    :param numpy_hash: numpy 数组形式的图片 Hash 值（imagehash 对象）
    :return: 由 01 组成的字符串，空值时返回 None
    """
    return _convert_numpy_hash_to_str(numpy_hash)


def numpy_hash_to_str(numpy_hash: numpy.ndarray | imagehash.ImageHash | None) -> str | None:
    """将 numpy 数组形式的图片 Hash 值转换为由 01 组成的字符串。
    :param numpy_hash: numpy 数组形式的图片 Hash 值（imagehash 对象）
    :return: 由 01 组成的字符串，空值时返回 None
    """
    return _convert_numpy_hash_to_str(numpy_hash)


def calc_hamming_distance(hash_1: str, hash_2: str) -> bool | int:
    """计算两个由 01 组成的字符串形式的图片 Hash 值之间的汉明距离。
    :param hash_1: 字符串形式的 hash 值
    :param hash_2: 字符串形式的 hash 值
    :return: 汉明距离，位数不一致时返回 False
    """
    return _calc_hamming_distance(hash_1, hash_2)


def calc_hash_hamming_distance(hash_1: str, hash_2: str) -> bool | int:
    """计算两个由 01 组成的字符串形式的图片 Hash 值之间的汉明距离。
    :param hash_1: 字符串形式的 hash 值
    :param hash_2: 字符串形式的 hash 值
    :return: 汉明距离，位数不一致时返回 False
    """
    return _calc_hamming_distance(hash_1, hash_2)


def calc_hash_similar(hash_1: str, hash_2: str) -> bool | float:
    """计算两个由 01 组成的字符串形式的图片 Hash 值之间的相似度。
    :param hash_1: 字符串形式的 hash 值
    :param hash_2: 字符串形式的 hash 值
    :return: 相似度（0~1），位数不一致时返回 False
    """
    return _calc_hash_similar(hash_1, hash_2)
