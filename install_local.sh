#!/usr/bin/env bash
# 安装本机定时任务：每天 08:30 在 Mac 上弹出 AI 简报（桌面通知 + 浏览器打开报告）
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$DIR/com.shuurii.ainews.plist"
DST="$HOME/Library/LaunchAgents/com.shuurii.ainews.plist"

mkdir -p "$HOME/Library/LaunchAgents"
mkdir -p "$DIR/data"

cp "$SRC" "$DST"
launchctl unload "$DST" 2>/dev/null || true
launchctl load "$DST"

echo "✅ 已安装每日定时任务：每天 08:30 在你 Mac 弹出 AI 简报"
echo "   手动测试一次：bash \"$DIR/run.sh\""
echo "   想卸载：launchctl unload \"$DST\""
