import inspect

from ._time import get_current_time


def print_function_info(mode: str = 'current'):
    """
    打印当前/上一个函数的信息
    :param mode: str，'current' 或 'last'
    """

    def _print_function_info(_stack_trace: inspect.FrameInfo):
        """打印函数信息"""
        # 打印当前时间
        print('当前时间:', get_current_time('%H:%M:%S'))

        # 获取函数名
        caller_function_name = _stack_trace.function
        print("调用函数名:", caller_function_name)

        # 获取文件路径
        caller_file_path = _stack_trace.filename
        print("调用文件路径:", caller_file_path)

    # return  # 不需要print信息时取消该备注

    # 获取当前帧对象
    # frame = inspect.currentframe()
    # 获取调用栈
    stack_trace = inspect.stack()  # stack_trace[0]为本函数，stack_trace[1]为调用本函数的函数
    if mode == 'current':  # 打印当前函数信息
        _print_function_info(stack_trace[1])
    elif mode == 'last':  # 打印上一个函数信息
        if len(stack_trace) >= 3:
            _print_function_info(stack_trace[2])


def get_subclasses(cls):
    """获取所有子类对象"""
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_subclasses(subclass))
    return subclasses
