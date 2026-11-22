import time
from datetime import datetime

"""----------常量----------"""

_DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
_DEFAULT_DURATION_FORMAT = '%H:%M:%S'
_SECONDS_PER_DAY = 86400
_SECONDS_PER_HOUR = 3600
_SECONDS_PER_MINUTE = 60

"""----------逻辑函数----------"""


def _get_current_date(_format: str = _DEFAULT_DATETIME_FORMAT) -> str:
    """获取本地时区的当前时间
    :param _format: strftime 时间格式
    :return: 格式化后的当前时间
    """
    return time.strftime(_format)


def _format_duration(duration: float, _format: str = _DEFAULT_DURATION_FORMAT) -> str:
    """将时长（秒）格式化为文本，主要用于计时
    :param duration: 时长，秒；负数以 '-' 开头
    :param _format: 自定义格式，支持 %D（天）、%H（小时）、%M（分）、%S（秒）
                    %M/%S 固定两位；%H 默认为总小时数，格式含 %D 时为当天小时数
    :return: 格式化后的时长文本
    """
    sign = '-' if duration < 0 else ''
    days, remainder = divmod(abs(duration), _SECONDS_PER_DAY)
    hours, remainder = divmod(remainder, _SECONDS_PER_HOUR)
    minutes, seconds = divmod(remainder, _SECONDS_PER_MINUTE)

    # 已单独输出天数时，小时不再重复计入整天
    display_hours = hours if '%D' in _format else days * 24 + hours

    time_str = _format.replace('%D', str(int(days)))
    time_str = time_str.replace('%H', str(int(display_hours)))
    time_str = time_str.replace('%M', str(int(minutes)).zfill(2))
    time_str = time_str.replace('%S', str(int(seconds)).zfill(2))

    return f'{sign}{time_str}'


def _convert_duration_to_date(tm_seconds: float, _format: str = _DEFAULT_DATETIME_FORMAT) -> str:
    """将 Unix 时间戳（秒）转换为本地时区的格式化时间
    :param tm_seconds: Unix 时间戳，秒
    :param _format: strftime 时间格式
    :return: 格式化后的时间文本
    """
    return datetime.fromtimestamp(tm_seconds).strftime(_format)


"""----------调用函数----------"""


def get_current_time(_format: str = _DEFAULT_DATETIME_FORMAT) -> str:
    """获取本地时区的当前时间
    :param _format: strftime 时间格式
    :return: 格式化后的当前时间
    """
    return _get_current_date(_format)


def get_current_date(_format: str = _DEFAULT_DATETIME_FORMAT) -> str:
    """获取本地时区的当前时间
    :param _format: strftime 时间格式
    :return: 格式化后的当前时间
    """
    return _get_current_date(_format)


def format_duration(duration: float, _format: str = _DEFAULT_DURATION_FORMAT) -> str:
    """将时长（秒）格式化为文本，主要用于计时
    :param duration: 时长，秒；负数以 '-' 开头
    :param _format: 自定义格式，支持 %D（天）、%H（小时）、%M（分）、%S（秒）
    :return: 格式化后的时长文本
    """
    return _format_duration(duration, _format)


def convert_time_hms(duration: float, _format: str = _DEFAULT_DURATION_FORMAT) -> str:
    """将时长（秒）格式化为文本
    :param duration: 时长，秒；负数以 '-' 开头
    :param _format: 自定义格式，支持 %D（天）、%H（小时）、%M（分）、%S（秒）
    :return: 格式化后的时长文本
    """
    return _format_duration(duration, _format)


def convert_duration_to_date(tm_seconds: float, _format: str = _DEFAULT_DATETIME_FORMAT) -> str:
    """将 Unix 时间戳（秒）转换为本地时区的格式化时间
    :param tm_seconds: Unix 时间戳，秒
    :param _format: strftime 时间格式
    :return: 格式化后的时间文本
    """
    return _convert_duration_to_date(tm_seconds, _format)


def convert_time_ymd(tm_seconds: float, _format: str = _DEFAULT_DATETIME_FORMAT) -> str:
    """将 Unix 时间戳（秒）转换为本地时区的格式化时间
    :param tm_seconds: Unix 时间戳，秒
    :param _format: strftime 时间格式
    :return: 格式化后的时间文本
    """
    return _convert_duration_to_date(tm_seconds, _format)
