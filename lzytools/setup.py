"""lzytools 的安装配置。"""

import setuptools

_ = setuptools.setup(
    name="lzytools",  # 项目名称
    version="0.2.1",  # 版本号
    author="PPJUST",  # 作者
    description="Python 自用工具包",  # 描述
    long_description="Python 自用工具包，提供文件、时间与常用通用方法。",  # 长描述
    long_description_content_type="text/markdown",  # 长描述语法 markdown
    url="https://github.com/PPJUST/lzytools",  # 项目地址
    packages=setuptools.find_packages(),
    python_requires=">=3.10",  # 代码使用了 3.10+ 的联合类型与泛型语法
)
