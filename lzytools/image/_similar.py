from typing import Union

import imagehash
import numpy
from PIL import ImageFile


def calc_hash(image: ImageFile, hash_type: str = 'ahash', hash_size: int = 8) -> dict:
    """计算图片的3种图片Hash值
    :param image: PIL.ImageFile图片对象
    :param hash_type: 计算的hash类型，ahash/phash/dhash/all
    :param hash_size: 计算的图片Hash值的边长
    :return: dict，{'ahash':None,'phash':None,'dhash':None}
    """
    hash_dict = {'ahash': None, 'phash': None, 'dhash': None}

    if hash_type.lower() == 'all' or hash_type.lower() == 'ahash':
        # 计算均值哈希
        ahash = imagehash.average_hash(image, hash_size=hash_size)
        ahash_str = numpy_hash_to_str(ahash)
        hash_dict['ahash'] = ahash_str

    if hash_type.lower() == 'all' or hash_type.lower() == 'phash':
        # 感知哈希
        phash = imagehash.phash(image, hash_size=hash_size)
        phash_str = numpy_hash_to_str(phash)
        hash_dict['phash'] = phash_str

    if hash_type.lower() == 'all' or hash_type.lower() == 'dhash':
        # 差异哈希
        dhash = imagehash.dhash(image, hash_size=hash_size)
        dhash_str = numpy_hash_to_str(dhash)
        hash_dict['dhash'] = dhash_str

    return hash_dict


def numpy_hash_to_str(numpy_hash: Union[imagehash.NDArray, imagehash.ImageHash]):
    """将numpy数组形式的图片Hash值(imagehash.hash)转换为01组成的字符串
    :param numpy_hash: numpy数组形式的图片Hash值
    :return: str，01组成的字符串"""
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


def calc_hash_hamming_distance(hash_1: str, hash_2: str):
    """计算两个01字符串形式的图片Hash值的汉明距离"""
    hamming_distance = sum(ch1 != ch2 for ch1, ch2 in zip(hash_1, hash_2))
    return hamming_distance


def calc_hash_similar(hash_1: str, hash_2: str):
    """计算两个01字符串形式的图片Hash值的相似度（0~1)"""
    hash_int1 = int(hash_1, 2)
    hash_int2 = int(hash_2, 2)
    # 使用异或操作计算差异位数
    diff_bits = bin(hash_int1 ^ hash_int2).count('1')
    # 计算相似性
    similarity = 1 - diff_bits / len(hash_1)

    return similarity


def calc_ssim(image_numpy_1: numpy.ndarray, image_numpy_2: numpy.ndarray) -> float:
    """计算两张图片的SSIM相似值（0~1，越大越相似）
    :param image_numpy_1: numpy图片对象
    :param image_numpy_2: numpy图片对象
    :return: float，SSIM相似值（0~1，越大越相似）"""
    # 计算均值、方差和协方差
    mean1, mean2 = numpy.mean(image_numpy_1), numpy.mean(image_numpy_2)
    var1, var2 = numpy.var(image_numpy_1), numpy.var(image_numpy_2)
    covar = numpy.cov(image_numpy_1.flatten(), image_numpy_2.flatten())[0][1]

    # 设置常数
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    # 计算SSIM
    numerator = (2 * mean1 * mean2 + c1) * (2 * covar + c2)
    denominator = (mean1 ** 2 + mean2 ** 2 + c1) * (var1 + var2 + c2)
    ssim = numerator / denominator

    return ssim
