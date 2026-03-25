"""
Pomodoro Timer - 数据存储模块
"""

import json
import os
from datetime import datetime, date
from config import DATA_FILE


class Storage:
    """数据持久化管理"""

    def __init__(self):
        self.data = self._load()

    def _load(self):
        """加载数据"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self._default_data()

    def _default_data(self):
        """默认数据结构"""
        return {
            "total_completed": 0,
            "total_minutes": 0,
            "daily_stats": {},
            "last_updated": str(date.today())
        }

    def _save(self):
        """保存数据"""
        self.data["last_updated"] = str(date.today())
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"警告：无法保存数据: {e}")

    def record_completed(self, minutes):
        """记录完成一个番茄钟"""
        today = str(date.today())

        # 更新总计
        self.data["total_completed"] += 1
        self.data["total_minutes"] += minutes

        # 更新每日统计
        if today not in self.data["daily_stats"]:
            self.data["daily_stats"][today] = {"completed": 0, "minutes": 0}

        self.data["daily_stats"][today]["completed"] += 1
        self.data["daily_stats"][today]["minutes"] += minutes

        self._save()

    def get_daily_stats(self):
        """获取今日统计"""
        today = str(date.today())
        if today in self.data["daily_stats"]:
            return self.data["daily_stats"][today]
        return {"completed": 0, "minutes": 0}

    def get_weekly_stats(self):
        """获取本周统计"""
        today = date.today()
        week_start = today.isoweekday()
        week_stats = {"completed": 0, "minutes": 0, "days": {}}

        for i in range(week_start):
            day = today - timedelta(days=week_start - i - 1)
            day_str = str(day)
            if day_str in self.data["daily_stats"]:
                week_stats["completed"] += self.data["daily_stats"][day_str]["completed"]
                week_stats["minutes"] += self.data["daily_stats"][day_str]["minutes"]
                week_stats["days"][day_str] = self.data["daily_stats"][day_str]

        return week_stats

    def reset_daily(self):
        """重置今日统计（保留历史）"""
        today = str(date.today())
        if today in self.data["daily_stats"]:
            del self.data["daily_stats"][today]
        self._save()

    def get_total_stats(self):
        """获取总统计"""
        return {
            "total_completed": self.data["total_completed"],
            "total_minutes": self.data["total_minutes"]
        }


from datetime import timedelta
