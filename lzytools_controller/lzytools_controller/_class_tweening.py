# 补间动画的类

from typing import Type, Union

import pyautogui


class Tweening:
    """补间动画"""

    class Linear:
        """匀速移动"""
        value = pyautogui.linear

    class EaseInQuad:
        """二次缓动 初始慢->逐渐加速"""
        value = pyautogui.easeInQuad

    class EaseOutQuad:
        """二次缓动 初始快->逐渐减速"""
        value = pyautogui.easeOutQuad

    class EaseInOutQuad:
        """二次缓动 两端慢->中间快"""
        value = pyautogui.easeInOutQuad

    class EaseInElastic:
        """弹性移动 带弹性的加速"""
        value = pyautogui.easeInElastic

    class EaseOutElastic:
        """弹性移动 带弹性的减速"""
        value = pyautogui.easeOutElastic

    class EaseInOutElastic:
        """弹性移动 两端带弹性"""
        value = pyautogui.easeInOutElastic

    class EaseInBounce:
        """反弹效果 带弹性的加速"""
        value = pyautogui.easeInBounce

    class EaseOutBounce:
        """反弹效果 带弹性的减速"""
        value = pyautogui.easeOutBounce

    class EaseInOutBounce:
        """反弹效果 两端带弹性"""
        value = pyautogui.easeInOutBounce


TweeningTpye = Union[Type[Tweening.Linear],
Type[Tweening.EaseInQuad], Type[Tweening.EaseOutQuad], Type[Tweening.EaseInOutQuad],
Type[Tweening.EaseInElastic], Type[Tweening.EaseOutElastic], Type[Tweening.EaseInOutElastic],
Type[Tweening.EaseInBounce], Type[Tweening.EaseOutBounce], Type[Tweening.EaseInOutBounce]]
