import ctypes


def check_mutex(mutex_name: str):
    """使用互斥体检查是否已经打开了一个程序实例
    :param mutex_name: str，互斥体名称，建议使用程序名称"""
    # 创建互斥体
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    # 如果创建时报错，则说明已经创建过该互斥体，即已经有一个程序在运行了
    if ctypes.windll.kernel32.GetLastError() == 183:
        ctypes.windll.kernel32.CloseHandle(mutex)
        return True
    return False
