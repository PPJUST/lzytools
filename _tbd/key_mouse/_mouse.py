import math
from typing import Tuple

import pyautogui

# 默认参数
_DEFAULT_MOVE_DURATION: float = 0.25  # 移动所需时间
_DEFAULT_BUTTON: str = 'left'  # 默认鼠标按键
_DEFAULT_CLICKS: int = 1  # 点击次数
_DEFAULT_INTERVAL: float = 0.1  # 间隔时间
_DEFAULT_MOVE_DIRECTION: int = 0  # 移动方向
_DEFAULT_MOVE_DISTANCE: int = 100  # 移动距离
_DEFAULT_SCROLL_DISTANCE: int = 100  # 滚动滚动距离
_MAX_X, _MAX_Y = pyautogui.size()  # x,y坐标值的最大值限制（屏幕大小）


def _check_position(x: int, y: int):
    """检查xy轴，0,0->1,1"""
    if x == 0 and y == 0:  # 0,0替换为1,1，防止提前终止
        return 1, 1
    else:
        return x, y


def _check_button(button: str):
    """检查按键，统一为pyautogui支持的格式"""
    if button.lower() in ['left', '左键']:
        return 'left'
    elif button.lower() in ['right', '右键']:
        return 'right'
    elif button.lower() in ['middle', '中键']:
        return 'middle'
    else:
        raise Exception(f'非法参数：{button}')


def get_position() -> Tuple[int, int]:
    """获取当前鼠标的位置坐标
    :return: x轴坐标，y轴坐标"""
    x, y = pyautogui.position()

    return x, y


def move_to_position(x: int, y: int, move_duration: float = _DEFAULT_MOVE_DURATION):
    """移动鼠标至指定坐标轴
    :param x: int，x轴坐标
    :param y: int，y轴坐标
    :param move_duration: float，移动所需时间（秒）"""
    x, y = _check_position(x, y)  # 检查坐标

    pyautogui.moveTo(x, y, duration=move_duration)

    return x, y


def drag_to_position(x: int, y: int, button: str = _DEFAULT_BUTTON,
                     move_duration: float = _DEFAULT_MOVE_DURATION):
    """按下鼠标键后拖拽至指定坐标轴
    :param x: int，x轴坐标
    :param y: int，y轴坐标
    :param button: str，鼠标按键，left/左键/right/右键/middle/中键
    :param move_duration: float，移动所需时间（秒）
    """
    x, y = _check_position(x, y)  # 检查坐标
    button = _check_button(button)  # 检查按键
    pyautogui.dragTo(x, y, button=button, duration=move_duration)

    return x, y


def move_relative(move_direction: int = _DEFAULT_MOVE_DIRECTION,
                  move_distance: int = _DEFAULT_MOVE_DISTANCE, move_duration: float = _DEFAULT_MOVE_DURATION):
    """以鼠标当前位置为基点，相对移动鼠标
    :param move_direction: int，移动角度（水平向左为0°，垂直向下为90°，水平向右为180°或-180°，垂直向上为270°或-90°）
    :param move_distance: int，移动距离
    :param move_duration: float，移动所需时间（秒）
    """
    # 计算目标位置的坐标轴
    x, y = pyautogui.position()
    angle_radians = math.radians(move_direction)  # 转弧度
    x = x + move_distance * math.cos(angle_radians)
    y = y + move_distance * math.sin(angle_radians)

    # 检查xy
    if x < 0:
        x = 1
    if x > _MAX_X:
        x = _MAX_X

    if y < 0:
        y = 1
    if y > _MAX_X:
        y = _MAX_X

    x, y = _check_position(x, y)  # 检查坐标

    pyautogui.moveTo(x, y, duration=move_duration)

    return x, y


def click(button: str = _DEFAULT_BUTTON, clicks: int = _DEFAULT_CLICKS,
          interval: float = _DEFAULT_INTERVAL):
    """点击鼠标按键
    :param button: str，鼠标按键，left/right/middle
    :param clicks: int，点击次数
    :param interval: float，两次点击之间的间隔时间（秒）"""
    button = _check_button(button)  # 检查按键
    pyautogui.click(button=button, clicks=clicks, interval=interval)

    return button


def press_down(button: str = _DEFAULT_BUTTON):
    """按下鼠标按键
    :param button: str，鼠标按键，left/right/middle"""
    button = _check_button(button)  # 检查按键
    pyautogui.mouseDown(button=button)

    return button


def release(button: str = _DEFAULT_BUTTON):
    """释放鼠标按键
    :param button: str，鼠标按键，left/right/middle"""
    button = _check_button(button)  # 检查按键
    pyautogui.mouseUp(button=button)

    return button


def scroll_wheel(distance: int = _DEFAULT_SCROLL_DISTANCE):
    """滚动鼠标滚轮
    :param distance: int，滚动距离，正数向上滚动，负数向下滚动"""
    pyautogui.scroll(clicks=distance)

    return distance
