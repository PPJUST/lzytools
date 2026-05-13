# 监听器
import time
from typing import List, Union

from pynput import keyboard

from _key_pynput_to_pyautogui import convert_key


class KeyboardEventInfo:
    """键盘事件信息"""

    class Press:
        """按下键盘事件"""

        def __init__(self, _time, key):
            self.time: float = _time
            self.key: Union[str, List[str], None] = key

    class Release:
        """释放键盘事件"""

        def __init__(self, _time, key):
            self.time: float = _time
            self.key: Union[str, List[str], None] = key

    class Click:
        """点击键盘事件"""

        def __init__(self, _time, key):
            self.time: float = _time
            self.key: Union[str, List[str], None] = key


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
        self._join_event()
        return self.events_collector

    def _join_event(self):
        """合并事件"""
        # 将时间差在150ms以内的连续press+release事件合并为click事件
        for i in range(len(self.events_collector) - 1):
            if isinstance(self.events_collector[i], KeyboardEventInfo.Press) and isinstance(
                    self.events_collector[i + 1], KeyboardEventInfo.Release):
                if self.events_collector[i].key == self.events_collector[i + 1].key:
                    if self.events_collector[i + 1].time - self.events_collector[i].time <= 0.15:
                        _time = self.events_collector[i].time
                        key = self.events_collector[i].key
                        click_event = KeyboardEventInfo.Click(_time, key)
                        self.events_collector[i] = click_event
                        self.events_collector[i + 1] = None

        # 剔除None
        self.events_collector = [i for i in self.events_collector if i is not None]

        # 转换key
        for event in self.events_collector:
            key_pynput = event.key
            key_pyautogui = convert_key(key_pynput)
            if key_pyautogui is not None:
                event.key = key_pyautogui

    def _on_press(self, key):
        """按下事件"""
        print(f'press {key}')
        time_ = time.time()
        event = KeyboardEventInfo.Press(time_, key)
        self.events_collector.append(event)

    def _on_release(self, key):
        """释放事件"""
        print(f'release {key}')
        time_ = time.time()
        event = KeyboardEventInfo.Release(time_, key)
        self.events_collector.append(event)


if __name__ == '__main__':
    l1 = ListenerKeyboard()
    l1.start()
    time.sleep(10)
    print(l1.get_events())
