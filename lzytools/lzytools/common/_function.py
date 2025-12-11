import inspect
import time
from typing import Tuple

"""----------逻辑函数----------"""


def _get_function_info(mode: str = 'current') -> Tuple[str, str, str]:
    """获取当前运行/上个运行的函数的信息
    :param mode: 'current' 或 'last'
    :return: 运行时间，函数名，函数文件路径
    """
    # 获取调用栈
    stack_trace = inspect.stack()  # stack_trace[0]为当前运行函数，stack_trace[1]为调用当前运行的函数

    # 函数基础信息参数
    local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 调用时间
    function_name = ''  # 函数名
    caller_path = ''  # 函数文件路径

    # 获取函数信息
    if mode.lower() == 'current':
        function_name = stack_trace[1].function
        caller_path = stack_trace[1].filename
    elif mode.lower() == 'last':
        if len(stack_trace) >= 3:
            function_name = stack_trace[2].function
            caller_path = stack_trace[2].filename

    if function_name and caller_path:
        return local_time, function_name, caller_path
    else:
        return None, None, None


def _get_subclasses(cls) -> list:
    """获取所有子类对象
    :return: 子类对象列表"""
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(_get_subclasses(subclass))
    return subclasses


"""----------调用函数----------"""


def print_function_info(mode: str = 'current'):
    """获取当前运行/上个运行的函数的信息
    :param mode: 'current' 或 'last'
    :return: 运行时间，函数名，函数文件路径
    """
    local_time, function_name, caller_path = _get_function_info(mode)
    print(local_time, function_name, caller_path)


def get_function_info(mode: str = 'current') -> Tuple[str, str, str]:
    """获取当前运行/上个运行的函数的信息
    :param mode: 'current' 或 'last'
    :return: 运行时间，函数名，函数文件路径
    """
    return _get_function_info(mode)


def get_subclasses(cls) -> list:
    """获取所有子类对象
    :return: 子类对象列表"""
    return _get_subclasses(cls)
