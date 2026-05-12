# 鼠标按键的自定义类

from typing import Type, Union


class MouseKey:
    class Left:
        """鼠标左键"""
        value = 'left'

    class Right:
        """鼠标右键"""
        value = 'right'

    class Middle:
        """鼠标中键"""
        value = 'middle'

class MouseEvent:
    class Press:
        """鼠标按下事件"""
        value = 'press'
    class Release:
        """鼠标释放事件"""
        value = 'release'

class MouseScroll:
    """鼠标滚轮事件"""
    class Up:
        """鼠标滚轮向上"""
        value = 'up'
    class Down:
        """鼠标滚轮向下"""
        value = 'down'
MouseButton = Union[Type[MouseKey.Left], Type[MouseKey.Right], Type[MouseKey.Middle]]
