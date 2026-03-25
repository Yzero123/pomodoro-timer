#!/usr/bin/env python3
"""
Pomodoro Timer CLI
一个简单实用的命令行番茄钟工具
"""

import argparse
import time
import sys
from datetime import datetime, timedelta

from config import (
    DEFAULT_WORK_DURATION,
    DEFAULT_BREAK_DURATION,
    DEFAULT_LONG_BREAK_DURATION,
    DEFAULT_INTERVALS,
    STATE_WORK, STATE_BREAK, STATE_LONG_BREAK, STATE_IDLE
)
from storage import Storage
from notification import NotificationManager


class PomodoroTimer:
    """番茄钟主类"""

    def __init__(self, work_duration=25, break_duration=5,
                 long_break_duration=15, intervals=4):
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.long_break_duration = long_break_duration
        self.intervals = intervals
        self.storage = Storage()
        self.completed_in_session = 0

    def _format_time(self, seconds):
        """格式化时间显示"""
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def _print_progress(self, state, remaining, total):
        """打印进度条"""
        bar_length = 30
        filled = int(bar_length * (total - remaining) / total)
        bar = "█" * filled + "░" * (bar_length - filled)

        state_icon = {
            STATE_WORK: "🍅",
            STATE_BREAK: "☕",
            STATE_LONG_BREAK: "🌟"
        }.get(state, "⏱️")

        state_text = {
            STATE_WORK: "专注中",
            STATE_BREAK: "短暂休息",
            STATE_LONG_BREAK: "长休息"
        }.get(state, "")

        # 使用 ANSI 转义码清除行并重绘
        sys.stdout.write("\r\033[K")
        sys.stdout.write(f"{state_icon} [{bar}] {state_text} | {self._format_time(remaining)}  ")
        sys.stdout.flush()

    def _run_timer(self, duration_minutes, state):
        """运行计时器"""
        total_seconds = duration_minutes * 60
        start_time = time.time()
        end_time = start_time + total_seconds

        last_notification = None

        while time.time() < end_time:
            remaining = int(end_time - time.time())

            # 每30秒显示通知（最后阶段）
            if remaining == 30 and last_notification != 30:
                NotificationManager.countdown(
                    remaining // 60, remaining % 60
                )
                last_notification = 30
            elif remaining == 10 and last_notification != 10:
                NotificationManager.countdown(0, 10)
                last_notification = 10

            self._print_progress(state, remaining, total_seconds)
            time.sleep(0.1)

        # 完成
        print()  # 换行

    def run_work(self):
        """运行工作周期"""
        self._run_timer(self.work_duration, STATE_WORK)
        NotificationManager.work_complete()
        self.storage.record_completed(self.work_duration)
        self.completed_in_session += 1

    def run_break(self):
        """运行休息周期"""
        self._run_timer(self.break_duration, STATE_BREAK)
        NotificationManager.break_complete()

    def run_long_break(self):
        """运行长休息周期"""
        self._run_timer(self.long_break_duration, STATE_LONG_BREAK)
        NotificationManager.long_break_complete()

    def start(self):
        """启动番茄钟"""
        print("\n" + "=" * 50)
        print("🍅  番茄钟启动！专注工作吧！")
        print("=" * 50)
        print(f"工作: {self.work_duration}分钟 | 休息: {self.break_duration}分钟")
        print(f"长休息: {self.long_break_duration}分钟 (每{self.intervals}个番茄钟后)")
        print("-" * 50)
        print("按 Ctrl+C 可以暂停并退出")
        print("-" * 50)

        try:
            while True:
                # 工作周期
                self.run_work()

                # 检查是否需要长休息
                if self.completed_in_session % self.intervals == 0:
                    print(f"\n🎉 太棒了！完成 {self.completed_in_session} 个番茄钟！")
                    self.run_long_break()
                else:
                    self.run_break()

                print("\n⏭️  开始下一个番茄钟...")

        except KeyboardInterrupt:
            print("\n\n👋 番茄钟已暂停。再见！")
            self._print_summary()

    def _print_summary(self):
        """打印本次会话总结"""
        daily = self.storage.get_daily_stats()
        print(f"\n📊 今日统计: 完成 {daily['completed']} 个番茄钟，"
              f"共 {daily['minutes']} 分钟")

    def show_stats(self, weekly=False):
        """显示统计"""
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel

            console = Console()
            total = self.storage.get_total_stats()

            # 总览面板
            panel_content = (
                f"总完成番茄钟: [bold cyan]{total['total_completed']}[/bold cyan]\n"
                f"总专注时间: [bold green]{total['total_minutes']}[/bold green] 分钟"
                f" ({total['total_minutes'] // 60} 小时)"
            )
            console.print(Panel(panel_content, title="📈 总体统计", expand=False))

            # 今日统计
            daily = self.storage.get_daily_stats()
            today_panel = (
                f"完成: [bold yellow]{daily['completed']}[/bold yellow] 个\n"
                f"时长: [bold blue]{daily['minutes']}[/bold blue] 分钟"
            )
            console.print(Panel(today_panel, title="📅 今日统计", expand=False))

            if weekly:
                # 周统计
                week = self.storage.get_weekly_stats()
                week_panel = (
                    f"本周完成: [bold magenta]{week['completed']}[/bold magenta] 个\n"
                    f"本周时长: [bold green]{week['minutes']}[/bold green] 分钟"
                )
                console.print(Panel(week_panel, title="📆 本周统计", expand=False))

        except ImportError:
            # 降级到简单输出
            total = self.storage.get_total_stats()
            daily = self.storage.get_daily_stats()

            print("\n" + "=" * 40)
            print("📊 统计信息")
            print("=" * 40)
            print(f"总完成番茄钟: {total['total_completed']}")
            print(f"总专注时间: {total['total_minutes']} 分钟")
            print(f"今日完成: {daily['completed']} 个")
            print("=" * 40)

    def reset(self):
        """重置今日统计"""
        self.storage.reset_daily()
        print("✅ 今日统计已重置")


