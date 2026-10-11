"""
SQLite 连接与初始化工具。
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from ..config import settings

SCHEMA_FILE = Path(__file__).with_name("schema.sql")


# get_connection 已改为上下文管理器，保留此函数以兼容旧代码
def get_connection_legacy(read_only: bool = False) -> sqlite3.Connection:
    """
    获取 SQLite 连接（旧版，不推荐使用）。
    推荐使用 get_connection 上下文管理器。
    """
    db_path = settings.DB_PATH
    if read_only:
        uri = f"file:{db_path}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, detect_types=sqlite3.PARSE_DECLTYPES)
    else:
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_connection(read_only: bool = False) -> Iterator[sqlite3.Connection]:
    """
    提供连接上下文管理器，自动提交/关闭。
    """
    db_path = settings.DB_PATH
    if read_only:
        uri = f"file:{db_path}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, detect_types=sqlite3.PARSE_DECLTYPES)
    else:
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        if not read_only:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def get_cursor(read_only: bool = False) -> Iterator[sqlite3.Cursor]:
    """
    提供游标上下文管理器，自动提交/回滚。
    """
    with get_connection(read_only=read_only) as conn:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()


def init_db(schema_path: Path | None = None) -> None:
    """
    初始化数据库（执行建表脚本）。
    """
    script_path = schema_path or SCHEMA_FILE
    with get_connection() as conn, open(script_path, "r", encoding="utf-8") as fh:
        conn.executescript(fh.read())

