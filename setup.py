from setuptools import setup, find_packages

"""
打包指令: python setup.py sdist
twine upload dist/*
"""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pycloudmusic163",
    version="0.1.1",
    description="使用Python快速调用网易云音乐api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    url="https://github.com/FengLiuFeseliud/pycloudmusic163",
    author="FengLiuFeseliud",
    author_email="17351198406@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests"],
    python_requires='>=3.7'
)