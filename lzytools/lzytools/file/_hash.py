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
