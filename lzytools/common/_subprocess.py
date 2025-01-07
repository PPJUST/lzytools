import subprocess


def flush_dns():
    """刷新DNS缓存"""
    subprocess.run(['ipconfig', '/flushdns'], shell=True)
