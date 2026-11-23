"""lzytools_archive 的安装配置。"""

import setuptools

_ = setuptools.setup(
    name="lzytools_archive",  # 项目名称
    version="0.1.0",  # 版本号
    author="PPJUST",  # 作者
    description="Python 自用包 - 压缩文件相关方法",  # 描述
    long_description="Python 自用包，提供压缩文件检测、读取与分卷处理方法。",  # 长描述
    long_description_content_type="text/markdown",  # 长描述语法 markdown
    url="https://github.com/PPJUST/lzytools",  # 项目地址
    packages=setuptools.find_packages(),
    python_requires=">=3.10",  # 代码使用了 3.10+ 的联合类型与泛型语法
)
