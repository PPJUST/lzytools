# 网络临时文本
# 网站为 https://textdb.online/


import requests

"""----------逻辑函数----------"""


def _set_key():
    """设置标识"""


def _get_key():
    """获取标识"""


def _get_link():
    """获取链接"""


def _read(key: str) -> str:
    """读取"""
    url = f"https://textdb.online/{key}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    text = response.text

    return text


def _update(key: str, value: str):
    """更新"""
    url = f"https://textdb.online/update/?key={key}&value={value}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }

    requests.post(url, headers=headers)


def _delete(key: str):
    """删除"""
    _update(key=key, value="")


"""----------调用函数----------"""


def read(key: str) -> str:
    """读取"""
    return _read(key)


def update(key: str, value: str):
    """更新"""
    _update(key, value)


def delete(key: str):
    """删除"""
    _delete(key)
