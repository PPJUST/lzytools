import os
import re
import string

"""----------常量----------"""

# Windows 文件名中不允许出现的字符
_ILLEGAL_CHARACTERS = frozenset('\\/:*?"<>|')
# Windows 保留设备名（不区分大小写，可带任意扩展名，如 CON.txt）
_RESERVED_NAMES = frozenset(
    {'CON', 'PRN', 'AUX', 'NUL'}
    | {f'COM{i}' for i in range(1, 10)}
    | {f'LPT{i}' for i in range(1, 10)}
)
# 文件名单个组件的最大长度（UTF-16 码元数）
_MAX_FILENAME_LENGTH = 255
# 需要剔除的前导字符：'.' 与各类空白
_LEADING_TRIM_CHARS = '.' + string.whitespace
# 常见的数字后缀：(1)、（1）
_DIGITAL_SUFFIX_PATTERNS = (
    re.compile(r'\s*\(\d+\)\s*$'),
    re.compile(r'\s*（\d+）\s*$'),
)

"""----------逻辑函数----------"""


def _get_existing_filenames(check_dirpath: str) -> set[str]:
    """获取目录中已存在的文件/文件夹名（统一为小写），用于大小写不敏感的重复检查
    :param check_dirpath: 需要检查的文件夹路径
    :return: 小写文件名集合"""
    return {name.lower() for name in os.listdir(check_dirpath)}


def _is_dup_filename_in_names(filename: str, existing_filenames: set[str]) -> bool:
    """在已有名称集合中检查文件名是否重复（大小写不敏感）"""
    return filename.lower() in existing_filenames


def _is_dup_filename(filename: str, check_dirpath: str) -> bool:
    """检查文件名在指定路径中是否已存在（检查重复文件名，大小写不敏感）
    :param filename: 文件名（包含文件扩展名）
    :param check_dirpath: 需要检查的文件夹路径
    :return: 已存在返回 True"""
    return _is_dup_filename_in_names(filename, _get_existing_filenames(check_dirpath))


def _is_legal_filename(filename: str) -> bool:
    """检查文件名是否符合 Windows 的文件命名规范
    :param filename: 文件名（可包含扩展名）
    :return: 合法返回 True"""
    if not filename:
        return False
    # 不能命名为 "." 或 ".."，也不能以 "." 开头
    if filename.startswith('.'):
        return False
    # 不能包含非法字符或控制字符（0-31）
    if any(char in _ILLEGAL_CHARACTERS or ord(char) < 32 for char in filename):
        return False
    # Windows 会自动去除结尾的点和空格，这类名称视为非法
    if filename.endswith(('.', ' ')):
        return False
    # 保留设备名不能作为文件名（可带扩展名，如 CON.txt）
    if filename.split('.', 1)[0].upper() in _RESERVED_NAMES:
        return False
    # 单个文件名组件最长 255 个 UTF-16 码元
    if len(filename.encode('utf-16-le', errors='surrogatepass')) // 2 > _MAX_FILENAME_LENGTH:
        return False
    return True


def _replace_illegal_character_in_filename(filename: str, replace_str: str = '') -> str:
    """替换文件名中的非法字符，并剔除开头无效的 '.' 与空白
    :param filename: 文件名
    :param replace_str: 用于替换的新字符（不能包含非法字符）
    :return: 替换后的文件名
    :raises ValueError: 替换字符非法，或替换结果为空"""
    if any(char in _ILLEGAL_CHARACTERS for char in replace_str):
        raise ValueError(f'替换字符非法：{replace_str}')

    # 一次遍历完成所有非法字符的替换
    translation_table = {ord(char): replace_str for char in _ILLEGAL_CHARACTERS}
    filename = filename.translate(translation_table).lstrip(_LEADING_TRIM_CHARS).strip()

    if not filename:
        raise ValueError('结果文件名非法：空文件名')
    return filename


def _remove_suffix(filetitle: str, suffix: str | None = None) -> str:
    """移除文件名末尾的数字后缀（如 (1)、（1））及指定的自定义后缀，可连续移除多个
    :param filetitle: 文件名（不包含文件扩展名）
    :param suffix: 指定后缀（按字面匹配，支持正则特殊字符）
    :return: 移除后缀后的文件名"""
    patterns = _DIGITAL_SUFFIX_PATTERNS
    if suffix:
        patterns = (*patterns, re.compile(rf'\s*{re.escape(suffix)}\s*\d+\s*$'))

    while True:
        removed = filetitle
        for pattern in patterns:
            removed = pattern.sub('', removed)
        if removed == filetitle:
            break
        filetitle = removed

    return filetitle.strip()


def _normalize_extension(filename_extension: str | None) -> str:
    """标准化文件扩展名（去除首尾空白与点号）；为空时按文件夹名处理"""
    if not filename_extension:
        return ''
    return filename_extension.strip().strip('.')


def _combine_filename(filetitle: str, extension: str) -> str:
    """组合文件名与扩展名；扩展名为空时视为文件夹名"""
    return f'{filetitle}.{extension}' if extension else filetitle


