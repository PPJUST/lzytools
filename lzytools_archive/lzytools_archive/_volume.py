import os
import re

"""----------常量----------"""

# 分卷规则表：(预编译正则, 首卷名后缀)
#   后缀为空串   -> 首个分卷就是原文件名（test.zip）
#   后缀含 {n}   -> 该处填入补零后的分卷序号（RAR 系列）
#   其余         -> 直接拼在文件标题（group 1）之后
# 统一使用 fullmatch，因此正则中不再需要 ^ / $ 锚点
_VOLUME_RULES: tuple[tuple[re.Pattern[str], str], ...] = (
    # test.7z.001 / test.7z.002 / test.7z.003
    (re.compile(r'(.+)\.7z\.\d+', re.I), '.7z.001'),
    # test.part1.rar / test.part2.rar / test.part3.rar
    (re.compile(r'(.+)\.part(\d+)\.rar', re.I), '.part{n}.rar'),
    # test.part1.exe / test.part2.rar / test.part3.rar（SFX 自解压分卷）
    (re.compile(r'(.+)\.part(\d+)\.exe', re.I), '.part{n}.exe'),
    # test.part1 / test.part2 / test.part3（无后缀也能解压）
    (re.compile(r'(.+)\.part(\d+)', re.I), '.part{n}'),
    # test.zip（zip 首个分卷通常就是 .zip，直接视为分卷文件）
    (re.compile(r'(.+)\.zip', re.I), ''),
    # test.zip / test.z01 / test.z02
    (re.compile(r'(.+)\.z\d+', re.I), '.zip'),
    # test.zip.001 / test.zip.002 / test.zip.003
    (re.compile(r'(.+)\.zip\.\d+', re.I), '.zip.001'),
    # test.bz2.001 / test.bz2.002 / test.bz2.003
    (re.compile(r'(.+)\.bz2\.\d+', re.I), '.bz2.001'),
    # test.gz.001 / test.gz.002 / test.gz.003
    (re.compile(r'(.+)\.gz\.\d+', re.I), '.gz.001'),
    # test.tar.001 / test.tar.002 / test.tar.003
    (re.compile(r'(.+)\.tar\.\d+', re.I), '.tar.001'),
    # test.wim.001 / test.wim.002 / test.wim.003
    (re.compile(r'(.+)\.wim\.\d+', re.I), '.wim.001'),
    # test.xz.001 / test.xz.002 / test.xz.003
    (re.compile(r'(.+)\.xz\.\d+', re.I), '.xz.001'),
)


def _match_volume(filename: str) -> tuple[re.Match[str], str] | None:
    """匹配分卷规则，返回 (match, suffix)；未匹配返回 None"""
    if not filename:
        return None
    for pattern, suffix in _VOLUME_RULES:
        match = pattern.fullmatch(filename)
        if match:
            return match, suffix
    return None


"""----------逻辑函数----------"""


def _is_volume_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为分卷压缩文件
    :param filename: 文件名（包含文件扩展名）"""
    return _match_volume(filename) is not None


def _guess_first_volume_archive_filename(filename: str) -> str | None:
    """根据传入的文件名，生成分卷压缩文件的首个分卷包文件名
    :param filename: 文件名（包含文件扩展名）
    :return: 生成的首个分卷包文件名，未生成时返回 None"""
    matched = _match_volume(filename)
    if matched is None:
        return None

    match, suffix = matched
    if not suffix:
        return match.group(0)
    if '{n}' in suffix:
        suffix = suffix.replace('{n}', '1'.zfill(len(match.group(2))))
    return match.group(1) + suffix


def _get_filetitle(filename: str) -> str:
    """剔除文件名中的压缩文件扩展名
    :param filename: 文件名（包含文件扩展名）
    :return: 压缩文件扩展名的文件标题"""
    matched = _match_volume(filename)
    if matched is not None:
        return matched[0].group(1)
    return os.path.basename(filename)


"""----------调用函数----------"""


def is_volume_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为分卷压缩文件
    :param filename: 文件名（包含文件扩展名）"""
    return _is_volume_archive_by_filename(filename)


def guess_first_volume_archive_filename(filename: str) -> str | None:
    """根据传入的文件名，生成分卷压缩文件的首个分卷包文件名
    :param filename: 文件名（包含文件扩展名）
    :return: 生成的首个分卷包文件名，未生成时返回 None"""
    return _guess_first_volume_archive_filename(filename)


def get_filetitle(filename: str) -> str:
    """剔除文件名中的压缩文件扩展名
    :param filename: 文件名（包含文件扩展名）
    :return: 压缩文件扩展名的文件标题"""
    return _get_filetitle(filename)
