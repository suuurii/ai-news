"""把简报 markdown 渲染成 HTML 页面（Bark 推送与桌面通知共用）。"""
import re
from datetime import datetime
from html import escape


def md_to_html(md: str) -> str:
    out = []
    list_type = None

    def close_list():
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            close_list()
            continue

        s = escape(line)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)

        if line.startswith("# "):
            close_list()
            out.append(f"<h1>{s[2:]}</h1>")
        elif line.startswith("## "):
            close_list()
            out.append(f"<h2>{s[3:]}</h2>")
        elif line.startswith("▎"):
            close_list()
            out.append(f'<h2 class="section">{s}</h2>')
        elif re.match(r"^\d+\.\s", line):
            if list_type != "ol":
                close_list()
                list_type = "ol"
                out.append("<ol>")
            text = re.sub(r"^\d+\.\s", "", s)
            out.append(f"<li>{text}</li>")
        elif line.startswith("- "):
            if list_type != "ul":
                close_list()
                list_type = "ul"
                out.append("<ul>")
            out.append(f"<li>{s[2:]}</li>")
        else:
            close_list()
            cls = "region" if re.match(r"^[🇺🇸🇨🇳]", line) else ""
            out.append(f'<p class="{cls}">{s}</p>')

    close_list()
    return "\n".join(out)


_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
         max-width: 720px; margin: 0 auto; padding: 32px 20px 72px;
         line-height: 1.75; color: #1c1c1e; background: #fff; }}
  @media (prefers-color-scheme: dark) {{
    body {{ color: #e5e5e7; background: #101012; }}
    a {{ color: #6cb0ff; }}
  }}
  .meta {{ color: #999; font-size: 13px; margin-bottom: 6px; }}
  h1 {{ font-size: 24px; margin: 6px 0 22px; line-height: 1.35; }}
  h2 {{ font-size: 18px; margin: 30px 0 12px; padding-bottom: 6px;
       border-bottom: 1px solid rgba(128,128,128,.25); }}
  h2.section {{ border-left: 4px solid #4f8cff; padding-left: 10px; border-bottom: none; }}
  p.region {{ font-weight: 600; margin: 16px 0 6px; }}
  li {{ margin: 8px 0; }}
  a {{ color: #0a66c2; text-decoration: none; word-break: break-all; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<div class="meta">{date}</div>
{content}
</body>
</html>"""


def render_page(md: str, title: str = "今日 AI 要闻", date: str = "") -> str:
    if not date:
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
    return _TEMPLATE.format(
        title=escape(title),
        date=f"AI 每日简报 · {date}",
        content=md_to_html(md),
    )
