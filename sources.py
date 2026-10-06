"""新闻源清单。

每个源字段：
    name    显示名
    url     RSS 地址
    region  地区：CN（中国）/ US（美国）
    topic   "ai"（专注 AI，直接收录）或 "general"（综合科技源，需按关键词过滤）

想增删新闻源，直接改下面这个列表即可。
"""

import re

SOURCES = [
    # ---- 中国 ----
    {"name": "量子位", "url": "https://www.qbitai.com/feed", "region": "CN", "topic": "ai"},
    {"name": "雷锋网", "url": "https://www.leiphone.com/feed", "region": "CN", "topic": "ai"},
    {"name": "InfoQ 中文", "url": "https://www.infoq.cn/feed", "region": "CN", "topic": "general"},
    {"name": "少数派", "url": "https://sspai.com/feed", "region": "CN", "topic": "general"},

    # ---- 美国 ----
    {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "region": "US", "topic": "ai"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "region": "US", "topic": "ai"},
    {"name": "Ars Technica AI", "url": "https://arstechnica.com/ai/feed/", "region": "US", "topic": "ai"},
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/", "region": "US", "topic": "general"},
    {"name": "Hugging Face", "url": "https://huggingface.co/blog/feed.xml", "region": "US", "topic": "ai"},
    {"name": "Google DeepMind", "url": "https://deepmind.google/blog/rss.xml", "region": "US", "topic": "ai"},
    {"name": "OpenAI News", "url": "https://openai.com/news/rss.xml", "region": "US", "topic": "ai"},

    # 可选：VentureBeat 常被 Cloudflare 限流（429），需要时再打开
    # {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "region": "US", "topic": "ai"},
]

# 综合源（topic="general"）里，只有标题/摘要命中这些关键词的条目才保留。
# 中文词用子串匹配，英文词用整词匹配（避免 "ai" 误匹配到 available/said 等）。
AI_KEYWORDS = [
    "人工智能", "大模型", "模型", "智能体", "生成式", "aigc", "深度学习", "机器学习",
    "算法", "芯片", "算力", "机器人", "自动驾驶", "多模态", "推理", "开源", "神经网络",
    "语音识别", "计算机视觉", "机器视觉",
    "ai", "gpt", "llm", "chatgpt", "agent", "openai", "claude", "anthropic",
    "google", "microsoft", "nvidia", "deepseek", "neural", "multimodal",
    "inference", "copilot", "foundation model",
    "谷歌", "微软", "英伟达", "字节", "阿里", "百度", "腾讯", "华为",
]


def _is_ascii(s: str) -> bool:
    return all(ord(c) < 128 for c in s)


def matches_ai(text: str) -> bool:
    """判断一段文本是否与 AI 相关。中文关键词子串匹配，英文关键词整词匹配。"""
    if not text:
        return False
    t = text.lower()
    for kw in AI_KEYWORDS:
        k = kw.lower()
        if _is_ascii(k):
            if re.search(rf"\b{re.escape(k)}\b", t):
                return True
        else:
            if k in t:
                return True
    return False
