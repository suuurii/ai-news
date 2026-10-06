"""抓取中美 AI 新闻源，输出近 24 小时（不足则放宽到 48 小时）的新闻列表。

结果写入 data/news.json，供 summarize.py 读取。
"""
import json
import re
import socket
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser

socket.setdefaulttimeout(30)  # 防止某个源卡住拖垮整条任务

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sources import SOURCES, matches_ai  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT = DATA_DIR / "news.json"

CN_TZ = timezone(timedelta(hours=8))
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def _parse_time(entry) -> datetime | None:
    for key in ("published_parsed", "updated_parsed", "created_parsed"):
        t = entry.get(key)
        if t:
            return datetime(*t[:6], tzinfo=timezone.utc)
    return None


def _clean_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _norm_key(title: str) -> str:
    # 去掉标点空格、转小写、截断，用于标题去重
    return re.sub(r"[\W_]+", "", title.lower())[:40]


def fetch_all() -> list[dict]:
    now = datetime.now(CN_TZ)
    window = timedelta(hours=24)
    items: list[dict] = []

    for src in SOURCES:
        try:
            feed = feedparser.parse(src["url"], agent=USER_AGENT)
        except Exception as e:  # noqa: BLE001
            print(f"[skip] {src['name']}: {e}", file=sys.stderr)
            continue
        if feed.bozo and not feed.entries:
            print(f"[skip] {src['name']}: 解析失败", file=sys.stderr)
            continue

        for e in feed.entries:
            title = _clean_html(e.get("title", ""))
            link = e.get("link", "")
            summary = _clean_html(e.get("summary", "") or e.get("description", ""))
            if not title or not link:
                continue
            if src["topic"] == "general" and not matches_ai(title + " " + summary):
                continue
            items.append(
                {
                    "title": title,
                    "link": link,
                    "summary": summary[:300],
                    "source": src["name"],
                    "region": src["region"],
                    "published": _parse_time(e),
                }
            )

    # 标题去重：同一事件多源报道只留一条
    seen: dict[str, dict] = {}
    deduped: list[dict] = []
    for it in items:
        k = _norm_key(it["title"])
        dup = any(k in kk or kk in k for kk in seen)
        if dup:
            continue
        seen[k] = it
        deduped.append(it)

    # 过滤时间窗口（无时间信息的条目保留）
    fresh = [it for it in deduped if not it["published"] or now - it["published"] <= window]
    if len(fresh) < 5:  # 太少就放宽到 48 小时
        wide = timedelta(hours=48)
        fresh = [it for it in deduped if not it["published"] or now - it["published"] <= wide]

    fresh.sort(key=lambda x: x["published"] or datetime(1970, 1, 1, tzinfo=timezone.utc), reverse=True)
    return fresh


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    news = fetch_all()
    OUT.write_text(json.dumps(news, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"抓取到 {len(news)} 条新闻，已写入 {OUT}")
    for n in news[:10]:
        print(f"  [{n['region']}] {n['title'][:50]}")


if __name__ == "__main__":
    main()
