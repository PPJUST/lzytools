import random
import time

# 默认参数
_DEFAULT_WAIT_TIME = 1.0
_DEFAULT_WAIT_TIME_MIN = 1
_DEFAULT_WAIT_TIME_MAX = 2


def wait_time(_wait_time: float = _DEFAULT_WAIT_TIME):
    """等待指定时间
    :param _wait_time: float，等待时间"""
    if _wait_time == 0:
        _wait_time = 0.01

    time.sleep(_wait_time)

    return _wait_time


def wait_random_time(wait_time_min: int = _DEFAULT_WAIT_TIME_MIN, wait_time_max: int = _DEFAULT_WAIT_TIME_MAX):
    """等待随机时间
    :param wait_time_min: int，随机时间的下限
    :param wait_time_max: int，随机时间的上限"""
    wait_time_random = round(random.uniform(wait_time_min, wait_time_max), 2)

    if wait_time_random == 0:
        wait_time_random = 0.01

    time.sleep(wait_time_random)

    return wait_time_random
