"""渲染 report.html（云端流程：推送前先渲染并提交到仓库，供手机点开）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import render_page  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BRIEFING = ROOT / "data" / "briefing.md"
OUT = ROOT / "report.html"


def main() -> None:
    md = BRIEFING.read_text(encoding="utf-8") if BRIEFING.exists() else "# 今日无更新\n\n暂未抓取到新闻。"
    lines = md.strip().splitlines()
    headline = "今日 AI 要闻"
    if lines and lines[0].lstrip().startswith("#"):
        headline = lines[0].lstrip().lstrip("#").strip() or headline
    OUT.write_text(render_page(md, title=headline), encoding="utf-8")
    print(f"已生成 {OUT}")


if __name__ == "__main__":
    main()
