"""
Pomodoro Timer - 二次元增强版命令行番茄钟

包入口。对外暴露版本号与主程序，便于 `from pomodoro_timer import main` 调用。
"""

__version__ = "1.1.0"
__all__ = ["main", "__version__"]


def main(argv=None):
    """命令行入口（延迟导入，避免导入包时就加载 rich / plyer）。"""
    from .cli import main as _main

    return _main(argv)
