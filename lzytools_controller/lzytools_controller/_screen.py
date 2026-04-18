from typing import Tuple, Union, List

import numpy
import pyautogui

"""----------逻辑函数----------"""


def _get_screen_size() -> Tuple[int, int]:
    """获取屏幕尺寸
    :return: 屏幕尺寸（宽x高）
    """
    w, h = pyautogui.size()
    return w, h


def _get_rgb_color(x: int, y: int) -> Tuple[int, int, int]:
    """获取指定轴坐标的RGB颜色
    :param x: x轴坐标
    :param y: y轴坐标
    :return: RGB颜色
    """
    r, g, b = pyautogui.pixel(x, y)

    return r, g, b


def _check_rbg_color(x: int, y: int, rbg_color: Tuple[int, int, int], tolerance: int = 0) -> bool:
    """检查指定轴坐标颜色是否等于指定RGB颜色
    :param x: x轴坐标
    :param y: y轴坐标
    :param rbg_color: 对比的RGB值
    :param tolerance: 颜色匹配容差，0表示完全匹配
    :return: 是否相等
    """
    is_match = pyautogui.pixelMatchesColor(x, y, rbg_color, tolerance=tolerance)
    return is_match


def _screenshot_fullscreen(pic_file: str = 'screenshot.png'):
    """全屏截图
    :param pic_file:保存的图片路径
    return: 保存的图片路径
    """
    pyautogui.screenshot(pic_file)  # 返回PIL.Image对象

    return pic_file


def _screenshot_area(area: Tuple[Tuple[int, int], Tuple[int, int]], pic_file: str = 'screenshot.png'):
    """截图指定区域
    :param area: 截图坐标，任意两个对角的轴坐标
    :param pic_file:保存的图片路径
    return: 保存的图片路径
    """
    # 　转换为region格式
    x = min(area[0][0], area[1][0])
    y = min(area[0][1], area[1][1])
    width = abs(area[0][0] - area[1][0])
    height = abs(area[0][1] - area[1][1])
    region = (x, y, width, height)

    pyautogui.screenshot(pic_file, region=region)  # 返回PIL.Image对象

    return pic_file


def _search_image_position(numpy_image: numpy.ndarray, precision: float = 0.95, gray_mode: bool = False,
                           search_region: Tuple[int, int, int, int] = None) -> Union[Tuple[int, int], None]:
    """检索图片在屏幕上首个出现的位置（图片中心轴坐标）
    :param numpy_image:需要检索的图片
    :param precision:搜索精度，0~1
    :param gray_mode: 是否使用灰度模式进行匹配
    :param search_region: 指定的搜索区域，左上角xy轴坐标，右下角xy轴坐标
    :return: 检索到的中心轴坐标
    """
    # 转换搜索区域格式
    if search_region:
        width = search_region[2] - search_region[0]
        height = search_region[3] - search_region[1]
        region = (search_region[0], search_region[1], width, height)
    else:
        region = None

    position = pyautogui.locateOnScreen(numpy_image, confidence=precision, grayscale=gray_mode, region=region)

    if position:
        x, y = pyautogui.center(position)
        return x, y
    else:
        return None


def _search_image_positions(numpy_image: numpy.ndarray, precision: float = 0.95, gray_mode: bool = False,
                            search_region: Tuple[int, int, int, int] = None) -> Union[List[Tuple[int, int]], None]:
    """检索图片在屏幕上全部出现的位置（图片中心轴坐标）
    :param numpy_image:需要检索的图片
    :param precision:搜索精度，0~1
    :param gray_mode: 是否使用灰度模式进行匹配
    :param search_region: 指定的搜索区域，左上角xy轴坐标，右下角xy轴坐标
    :return: 检索到的中心轴坐标
    """
    # 转换搜索区域格式
    if search_region:
        width = search_region[2] - search_region[0]
        height = search_region[3] - search_region[1]
        region = (search_region[0], search_region[1], width, height)
    else:
        region = None

    positions = pyautogui.locateAllOnScreen(numpy_image, confidence=precision, grayscale=gray_mode, region=region)

    if positions:
        positions_center = []
        for pos in positions:
            x, y = pyautogui.center(pos)
            position = (x, y)
            positions_center.append(position)

        return positions_center
    else:
        return None


"""----------调用函数----------"""


def get_rgb_color(x: int, y: int) -> Tuple[int, int, int]:
    """获取指定轴坐标的RGB颜色
    :param x: x轴坐标
    :param y: y轴坐标
    :return: RGB颜色
    """
    return _get_rgb_color(x, y)


def get_screen_size() -> Tuple[int, int]:
    """获取屏幕尺寸
    :return: 屏幕尺寸（宽x高）
    """
    return _get_screen_size()


def check_rbg_color(x: int, y: int, rbg_color: Tuple[int, int, int], tolerance: int = 0) -> bool:
    """检查指定轴坐标颜色是否等于指定RGB颜色
    :param x: x轴坐标
    :param y: y轴坐标
    :param rbg_color: 对比的RGB值
    :param tolerance: 颜色匹配容差，0表示完全匹配
    :return: 是否相等
    """
    return _check_rbg_color(x, y, rbg_color, tolerance)


def screenshot_fullscreen(pic_file: str = 'screenshot.png'):
    """全屏截图
    :param pic_file:保存的图片路径
    return: 保存的图片路径
    """
    return _screenshot_fullscreen(pic_file)


def screenshot_area(area: Tuple[Tuple[int, int], Tuple[int, int]], pic_file: str = 'screenshot.png'):
    """截图指定区域
    :param area: 截图坐标，任意两个对角的轴坐标
    :param pic_file:保存的图片路径
    return: 保存的图片路径
    """
    return _screenshot_area(area, pic_file)


def search_image_position(numpy_image: numpy.ndarray, precision: float = 0.95) -> Union[Tuple[int, int], None]:
    """检索图片在屏幕上首个出现的位置（图片中心轴坐标）
    :param numpy_image:需要检索的图片
    :param precision:搜索精度，0~1
    :return: 检索到的中心轴坐标
    """
    return _search_image_position(numpy_image, precision)


def search_image_positions(numpy_image: numpy.ndarray, precision: float = 0.95) -> Union[List[Tuple[int, int]], None]:
    """检索图片在屏幕上全部出现的位置（图片中心轴坐标）
    :param numpy_image:需要检索的图片
    :param precision:搜索精度，0~1
    :return: 检索到的中心轴坐标
    """
    return _search_image_positions(numpy_image, precision)
