"""
Pomodoro Timer - 配置文件
"""

# 默认设置
DEFAULT_WORK_DURATION = 25      # 工作时长（分钟）
DEFAULT_BREAK_DURATION = 5      # 短暂休息（分钟）
DEFAULT_LONG_BREAK_DURATION = 15 # 长休息（分钟）
DEFAULT_INTERVALS = 4           # 长休息间隔

# 数据文件路径
import os
DATA_FILE = os.path.expanduser("~/.pomodoro_data.json")

# 番茄钟状态
STATE_WORK = "work"
STATE_BREAK = "break"
STATE_LONG_BREAK = "long_break"
STATE_IDLE = "idle"
