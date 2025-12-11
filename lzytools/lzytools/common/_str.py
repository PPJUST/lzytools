import random
import string

import unicodedata

"""----------逻辑函数----------"""


def _create_random_string(length: int = 16, lowercase: bool = True, uppercase: bool = True,
                          digits: bool = True, special_characters: bool = True) -> str:
    """生成一个指定长度的随机文本
    :param length: 文本长度
    :param lowercase: 是否包含小写英文字母
    :param uppercase: 是否包含大写英文字母
    :param digits: 是否包含数字
    :param special_characters: 是否包含特殊符号
    :return: 生成的文本"""
    characters = ''
    if lowercase:
        characters += string.ascii_lowercase
    if uppercase:
        characters += string.ascii_uppercase
    if digits:
        characters += string.digits
    if special_characters:
        characters += string.punctuation
    if not characters:
        return ''

    random_string = ''.join(random.choices(characters, k=length))

    return random_string


def _convert_character_to_half_width(text: str) -> str:
    """将传入文本中的字符转换为半角字符"""
    # 先将字符串进行Unicode规范化为NFKC格式（兼容性组合用序列）
    normalized_string = unicodedata.normalize('NFKC', text)

    # 对于ASCII范围内的全角字符，将其替换为对应的半角字符
    half_width_string = []
    for char in normalized_string:
        code_point = ord(char)
        if 0xFF01 <= code_point <= 0xFF5E:
            half_width_string.append(chr(code_point - 0xFEE0))
        else:
            half_width_string.append(char)

    return ''.join(half_width_string)


def _convert_character_to_full_width(text: str) -> str:
    """将传入文本中的字符转换为全角字符"""
    # 将字符串进行Unicode规范化为NFKC格式（兼容性组合用序列）
    normalized_string = unicodedata.normalize('NFKC', text)

    # 对于ASCII范围内的字符，将其替换为对应的全角字符
    full_width_string = []
    for char in normalized_string:
        code_point = ord(char)
        if 0x0020 <= code_point <= 0x007E:
            full_width_string.append(chr(code_point + 0xFF00 - 0x0020))
        else:
            full_width_string.append(char)

    return ''.join(full_width_string)


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
