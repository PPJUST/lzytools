import ctypes

"""----------逻辑函数----------"""


def _is_file_hidden(path: str) -> bool:
    """文件是否隐藏
    :param path: 文件路径"""
    get_file_attributes_w = ctypes.windll.kernel32.GetFileAttributesW
    file_attribute_hidden = 0x2
    invalid_file_attributes = -1

    def is_hidden(_file):
        # 获取文件属性
        attrs = get_file_attributes_w(_file)
        if attrs == invalid_file_attributes:
            # 文件不存在或无法访问
            return False

        return attrs & file_attribute_hidden == file_attribute_hidden

    return is_hidden(path)


"""----------调用函数----------"""


def is_hidden_file(path: str) -> bool:
    """文件是否隐藏
    :param path: 文件路径"""
    return _is_file_hidden(path)


def is_file_hidden(path: str) -> bool:
    """文件是否隐藏
    :param path: 文件路径"""
    return _is_file_hidden(path)
