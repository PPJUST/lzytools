# 监听器
import time
from typing import List

from pynput import keyboard


class KeyboardEventInfo:
    """键盘事件信息"""

    class Press:
        """按下键盘事件"""

        def __init__(self, _time, key):
            self.time = _time
            self.key = key

    class Release:
        """释放键盘事件"""

        def __init__(self, _time, key):
            self.time = _time
            self.key = key


class ListenerKeyboard:
    """键盘事件监听器"""

    def __init__(self):
        self.events_collector: List[KeyboardEventInfo] = []
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release)

    def get_listener(self):
        return self.listener

    def start(self):
        self.events_collector.clear()
        self.listener.start()

    def get_events(self):
        return self.events_collector

    def _on_press(self, key):
        """按下事件"""
        print(key)
        time_ = time.time()
        event = KeyboardEventInfo.Press(time_, key)
        self.events_collector.append(event)

    def _on_release(self, key):
        """释放事件"""
        print(key)
        time_ = time.time()
        event = KeyboardEventInfo.Release(time_, key)
        self.events_collector.append(event)


if __name__ == '__main__':
    l1 = ListenerKeyboard()
    l1.start()
    time.sleep(100)
