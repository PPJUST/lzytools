from ._check import *
from ._convert import *
from ._info import *
from ._read import *
from ._save import *
from ._similar import *

ImageFile.LOAD_TRUNCATED_IMAGES = True  # 允许加载截断的图像 防止报错OSError: image file is truncated
