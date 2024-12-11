import random
import string

import unicodedata


def create_random_string(length: int = 16, lowercase: bool = True, uppercase: bool = True, digits: bool = True) -> str:
    """生成一个指定长度的随机字符串
    :param length: int，字符串长度
    :param lowercase: bool，小写英文字母
    :param uppercase: bool，大写英文字母
    :param digits: bool，数字
    :return: str，随机字符串"""
    characters = ''
    if lowercase:
        characters += string.ascii_lowercase
    if uppercase:
        characters += string.ascii_uppercase
    if digits:
        characters += string.digits
    if not characters:
        raise Exception('没有选择字符')

    random_string = ''.join(random.choices(characters, k=length))

    return random_string


def to_half_width_character(text: str):
    """将传入字符串转换为半角字符"""
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


def to_full_width_character(text: str):
    """将传入字符串转换为全角字符"""
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
