import time
from typing import Union

import pyautogui
import pyperclip

from ._pyautogui_keyboard_keys import KEY_NAMES

"""----------逻辑函数----------"""


def press_chars(chars: str, loop_count: int = 1, loop_interval: float = 0.1):
    """输入文本
    :param chars: 要输入的文本
    :param loop_count: 重复次数
    :param loop_interval:每次重复的间隔时间（秒）
    :return: 输入的文本
    """
    for _ in range(loop_count):
        pyperclip.copy(chars)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(loop_interval)

    return chars


def click_keys(keys: Union[list, str], loop_count: int = 1, loop_interval: float = 0.1):
    """逐个敲击指定键，支持多键（不能实现热键组合）
    :param keys:需要敲击的键
    :param loop_count: 重复次数
    :param loop_interval:每次重复的间隔时间（秒）
    :return: 敲击的键
    """
    if type(keys) is str:
        keys = keys.split(' ')

    for i in keys:
        if i.lower() not in KEY_NAMES:
            raise ValueError(f'{i} is not a valid key')

    pyautogui.press(keys=keys, presses=loop_count, interval=loop_interval)

    return keys


def press_key(key: str):
    """按下指定键
    :param key:要按下的键
    :return: 按下的键
    """
    pyautogui.keyDown(key)

    return key


def release_key(key: str):
    """释放指定键
    :param key:要释放的键
    :return: 释放的键
    """
    pyautogui.keyUp(key)

    return key


def press_hotkey(hotkeys: Union[list, str]):
    """敲击热键组合
    :param hotkeys:需要敲击的热键组合
    :return: 敲击的热键组合
    """
    if type(hotkeys) is str:
        hotkeys = hotkeys.split(' ')

    for i in hotkeys:
        if i.lower() not in KEY_NAMES:
            raise ValueError(f'{i} is not a valid key')

    pyautogui.hotkey(hotkeys)

    return hotkeys


"""----------调用函数----------"""
