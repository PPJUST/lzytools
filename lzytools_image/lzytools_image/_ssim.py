from typing import Tuple

import numpy

from ._convert import _resize_numpy_image

# 统一的尺寸
DEFAULT_TARGET_SIZE: Tuple[int, int] = (256, 256)
# SSIM计算固定常数
C1: float = (0.01 * 255) ** 2
C2: float = (0.03 * 255) ** 2

"""----------逻辑函数----------"""


def _calc_ssim(numpy_image_1: numpy.ndarray, numpy_image_2: numpy.ndarray) -> float:
    """计算两个numpy图片对象的SSIM相似值
    :param numpy_image_1: numpy图片对象
    :param numpy_image_2: numpy图片对象
    :return: SSIM相似值
    """
    # 入参校验
    if not isinstance(numpy_image_1, numpy.ndarray) or not isinstance(numpy_image_2, numpy.ndarray):
        raise TypeError("输入必须为numpy.ndarray类型的图片对象")
    if numpy_image_1.ndim not in (2, 3) or numpy_image_2.ndim not in (2, 3):
        raise ValueError("图片维度不合法，仅支持 (H,W)灰度图 或 (H,W,C)彩色图")

    # 统一尺寸
    numpy_image_1_resized = _resize_numpy_image(numpy_image_1, DEFAULT_TARGET_SIZE[0], DEFAULT_TARGET_SIZE[1])
    numpy_image_2_resized = _resize_numpy_image(numpy_image_2, DEFAULT_TARGET_SIZE[0], DEFAULT_TARGET_SIZE[1])

    #  数据类型归一化（转为float32，避免uint8溢出）
    numpy_image_1_resized = numpy_image_1_resized.astype(numpy.float32)
    numpy_image_2_resized = numpy_image_2_resized.astype(numpy.float32)

    # 计算均值、方差和协方差
    mean1 = numpy.mean(numpy_image_1_resized)
    mean2 = numpy.mean(numpy_image_2_resized)
    var1 = numpy.var(numpy_image_1_resized)
    var2 = numpy.var(numpy_image_2_resized)
    covar = numpy.cov(numpy_image_1_resized.ravel(), numpy_image_2_resized.ravel())[0, 1]

    # 计算SSIM
    numerator = (2 * mean1 * mean2 + C1) * (2 * covar + C2)
    denominator = (mean1 ** 2 + mean2 ** 2 + C1) * (var1 + var2 + C2)
    ssim = numerator / denominator

    #  边界值修正：确保SSIM值在[0,1]范围内
    ssim = float(numpy.clip(ssim, 0.0, 1.0))

    return ssim


"""----------调用函数----------"""


def calc_ssim(numpy_image_1: numpy.ndarray, numpy_image_2: numpy.ndarray) -> float:
    """计算两个numpy图片对象的SSIM相似值
    :param numpy_image_1: numpy图片对象
    :param numpy_image_2: numpy图片对象
    :return: SSIM相似值
    """
    return _calc_ssim(numpy_image_1, numpy_image_2)
