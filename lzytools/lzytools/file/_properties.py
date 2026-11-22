import ctypes
import os

"""----------常量----------"""

_FILE_ATTRIBUTE_HIDDEN = 0x2
_INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF

if os.name == 'nt':
    _get_file_attributes_w = ctypes.windll.kernel32.GetFileAttributesW
    _get_file_attributes_w.argtypes = [ctypes.c_wchar_p]
    _get_file_attributes_w.restype = ctypes.c_uint32
else:
    _get_file_attributes_w = None

"""----------逻辑函数----------"""


def _is_file_hidden(path: str) -> bool:
    """文件是否隐藏
    :param path: 文件路径
    :return: 隐藏返回 True；文件不存在、无法访问或非 Windows 平台返回 False"""
    if _get_file_attributes_w is None:
        return False

    attrs = _get_file_attributes_w(os.fspath(path))
    if attrs == _INVALID_FILE_ATTRIBUTES:
        return False

    return bool(attrs & _FILE_ATTRIBUTE_HIDDEN)


"""----------调用函数----------"""


def is_hidden_file(path: str) -> bool:
    """文件是否隐藏
    :param path: 文件路径"""
    return _is_file_hidden(path)


def is_file_hidden(path: str) -> bool:
    """文件是否隐藏
    :param path: 文件路径"""
    return _is_file_hidden(path)
