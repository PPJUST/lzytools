import setuptools

setuptools.setup(
    name="lzytools",  # 项目名称
    version="0.0.39",  # 版本号
    author="PPJUST",  # 作者
    description="Python自用包",  # 描述
    long_description='Python自用包',  # 长描述
    long_description_content_type="text/markdown",  # 长描述语法 markdown
    url="https://github.com/PPJUST/lzytools",  # 项目地址
    packages=setuptools.find_packages(),
    python_requires='>=3',  # Python版本限制
    # setup_requires=["filetype",
    #                   "ImageHash",
    #                   "numpy<2.0.0",
    #                   "opencv_python",
    #                   "Pillow",
    #                   "pynput",
    #                   "PySide6",
    #                   "pywin32",
    #                   "rarfile",
    #                   "Send2Trash"],
)
