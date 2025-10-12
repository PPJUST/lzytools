import time
from datetime import datetime


def get_current_time(_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取当前时间的标准化格式str
    :param _format: str，自定义时间格式
    :return: str，时间格式表示的字符串"
    """
    return time.strftime(_format, time.localtime())


def convert_time_hms(runtime: float):
    """将一个时间差转换为时分秒的字符串"""
    hours = int(runtime // 3600)
    minutes = int((runtime % 3600) // 60)
    seconds = int(runtime % 60)
    time_str = f'{hours}:{minutes:02d}:{seconds:02d}'

    return time_str


def convert_time_ymd(time_second: float, _format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """将一个秒数时间转换为年月日的字符串"""
    date = datetime.fromtimestamp(time_second).strftime(_format)

    return date
