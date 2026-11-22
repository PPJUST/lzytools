import ctypes
import sys

"""----------逻辑函数----------"""

# use_last_error=True：把 LastError 存到当前线程，调用后立刻用 get_last_error() 读取，
# 避免中间其他 ctypes 调用覆盖系统全局的 LastError
if sys.platform == 'win32':
    _kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    _create_mutex_w = _kernel32.CreateMutexW
    # HANDLE 是指针大小（64 位系统上为 8 字节），必须显式声明 restype，否则句柄会被截断成 32 位
    _create_mutex_w.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_wchar_p)
    _create_mutex_w.restype = ctypes.c_void_p
    _close_handle = _kernel32.CloseHandle
    _close_handle.argtypes = (ctypes.c_void_p,)
    _close_handle.restype = ctypes.c_bool
else:
    _create_mutex_w = None
    _close_handle = None

_ERROR_ALREADY_EXISTS = 183  # winerror.h: ERROR_ALREADY_EXISTS

# 互斥体句柄需要保持打开才持有锁：首次创建时保存，显式释放或进程退出时由系统回收
_held_mutexes: dict[str, int] = {}


def _check_mutex(mutex_name: str) -> bool:
    """使用互斥体检查是否已经打开了一个程序实例
    :param mutex_name: str，互斥体名称，建议使用程序名称
    :return: 是否已有实例在运行；非 Windows 平台返回 False
    """
    if _create_mutex_w is None or _close_handle is None:
        return False

    mutex = _create_mutex_w(None, False, mutex_name)
    # 必须在下一次 ctypes 调用前读取，否则 LastError 可能被覆盖
    already_exists = ctypes.get_last_error() == _ERROR_ALREADY_EXISTS

    if already_exists:
        # 已有实例持有该互斥体：关闭本次得到的重复句柄即可，不会销毁对方的互斥体
        _close_handle(mutex)
        return True

    if mutex:
        _held_mutexes[mutex_name] = mutex  # 保留句柄，本进程持续持有该互斥体
    return False


def _release_mutex(mutex_name: str) -> None:
    """释放本进程持有的互斥体
    :param mutex_name: str，互斥体名称
    """
    mutex = _held_mutexes.pop(mutex_name, None)
    if mutex is not None and _close_handle is not None:
        _close_handle(mutex)


"""----------调用函数----------"""


def check_mutex(mutex_name: str) -> bool:
    """使用互斥体检查是否已经打开了一个程序实例
    :param mutex_name: str，互斥体名称，建议使用程序名称
    :return: 是否已有实例在运行；非 Windows 平台返回 False
    """
    return _check_mutex(mutex_name)


def release_mutex(mutex_name: str) -> None:
    """释放本进程持有的互斥体
    :param mutex_name: str，互斥体名称
    """
    _release_mutex(mutex_name)
