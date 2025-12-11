import setuptools

setuptools.setup(
    name="lzytools_Qt",  # 项目名称
    version="0.0.1",  # 版本号
    author="PPJUST",  # 作者
    description="Python自用包-Qt相关方法",  # 描述
    long_description='Python自用包-Qt相关方法',  # 长描述
    long_description_content_type="text/markdown",  # 长描述语法 markdown
    url="https://github.com/PPJUST/lzytools",  # 项目地址
    packages=setuptools.find_packages(),
    python_requires='>=3',  # Python版本限制
)