def _create_nodup_filename_standard_digital_suffix(filetitle: str, check_dirpath: str,
                                                   filename_extension: str | None = None) -> str:
    """生成在目标文件夹中不重复的文件名（统一使用 (1) 形式的数字后缀）
    :param filetitle: 文件名（不包含文件扩展名）
    :param check_dirpath: 目标文件夹路径
    :param filename_extension: 文件扩展名（检查文件名时必须提供）
    :return: 不重复的文件名（包含文件扩展名）
    :raises ValueError: filetitle 为空"""
    filetitle = _remove_suffix(filetitle)
    if not filetitle:
        raise ValueError('filetitle 不能为空')

    extension = _normalize_extension(filename_extension)
    existing_filenames = _get_existing_filenames(check_dirpath)

    filename = _combine_filename(filetitle, extension)
    count = 1
    while _is_dup_filename_in_names(filename, existing_filenames):
        filename = _combine_filename(f'{filetitle} ({count})', extension)
        count += 1

    return filename


def _create_nodup_filename_custom_suffix(filetitle: str, check_dirpath: str, add_suffix: str,
                                         filename_extension: str | None = None) -> str:
    """生成在目标文件夹中不重复的文件名（重复时累加自定义后缀）
    :param filetitle: 文件名（不包含文件扩展名）
    :param check_dirpath: 目标文件夹路径
    :param add_suffix: 重复时累加的后缀，不能为空或包含非法字符
    :param filename_extension: 文件扩展名（检查文件名时必须提供）
    :return: 不重复的文件名（包含文件扩展名）
    :raises ValueError: filetitle 为空，或 add_suffix 为空/包含非法字符"""
    if not add_suffix:
        raise ValueError('add_suffix 不能为空')
    if any(char in _ILLEGAL_CHARACTERS for char in add_suffix):
        raise ValueError(f'add_suffix 包含非法字符：{add_suffix}')

    filetitle = _remove_suffix(filetitle, add_suffix)
    if not filetitle:
        raise ValueError('filetitle 不能为空')

    extension = _normalize_extension(filename_extension)
    existing_filenames = _get_existing_filenames(check_dirpath)

    filename = _combine_filename(filetitle, extension)
    count = 1
    while _is_dup_filename_in_names(filename, existing_filenames):
        filename = _combine_filename(f'{filetitle}{add_suffix * count}', extension)
        count += 1

    return filename


"""----------调用函数----------"""


def is_dup_filename(filename: str, check_dirpath: str) -> bool:
    """检查文件名在指定路径中是否已存在（检查重复文件名，大小写不敏感）
    :param filename: 文件名（包含文件扩展名）
    :param check_dirpath: 需要检查的文件夹路径
    :return: 已存在返回 True"""
    return _is_dup_filename(filename, check_dirpath)


def is_legal_filename(filename: str) -> bool:
    """检查文件名是否符合 Windows 的文件命名规范
    :param filename: 文件名（可包含扩展名）
    :return: 合法返回 True"""
    return _is_legal_filename(filename)


def replace_illegal_filename(filename: str, replace_str: str = '') -> str:
    """替换文件名中的非法字符，并剔除开头无效的 '.' 与空白
    :param filename: 文件名
    :param replace_str: 用于替换的新字符（不能包含非法字符）
    :return: 替换后的文件名"""
    return _replace_illegal_character_in_filename(filename, replace_str)


def replace_illegal_character_in_filename(filename: str, replace_str: str = '') -> str:
    """替换文件名中的非法字符，并剔除开头无效的 '.' 与空白
    :param filename: 文件名
    :param replace_str: 用于替换的新字符（不能包含非法字符）
    :return: 替换后的文件名"""
    return _replace_illegal_character_in_filename(filename, replace_str)


def remove_suffix(filetitle: str, suffix: str | None = None) -> str:
    """移除文件名末尾的数字后缀（如 (1)、（1））及指定的自定义后缀，可连续移除多个
    :param filetitle: 文件名（不包含文件扩展名）
    :param suffix: 指定后缀（按字面匹配，支持正则特殊字符）
    :return: 移除后缀后的文件名"""
    return _remove_suffix(filetitle, suffix)


def create_nodup_filename_standard_digital_suffix(filetitle: str, check_dirpath: str,
                                                  filename_extension: str | None = None) -> str:
    """生成在目标文件夹中不重复的文件名（统一使用 (1) 形式的数字后缀）
    :param filetitle: 文件名（不包含文件扩展名）
    :param check_dirpath: 目标文件夹路径
    :param filename_extension: 文件扩展名（检查文件名时必须提供）
    :return: 不重复的文件名（包含文件扩展名）"""
    return _create_nodup_filename_standard_digital_suffix(filetitle, check_dirpath, filename_extension)


def create_nodup_filename_custom_suffix(filetitle: str, check_dirpath: str, add_suffix: str,
                                        filename_extension: str | None = None) -> str:
    """生成在目标文件夹中不重复的文件名（重复时累加自定义后缀）
    :param filetitle: 文件名（不包含文件扩展名）
    :param check_dirpath: 目标文件夹路径
    :param add_suffix: 重复时累加的后缀，不能为空或包含非法字符
    :param filename_extension: 文件扩展名（检查文件名时必须提供）
    :return: 不重复的文件名（包含文件扩展名）"""
    return _create_nodup_filename_custom_suffix(filetitle, check_dirpath, add_suffix, filename_extension)
