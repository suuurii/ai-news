"""通过 Bark 推送到 iPhone：通知含标题 + 简短 Top3 摘要，点击打开完整 HTML 报告。"""
import os
import re
import sys
import urllib.parse
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import BARK_KEY  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BRIEFING = ROOT / "data" / "briefing.md"

DEFAULT_REPORT_URL = "https://raw.githubusercontent.com/suuurii/ai-news/main/report.html"


def _plain(text: str) -> str:
    """去掉 markdown 链接/加粗/符号，得到干净短文本。"""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    text = re.sub(r"[*#▎`]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    if not BARK_KEY:
        print("缺少 BARK_KEY，跳过推送", file=sys.stderr)
        sys.exit(2)

    md = BRIEFING.read_text(encoding="utf-8") if BRIEFING.exists() else "# 今日无更新\n\n暂未抓取到新闻。"
    lines = md.strip().splitlines()

    headline = "今日 AI 要闻"
    if lines and lines[0].lstrip().startswith("#"):
        headline = lines[0].lstrip().lstrip("#").strip() or headline

    # 从 Top3 里取干净标题，拼成简短正文（避免 URL 过长被 Bark 拒绝）
    top3 = []
    for line in lines:
        if re.match(r"^[1-3]\.\s", line):
            t = _plain(line.split("——")[0].split("—")[0])
            t = re.sub(r"^\d+\.\s*", "", t)  # 去掉原有序号，避免「1. 1.」双序号
            top3.append(t)
        if len(top3) >= 3:
            break
    if top3:
        body = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(top3))
    else:
        body = _plain(" ".join(lines[1:6]))
    body = body[:200]

    report_url = os.environ.get("REPORT_URL", DEFAULT_REPORT_URL)

    base = BARK_KEY if BARK_KEY.startswith("http") else f"https://api.day.app/{BARK_KEY}"
    url = f"{base}/{urllib.parse.quote(headline)}/{urllib.parse.quote(body)}"
    params = {
        "url": report_url,        # 点击通知跳转
        "group": "AI每日简报",    # 通知分组
        "level": "active",        # 提醒级别
        "isArchive": "1",         # 归档到历史
    }
    resp = requests.get(url, params=params, timeout=30)
    print("Bark 响应：", resp.text)

    ok = False
    try:
        ok = resp.json().get("code") == 200
    except Exception:  # noqa: BLE001
        ok = resp.status_code == 200
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
