import numpy

"""----------逻辑函数----------"""


def _calc_ssim(numpy_image_1: numpy.ndarray, numpy_image_2: numpy.ndarray) -> float:
    """计算两个numpy图片对象的SSIM相似值
    :param numpy_image_1: numpy图片对象
    :param numpy_image_2: numpy图片对象
    :return: SSIM相似值
    """
    # 计算均值、方差和协方差
    mean1, mean2 = numpy.mean(numpy_image_1), numpy.mean(numpy_image_2)
    var1, var2 = numpy.var(numpy_image_1), numpy.var(numpy_image_2)
    covar = numpy.cov(numpy_image_1.flatten(), numpy_image_2.flatten())[0][1]

    # 设置常数
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    # 计算SSIM
    numerator = (2 * mean1 * mean2 + c1) * (2 * covar + c2)
    denominator = (mean1 ** 2 + mean2 ** 2 + c1) * (var1 + var2 + c2)
    ssim = numerator / denominator

    return ssim


"""----------调用函数----------"""


def calc_ssim(numpy_image_1: numpy.ndarray, numpy_image_2: numpy.ndarray) -> float:
    """计算两个numpy图片对象的SSIM相似值
    :param numpy_image_1: numpy图片对象
    :param numpy_image_2: numpy图片对象
    :return: SSIM相似值
    """
    return _calc_ssim(numpy_image_1, numpy_image_2)