def main():
    parser = argparse.ArgumentParser(
        description="🍅 Pomodoro Timer - 命令行番茄钟",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s start              # 启动番茄钟
  %(prog)s start --work 30    # 30分钟工作周期
  %(prog)s stats              # 查看统计
  %(prog)s stats --week       # 查看本周统计
  %(prog)s reset              # 重置今日统计
        """
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="start",
        choices=["start", "stats", "reset", "help"],
        help="命令: start (默认), stats, reset, help"
    )

    parser.add_argument(
        "--work", "-w",
        type=int,
        default=DEFAULT_WORK_DURATION,
        help=f"工作时长（分钟），默认 {DEFAULT_WORK_DURATION}"
    )

    parser.add_argument(
        "--break", "-b",
        dest="break_duration",
        type=int,
        default=DEFAULT_BREAK_DURATION,
        help=f"休息时长（分钟），默认 {DEFAULT_BREAK_DURATION}"
    )

    parser.add_argument(
        "--long-break", "-l",
        dest="long_break_duration",
        type=int,
        default=DEFAULT_LONG_BREAK_DURATION,
        help=f"长休息时长（分钟），默认 {DEFAULT_LONG_BREAK_DURATION}"
    )

    parser.add_argument(
        "--intervals", "-i",
        type=int,
        default=DEFAULT_INTERVALS,
        help=f"长休息间隔，默认 {DEFAULT_INTERVALS}"
    )

    parser.add_argument(
        "--week", "-W",
        action="store_true",
        help="显示本周统计"
    )

    args = parser.parse_args()

    # 创建计时器实例
    timer = PomodoroTimer(
        work_duration=args.work,
        break_duration=args.break_duration,
        long_break_duration=args.long_break_duration,
        intervals=args.intervals
    )

    # 执行命令
    if args.command == "start":
        timer.start()
    elif args.command == "stats":
        timer.show_stats(weekly=args.week)
    elif args.command == "reset":
        timer.reset()
    elif args.command == "help":
        parser.print_help()


if __name__ == "__main__":
    main()
