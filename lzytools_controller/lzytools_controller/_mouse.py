import math
from typing import Tuple

import pyautogui

from ._class_key import MouseKey, MouseButton

"""----------逻辑函数----------"""


def _get_position() -> Tuple[int, int]:
    """获取鼠标当前的轴坐标
    :return: x, y
    """
    mouse_x, mouse_y = pyautogui.position()

    return mouse_x, mouse_y


def _move_to_position(x: int, y: int, duration: float = 0.5):
    """移动鼠标至指定轴坐标
    :param x: x轴坐标
    :param y: y轴坐标
    :param duration: 移动时长，值为0时为瞬间移动
    :return: 移动后的轴坐标
    """
    if x == 0 and y == 0:  # 鼠标位于坐标轴(0, 0)时，pyautogui会触发中断机制返回报错
        x, y = 1, 1

    pyautogui.moveTo(x, y, duration=duration)

    return x, y


def _drag_to_position(x: int, y: int, button: MouseButton = MouseKey.Left, duration: float = 0.5):
    """拖动鼠标至指定轴坐标
    :param x: x轴坐标
    :param y: y轴坐标
    :param button: 鼠标按键
    :param duration: 移动时长，值为0时为瞬间移动
    :return: 移动后的轴坐标
    """
    if x == 0 and y == 0:  # 鼠标位于坐标轴(0, 0)时，pyautogui会触发中断机制返回报错
        x, y = 1, 1

    pyautogui.dragTo(x, y, button=button.value, duration=duration)

    return x, y


def _move_relative(angle: float = 0.00, distance: int = 0, duration: float = 0.5):
    """向指定方向移动鼠标
    :param angle: 角度，-360°~360°，以水平向左为0°，垂直向下为90°，垂直向上为-90°
    :param distance: 移动距离
    :param duration: 移动时长，值为0时为瞬间移动
    :return: 移动后的轴坐标
    """
    # 获取当前坐标
    current_x, current_y = pyautogui.position()

    # 角度转弧度
    angle_rad = math.radians(angle)

    # 计算坐标增量
    dx = distance * math.cos(angle_rad)
    dy = distance * math.sin(angle_rad)

    # 计算新坐标（向左x减小，向下y增加）
    new_x = current_x - dx
    new_y = current_y + dy

    # 限制坐标范围
    if new_x < 0:
        new_x = 0
    if new_y < 0:
        new_y = 0
    if new_x == 0 and new_y == 0:  # 鼠标位于坐标轴(0, 0)时，pyautogui会触发中断机制返回报错
        new_x, new_y = 1, 1

    pyautogui.moveTo(new_x, new_y, duration=duration)

    return new_x, new_y


def _click(button: MouseButton = MouseKey.Left, click_count: int = 1, click_interval: float = 0.1):
    """连续点击鼠标按键
    :param button: 鼠标按键
    :param click_count: 点击次数
    :param click_count: 每次点击间隔的时间（秒）
    :return: 点击的按键
    """
    pyautogui.click(button=button.value, clicks=click_count, interval=click_interval)

    return button.value


def _press(button: MouseButton = MouseKey.Left):
    """按下鼠标按键
    :param button: 鼠标按键
    :return: 按下的按键
    """
    pyautogui.mouseDown(button=button.value)

    return button.value


def _release(button: MouseButton = MouseKey.Left):
    """释放鼠标按键
    :param button: 鼠标按键
    :return: 释放的按键
    """
    pyautogui.mouseUp(button=button.value)

    return button.value


def _scroll_wheel(distance: int = 0):
    """滚动滚轮
    :param distance: 滚动格数，+为向上滚动，-为向下滚动
    :return: 滚动格数
    """
    pyautogui.scroll(clicks=distance)

    return distance


"""----------调用函数----------"""


def get_position() -> Tuple[int, int]:
    """获取鼠标当前的轴坐标
    :return: x, y
    """
    return _get_position()


def move_to_position(x: int, y: int, duration: float = 0.5):
    """移动鼠标至指定轴坐标
    :param x: x轴坐标
    :param y: y轴坐标
    :param duration: 移动时长，值为0时为瞬间移动
    :return: 移动后的轴坐标
    """
    return _move_to_position(x, y, duration)


def drag_to_position(x: int, y: int, button: MouseButton = MouseKey.Left, duration: float = 0.5):
    """拖动鼠标至指定轴坐标
    :param x: x轴坐标
    :param y: y轴坐标
    :param button: 鼠标按键
    :param duration: 移动时长，值为0时为瞬间移动
    :return: 移动后的轴坐标
    """
    return _drag_to_position(x, y, button, duration)


def move_relative(angle: float = 0.00, distance: int = 0, duration: float = 0.5):
    """向指定方向移动鼠标
    :param angle: 角度，-360°~360°，以水平向左为0°，垂直向下为90°，垂直向上为-90°
    :param distance: 移动距离
    :param duration: 移动时长，值为0时为瞬间移动
    :return: 移动后的轴坐标
    """
    return _move_relative(angle, distance, duration)


def click(button: MouseButton = MouseKey.Left, click_count: int = 1, click_interval: float = 0.1):
    """连续点击鼠标按键
    :param button: 鼠标按键
    :param click_count: 点击次数
    :param click_interval: 每次点击间隔的时间（秒）
    :return: 点击的按键
    """
    return _click(button, click_count, click_interval)


def press(button: MouseButton = MouseKey.Left):
    """按下鼠标按键
    :param button: 鼠标按键
    :return: 按下的按键
    """
    return _press(button)


def release(button: MouseButton = MouseKey.Left):
    """释放鼠标按键
    :param button: 鼠标按键
    :return: 释放的按键
    """
    return _release(button)


def scroll_wheel(distance: int = 0):
    """滚动滚轮
    :param distance: 滚动格数，+为向上滚动，-为向下滚动
    :return: 滚动格数
    """
    return _scroll_wheel(distance)
