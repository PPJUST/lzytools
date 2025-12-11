from typing import Literal
from typing import Union

import imagehash
from PIL import ImageFile

HASH_TYPE = Literal['ahash', 'phash', 'dhash', 'all']

"""----------逻辑函数----------"""


def _calc_hash(pillow_image: ImageFile, hash_type: HASH_TYPE = 'ahash', hash_size: int = 8) -> dict:
    """计算图片的3种图片Hash值
    :param pillow_image: PIL.ImageFile图片对象
    :param hash_type: 需要计算的hash类型，ahash/phash/dhash/all
    :param hash_size: 计算图片的边长，最终hash值为边长的平方
    :return: {'ahash':None,'phash':None,'dhash':None}
    """
    hash_dict = {'ahash': None, 'phash': None, 'dhash': None}

    if hash_type.lower() == 'all' or hash_type.lower() == 'ahash':
        # 计算均值哈希
        ahash = imagehash.average_hash(pillow_image, hash_size=hash_size)
        ahash_str = _convert_numpy_hash_to_str(ahash)
        hash_dict['ahash'] = ahash_str

    if hash_type.lower() == 'all' or hash_type.lower() == 'phash':
        # 感知哈希
        phash = imagehash.phash(pillow_image, hash_size=hash_size)
        phash_str = _convert_numpy_hash_to_str(phash)
        hash_dict['phash'] = phash_str

    if hash_type.lower() == 'all' or hash_type.lower() == 'dhash':
        # 差异哈希
        dhash = imagehash.dhash(pillow_image, hash_size=hash_size)
        dhash_str = _convert_numpy_hash_to_str(dhash)
        hash_dict['dhash'] = dhash_str

    return hash_dict


def _convert_numpy_hash_to_str(numpy_hash: Union[imagehash.NDArray, imagehash.ImageHash]) -> Union[str, None]:
    """将numpy数组形式的图片Hash值(imagehash.hash)转换为由01组成的字符串
    :param numpy_hash: numpy数组形式的图片Hash值
    :return: 由01组成的字符串"""
    if not numpy_hash:
        return None
    if isinstance(numpy_hash, imagehash.ImageHash):
        numpy_hash = numpy_hash.hash

    hash_str = ''
    for row in numpy_hash:
        for col in row:
            if col:
                hash_str += '1'
            else:
                hash_str += '0'

    return hash_str


def _calc_hamming_distance(hash_1: str, hash_2: str) -> Union[bool, int]:
    """计算两个由01组成的字符串形式的图片Hash值之间的汉明距离
    :param hash_1: 字符串形式的hash值
    :param hash_2: 字符串形式的hash值
    :return: 汉明距离，或者计算失败时返回False
    """
    if len(hash_1) != len(hash_2):  # 位数不同时，无法进行比较
        raise False

    hamming_distance = sum(ch1 != ch2 for ch1, ch2 in zip(hash_1, hash_2))

    return hamming_distance


def _calc_hash_similar(hash_1: str, hash_2: str) -> Union[bool, float]:
    """计算两个由01组成的字符串形式的图片Hash值之间的相似度
    :param hash_1: 字符串形式的hash值
    :param hash_2: 字符串形式的hash值
    :return: 相似度（0~1），或者计算失败时返回False
    """
    if len(hash_1) != len(hash_2):  # 位数不同时，无法进行比较
        raise False

    hash_int1 = int(hash_1, 2)
    hash_int2 = int(hash_2, 2)
    # 使用异或操作计算差异位数
    diff_bits = bin(hash_int1 ^ hash_int2).count('1')
    # 计算相似性
    similarity = 1 - diff_bits / len(hash_1)

    return similarity


"""----------调用函数----------"""


def calc_hash(pillow_image: ImageFile, hash_type: HASH_TYPE = 'ahash', hash_size: int = 8) -> dict:
    """计算图片的3种图片Hash值
    :param pillow_image: PIL.ImageFile图片对象
    :param hash_type: 需要计算的hash类型，ahash/phash/dhash/all
    :param hash_size: 计算图片的边长，最终hash值为边长的平方
    :return: {'ahash':None,'phash':None,'dhash':None}
    """
    return _calc_hash(pillow_image, hash_type, hash_size)


def convert_numpy_hash_to_str(numpy_hash: Union[imagehash.NDArray, imagehash.ImageHash]) -> Union[str, None]:
    """将numpy数组形式的图片Hash值(imagehash.hash)转换为由01组成的字符串
    :param numpy_hash: numpy数组形式的图片Hash值
    :return: 由01组成的字符串"""
    return _convert_numpy_hash_to_str(numpy_hash)


def numpy_hash_to_str(numpy_hash: Union[imagehash.NDArray, imagehash.ImageHash]) -> Union[str, None]:
    """将numpy数组形式的图片Hash值(imagehash.hash)转换为由01组成的字符串
    :param numpy_hash: numpy数组形式的图片Hash值
    :return: 由01组成的字符串"""
    return _convert_numpy_hash_to_str(numpy_hash)


def calc_hamming_distance(hash_1: str, hash_2: str) -> Union[bool, int]:
    """计算两个由01组成的字符串形式的图片Hash值之间的汉明距离
    :param hash_1: 字符串形式的hash值
    :param hash_2: 字符串形式的hash值
    :return: 汉明距离，或者计算失败时返回False
    """
    return _calc_hamming_distance(hash_1, hash_2)


def calc_hash_hamming_distance(hash_1: str, hash_2: str) -> Union[bool, int]:
    """计算两个由01组成的字符串形式的图片Hash值之间的汉明距离
    :param hash_1: 字符串形式的hash值
    :param hash_2: 字符串形式的hash值
    :return: 汉明距离，或者计算失败时返回False
    """
    return _calc_hamming_distance(hash_1, hash_2)


def calc_hash_similar(hash_1: str, hash_2: str) -> Union[bool, float]:
    """计算两个由01组成的字符串形式的图片Hash值之间的相似度
    :param hash_1: 字符串形式的hash值
    :param hash_2: 字符串形式的hash值
    :return: 相似度（0~1），或者计算失败时返回False
    """
    return _calc_hash_similar(hash_1, hash_2)
