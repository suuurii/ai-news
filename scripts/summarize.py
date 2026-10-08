"""调用 DeepSeek 把抓取的新闻浓缩成 5 分钟简报。

读取 data/news.json，生成 markdown 简报写入 data/briefing.md。
"""
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DEEPSEEK_API_KEY  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
NEWS_FILE = DATA_DIR / "news.json"
OUT = DATA_DIR / "briefing.md"

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

SYSTEM_PROMPT = """你是一名专业的 AI 行业分析师，负责为读者编写一份「精简」的每日 AI 简报，只挑最重要的 5–10 条。

要求：
1. 只基于我提供的新闻列表撰写，不要编造新闻里没有的事实。
2. 第一行是标题（# 开头，10–20 字，概括今日最值得关注的一条）。
3. 「今日速览（Top 3）」：选出最值得关注的 3 件事，编号列出，每条一行「**标题** —— 一句话要点，[原文](链接)」。
4. 「其他值得关注」：再选 2–7 条次重要的（全文合计 5–10 条），每条一行，格式「- 🇺🇸/🇨🇳 技术/商业 · 一句话要点，[原文](链接)」。
   - 「技术」：新模型发布、能力提升、论文、开源、芯片算力等；「商业」：产品上线、落地案例、融资、合作等。
5. 每条突出「是什么 + 能实现什么效果 / 商业价值」，面向非技术深度的从业者，避免堆砌参数。
6. 每条末尾必须附上可点击原文链接 [原文](链接)，不要遗漏。
7. 结尾「今日趋势」一句话点评。
8. 全文控制在 500 字左右（2–3 分钟读完），宁可少而精，不要凑数。
9. 输出为 Markdown。
"""


def build_user_prompt(news: list[dict]) -> str:
    lines = ["以下是今天抓取到的 AI 相关新闻（按时间倒序，最多 20 条）：", ""]
    for i, n in enumerate(news[:20], 1):
        region = "中国" if n["region"] == "CN" else "美国"
        lines.append(f"{i}. [{region}/{n['source']}] {n['title']}")
        if n.get("summary"):
            lines.append(f"   摘要：{n['summary']}")
        lines.append(f"   链接：{n['link']}")
        lines.append("")
    return "\n".join(lines)


def _fallback(news: list[dict]) -> str:
    """DeepSeek 不可用时，退化为直接列标题，保证推送不中断。"""
    lines = ["# 今日 AI 要闻速览", ""]
    for region, label in (("CN", "🇨🇳 中国"), ("US", "🇺🇸 美国")):
        lines.append(f"## {label}")
        rows = [n for n in news if n["region"] == region][:6]
        if not rows:
            lines.append("（今日无）")
        for n in rows:
            lines.append(f"- [{n['title']}]({n['link']})（{n['source']}）")
        lines.append("")
    return "\n".join(lines)


def call_deepseek(user_prompt: str) -> str:
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 3000,
        "stream": False,
    }
    resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def main() -> None:
    if not DEEPSEEK_API_KEY:
        print("缺少 DEEPSEEK_API_KEY，跳过摘要", file=sys.stderr)
        sys.exit(2)

    news = json.loads(NEWS_FILE.read_text(encoding="utf-8")) if NEWS_FILE.exists() else []
    if not news:
        OUT.write_text("# 今日无更新\n\n暂未抓取到新的 AI 新闻。", encoding="utf-8")
        print("无新闻，写入空简报")
        return

    try:
        body = call_deepseek(build_user_prompt(news))
    except Exception as e:  # noqa: BLE001
        body = _fallback(news)
        print(f"DeepSeek 调用失败，使用兜底摘要：{e}", file=sys.stderr)

    OUT.write_text(body, encoding="utf-8")
    print(body)


if __name__ == "__main__":
    main()
