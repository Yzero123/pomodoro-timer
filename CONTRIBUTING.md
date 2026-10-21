# 贡献指南

感谢你愿意为 Pomodoro Timer CLI 出力。这份文档说明如何把改动顺利合进来。

## 环境准备

```bash
git clone https://github.com/Yzero123/pomodoro-timer.git
cd pomodoro-timer

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -e .
pip install -r requirements-dev.txt
```

## 本地验证

提交前请确保下面两条命令都通过：

```bash
python -m unittest discover -s tests -v
python pomodoro.py help
```

CI 会在 Python 3.8 / 3.11 / 3.12 上跑同一套测试，并额外做一次命令行冒烟测试。

## 代码约定

- 遵循 [PEP 8](https://peps.python.org/pep-0008/)，4 空格缩进，UTF-8 编码。
- 新增行为请配套补测试；测试放在 `tests/`，命名 `test_*.py`。
- 主包代码放在 `pomodoro_timer/`，不要把业务代码塞回根目录的 `pomodoro.py`（它只是兼容入口）。
- 不要提交 `~/.pomodoro_data.json`、虚拟环境、缓存目录或任何本机凭据。

## 提交信息

用祈使句描述改动本身，必要时补充动机：

```
fix: 修复长休息方法的缩进错误
feat: 新增 .pomodororc 配置支持
docs: 补充英文版 README 的命令参考
```

## Pull Request

1. 从 `main` 切出特性分支：`git checkout -b feat/your-feature`
2. 提交并推送：`git push -u origin feat/your-feature`
3. 在 GitHub 上开 PR，描述里写清**改了什么**和**怎么验证的**。
4. 等 CI 通过，PR 描述里贴上测试输出。

## 报告 Bug

请用 [Bug 报告模板](.github/ISSUE_TEMPLATE/bug_report.md)，包含：

- 操作系统与 Python 版本
- 复现步骤
- 实际输出与期望输出
- 完整报错信息

## 需要帮助？

开一个 Issue 描述你的想法，附上使用场景。功能讨论欢迎在 Issue 里进行，避免在 PR 里讨论范围之外的事。
