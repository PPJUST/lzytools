import hashlib

import xxhash

"""----------逻辑函数----------"""


def _calc_xxhash_from_bytes(data: bytes) -> str:
    """从字节流计算xxHash"""
    hasher = xxhash.xxh64()
    hasher.update(data)
    return hasher.hexdigest()


def _calc_xxhash_from_file(file_path: str, block_size: int = 65536) -> str:
    """从文件计算xxHash"""
    hasher = xxhash.xxh64()
    with open(file_path, 'rb') as f:
        while chunk := f.read(block_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def _calc_xxhash_from_files(file_paths: list, block_size: int = 65536) -> str:
    """从文件列表计算xxHash"""
    hasher = xxhash.xxh64()
    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            while chunk := f.read(block_size):
                hasher.update(chunk)
    return hasher.hexdigest()


def _calc_md5_from_file(file_path: str, chunk_size: int = 8192) -> str:
    """从文件计算MD5"""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            md5.update(chunk)
    return md5.hexdigest()


def _calc_md5_from_bytes(data: bytes, chunk_size: int = 8192) -> str:
    """从字节流计算MD5"""
    md5 = hashlib.md5()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        md5.update(chunk)
    return md5.hexdigest()


def _calc_sha256_from_file(file_path: str, chunk_size: int = 8192) -> str:
    """从文件计算SHA-256"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _calc_sha256_from_bytes(data: bytes, chunk_size: int = 8192) -> str:
    """从字节流计算SHA-256"""
    sha256 = hashlib.sha256()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        sha256.update(chunk)
    return sha256.hexdigest()


"""----------调用函数----------"""


def calc_xxhash_from_bytes(data: bytes) -> str:
    """从字节流计算xxHash"""
    return _calc_xxhash_from_bytes(data)


def calc_xxhash_from_file(file_path: str, block_size: int = 65536) -> str:
    """从文件计算xxHash"""
    return _calc_xxhash_from_file(file_path, block_size)


def calc_xxhash_from_files(file_paths: list, block_size: int = 65536) -> str:
    """从文件列表计算xxHash"""
    return _calc_xxhash_from_files(file_paths, block_size)


def calc_md5_from_file(file_path: str, chunk_size: int = 8192) -> str:
    """从文件计算MD5"""
    return _calc_md5_from_file(file_path, chunk_size)


def calc_md5_from_bytes(data: bytes, chunk_size: int = 8192) -> str:
    """从字节流计算MD5"""
    return _calc_md5_from_bytes(data, chunk_size)


def calc_sha256_from_file(file_path: str, chunk_size: int = 8192) -> str:
    """从文件计算SHA-256"""
    return _calc_sha256_from_file(file_path, chunk_size)


def calc_sha256_from_bytes(data: bytes, chunk_size: int = 8192) -> str:
    """从字节流计算SHA-256"""
    return _calc_sha256_from_bytes(data, chunk_size)
