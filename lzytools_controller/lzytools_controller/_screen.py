from typing import Tuple, Union, List

import numpy
import pyautogui

"""----------逻辑函数----------"""


def _screenshot_fullscreen(pic_file: str = 'screenshot.png'):
    """全屏截图
    :param pic_file:保存的图片路径
    return: 保存的图片路径
    """
    pyautogui.screenshot(pic_file)

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

    pyautogui.screenshot(pic_file, region=region)

    return pic_file


def _search_image_position(numpy_image: numpy.ndarray, precision: float = 0.95) -> Union[Tuple[int, int], None]:
    """检索图片在屏幕上首个出现的位置（图片中心轴坐标）
    :param numpy_image:需要检索的图片
    :param precision:搜索精度，0~1
    :return: 检索到的中心轴坐标
    """
    position = pyautogui.locateCenterOnScreen(numpy_image, confidence=precision)

    if position:
        x, y = position.x, position.y
        return x, y
    else:
        return None


def _search_image_positions(numpy_image: numpy.ndarray, precision: float = 0.95) -> Union[List[Tuple[int, int]], None]:
    """检索图片在屏幕上全部出现的位置（图片中心轴坐标）
    :param numpy_image:需要检索的图片
    :param precision:搜索精度，0~1
    :return: 检索到的中心轴坐标
    """
    positions = pyautogui.locateAllOnScreen(numpy_image, confidence=precision)

    if positions:
        positions_center = []
        for pos in positions:
            x_center = pos.left + pos.width // 2
            y_center = pos.top + pos.height // 2
            position = (x_center, y_center)
            positions_center.append(position)

        return positions_center
    else:
        return None


"""----------调用函数----------"""


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
