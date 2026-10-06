# AI 每日简报（5 分钟 · 中美聚焦）

每天早晨自动生成一份中文 AI 行业简报，聚焦**中国与美国**，覆盖两条主线：

- **技术突破** —— 最新模型发布及其可实现的效果
- **商业化落地** —— 技术与产业结合的产品、案例、融资等

并自动推送到你的**微信**。全程跑在 GitHub 云端，**无需自己的电脑开机**。

## 工作流程

```
GitHub Actions（每天北京时间 08:30 触发）
   └─ fetch_news.py    抓取 11 个中美 RSS 源，取近 24 小时新闻
   └─ summarize.py     调用 DeepSeek 浓缩成 5 分钟简报
   └─ push.py          通过 PushPlus 推送到微信
```

## 一次性准备（约 10 分钟）

### 1. 拿到两把「钥匙」

| 服务 | 用途 | 获取方式 | 费用 |
|---|---|---|---|
| DeepSeek | 摘要写简报 | 注册 [platform.deepseek.com](https://platform.deepseek.com) → 支付宝充值 ¥10 → 「API Keys」创建，复制 `sk-...` | 约 ¥1/月 |
| PushPlus | 推送到微信 | 打开 [pushplus.plus](https://www.pushplus.plus) → 微信扫码登录 → 首页复制你的 token | 免费 |

### 2. 建 GitHub 仓库

1. 把本目录上传到 GitHub 新建仓库（推荐 **public**，Actions 分钟免费无上限）。
2. 进仓库 **Settings → Secrets and variables → Actions → New repository secret**，添加两个 secret：
   - `DEEPSEEK_API_KEY`
   - `PUSHPLUS_TOKEN`

> 密钥存在 GitHub Secrets 里，不写进代码，公开仓库也安全。

### 3. 首次手动测试

仓库 **Actions** 页 → 左侧点 **Daily AI Briefing** → **Run workflow** → **Run workflow**。跑完后微信应收到一条简报。

### 4. 完成

之后每天 **08:30** 自动推送。定时任务要求该 workflow 文件在默认分支（`main`）上。

## 本地调试（可选）

```bash
pip install -r requirements.txt
cp .env.example .env    # 用编辑器填入真实 key
bash run.sh             # 依次执行：抓取 -> 摘要 -> 推送
```

## 自定义新闻源

编辑 [`sources.py`](sources.py)：每个源一行 `{"name", "url", "region", "topic"}`。

- `region`：`CN`（中国）/ `US`（美国）
- `topic`：`ai`（专注 AI，直接收录）/ `general`（综合源，按 `AI_KEYWORDS` 过滤）

增删后提交即可。

## 常见问题

- **没收到推送**：到 Actions 运行日志看是哪一步失败。常见原因：secret 名拼错、某个 RSS 地址失效（在 `sources.py` 里换一个源即可）。
- **想改推送时间**：编辑 [`.github/workflows/daily.yml`](.github/workflows/daily.yml) 的 `cron`。它是 UTC 时间，`30 0 * * *` 表示北京时间 08:30。
- **想换推送渠道**：改 [`scripts/push.py`](scripts/push.py)，换成 Server酱 / 企业微信群机器人等。

## 成本

- DeepSeek：约 ¥1/月
- GitHub Actions：免费
- PushPlus：免费额度足够（每天 1 条）

年成本 ≈ ¥10（一次充值）。
