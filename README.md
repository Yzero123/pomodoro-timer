# Pomodoro Timer CLI

一个简单实用的命令行番茄钟工具，专注于时间管理和效率提升。

## 功能特性

- 25分钟专注 + 5分钟休息的标准番茄工作法
- 自定义工作/休息时长
- 桌面通知提醒
- 每日/每周统计数据
- 数据持久化存储
- 简洁的命令行界面

## 安装

### 方式一：直接运行

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/pomodoro-timer.git
cd pomodoro-timer

# 安装依赖
pip install -r requirements.txt

# 运行
python pomodoro.py
```

### 方式二：全局安装

```bash
pip install -e .
pomodoro
```

## 使用方法

### 启动番茄钟

```bash
python pomodoro.py start
```

### 查看统计

```bash
python pomodoro.py stats
python pomodoro.py stats --week    # 查看本周统计
```

### 自定义时长

```bash
python pomodoro.py start --work 30 --break 10
```

### 其他命令

```bash
python pomodoro.py help    # 显示帮助
python pomodoro.py reset   # 重置今天的统计
```

## 命令行参数

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `--work` | 工作时长（分钟） | 25 |
| `--break` | 休息时长（分钟） | 5 |
| `--long-break` | 长休息时长（分钟） | 15 |
| `--intervals` | 长休息间隔 | 4 |

## 工作流程

1. 开始专注工作（默认25分钟）
2. 专注时间结束，收到桌面通知
3. 短暂休息（默认5分钟）
4. 每4个番茄钟后，长休息（15分钟）

## 数据存储

统计数据显示保存在 `~/.pomodoro_data.json` 文件中，包括：
- 完成的任务数
- 累计专注时间
- 每日/每周统计

## 依赖

- Python 3.7+
- plyer (桌面通知)
- rich (美化输出)

## License

MIT License
