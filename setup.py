"""
Pomodoro Timer - 打包配置
"""

from pathlib import Path

from setuptools import setup

ROOT = Path(__file__).parent
README = (ROOT / "README.md").read_text(encoding="utf-8")

setup(
    name="pomodoro-timer",
    version="1.1.0",
    author="Yzero123",
    author_email="248119587@qq.com",
    description="一个简单实用的命令行番茄钟工具（二次元增强版）",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Yzero123/pomodoro-timer",
    project_urls={
        "Source": "https://github.com/Yzero123/pomodoro-timer",
        "Issues": "https://github.com/Yzero123/pomodoro-timer/issues",
    },
    packages=["pomodoro_timer"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "plyer>=2.0.1",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pomodoro=pomodoro_timer.cli:main",
        ],
    },
)
