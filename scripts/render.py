"""把简报 markdown 渲染成 HTML 页面（Bark 推送与桌面通知共用）。

样式参考 theroboradar.com：青绿主色 + 技术绿/商业橙徽章。
"""
import re
from datetime import datetime
from html import escape

_TAG_RE = re.compile(r"^(🇺🇸|🇨🇳)\s*(技术|商业)\s*(?:·|：|:)?\s*")


def _badge(s: str) -> str:
    """把行首的「🇺🇸 技术」这类标签转成彩色小徽章。"""
    m = _TAG_RE.match(s)
    if m:
        cat = "tech" if m.group(2) == "技术" else "biz"
        return f'<span class="tag {cat}">{m.group(1)} {m.group(2)}</span> ' + s[m.end():]
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
         max-width: 700px; margin: 0 auto; padding: 32px 20px 88px;
         line-height: 1.7; font-size: 16px; color: #1a211f; background: #fbfdfc;
         -webkit-font-smoothing: antialiased; }}
  .meta {{ color: #8a9492; font-size: 13px; letter-spacing: .2px; margin-bottom: 6px; }}
  h1 {{ font-size: 27px; line-height: 1.35; margin: 4px 0 26px; color: #0f2420; }}
  h2 {{ font-size: 19px; margin: 34px 0 14px; padding-left: 12px;
       border-left: 4px solid #007A6D; color: #0f2420; }}

  ol.top3 {{ list-style: none; padding: 0; margin: 0; counter-reset: n; }}
  ol.top3 li {{ position: relative; padding: 16px 18px 16px 54px; margin: 12px 0;
       background: #eef6f4; border-radius: 14px; }}
  ol.top3 li::before {{ counter-increment: n; content: counter(n);
       position: absolute; left: 14px; top: 16px; width: 28px; height: 28px;
       border-radius: 50%; background: #007A6D; color: #fff; font-size: 14px;
       font-weight: 700; display: flex; align-items: center; justify-content: center; }}

  ul {{ list-style: none; padding: 0; margin: 0; }}
  ul li {{ padding: 12px 4px; border-bottom: 1px solid #e6ecea; }}
  ul li:last-child {{ border-bottom: none; }}

  .tag {{ display: inline-block; font-size: 12px; font-weight: 600; line-height: 1;
         padding: 4px 9px; border-radius: 6px; margin-right: 7px; }}
  .tag.tech {{ background: #dcefeb; color: #00655a; }}
  .tag.biz  {{ background: #ffe7dd; color: #bf4318; }}

  a {{ color: #007A6D; text-decoration: none; border-bottom: 1px solid rgba(0,122,109,.35);
      word-break: break-all; }}
  a:hover {{ border-bottom-color: #007A6D; }}

  @media (prefers-color-scheme: dark) {{
    body {{ color: #dde6e4; background: #0f1413; }}
    h1, h2 {{ color: #e8f0ee; }}
    ol.top3 li {{ background: #16211f; }}
    .tag.tech {{ background: #14332c; color: #6fd3c2; }}
    .tag.biz  {{ background: #3a2418; color: #ff9c74; }}
    ul li {{ border-bottom-color: #22302d; }}
    a {{ color: #4fd1bd; border-bottom-color: rgba(79,209,189,.35); }}
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
