#!/usr/bin/env python3
"""
Pomodoro Timer CLI
一个简单实用的命令行番茄钟工具 (二次元增强版)
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


# ============================================
# 二次元风格常量
# ============================================
ANIME_TOMATO = r"""
    ╭━━━━━━━━━━━━━━━━━━━━━╮
    ┃                     ┃
    ┃   🍅 ポモドーロ 🍅   ┃
    ┃   ═══════════════   ┃
    ┃    专注时间到！      ┃
    ┃                     ┃
    ╰━━━━━━━━━━━━━━━━━━━━━╯
"""

MOTIVATIONAL_QUOTES = [
    "加油！你是最棒的！ヾ(◍°∇°◍)ﾉﾞ",
    "专注的你闪闪发光呢~ ✨",
    "再坚持一下就胜利啦！💪",
    "效率王者就是你！👑",
    "距离目标越来越近了！🎯",
    "好厉害！继续冲鸭！🦆",
    "今天也要元气满满哟！💖",
    "专注的样子超帅的！😎",
]

BREAK_MESSAGES = [
    "休息一下吧~ 伸个懒腰！🧘",
    "喝杯水补充能量吧！💧",
    "看看窗外放松眼睛吧！👀",
    "休息是为了走更远的路~ 🚶",
    "给自己点个赞吧！👍",
]

LONG_BREAK_MESSAGES = [
    "太棒了！休息一下吧~ 🌟",
    "一个循环结束！休息一下吧！☕",
    "做得很好！稍微休息一下吧！🎉",
]


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

    def _get_random_message(self, message_list):
        """获取随机消息"""
        import random
        return random.choice(message_list)

    def _print_anime_header(self, state):
        """打印二次元风格标题"""
        if state == STATE_WORK:
            header = r"""
  ╔══════════════════════════════════╗
  ║   🍅 ポ モ ド ー ロ  🍅           ║
  ║   ═══════════════════════════    ║
  ║     专注模式 · FOCUS MODE         ║
  ╚══════════════════════════════════╝"""
        elif state == STATE_BREAK:
            header = r"""
  ╔══════════════════════════════════╗
  ║   ☕ 休 憩 时 间  ☕              ║
  ║   ═══════════════════════════    ║
  ║     休息模式 · BREAK TIME        ║
  ╚══════════════════════════════════╝"""
        else:
            header = r"""
  ╔══════════════════════════════════╗
  ║   🌟 长 休 息 时 间  🌟           ║
  ║   ═══════════════════════════    ║
  ║   LONG BREAK · 充分休息吧        ║
  ╚══════════════════════════════════╝"""
        print(header)

    def _print_progress(self, state, remaining, total):
        """打印二次元风格进度条"""
        bar_length = 28
        filled = int(bar_length * (total - remaining) / total)

        # 不同状态的进度条颜色
        if state == STATE_WORK:
            bar_filled = "█" * filled
            bar_empty = "░" * (bar_length - filled)
        elif state == STATE_BREAK:
            bar_filled = "▓" * filled
            bar_empty = "░" * (bar_length - filled)
        else:
            bar_filled = "▒" * filled
            bar_empty = "░" * (bar_length - filled)

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

        # 打印进度条
        sys.stdout.write("\r\033[K")
        sys.stdout.write(f"  {state_icon} │{bar_filled}{bar_empty}│ {state_text} │ {self._format_time(remaining)} ")
        sys.stdout.flush()

    def _run_timer(self, duration_minutes, state):
        """运行计时器"""
        total_seconds = duration_minutes * 60
        start_time = time.time()
        end_time = start_time + total_seconds

        last_notification = None

        # 打印状态头
        self._print_anime_header(state)
        print(f"  {self._get_random_message(MOTIVATIONAL_QUOTES if state == STATE_WORK else BREAK_MESSAGES)}")
        print()

        while time.time() < end_time:
            remaining = int(end_time - time.time())

            # 每30秒显示通知（最后阶段）
            if remaining == 30 and last_notification != 30:
                NotificationManager.countdown(remaining // 60, remaining % 60)
                last_notification = 30
            elif remaining == 10 and last_notification != 10:
                NotificationManager.countdown(0, 10)
                last_notification = 10

            self._print_progress(state, remaining, total_seconds)
            time.sleep(0.1)

        # 完成
        print()

    def run_work(self):
        """运行工作周期"""
        self._run_timer(self.work_duration, STATE_WORK)
        NotificationManager.work_complete()
        self.storage.record_completed(self.work_duration)
        self.completed_in_session += 1

        # 打印完成庆祝
        print("\n" + "=" * 40)
        print("🎊 太棒了！一个番茄钟完成啦！")
        print(f"💖 {self._get_random_message(MOTIVATIONAL_QUOTES)}")
        print("=" * 40)

    def run_break(self):
        """运行休息周期"""
        self._run_timer(self.break_duration, STATE_BREAK)
        NotificationManager.break_complete()

        print("\n" + "-" * 40)
        print("☕ 休息结束！准备开始下一个吧~")
        print("-" * 40)

def run_long_break(self):
        """运行长休息周期"""
        self._run_timer(self.long_break_duration, STATE_LONG_BREAK)
        NotificationManager.long_break_complete()

        print("\n" + "=" * 40)
        print("🌟 长休息结束！休息得怎么样？")
        print("✨ 精力充沛地继续前进吧！")
        print("=" * 40)

    def start(self):
        """启动番茄钟"""
        print("\n" + "╭" + "━" * 48 + "╮")
        print("│" + " " * 10 + "🍅 ポモドーロタイマー 🍅" + " " * 10 + "│")
        print("│" + " " * 15 + "二次元增强版" + " " * 15 + "│")
        print("╰" + "━" * 48 + "╯")
        print()
        print("  ✨ 欢迎使用番茄钟！让我们开始专注吧~ ✨")
        print("  " + "─" * 44)
        print(f"  📋 工作时长: {self.work_duration}分钟")
        print(f"  📋 休息时长: {self.break_duration}分钟")
        print(f"  📋 长休息: {self.long_break_duration}分钟 (每{self.intervals}个后)")
        print("  " + "─" * 44)
        print("  💡 按 Ctrl+C 可以暂停并退出")
        print("  " + "─" * 44)
        print()

        try:
            while True:
                # 工作周期
                self.run_work()

                # 检查是否需要长休息
                if self.completed_in_session % self.intervals == 0:
                    print(f"\n🎉 太棒了！已连续完成 {self.completed_in_session} 个番茄钟！")
                    print("🌟 建议休息一下~ 身体是革命的本钱！")
                    self.run_long_break()
                else:
                    self.run_break()

                remaining = self.intervals - (self.completed_in_session % self.intervals)
                if remaining == 0:
                    remaining = self.intervals
                print(f"\n⏭️  距离长休息还有 {remaining} 个番茄钟~ 继续加油鸭！🦆")
                print()

        except KeyboardInterrupt:
            print("\n\n" + "╭" + "─" * 46 + "╮")
            print("│" + " " * 14 + "👋 再见啦！下次见~" + " " * 14 + "│")
            print("╰" + "─" * 46 + "╯")
            self._print_summary()

    def _print_summary(self):
        """打印本次会话总结"""
        daily = self.storage.get_daily_stats()
        print()
        print("╭" + "─" * 46 + "╮")
        print(f"│  📊 今日统计: {daily['completed']} 个番茄钟，共 {daily['minutes']} 分钟  │")
        print("╰" + "─" * 46 + "╯")
        print(f"│  💪 本次会话完成了 {self.completed_in_session} 个番茄钟！继续努力~  │")
        print("╰" + "─" * 46 + "╯")

    def show_stats(self, weekly=False):
        """显示统计（二次元风格）"""
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel
            from rich.text import Text

            console = Console()
            total = self.storage.get_total_stats()

            # 装饰边框
            console.print("\n  ╭" + "━" * 40 + "╮")
            console.print("  │" + " " * 12 + "📈 统计面板" + " " * 13 + "│")
            console.print("  ╰" + "━" * 40 + "╯\n")

            # 总览面板
            panel_content = (
                f" 🌟 总完成番茄钟: [bold cyan]{total['total_completed']}[/bold cyan]\n"
                f" ⏰ 总专注时间: [bold green]{total['total_minutes']}[/bold green] 分钟\n"
                f" ⌛ 折合约: [bold yellow]{total['total_minutes'] // 60}[/bold yellow] 小时"
            )
            console.print(Panel(panel_content, title="💎 总体成就", expand=False, border_style="cyan"))

            # 今日统计
            daily = self.storage.get_daily_stats()
            today_panel = (
                f" 🍅 完成: [bold yellow]{daily['completed']}[/bold yellow] 个\n"
                f" ⏱️ 时长: [bold blue]{daily['minutes']}[/bold blue] 分钟\n"
                f" 💯 加油！今天也很努力呢！"
            )
            console.print(Panel(today_panel, title="📅 今日战报", expand=False, border_style="green"))

            if weekly:
                # 周统计
                week = self.storage.get_weekly_stats()
                week_panel = (
                    f" 📆 本周完成: [bold magenta]{week['completed']}[/bold magenta] 个\n"
                    f" ⏰ 本周时长: [bold green]{week['minutes']}[/bold green] 分钟\n"
                    f" ✨ 持续努力就是胜利！"
                )
                console.print(Panel(week_panel, title="📆 本周汇总", expand=False, border_style="magenta"))

            console.print()

        except ImportError:
            # 降级到简单输出
            total = self.storage.get_total_stats()
            daily = self.storage.get_daily_stats()

            print("\n" + "╭" + "━" * 40 + "╮")
            print("│" + " " * 12 + "📊 统计信息" + " " * 13 + "│")
            print("╰" + "━" * 40 + "╯")
            print(f"│  🌟 总完成番茄钟: {total['total_completed']}")
            print(f"│  ⏰ 总专注时间: {total['total_minutes']} 分钟 ({total['total_minutes'] // 60} 小时)")
            print(f"│  🍅 今日完成: {daily['completed']} 个")
            print("╰" + "━" * 40 + "╯")

    def reset(self):
        """重置今日统计"""
        self.storage.reset_daily()
        print("\n  ╭" + "━" * 30 + "╮")
        print("  │  ✅ 今日统计已重置！        │")
        print("  │  💪 重新开始新的一天吧~    │")
        print("  ╰" + "━" * 30 + "╯")


def main():
    parser = argparse.ArgumentParser(
        description="🍅 Pomodoro Timer - 二次元增强版命令行番茄钟",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
  ╭────────────────────────────────────────╮
  │  示例:                                  │
  │    %(prog)s start              启动番茄钟  │
  │    %(prog)s start --work 30    30分钟工作  │
  │    %(prog)s stats              查看统计    │
  │    %(prog)s stats --week       本周统计    │
  │    %(prog)s reset              重置统计    │
  ╰────────────────────────────────────────╯
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
