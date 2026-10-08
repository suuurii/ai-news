"""本机桌面通知：生成 HTML 报告，发 macOS 通知并在浏览器打开（本地测试用，非主通道）。"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import render_page  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BRIEFING = ROOT / "data" / "briefing.md"
HTML_OUT = ROOT / "report.html"


def main() -> None:
    md = BRIEFING.read_text(encoding="utf-8") if BRIEFING.exists() else "# 今日无更新\n\n暂未抓取到新闻。"
    lines = md.strip().splitlines()
    headline = "今日 AI 要闻"
    if lines and lines[0].lstrip().startswith("#"):
        headline = lines[0].lstrip().lstrip("#").strip() or headline

    HTML_OUT.write_text(render_page(md, title=headline), encoding="utf-8")

    preview = " ".join(x.strip() for x in lines[1:6] if x.strip())[:120]
    _notify(headline, preview)
    _open(HTML_OUT)
    print(f"已生成 {HTML_OUT} 并发送通知")


def _notify(headline: str, preview: str) -> None:
    try:
        subtitle = headline.replace('"', "'")[:60]
        msg = preview.replace('"', "'")
        script = f'display notification "{msg}" with title "AI 每日简报" subtitle "{subtitle}"'
        subprocess.run(["osascript", "-e", script], check=False, timeout=15)
    except Exception as e:  # noqa: BLE001
        print(f"[notify] 通知发送失败（可忽略）：{e}", file=sys.stderr)


def _open(path: Path) -> None:
    try:
        subprocess.run(["open", str(path)], check=False, timeout=15)
    except Exception as e:  # noqa: BLE001
        print(f"[open] 打开浏览器失败（可忽略）：{e}", file=sys.stderr)


if __name__ == "__main__":
    main()
