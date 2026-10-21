"""
Pomodoro Timer - 单元测试

只覆盖纯逻辑，不启动计时、不发系统通知、不依赖 GUI 环境。
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pomodoro_timer import config, notification, storage  # noqa: E402
from pomodoro_timer.cli import main  # noqa: E402


class ConfigTest(unittest.TestCase):
    def test_default_durations(self):
        self.assertEqual(config.DEFAULT_WORK_DURATION, 25)
        self.assertEqual(config.DEFAULT_BREAK_DURATION, 5)
        self.assertEqual(config.DEFAULT_LONG_BREAK_DURATION, 15)
        self.assertEqual(config.DEFAULT_INTERVALS, 4)

    def test_data_file_is_absolute(self):
        self.assertTrue(os.path.isabs(config.DATA_FILE))
        self.assertIn("pomodoro_data.json", config.DATA_FILE)


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "pomodoro_data.json")
        self.patcher = mock.patch.object(storage, "DATA_FILE", self.path)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_default_data_on_first_use(self):
        st = storage.Storage()
        self.assertEqual(st.get_total_stats()["total_completed"], 0)
        self.assertEqual(st.get_daily_stats()["completed"], 0)

    def test_record_completed_persists(self):
        st = storage.Storage()
        st.record_completed(25)
        st.record_completed(25)
        self.assertEqual(st.get_total_stats()["total_completed"], 2)
        self.assertEqual(st.get_total_stats()["total_minutes"], 50)
        self.assertEqual(st.get_daily_stats()["completed"], 2)

        # 重新打开应从磁盘读到同样的数据
        self.assertEqual(storage.Storage().get_total_stats()["total_completed"], 2)

    def test_reset_daily_keeps_total(self):
        st = storage.Storage()
        st.record_completed(25)
        st.reset_daily()
        self.assertEqual(st.get_daily_stats()["completed"], 0)
        self.assertEqual(st.get_total_stats()["total_completed"], 1)

    def test_corrupt_file_falls_back_to_defaults(self):
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write("{ this is not json")
        self.assertEqual(storage.Storage().get_total_stats()["total_completed"], 0)

    def test_saved_file_is_valid_json(self):
        st = storage.Storage()
        st.record_completed(25)
        with open(self.path, encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertIn("daily_stats", data)
        self.assertIn("total_completed", data)

    def test_weekly_stats_shape(self):
        st = storage.Storage()
        st.record_completed(25)
        week = st.get_weekly_stats()
        self.assertIn("completed", week)
        self.assertIn("minutes", week)
        self.assertIn("days", week)


class NotificationTest(unittest.TestCase):
    def test_countdown_fires_at_30_and_10_seconds(self):
        with mock.patch.object(notification, "send_notification") as send:
            notification.NotificationManager.countdown(0, 30)
            notification.NotificationManager.countdown(0, 10)
        self.assertEqual(send.call_count, 2)
        self.assertIn("30", send.call_args_list[0][0][1])
        self.assertIn("10", send.call_args_list[1][0][1])

    def test_countdown_silent_for_other_values(self):
        with mock.patch.object(notification, "send_notification") as send:
            notification.NotificationManager.countdown(0, 45)
            notification.NotificationManager.countdown(1, 0)
        send.assert_not_called()

    def test_mac_notification_escapes_quotes(self):
        """标题和正文里的引号不能破坏 AppleScript 语法。"""
        recorded = {}

        def fake_run(cmd, **kwargs):
            recorded["cmd"] = cmd

        with mock.patch("subprocess.run", fake_run):
            notification._mac_notification('He said "hi"', 'a "quoted" body')

        cmd = recorded["cmd"]
        self.assertEqual(cmd[0], "osascript")
        # 正文与标题作为独立 argv 传入，不做字符串拼接
        self.assertIn('He said "hi"', cmd)
        self.assertIn('a "quoted" body', cmd)
        self.assertNotIn('display notification "a "quoted" body"', " ".join(cmd))

    def test_linux_notification_falls_back_when_missing(self):
        def fake_run(cmd, **kwargs):
            raise FileNotFoundError("notify-send not found")

        with mock.patch("subprocess.run", fake_run):
            with mock.patch("builtins.print") as printer:
                notification._linux_notification("t", "m")
        self.assertTrue(printer.called)


class CliTest(unittest.TestCase):
    def test_help_prints_usage(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            main(["help"])
        self.assertIn("start", buffer.getvalue())
        self.assertIn("--work", buffer.getvalue())

    def test_dash_dash_help_exits_cleanly(self):
        with self.assertRaises(SystemExit) as ctx:
            with contextlib.redirect_stdout(io.StringIO()):
                main(["--help"])
        self.assertEqual(ctx.exception.code, 0)

    def test_invalid_command_rejected(self):
        with self.assertRaises(SystemExit) as ctx:
            with contextlib.redirect_stdout(io.StringIO()):
                main(["nope"])
        self.assertNotEqual(ctx.exception.code, 0)

    def test_stats_runs(self):
        with mock.patch.object(storage, "DATA_FILE", os.devnull + ".json"):
            with contextlib.redirect_stdout(io.StringIO()):
                main(["stats"])


if __name__ == "__main__":
    unittest.main()
