"""
应用配置模块，提供数据库路径、模板目录等通用设置。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# 加载 .env（若存在）
load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
TEMPLATE_SEED_DIR = BASE_DIR / "templates_seed"
OUTPUT_DIR = Path(os.getenv("GZ_FOODCMS_OUTPUT_DIR", BASE_DIR / "output"))
LOG_DIR = Path(os.getenv("GZ_FOODCMS_LOG_DIR", BASE_DIR / "logs"))

# SQLite 数据库路径（默认为项目根目录下）
DB_PATH = Path(os.getenv("GZ_FOODCMS_DB_PATH", BASE_DIR / "gz_foodcms.db"))

DEFAULT_LOG_LEVEL = os.getenv("GZ_FOODCMS_LOG_LEVEL", "INFO")

for directory in (DATA_DIR, TEMPLATE_SEED_DIR, OUTPUT_DIR, LOG_DIR):
    directory.mkdir(parents=True, exist_ok=True)


def resolve_path(path: str | os.PathLike[str]) -> Path:
    """
    将输入路径解析为绝对路径。
    """
    candidate = Path(path)
    return candidate if candidate.is_absolute() else (BASE_DIR / candidate).resolve()

