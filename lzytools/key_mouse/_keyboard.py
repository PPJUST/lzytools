import time

import pyautogui
import pyperclip

# 默认参数
_DEFAULT_INTERVAL: float = 0.1  # 间隔时间
_DEFAULT_PRESSES: int = 1  # 重复次数


def press_text(message: str, presses: int = _DEFAULT_PRESSES, interval: float = _DEFAULT_INTERVAL):
    """输入字符串（通过复制粘贴实现）
    :param message: str，输入的文本
    :param presses: int，重复次数
    :param interval: float，两次输入之间的间隔时间
    """
    for _ in range(presses):
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(interval)

    return message


def press_keys(keys: list, presses: int = _DEFAULT_PRESSES, interval: float = _DEFAULT_INTERVAL):
    """敲击指定键盘按键
    :param keys: list，单个或多个键盘按键，需要指定的按键名称
    :param presses: int，重复次数
    :param interval: float，两次输入之间的间隔时间
    """
    pyautogui.press(keys=keys, presses=presses, interval=interval)

    return keys


def press_down(key: str):
    """按下键盘按键
    :param key: str，单个键盘按键，需要指定的按键名称"""
    pyautogui.keyDown(key)

    return key


def release(key: str):
    """释放键盘按键
    :param key: str，单个键盘按键，需要指定的按键名称"""
    pyautogui.keyUp(key)

    return key


def press_hotkey(hotkeys: list):
    """按下组合键盘按键，实现热键操作
    :param hotkeys: list，单个或多个键盘按键，需要指定的按键名称"""
    pyautogui.hotkey(hotkeys)

    return hotkeys
