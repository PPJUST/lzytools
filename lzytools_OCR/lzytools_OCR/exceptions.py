"""lzytools_OCR 的异常类型。"""


class LzytoolsOcrError(Exception):
    """库的基础异常。"""


class ConfigurationError(LzytoolsOcrError, ValueError):
    """配置参数不合法。"""


class EngineError(LzytoolsOcrError, RuntimeError):
    """OCR 引擎初始化或识别失败。"""


class UnsupportedSourceError(LzytoolsOcrError, TypeError):
    """输入不是受支持的图片来源。"""
