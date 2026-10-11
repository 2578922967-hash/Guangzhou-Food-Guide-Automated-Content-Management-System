"""
模板数据访问层。
"""

from __future__ import annotations

import json
from typing import Any, Iterable

from ..connection import get_connection

TEMPLATE_COLUMNS = [
    "template_id",
    "title",
    "keywords",
    "default_format",
    "content",
    "placeholders_json",
    "sample_output",
    "version",
]


def upsert_template(payload: dict[str, Any]) -> None:
    """
    插入或更新模板。
    """
    fields = [field for field in TEMPLATE_COLUMNS if field in payload]
    placeholders = ", ".join("?" for _ in fields)
    assignments = ", ".join(f"{field}=excluded.{field}" for field in fields if field != "template_id")
    sql = (
        f"INSERT INTO templates ({', '.join(fields)}) VALUES ({placeholders}) "
        f"ON CONFLICT(template_id) DO UPDATE SET {assignments}, version = templates.version + 1"
    )
    values = [payload[field] for field in fields]
    with get_connection() as conn:
        conn.execute(sql, values)
        # commit 由上下文管理器自动处理


def get_template(template_id: int) -> dict[str, Any] | None:
    with get_connection(read_only=True) as conn:
        cursor = conn.execute("SELECT * FROM templates WHERE template_id = ?", (template_id,))
        row = cursor.fetchone()
    return dict(row) if row else None


def list_templates(filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    filters = filters or {}
    sql = "SELECT * FROM templates"
    conditions: list[str] = []
    params: list[Any] = []
    if template_ids := filters.get("template_ids"):
        placeholders = ", ".join("?" for _ in template_ids)
        conditions.append(f"template_id IN ({placeholders})")
        params.extend(template_ids)
    if keyword := filters.get("keyword"):
        conditions.append("(title LIKE ? OR keywords LIKE ?)")
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY template_id"

    with get_connection(read_only=True) as conn:
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
    return [dict(row) for row in rows]


def delete_template(template_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM templates WHERE template_id = ?", (template_id,))
        # commit 由上下文管理器自动处理
        rowcount = cursor.rowcount
    return rowcount > 0


def seed_templates(records: Iterable[dict[str, Any]]) -> None:
    """
    批量写入模板种子数据，存在则忽略。
    """
    sql = (
        "INSERT INTO templates (template_id, title, keywords, default_format, content, placeholders_json, sample_output, version) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(template_id) DO NOTHING"
    )
    with get_connection() as conn:
        conn.executemany(
            sql,
            [
                (
                    record["template_id"],
                    record["title"],
                    record.get("keywords", ""),
                    record["default_format"],
                    record["content"],
                    json.dumps(record.get("placeholders", {}), ensure_ascii=False),
                    record.get("sample_output"),
                    record.get("version", 1),
                )
                for record in records
            ],
        )
        conn.commit()

