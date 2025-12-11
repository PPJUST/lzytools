import subprocess

"""----------逻辑函数----------"""


def _flush_dns():
    """刷新DNS缓存"""
    subprocess.run(['ipconfig', '/flushdns'], shell=True)


"""----------调用函数----------"""


def flush_dns():
    """刷新DNS缓存"""
    _flush_dns()
