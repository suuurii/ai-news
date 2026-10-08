"""把简报 markdown 渲染成 HTML 页面（Bark 推送与桌面通知共用）。"""
import re
from datetime import datetime
from html import escape

_TAG_RE = re.compile(r"^(🇺🇸|🇨🇳)\s*(技术|商业)\s*(?:·|：|:)?\s*")


def _badge(s: str) -> str:
    """把行首的「🇺🇸 技术」这类标签转成小徽章。"""
    m = _TAG_RE.match(s)
    if m:
        return f'<span class="tag">{m.group(1)} {m.group(2)}</span> ' + s[m.end():]
    return s


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
                out.append('<ol class="top3">')
            text = re.sub(r"^\d+\.\s", "", s)
            out.append(f"<li>{text}</li>")
        elif line.startswith("- "):
            if list_type != "ul":
                close_list()
                list_type = "ul"
                out.append("<ul>")
            out.append(f"<li>{_badge(s[2:])}</li>")
        else:
            close_list()
            out.append(f"<p>{s}</p>")

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
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
         max-width: 680px; margin: 0 auto; padding: 30px 20px 80px;
         line-height: 1.75; font-size: 16px; color: #1b1b1f; background: #fff;
         -webkit-font-smoothing: antialiased; }}
  .meta {{ color: #999; font-size: 13px; margin-bottom: 4px; }}
  h1 {{ font-size: 26px; line-height: 1.35; margin: 6px 0 24px; }}
  h2 {{ font-size: 19px; margin: 34px 0 14px; padding-bottom: 8px;
       border-bottom: 2px solid #4f8cff; }}
  h2.section {{ border-left: 4px solid #4f8cff; padding-left: 12px; border-bottom: none; }}

  ol.top3 {{ list-style: none; padding: 0; margin: 0; counter-reset: n; }}
  ol.top3 li {{ position: relative; padding: 16px 16px 16px 52px; margin: 12px 0;
       background: #f4f6fb; border-radius: 12px; }}
  ol.top3 li::before {{ counter-increment: n; content: counter(n);
       position: absolute; left: 14px; top: 16px; width: 26px; height: 26px;
       border-radius: 50%; background: #4f8cff; color: #fff; font-size: 14px;
       font-weight: 700; display: flex; align-items: center; justify-content: center; }}

  ul {{ list-style: none; padding: 0; margin: 0; }}
  ul li {{ padding: 12px 2px; border-bottom: 1px solid rgba(128,128,128,.15); }}
  ul li:last-child {{ border-bottom: none; }}

  .tag {{ display: inline-block; font-size: 12px; font-weight: 600; line-height: 1;
         padding: 3px 8px; border-radius: 6px; background: #e7ecfb; color: #3f62e0;
         margin-right: 6px; }}
  a {{ color: #0a66c2; text-decoration: none; border-bottom: 1px solid rgba(10,102,194,.35);
      word-break: break-all; }}
  a:hover {{ border-bottom-color: #0a66c2; }}

  @media (prefers-color-scheme: dark) {{
    body {{ color: #e6e6ea; background: #111114; }}
    ol.top3 li {{ background: #1c1d24; }}
    .tag {{ background: #2a3350; color: #9db4ff; }}
    ul li {{ border-bottom-color: rgba(255,255,255,.12); }}
    a {{ color: #7ab7ff; border-bottom-color: rgba(122,183,255,.35); }}
  }}
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
