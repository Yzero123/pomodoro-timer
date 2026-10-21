#!/usr/bin/env python3
"""
Pomodoro Timer - 兼容入口

项目主体已迁移到 `pomodoro_timer/` 包中，本文件保留是为了兼容
`python pomodoro.py start` 这种早期用法。

推荐用法：
    python -m pomodoro_timer.cli start
    pip install -e . && pomodoro start
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pomodoro_timer.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
