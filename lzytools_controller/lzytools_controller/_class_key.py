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


MouseButton = Union[Type[MouseKey.Left], Type[MouseKey.Right], Type[MouseKey.Middle]]
