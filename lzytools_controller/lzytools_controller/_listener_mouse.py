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
            self.time: float = _time
            self.x: int = x
            self.y: int = y

    class Press:
        """按下鼠标事件"""

        def __init__(self, _time, x, y, button):
            self.time: float = _time
            self.x: int = x
            self.y: int = y
            self.button: MouseKey = button

    class Release:
        """释放鼠标事件"""

        def __init__(self, _time, x, y, button):
            self.time: float = _time
            self.x: int = x
            self.y: int = y
            self.button: MouseKey = button

    class Click:
        """鼠标点击事件"""

        def __init__(self, _time, x, y, button):
            self.time: float = _time
            self.x: int = x
            self.y: int = y
            self.button: MouseKey = button

    class Scroll:
        """鼠标滚轮事件"""

        def __init__(self, _time, x, y, direction):
            self.time: float = _time
            self.x: int = x
            self.y: int = y
            self.direction: MouseScroll = direction


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
        self._join_event()
        return self.events_collector

    def _join_event(self):
        """合并事件"""
        # 将时间差在150ms以内的连续press+release事件合并为click事件
        for i in range(len(self.events_collector) - 1):
            if isinstance(self.events_collector[i], MouseEventInfo.Press) and isinstance(self.events_collector[i + 1],
                                                                                         MouseEventInfo.Release):
                if self.events_collector[i].button == self.events_collector[i + 1].button:
                    if self.events_collector[i + 1].time - self.events_collector[i].time <= 0.15:
                        _time = self.events_collector[i].time
                        x = self.events_collector[i].x
                        y = self.events_collector[i].y
                        button = self.events_collector[i].button
                        click_event = MouseEventInfo.Click(_time, x, y, button)
                        self.events_collector[i] = click_event
                        self.events_collector[i + 1] = None

        # 剔除None
        self.events_collector = [i for i in self.events_collector if i is not None]

    def _on_move(self, x, y):
        """移动事件"""
        print(f'move {x}, {y}')
        time_ = time.time()
        event = MouseEventInfo.Move(time_, x, y)
        self.events_collector.append(event)

    def _on_click(self, x, y, button, is_pressed):
        """点击事件"""
        print(f'click {x}, {y}, {button}, {is_pressed}')
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
        print(f'scroll {x}, {y}, {dx}, {dy}')
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
    time.sleep(10)
    print(l1.get_events())
