#!/usr/bin/env bash
# 本地运行：抓取 -> 摘要 -> 桌面通知 + 浏览器打开报告
set -euo pipefail
cd "$(dirname "$0")"

PY=".venv/bin/python"
"$PY" scripts/fetch_news.py
"$PY" scripts/summarize.py
"$PY" scripts/notify.py
