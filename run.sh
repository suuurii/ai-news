#!/usr/bin/env bash
# 本地运行：抓取 -> 摘要 -> 生成报告 -> Bark 推送到 iPhone
set -euo pipefail
cd "$(dirname "$0")"

PY=".venv/bin/python"
"$PY" scripts/fetch_news.py
"$PY" scripts/summarize.py
"$PY" scripts/render_report.py
"$PY" scripts/push_bark.py
