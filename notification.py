"""
Pomodoro Timer - 通知模块
"""

import sys


def send_notification(title, message, notification_type="info"):
    """
    发送桌面通知
    
    Args:
        title: 通知标题
        message: 通知内容
        notification_type: 通知类型 (info, success, warning)
    """
    # 尝试使用 plyer
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name="Pomodoro Timer",
            timeout=10
        )
        return
    except ImportError:
        pass

    # 降级：使用系统命令
    if sys.platform == "win32":
        _windows_notification(title, message)
    elif sys.platform == "darwin":
        _mac_notification(title, message)
    else:
        _linux_notification(title, message)


def _windows_notification(title, message):
    """Windows 通知"""
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=10)
    except ImportError:
        print(f"\n📢 {title}: {message}")


def _mac_notification(title, message):
    """macOS 通知"""
    import subprocess
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])


def _linux_notification(title, message):
    """Linux 通知"""
    import subprocess
    subprocess.run(["notify-send", title, message])


class NotificationManager:
    """通知管理器"""

    @staticmethod
    def work_complete():
        """工作完成通知"""
        send_notification(
            "🍅 番茄钟完成！",
            "恭喜！你完成了一个番茄钟。休息一下吧！"
        )

    @staticmethod
    def break_complete():
        """休息结束通知"""
        send_notification(
            "☕ 休息结束！",
            "休息时间结束，准备开始下一个番茄钟吧！"
        )

    @staticmethod
    def long_break_complete():
        """长休息结束通知"""
        send_notification(
            "🌟 长休息结束！",
            "休息充分了！继续加油，准备开始新的工作周期。"
        )

    @staticmethod
    def countdown(minutes, seconds):
        """倒计时提醒（最后1分钟）"""
        if minutes == 0 and seconds == 30:
            send_notification("⏰", "还剩30秒！")
