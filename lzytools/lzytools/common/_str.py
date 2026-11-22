import random
import string
from functools import lru_cache

import unicodedata

"""----------常量----------"""

# NFKC 会把全角 ASCII 规范化为半角，转换全角时再用映射表转回去。
# 空格单独映射到全角空格 U+3000，而不是按偏移得到的未分配码位 U+FF00。
_FULL_WIDTH_TABLE = str.maketrans(
    {code: chr(code + 0xFEE0) for code in range(0x21, 0x7F)} | {0x20: chr(0x3000)}
)
_HALF_WIDTH_TABLE = str.maketrans({code: chr(code - 0xFEE0) for code in range(0xFF01, 0xFF5F)})

"""----------逻辑函数----------"""


@lru_cache(maxsize=16)
def _get_random_characters(lowercase: bool, uppercase: bool, digits: bool, special_characters: bool) -> str:
    """按开关生成并缓存随机字符池，避免每次调用都重复拼接字符串"""
    characters = ''
    if lowercase:
        characters += string.ascii_lowercase
    if uppercase:
        characters += string.ascii_uppercase
    if digits:
        characters += string.digits
    if special_characters:
        characters += string.punctuation
    return characters


def _create_random_string(length: int = 16, lowercase: bool = True, uppercase: bool = True,
                          digits: bool = True, special_characters: bool = True) -> str:
    """生成一个指定长度的随机文本
    :param length: 文本长度
    :param lowercase: 是否包含小写英文字母
    :param uppercase: 是否包含大写英文字母
    :param digits: 是否包含数字
    :param special_characters: 是否包含特殊符号
    :return: 生成的文本"""
    if length < 0:
        raise ValueError('length 不能为负数')
    characters = _get_random_characters(lowercase, uppercase, digits, special_characters)
    if not characters:
        return ''
    return ''.join(random.choices(characters, k=length))


def _convert_character_to_half_width(text: str) -> str:
    """将传入文本中的字符转换为半角字符"""
    return unicodedata.normalize('NFKC', text).translate(_HALF_WIDTH_TABLE)


def _convert_character_to_full_width(text: str) -> str:
    """将传入文本中的字符转换为全角字符"""
    return unicodedata.normalize('NFKC', text).translate(_FULL_WIDTH_TABLE)


"""----------调用函数----------"""


def create_random_string(length: int = 16, lowercase: bool = True, uppercase: bool = True,
                         digits: bool = True, special_characters: bool = False) -> str:
    """生成一个指定长度的随机文本
    :param length: 文本长度
    :param lowercase: 是否包含小写英文字母
    :param uppercase: 是否包含大写英文字母
    :param digits: 是否包含数字
    :param special_characters: 是否包含特殊符号
    :return: 生成的文本"""
    return _create_random_string(length, lowercase, uppercase, digits, special_characters)


def to_half_width_character(text: str) -> str:
    """将传入文本中的字符转换为半角字符"""
    return _convert_character_to_half_width(text)


def convert_character_to_half_width(text: str) -> str:
    """将传入文本中的字符转换为半角字符"""
    return _convert_character_to_half_width(text)


def to_full_width_character(text: str) -> str:
    """将传入文本中的字符转换为全角字符"""
    return _convert_character_to_full_width(text)


def convert_character_to_full_width(text: str) -> str:
    """将传入文本中的字符转换为全角字符"""
    return _convert_character_to_full_width(text)
