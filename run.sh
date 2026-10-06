#!/usr/bin/env bash
# 本地一次性运行：抓取 -> 摘要 -> 推送到微信
set -euo pipefail
cd "$(dirname "$0")"

python scripts/fetch_news.py
python scripts/summarize.py
python scripts/push.py
