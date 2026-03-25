"""
Pomodoro Timer - Setup Script
用于打包和安装
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pomodoro-timer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个简单实用的命令行番茄钟工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/pomodoro-timer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "plyer>=2.0.1",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pomodoro=pomodoro:main",
        ],
    },
)
