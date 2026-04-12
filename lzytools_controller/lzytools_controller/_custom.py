import random
import time

"""----------逻辑函数----------"""


def _wait_time(_time: float):
    """等待时间
    :param _time:等待时间
    :return: 等待的时间
    """
    if _time == 0:
        _time = 0.01

    time.sleep(_time)

    return _time


def _wait_time_random(min_time: int, max_time: int):
    """等待随机时间
    :param min_time: 最小等待时间
    :param max_time: 最大等待时间
    :return: 等待的时间
    """
    random_time = round(random.uniform(min_time, max_time), 2)

    if random_time == 0:
        random_time = 0.01

    time.sleep(random_time)

    return random_time


"""----------调用函数----------"""
