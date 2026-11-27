# lzytools_OCR

`lzytools_OCR` 是一个个人使用的轻量 Python OCR 库，提供统一的图片输入、本地 OCR 模型调用、文块后处理和结果导出接口。

## 设计思路

库的处理链路是：

1. 本地 OCR 引擎识别图片，输出若干文块：`{"text", "score", "box"}`
2. 后处理模块执行忽略区域与排版解析，为每个文块补充 `end` 结束符
3. 结果层按需返回文块字典或拼接后的纯文本

内置引擎：

- `rapid`：本地 RapidOCR，自动兼容新版 `rapidocr` 和旧版 `rapidocr_onnxruntime`

## 安装

```bash
python -m pip install -e .
```

安装本地 RapidOCR 引擎（二选一）：

```bash
python -m pip install -e ".[rapid]"
# 或旧版：
python -m pip install -e ".[rapid-legacy]"
```

## 快速开始

```python
from lzytools_OCR import OCR

ocr = OCR()  # 默认本地 RapidOCR，parser="multi_para"，limit_side_len=960

result = ocr.recognize("demo.png")
print(result.code)        # 100 成功，101 无文字
print(result.text)        # 按排版解析拼接后的全文
print(result.mean_score)  # 平均置信度

# 只取文本
text = ocr.recognize_text("demo.png")

# 直接把 OCR 实例当函数调用
text = ocr("demo.png")
```

## 常用参数

```python
from pathlib import Path
from lzytools_OCR import OCR

ocr = OCR(
    parser="single_line",       # 排版解析方案
    limit_side_len=2880,        # 图像最长边限制，0 表示不限制
    ignore_area=[               # 忽略区域，区域内部完整文块会被丢弃
        [[0, 0], [200, 60]],
    ],
)

result = ocr.recognize(Path("demo.png"))
result.save("demo.json")       # 也可保存为 demo.txt
```

支持的 `parser`：

| 方案 | 说明 |
| --- | --- |
| `none` | 不做处理，保留引擎返回的文块顺序 |
| `single_line` | 单栏，总是换行 |
| `single_none` | 单栏，不换行 |
| `single_para` | 单栏，按行间距近似自然段 |
| `single_code` | 单栏，尽量保留空格缩进 |
| `multi_line` | 多栏，总是换行 |
| `multi_none` | 多栏，不换行 |
| `multi_para` | 多栏，按行间距近似自然段 |

> 多栏方案使用基于列间距的轻量启发式实现。

## 输入类型

`recognize()` 支持：

- 图片路径：`str` / `pathlib.Path`
- 图片字节：`bytes` / `bytearray` / `memoryview`
- `PIL.Image.Image`
- `numpy.ndarray`（RGB 或灰度）

base64 图片建议使用专用方法：

```python
result = ocr.recognize_base64(base64_string)  # 兼容 data URI 前缀
```

批量识别：

```python
results = ocr.recognize_many(["a.png", "b.png"])
for item in results:
    print(item.text)
```

## 结果结构

`OCRResult` 主要属性：

| 属性 | 说明 |
| --- | --- |
| `code` | `100` 成功，`101` 无文字，其他值由引擎异常体现 |
| `blocks` | `TextBlock` 列表，每项含 `text`、`score`、`box`、`end` |
| `text` | 按 `end` 拼接后的全文 |
| `mean_score` | 平均置信度 |
| `elapsed` / `timestamp` | 耗时秒数 / 任务开始时间戳 |
| `raw` | 引擎原始返回，便于调试 |

字典输出：

```python
result.to_dict()          # data 为文块字典列表
result.to_dict("text")    # data 为纯文本
```

## 自定义本地引擎

任何实现 `recognize(image) -> (blocks, elapsed)` 的对象都可以作为本地引擎：

```python
from lzytools_OCR import OCR, BaseEngine

class MyEngine(BaseEngine):
    name = "my-engine"

    def recognize(self, image):
        return [
            {
                "text": "Hello",
                "score": 0.99,
                "box": [[0, 0], [50, 0], [50, 20], [0, 20]],
            }
        ], 0.01

ocr = OCR(engine=MyEngine(), parser="none")
print(ocr.recognize_text("demo.png"))
```

## 测试

```bash
python -m pip install -e .
python -m unittest discover -s tests -p "test_lzytools_OCR.py" -v
```
