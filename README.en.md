# 🍅 Pomodoro Timer CLI · Anime-Style Command-Line Focus Timer

[![CI](https://github.com/Yzero123/pomodoro-timer/actions/workflows/ci.yml/badge.svg)](https://github.com/Yzero123/pomodoro-timer/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#cross-platform)
[![Code style](https://img.shields.io/badge/code-4-space%20indent-blue.svg)](https://peps.python.org/pep-0008/)

> A ready-to-use command-line Pomodoro timer: the standard Pomodoro technique, an anime-style terminal UI, random motivational quotes, desktop notifications, and persistent statistics.
> No GUI framework, no configuration required, works on Windows / macOS / Linux.

[中文](README.md) · [Quick start](#-quick-start) · [Commands](#-commands) · [Project layout](#-project-layout) · [Roadmap](#-roadmap) · [Contributing](CONTRIBUTING.md)

---

## ✨ Features

| Capability | Details |
| --- | --- |
| 🍅 Standard Pomodoro flow | 25 min focus + 5 min break, with a 15 min long break every 4 rounds; every duration is configurable |
| 🎨 Anime-style UI | Unicode borders, three state headers (focus / break / long break), and a live progress bar |
| 💖 Random motivational quotes | Separate quote pools for focus and break phases, picked at random each time |
| ⏰ Desktop notifications | Uses `plyer` when available, and falls back per OS (osascript / notify-send / terminal output) |
| 📊 Statistics dashboard | Today, this week, and all-time totals, rendered with `rich` |
| 💾 Persistent storage | Statistics live in `~/.pomodoro_data.json`; a corrupted file falls back to defaults instead of crashing |
| ⌨️ Keyboard-first | Starts with a single command; `Ctrl+C` pauses at any time and prints a session summary |
| 🧪 Tested | 16 unit tests, verified by GitHub Actions across a Python version matrix |

---

## 📸 Preview

The blocks below are **real program output**, not hand-drawn mockups.

**Focus mode**

```
  ╔══════════════════════════════════╗
  ║   🍅 ポ モ ド ー ロ  🍅           ║
  ║   ═══════════════════════════    ║
  ║     专注模式 · FOCUS MODE         ║
  ╚══════════════════════════════════╝

  💖 专注的你闪闪发光呢~ ✨

  🍅 │████████████████░░░░░░░░░░░░│ 专注中 │ 25:00
```

**Statistics dashboard**

```
  ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
  │            📈 统计面板             │
  ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

╭───── 💎 总体成就 ──────╮
│  🌟 总完成番茄钟: 0    │
│  ⏰ 总专注时间: 0 分钟 │
│  ⌛ 折合约: 0 小时     │
╰────────────────────────╯
╭─────── 📅 今日战报 ────────╮
│  🍅 完成: 0 个             │
│  ⏱️ 时长: 0 分钟           │
│  💯 加油！今天也很努力呢！ │
╰────────────────────────────╯
```

(The UI copy is intentionally in Chinese; the surrounding terminal chrome is plain ASCII.)

---

## 🚀 Quick start

### Option 1 — run straight from the clone (no install)

```bash
git clone https://github.com/Yzero123/pomodoro-timer.git
cd pomodoro-timer

pip install -r requirements.txt

python pomodoro.py            # start the timer
```

### Option 2 — install as a command (recommended)

```bash
git clone https://github.com/Yzero123/pomodoro-timer.git
cd pomodoro-timer

pip install .

pomodoro start
```

After installation the `pomodoro` command is available from any directory.

### Option 3 — development setup

```bash
pip install -e .
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

---

## 📖 Commands

| Command | Description |
| --- | --- |
| `pomodoro start` | Start the Pomodoro loop (the default command) |
| `pomodoro stats` | Show the statistics dashboard |
| `pomodoro stats --week` | Additionally show this week's summary |
| `pomodoro reset` | Reset **today's** statistics (history and totals are kept) |
| `pomodoro help` | Show help text |

### Options

| Option | Short | Default | Description |
| --- | --- | --- | --- |
| `--work` | `-w` | 25 | Focus duration in minutes |
| `--break` | `-b` | 5 | Short break duration in minutes |
| `--long-break` | `-l` | 15 | Long break duration in minutes |
| `--intervals` | `-i` | 4 | Number of focus rounds before a long break |
| `--week` | `-W` | off | Add the weekly summary to the dashboard |

**Examples**

```bash
# 30 minutes of focus, 10 minute break
pomodoro start --work 30 --break 10

# A 20 minute long break every 3 rounds
pomodoro start --intervals 3 --long-break 20
```

---

## 🔄 How a session runs

1. Enter a focus period, 25 minutes by default 🍅
2. On completion → desktop notification + motivational quote + celebration
3. Enter a short break, 5 minutes by default ☕
4. Every `--intervals` rounds the loop takes a long break, 15 minutes by default 🌟
5. Repeat; press `Ctrl+C` at any time to exit and print a session summary

---

## 💾 Data storage

Statistics are stored in `~/.pomodoro_data.json`:

```json
{
  "total_completed": 12,
  "total_minutes": 300,
  "daily_stats": {
    "2026-10-21": { "completed": 4, "minutes": 100 }
  },
  "last_updated": "2026-10-21"
}
```

- If the file is corrupted or unreadable, the program restores the default structure instead of crashing.
- `pomodoro reset` removes only the current day's entry; cumulative totals are preserved.
- The file is listed in `.gitignore` and is never committed.

---

## 📂 Project layout

```
pomodoro-timer/
├── pomodoro.py                  # Compatibility entry point: `python pomodoro.py start`
├── pomodoro_timer/              # Main package
│   ├── __init__.py              # Package entry, exposes __version__ and main()
│   ├── cli.py                   # Argument parsing and the main loop
│   ├── config.py                # Default durations, state constants, data file path
│   ├── notification.py          # Desktop notifications and OS fallbacks
│   └── storage.py               # Reading, writing and aggregating statistics
├── tests/
│   └── test_pomodoro.py         # 16 unit tests
├── .github/workflows/ci.yml     # CI matrix: Python 3.8 / 3.11 / 3.12
├── requirements.txt             # Runtime dependencies
├── requirements-dev.txt         # Development dependencies
├── setup.py                     # Packaging configuration
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE                      # MIT
├── README.md
└── README.en.md
```

---

## 🧪 Development and testing

```bash
pip install -r requirements-dev.txt

python -m unittest discover -s tests -v
python -m unittest tests.test_pomodoro -v
```

CI runs the same suite on Python 3.8 / 3.11 / 3.12 and adds a command-line smoke test (`pomodoro help`, `pomodoro stats`).

---

## 🗺️ Roadmap

- [x] v1.0.0 Core timer, persistent statistics, desktop notifications
- [x] v1.1.0 Anime UI, random motivational quotes, ASCII borders, celebration animation
- [x] v1.1.1 Fix the `run_long_break` indentation error (the module previously failed to import)
- [x] v1.1.1 Restructure into a proper `pomodoro_timer` package so `pip install .` works
- [x] v1.1.1 Add 16 unit tests and a CI workflow
- [ ] v1.2.0 Config file support (`.pomodororc`) so options don't have to be passed every time
- [ ] v1.2.0 Task labels and a daily goal
- [ ] v1.3.0 Session history export (CSV / Markdown)

---

## 🤝 Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first, and include the verification output related to your change (`python -m unittest discover -s tests`).

---

## 📄 License

MIT License — see the [LICENSE](LICENSE) file.
