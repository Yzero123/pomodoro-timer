# 🍅 Pomodoro Timer CLI · 二次元增强版命令行番茄钟

[![CI](https://github.com/Yzero123/pomodoro-timer/actions/workflows/ci.yml/badge.svg)](https://github.com/Yzero123/pomodoro-timer/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#-跨平台)
[![Code style](https://img.shields.io/badge/code-4-space%20indent-blue.svg)](https://peps.python.org/pep-0008/)

> 一个开箱即用的命令行番茄钟：标准番茄工作法 + 二次元风格界面 + 随机励志语录 + 桌面通知 + 统计持久化。
> 零配置启动，不依赖任何 GUI 框架，Windows / macOS / Linux 通用。

[English](README.en.md) · [快速开始](#-快速开始) · [命令参考](#-命令参考) · [项目结构](#-项目结构) · [路线图](#-路线图) · [贡献指南](CONTRIBUTING.md)

---

## ✨ 特性

| 能力 | 说明 |
| --- | --- |
| 🍅 标准番茄工作法 | 25 分钟专注 + 5 分钟休息，每 4 轮进入 15 分钟长休息，全部可自定义 |
| 🎨 二次元风格 UI | Unicode 边框、专注 / 休息 / 长休息三套状态标题、实时进度条 |
| 💖 随机励志语录 | 工作与休息分别使用不同语料库，每次随机抽取 |
| ⏰ 桌面通知 | 优先使用 `plyer`；不可用时按系统降级（osascript / notify-send / 终端输出） |
| 📊 统计面板 | 今日 / 本周 / 累计三个维度，基于 `rich` 渲染 |
| 💾 数据持久化 | 统计写入 `~/.pomodoro_data.json`，损坏时自动回退到默认结构 |
| ⌨️ 全键盘友好 | 单命令启动，`Ctrl+C` 随时暂停并打印本次会话小结 |
| 🧪 测试覆盖 | 16 项单元测试，GitHub Actions 多 Python 版本矩阵验证 |

---

## 📸 界面预览

以下为**实际运行输出**，非手绘示意图。

**专注模式**

```
  ╔══════════════════════════════════╗
  ║   🍅 ポ モ ド ー ロ  🍅           ║
  ║   ═══════════════════════════    ║
  ║     专注模式 · FOCUS MODE         ║
  ╚══════════════════════════════════╝

  💖 专注的你闪闪发光呢~ ✨

  🍅 │████████████████░░░░░░░░░░░░│ 专注中 │ 25:00
```

**统计面板**

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

---

## 🚀 快速开始

### 方式一：直接运行（免安装）

```bash
git clone https://github.com/Yzero123/pomodoro-timer.git
cd pomodoro-timer

pip install -r requirements.txt

python pomodoro.py            # 直接启动番茄钟
```

### 方式二：安装为命令行工具（推荐）

```bash
git clone https://github.com/Yzero123/pomodoro-timer.git
cd pomodoro-timer

pip install .

pomodoro start
```

安装后 `pomodoro` 命令在任意目录可用。

### 方式三：开发模式

```bash
pip install -e .
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

---

## 📖 命令参考

| 命令 | 说明 |
| --- | --- |
| `pomodoro start` | 启动番茄钟循环（默认命令） |
| `pomodoro stats` | 查看统计面板 |
| `pomodoro stats --week` | 追加显示本周汇总 |
| `pomodoro reset` | 重置**今天**的统计（保留历史与累计值） |
| `pomodoro help` | 显示帮助信息 |

### 可选参数

| 参数 | 简写 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--work` | `-w` | 25 | 专注时长（分钟） |
| `--break` | `-b` | 5 | 短暂休息时长（分钟） |
| `--long-break` | `-l` | 15 | 长休息时长（分钟） |
| `--intervals` | `-i` | 4 | 多少个番茄钟后进入长休息 |
| `--week` | `-W` | 关 | 在统计面板中追加本周汇总 |

**示例**

```bash
# 30 分钟专注 + 10 分钟休息
pomodoro start --work 30 --break 10

# 每 3 轮进入一次 20 分钟长休息
pomodoro start --intervals 3 --long-break 20
```

---

## 🔄 工作流程

1. 进入专注周期，默认 25 分钟 🍅
2. 专注结束 → 桌面通知 + 励志语录 + 庆祝动画
3. 进入短暂休息，默认 5 分钟 ☕
4. 每满 `--intervals` 轮改走长休息，默认 15 分钟 🌟
5. 循环继续；`Ctrl+C` 随时退出并打印本次会话小结

---

## 💾 数据存储

统计数据保存在 `~/.pomodoro_data.json`：

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

- 文件损坏或解析失败时，程序会自动回退到默认结构而不是崩溃。
- `pomodoro reset` 只删除当天条目，累计值保留。
- 该文件已在 `.gitignore` 中，不会被误提交。

---

## 📂 项目结构

```
pomodoro-timer/
├── pomodoro.py                  # 兼容入口，支持 `python pomodoro.py start`
├── pomodoro_timer/              # 主包
│   ├── __init__.py              # 包入口，暴露 __version__ 与 main()
│   ├── cli.py                   # 命令行解析与主循环
│   ├── config.py                # 默认时长、状态常量、数据文件路径
│   ├── notification.py          # 桌面通知与系统降级
│   └── storage.py               # 统计数据的读写与聚合
├── tests/
│   └── test_pomodoro.py         # 16 项单元测试
├── .github/workflows/ci.yml     # CI：Python 3.8 / 3.11 / 3.12 矩阵
├── requirements.txt             # 运行依赖
├── requirements-dev.txt         # 开发依赖
├── setup.py                     # 打包配置
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE                      # MIT
├── README.md
└── README.en.md
```

---

## 🧪 开发与测试

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行全部测试
python -m unittest discover -s tests -v

# 单个测试文件
python -m unittest tests.test_pomodoro -v
```

CI 在 Python 3.8 / 3.11 / 3.12 上运行同一套测试，并额外执行一次命令行冒烟测试（`pomodoro help`、`pomodoro stats`）。

---

## 🗺️ 路线图

- [x] v1.0.0 基础番茄钟、统计持久化、桌面通知
- [x] v1.1.0 二次元 UI、随机励志语录、ASCII 边框、庆祝动画
- [x] v1.1.1 修正 `run_long_break` 缩进错误（此前整个模块无法导入）
- [x] v1.1.1 重构为标准 `pomodoro_timer` 包，`pip install .` 可用
- [x] v1.1.1 补齐 16 项单元测试与 CI 工作流
- [ ] v1.2.0 配置文件支持（`.pomodororc`），免去每次传参
- [ ] v1.2.0 任务标签与每日目标
- [ ] v1.3.0 会话历史导出（CSV / Markdown）

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request。提交前请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

代码贡献请附带与改动相关的验证结果（`python -m unittest discover -s tests`）。

---

## 📄 License

MIT License — 详见 [LICENSE](LICENSE) 文件。

---

## 📞 联系

问题反馈与建议欢迎通过 GitHub Issues 提交。

> 💖 *专注是一种力量，让每一次番茄钟都充满意义！*
