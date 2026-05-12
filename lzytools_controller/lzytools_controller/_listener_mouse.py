# 监听器
import time
from typing import List

from pynput import mouse

from _class_key import MouseKey, MouseScroll


class MouseEventInfo:
    """鼠标事件信息"""

    class Move:
        """鼠标移动事件"""

        def __init__(self, _time, x, y):
            self.time = _time
            self.x = x
            self.y = y

    class Press:
        """按下鼠标事件"""

        def __init__(self, _time, x, y, button):
            self.time = _time
            self.x = x
            self.y = y
            self.button = button

    class Release:
        """释放鼠标事件"""

        def __init__(self, _time, x, y, button):
            self.time = _time
            self.x = x
            self.y = y
            self.button = button

    class Click:
        """鼠标点击事件"""

        def __init__(self, _time, x, y, button):
            self.time = _time
            self.x = x
            self.y = y
            self.button = button

    class Scroll:
        """鼠标滚轮事件"""

        def __init__(self, _time, x, y, direction):
            self.time = _time
            self.x = x
            self.y = y
            self.direction = direction


class ListenerMouse:
    """鼠标事件监听器"""

    def __init__(self):
        self.events_collector: List[MouseEventInfo] = []
        self.listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll)

    def get_listener(self):
        return self.listener

    def start(self):
        self.events_collector.clear()
        self.listener.start()

    def get_events(self):
        return self.events_collector

    def _on_move(self, x, y):
        """移动事件"""
        print(f'{x}, {y}')
        time_ = time.time()
        event = MouseEventInfo.Move(time_, x, y)
        self.events_collector.append(event)

    def _on_click(self, x, y, button, is_pressed):
        """点击事件"""
        print(f'{x}, {y}, {button}, {is_pressed}')
        time_ = time.time()

        # 转换button
        if button == mouse.Button.left:
            button_class = MouseKey.Left
        elif button == mouse.Button.middle:
            button_class = MouseKey.Middle
        elif button == mouse.Button.right:
            button_class = MouseKey.Right
        else:
            button_class = None

        # 转换pressed
        if is_pressed:
            event = MouseEventInfo.Press(time_, x, y, button_class)
        else:
            event = MouseEventInfo.Release(time_, x, y, button_class)

        self.events_collector.append(event)

    def _on_scroll(self, x, y, dx, dy):
        """滚轮事件"""
        print(f'{x}, {y}, {dx}, {dy}')
        time_ = time.time()

        # 转换direction
        if dy > 0:
            direction = MouseScroll.Up
        else:
            direction = MouseScroll.Down

        event = MouseEventInfo.Scroll(time_, x, y, direction)
        self.events_collector.append(event)


if __name__ == '__main__':
    l1 = ListenerMouse()
    l1.start()
    time.sleep(100)
