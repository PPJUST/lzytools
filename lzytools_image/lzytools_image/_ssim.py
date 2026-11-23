import numpy

from ._convert import _resize_numpy_image

# 统一的尺寸
DEFAULT_TARGET_SIZE: tuple[int, int] = (256, 256)
# SSIM 计算固定常数
C1: float = (0.01 * 255) ** 2
C2: float = (0.03 * 255) ** 2

"""----------逻辑函数----------"""


def _calc_ssim(numpy_image_1: numpy.ndarray, numpy_image_2: numpy.ndarray) -> float:
    """计算两个 numpy 图片对象的 SSIM 相似值。
    :param numpy_image_1: numpy 图片对象
    :param numpy_image_2: numpy 图片对象
    :return: SSIM 相似值，范围 0~1
    """
    # 入参校验
    if not isinstance(numpy_image_1, numpy.ndarray) or not isinstance(numpy_image_2, numpy.ndarray):
        raise TypeError('输入必须为 numpy.ndarray 类型的图片对象')
    if numpy_image_1.ndim not in (2, 3) or numpy_image_2.ndim not in (2, 3):
        raise ValueError('图片维度不合法，仅支持 (H,W) 灰度图 或 (H,W,C) 彩色图')

    # 统一尺寸并转为 float32，避免 uint8 溢出
    width, height = DEFAULT_TARGET_SIZE
    image_1 = _resize_numpy_image(numpy_image_1, width, height).astype(numpy.float32)
    image_2 = _resize_numpy_image(numpy_image_2, width, height).astype(numpy.float32)

    # 计算均值、方差和协方差
    mean_1 = numpy.mean(image_1)
    mean_2 = numpy.mean(image_2)
    var_1 = numpy.var(image_1)
    var_2 = numpy.var(image_2)
    # 与 numpy.var 统一使用 ddof=0，同时避免 numpy.cov 构造协方差矩阵
    covar = numpy.mean((image_1 - mean_1) * (image_2 - mean_2))

    # 计算 SSIM 并修正边界值
    numerator = (2 * mean_1 * mean_2 + C1) * (2 * covar + C2)
    denominator = (mean_1 ** 2 + mean_2 ** 2 + C1) * (var_1 + var_2 + C2)
    ssim = numerator / denominator

    return float(numpy.clip(ssim, 0.0, 1.0))


"""----------调用函数----------"""


def calc_ssim(numpy_image_1: numpy.ndarray, numpy_image_2: numpy.ndarray) -> float:
    """计算两个 numpy 图片对象的 SSIM 相似值。
    :param numpy_image_1: numpy 图片对象
    :param numpy_image_2: numpy 图片对象
    :return: SSIM 相似值，范围 0~1
    """
    return _calc_ssim(numpy_image_1, numpy_image_2)
