# AI 每日简报（5 分钟 · 中美聚焦）

每天早晨自动生成一份中文 AI 行业简报，聚焦**中国与美国**，覆盖两条主线：

- **技术突破** —— 最新模型发布及其可实现的效果
- **商业化落地** —— 技术与产业结合的产品、案例、融资等

## 报告内容

1. 开头 **今日速览（Top 3）**：今天最值得关注的 3 件事
2. **技术突破** / **商业化落地**，各按 🇺🇸 美国 / 🇨🇳 中国 分栏
3. 每条新闻**附原文链接**，可点击查看详情
4. 结尾 **今日趋势** 一句话点评

## 推送方式

| 方式 | 说明 |
|---|---|
| **桌面通知（主）** | 每天 08:30 在你 Mac 弹通知并**自动用浏览器打开报告**，链路最短。需要 Mac 开机；没开机则开机后自动补跑。 |
| **微信（备）** | GitHub Actions 云端定时推送，Mac 不开机也能收到，作为兜底。 |

---

## 一、本机桌面通知（推荐，约 2 分钟）

前置：已完成依赖安装（本目录有 `.venv`）和 `.env` 配置（已填好 key）。

```bash
# 1. 安装定时任务（每天 08:30）
bash install_local.sh

# 2. 手动测试一次（会弹通知 + 浏览器打开报告）
bash run.sh
```

之后每天 08:30 自动推送；没开机则开机后几分钟内自动补跑。

- **改时间**：编辑 `com.shuurii.ainews.plist` 里的 `Hour`/`Minute`，再跑一次 `bash install_local.sh`
- **卸载**：`launchctl unload ~/Library/LaunchAgents/com.shuurii.ainews.plist`

## 二、微信备份（GitHub Actions 云端）

云端每天 08:30 生成并推送到微信。若已按上一版配好 GitHub 仓库 + 两个 secret，此通道已在工作；若未配，步骤如下：

1. 本目录推到 GitHub 仓库（public）
2. Settings → Secrets and variables → Actions 添加两个 secret：`DEEPSEEK_API_KEY`、`PUSHPLUS_TOKEN`
3. Actions → Daily AI Briefing → Run workflow 手动触发一次

> 不想要微信了：到 GitHub 仓库 Settings → Secrets 里删掉 `PUSHPLUS_TOKEN` 即可停用。

## 本地调试

```bash
pip install -r requirements.txt
cp .env.example .env    # 填 key
bash run.sh             # 抓取 -> 摘要 -> 桌面通知
```

## 自定义新闻源

编辑 [`sources.py`](sources.py)：每个源一行 `{"name", "url", "region", "topic"}`。
- `region`：`CN`（中国）/ `US`（美国）
- `topic`：`ai`（专注 AI，直接收录）/ `general`（综合源，按 `AI_KEYWORDS` 过滤）

## 成本

- DeepSeek：约 ¥1/月；GitHub Actions 免费；本机定时免费
- 年成本 ≈ ¥10（一次充值）
