import hashlib
from collections.abc import Callable as _Callable
from collections.abc import Iterable as _Iterable
from collections.abc import Iterator as _Iterator
from typing import Protocol as _Protocol

import xxhash

"""----------逻辑函数----------"""


class _Hasher(_Protocol):
    """hashlib 与 xxhash 哈希对象共用的最小接口。"""

    def update(self, data: bytes, /) -> None: ...

    def hexdigest(self) -> str: ...


_HasherFactory = _Callable[[], _Hasher]


def _iter_bytes_chunks(data: bytes, chunk_size: int) -> _Iterator[bytes]:
    """按指定大小切分字节流。"""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def _iter_file_chunks(file_path: str, chunk_size: int) -> _Iterator[bytes]:
    """按指定大小读取文件内容。"""
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            yield chunk


def _iter_files_chunks(file_paths: list[str], chunk_size: int) -> _Iterator[bytes]:
    """按指定大小依次读取多个文件的内容。"""
    for file_path in file_paths:
        yield from _iter_file_chunks(file_path, chunk_size)


def _hash_chunks(chunks: _Iterable[bytes], hasher: _Hasher) -> str:
    """用指定哈希对象累加所有数据块并返回十六进制摘要。"""
    for chunk in chunks:
        hasher.update(chunk)
    return hasher.hexdigest()


def _hash_bytes(data: bytes, chunk_size: int, hasher_factory: _HasherFactory) -> str:
    """按块计算字节流的哈希值。"""
    return _hash_chunks(_iter_bytes_chunks(data, chunk_size), hasher_factory())


def _hash_file(file_path: str, chunk_size: int, hasher_factory: _HasherFactory) -> str:
    """按块计算单个文件的哈希值。"""
    return _hash_chunks(_iter_file_chunks(file_path, chunk_size), hasher_factory())


def _hash_files(file_paths: list[str], block_size: int, hasher_factory: _HasherFactory) -> str:
    """按块计算多个文件拼接内容的哈希值。"""
    return _hash_chunks(_iter_files_chunks(file_paths, block_size), hasher_factory())


def _calc_xxhash_from_bytes(data: bytes) -> str:
    """从字节流计算xxHash"""
    return xxhash.xxh64(data).hexdigest()


def _calc_xxhash_from_file(file_path: str, block_size: int = 65536) -> str:
    """从文件计算xxHash"""
    return _hash_file(file_path, block_size, xxhash.xxh64)


def _calc_xxhash_from_files(file_paths: list[str], block_size: int = 65536) -> str:
    """从文件列表计算xxHash"""
    return _hash_files(file_paths, block_size, xxhash.xxh64)


def _calc_md5_from_file(file_path: str, chunk_size: int = 8192) -> str:
    """从文件计算MD5"""
    return _hash_file(file_path, chunk_size, hashlib.md5)


def _calc_md5_from_bytes(data: bytes, chunk_size: int = 8192) -> str:
    """从字节流计算MD5"""
    return _hash_bytes(data, chunk_size, hashlib.md5)


def _calc_sha256_from_file(file_path: str, chunk_size: int = 8192) -> str:
    """从文件计算SHA-256"""
    return _hash_file(file_path, chunk_size, hashlib.sha256)


def _calc_sha256_from_bytes(data: bytes, chunk_size: int = 8192) -> str:
    """从字节流计算SHA-256"""
    return _hash_bytes(data, chunk_size, hashlib.sha256)


"""----------调用函数----------"""


def calc_xxhash_from_bytes(data: bytes) -> str:
    """从字节流计算xxHash"""
    return _calc_xxhash_from_bytes(data)


def calc_xxhash_from_file(file_path: str, block_size: int = 65536) -> str:
    """从文件计算xxHash"""
    return _calc_xxhash_from_file(file_path, block_size)


def calc_xxhash_from_files(file_paths: list[str], block_size: int = 65536) -> str:
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
