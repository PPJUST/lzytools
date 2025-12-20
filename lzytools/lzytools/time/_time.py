import time
from datetime import datetime

"""----------逻辑函数----------"""


def _get_current_date(_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取当前的标准格式时间
    :param _format: 自定义时间格式
    :return: 标准格式时间
    """
    return time.strftime(_format, time.localtime())


def _format_duration(duration: float, _format: str = '%H:%M:%S') -> str:
    """将一个时长（秒）转换为格式化文本，主要用于计时
    :param duration: 时长，秒
    :param _format: 自定义时间格式
    :return: 时分秒格式的时长"""
    days = int(duration // 86400)
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)

    time_str = _format.replace('%D', str(days))
    time_str = time_str.replace('%H', str(hours))
    time_str = time_str.replace('%M', str(minutes).zfill(2))
    time_str = time_str.replace('%S', str(seconds).zfill(2))

    return time_str


def _convert_duration_to_date(tm_seconds: float, _format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """将一个秒数时间转换为标准格式时间
    :param tm_seconds: 时长，秒
    :param _format: 自定义时间格式
    :return: 标准格式时间"""
    date = datetime.fromtimestamp(tm_seconds).strftime(_format)

    return date


"""----------调用函数----------"""


def get_current_time(_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取当前的标准格式时间
    :param _format: 自定义时间格式
    :return: 标准格式时间
    """
    return _get_current_date(_format)


def get_current_date(_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取当前的标准格式时间
    :param _format: 自定义时间格式
    :return: 标准格式时间
    """
    return _get_current_date(_format)


def format_duration(duration: float, _format: str = '%H:%M:%S') -> str:
    """将一个时长（秒）转换为格式化文本，主要用于计时
    :param duration: 时长，秒
    :param _format: 自定义时间格式
    :return: 时分秒格式的时长"""
    return _format_duration(duration, _format)


def convert_time_hms(duration: float, _format: str = '%H:%M:%S') -> str:
    """将一个时长（秒）转换为格式化文本，主要用于计时
    :param duration: 时长，秒
    :param _format: 自定义时间格式
    :return: 时分秒格式的时长"""
    return _format_duration(duration, _format)


def convert_duration_to_date(tm_seconds: float, _format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """将一个秒数时间转换为标准格式时间
    :param tm_seconds: 时长，秒
    :param _format: 自定义时间格式
    :return: 标准格式时间"""
    return _convert_duration_to_date(tm_seconds, _format)


def convert_time_ymd(tm_seconds: float, _format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """将一个秒数时间转换为标准格式时间
    :param tm_seconds: 时长，秒
    :param _format: 自定义时间格式
    :return: 标准格式时间"""
    return _convert_duration_to_date(tm_seconds, _format)
