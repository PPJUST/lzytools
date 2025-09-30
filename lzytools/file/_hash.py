import xxhash


def calc_xxhash_from_bytes(data: bytes) -> str:
    """从字节流计算xxHash"""
    hasher = xxhash.xxh64()
    hasher.update(data)
    return hasher.hexdigest()


def calc_xxhash_from_file(file_path: str, block_size: int = 65536) -> str:
    """从文件计算xxHash"""
    hasher = xxhash.xxh64()
    with open(file_path, 'rb') as f:
        while chunk := f.read(block_size):
            hasher.update(chunk)
    return hasher.hexdigest()
