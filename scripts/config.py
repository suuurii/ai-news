"""读取环境变量；本地开发可用 .env 文件兜底。"""
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip()
PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN", "").strip()
BARK_KEY = os.environ.get("BARK_KEY", "").strip()

CN_TZ = timezone(timedelta(hours=8))

_WEEKDAYS_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def beijing_now() -> datetime:
    """当前北京时间。"""
    return datetime.now(CN_TZ)


def weekday_cn(dt: datetime) -> str:
    return _WEEKDAYS_CN[dt.weekday()]
