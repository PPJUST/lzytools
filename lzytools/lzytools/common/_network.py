import subprocess

"""----------逻辑函数----------"""


def _flush_dns() -> bool:
    """刷新 DNS 缓存（仅 Windows）
    :return: 是否刷新成功；命令不可用（如非 Windows）时返回 False
    """
    # 直接调用 ipconfig，不使用 shell=True：少启动一层 cmd，也避免命令注入风险
    # 输出重定向到 DEVNULL，避免库函数污染调用方控制台，同时免去文本解码开销
    try:
        result = subprocess.run(
            ['ipconfig', '/flushdns'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return False
    return result.returncode == 0


"""----------调用函数----------"""


def flush_dns() -> bool:
    """刷新 DNS 缓存（仅 Windows）
    :return: 是否刷新成功；命令不可用（如非 Windows）时返回 False
    """
    return _flush_dns()
