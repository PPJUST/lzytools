import inspect
import time

"""----------逻辑函数----------"""


def _get_function_info(mode: str = 'current') -> tuple[str | None, str | None, str | None]:
    """获取当前运行/上个运行的函数的信息
    :param mode: 'current'（调用当前函数）或 'last'（调用者的函数）
    :return: (调用时间, 函数名, 函数文件路径)；模式无效或栈深度不足时返回 (None, None, None)
    """
    mode_key = mode.lower()
    if mode_key not in ('current', 'last'):
        return None, None, None

    # inspect.stack() 会遍历整个栈并读取源码上下文，直接访问帧对象更快
    frame = inspect.currentframe()
    target = None
    try:
        if frame is not None:
            target = frame.f_back
            if mode_key == 'last' and target is not None:
                target = target.f_back
        if target is None:
            return None, None, None
        return time.strftime('%Y-%m-%d %H:%M:%S'), target.f_code.co_name, target.f_code.co_filename
    finally:
        # 及时释放帧引用，避免与局部变量形成循环引用
        del frame, target


def _get_subclasses(cls: type) -> list[type]:
    """获取所有子类对象（深度优先，遍历顺序与递归实现一致）
    :return: 子类对象列表"""
    subclasses: list[type] = []
    stack = list(reversed(cls.__subclasses__()))
    while stack:
        subclass = stack.pop()
        subclasses.append(subclass)
        stack.extend(reversed(subclass.__subclasses__()))
    return subclasses


"""----------调用函数----------"""


def print_function_info(mode: str = 'current') -> None:
    """打印当前运行/上个运行的函数的信息
    :param mode: 'current' 或 'last'
    """
    print(*_get_function_info(mode))


def get_function_info(mode: str = 'current') -> tuple[str | None, str | None, str | None]:
    """获取当前运行/上个运行的函数的信息
    :param mode: 'current' 或 'last'
    :return: (调用时间, 函数名, 函数文件路径)
    """
    return _get_function_info(mode)


def get_subclasses(cls: type) -> list[type]:
    """获取所有子类对象
    :return: 子类对象列表"""
    return _get_subclasses(cls)
