# AI 每日简报（5 分钟 · 中美聚焦）

每天早晨 **08:30** 自动生成一份中文 AI 行业简报，聚焦**中国与美国**，覆盖：

- **技术突破** —— 最新模型发布及其可实现的效果
- **商业化落地** —— 技术与产业结合的产品、案例、融资等

推送到你的 **iPhone**（Bark 通知），点一下通知即可打开带**原文链接**的完整报告。

## 报告内容

1. 开头 **今日速览（Top 3）**
2. **其他值得关注**：补齐到全文共 5–10 条（标 🇺🇸/🇨🇳 + 技术/商业）
3. 每条新闻**附原文链接**，点击查看详情
4. 结尾 **今日趋势** 一句话点评

## 架构

```
GitHub Actions（云端，每天 08:30）
   └─ 抓取中美 RSS → DeepSeek 摘要 → 生成 HTML 报告并提交仓库 → Bark 推送 iPhone
```

纯云端，**不依赖 Mac 开机**。

## 一次性配置（约 5 分钟）

1. **DeepSeek**：注册 [platform.deepseek.com](https://platform.deepseek.com) → 支付宝充 ¥10 → 创建 API Key。
2. **Bark**：iPhone 在 App Store 搜 **Bark**（作者 Finb，免费开源）安装 → 打开，首页有一串「推送 Key」（形如 `https://api.day.app/xxxx` 或纯 key）。
3. GitHub 仓库 → **Settings → Secrets and variables → Actions**，添加两个 secret：
   - `DEEPSEEK_API_KEY`
   - `BARK_KEY`（填上面 Bark 的 key）
4. 仓库 → **Actions → Daily AI Briefing → Run workflow** 手动触发一次，iPhone 应收到通知。

## 本地调试（可选）

```bash
pip install -r requirements.txt
cp .env.example .env    # 填 key
python scripts/fetch_news.py
python scripts/summarize.py
python scripts/render_report.py
python scripts/push_bark.py
```

## 自定义新闻源

编辑 [`sources.py`](sources.py)：每个源一行 `{"name", "url", "region", "topic"}`。
- `region`：`CN`（中国）/ `US`（美国）
- `topic`：`ai`（专注 AI，直接收录）/ `general`（综合源，按 `AI_KEYWORDS` 过滤）

## 改推送时间

编辑 [`.github/workflows/daily.yml`](.github/workflows/daily.yml) 的 `cron`（UTC 时间，`30 0 * * *` = 北京时间 08:30）。

## 成本

DeepSeek 约 ¥1/月；GitHub Actions 免费；Bark 免费。年成本 ≈ ¥10。
