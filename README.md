# DreamForge（增强版）

DreamForge 现在包含：

- CLI 创意生成器
- 技术栈推荐
- 商业模式建议
- MVP 路线图自动生成
- Web 可视化点子卡片

## CLI 用法

```bash
python3 dreamforge.py
python3 dreamforge.py --seed 42
python3 dreamforge.py --json
python3 dreamforge.py --seed 42 --save ideas/today.json
```

## Web 可视化版

```bash
python3 web_app.py --host 127.0.0.1 --port 8000
# 浏览器打开 http://127.0.0.1:8000
```

页面会生成一张包含「领域、目标用户、问题、玩法、亮点、技术栈、商业模式、MVP 路线图」的卡片。

## 测试

```bash
python3 -m pytest -q
```
