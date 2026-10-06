"""把简报推送到微信（PushPlus）。

读取 data/briefing.md，标题取第一行，正文其余部分作为推送内容。
"""
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import PUSHPLUS_TOKEN, beijing_now, weekday_cn  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BRIEFING = ROOT / "data" / "briefing.md"

PUSHPLUS_URL = "https://www.pushplus.plus/send"


def main() -> None:
    if not PUSHPLUS_TOKEN:
        print("缺少 PUSHPLUS_TOKEN，跳过推送", file=sys.stderr)
        sys.exit(2)

    body = BRIEFING.read_text(encoding="utf-8").strip()
    lines = body.splitlines()

    headline = "今日 AI 要闻"
    content_lines = lines
    if lines and lines[0].lstrip().startswith("#"):
        headline = lines[0].lstrip().lstrip("#").strip() or headline
        content_lines = lines[1:]
    content = "\n".join(content_lines).strip()

    now = beijing_now()
    title = f"【AI 简报】{now.strftime('%m-%d')} {weekday_cn(now)}｜{headline}"

    resp = requests.post(
        PUSHPLUS_URL,
        json={"token": PUSHPLUS_TOKEN, "title": title, "content": content, "template": "markdown"},
        timeout=30,
    )
    data = resp.json()
    if data.get("code") == 200:
        print("推送成功")
    else:
        print(f"推送失败：{data}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
