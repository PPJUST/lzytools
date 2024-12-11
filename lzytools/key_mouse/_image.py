import time
from typing import Union

import numpy
import pyautogui

# 默认参数
_DEFAULT_INTERVAL: float = 1  # 间隔时间
_DEFAULT_CONFIDENCE = 0.9  # 寻图精度
_DEFAULT_SCREENSHOT_IMAGE = 'screenshot.jpg'

"""
pyautogui库关于图像的操作调用了PyScreeze库
如果指定了confidence参数，则需要安装opencv库
"""


def screenshot_fullscreen(save_path: str = _DEFAULT_SCREENSHOT_IMAGE):
    """全屏截图并保存到本地
    :param save_path: str，保存的图片路径"""
    pyautogui.screenshot(save_path)

    return save_path


def screenshot_area(area: tuple, save_path: str = 'screenshot.png'):
    """指定区域截图并保存到本地图片
    :param area: tuple，截图区域(左上角X坐标值, 左上角Y坐标值, 右下角X坐标值, 右下角Y坐标值)
    :param save_path: str，保存的图片路径
    """
    region = (area[0], area[1], area[2] + area[0], area[3] + area[1])  # 转换area参数至pyautogui格式
    pyautogui.screenshot(save_path, region=region)

    return save_path


def _search_first_position(image_numpy: numpy.ndarray, confidence: float = _DEFAULT_CONFIDENCE) -> Union[tuple, None]:
    """在屏幕上搜索图片，获取第一次匹配到的中心点坐标
    :param image_numpy: numpy图片对象，需要搜索的图片
    :param confidence: float，搜索精度，0~1
    :return: 坐标轴元组(x, y)或None
    """
    position = pyautogui.locateCenterOnScreen(image_numpy, confidence=confidence)
    if position:
        loc = (position.x, position.y)
        return loc
    else:
        return None


def _search_all_position(image_numpy: numpy.ndarray, confidence: float = _DEFAULT_CONFIDENCE,
                         timeout: int = 60) -> list:
    """在屏幕上搜索图片，获取所有匹配到的中心点坐标
    :param image_numpy: numpy图片对象，需要搜索的图片
    :param confidence: float，搜索精度，0~1
    :param timeout: int，超时时间（秒）
    :return: list，包含坐标轴的元组[(x1, y1), (x2, y2)...]
    """
    time_start = time.time()
    positions = []
    while True:
        poss = pyautogui.locateAllOnScreen(image_numpy, confidence=confidence)
        for pos in poss:
            mid_x = pos.left + pos.width // 2
            mid_y = pos.top + pos.height // 2
            positions.append((mid_x, mid_y))
        if positions:
            break

        time_current = time.time()
        run_time = time_start - time_current
        if run_time >= timeout:
            break
        else:
            time.sleep(_DEFAULT_INTERVAL)

    return positions
