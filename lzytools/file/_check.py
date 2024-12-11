import ctypes
import os


def is_hidden_file(path: str):
    """路径对应的文件是否隐藏
    :param path: str，需要删除的路径"""
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


def is_dup_filename(filename: str, check_dirpath: str) -> bool:
    """检查文件名在指定路径中是否已存在（检查重复文件名）
    :param filename: str，文件名（包含文件扩展名）
    :param check_dirpath: str，需要检查的文件夹路径
    :return: bool，是否在指定文件夹中存在重复文件名
    """
    filenames_in_dirpath = [i.lower() for i in os.listdir(check_dirpath)]
    return filename.lower() in filenames_in_dirpath
