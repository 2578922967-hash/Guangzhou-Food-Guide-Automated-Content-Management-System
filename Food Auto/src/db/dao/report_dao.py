"""
报告生成记录 DAO。
"""

from __future__ import annotations

from typing import Any

from ..connection import get_connection


def create_report_record(payload: dict[str, Any]) -> int:
    """
    创建报告记录，返回 report_id。
    """
    fields = list(payload.keys())
    placeholders = ", ".join("?" for _ in fields)
    sql = f"INSERT INTO reports ({', '.join(fields)}) VALUES ({placeholders})"
    values = [payload[field] for field in fields]
    with get_connection() as conn:
        cursor = conn.execute(sql, values)
        conn.commit()
        return cursor.lastrowid


def get_report(report_id: int) -> dict[str, Any] | None:
    with get_connection(read_only=True) as conn:
        cursor = conn.execute("SELECT * FROM reports WHERE report_id = ?", (report_id,))
        row = cursor.fetchone()
    return dict(row) if row else None


def list_reports(limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
    with get_connection(read_only=True) as conn:
        cursor = conn.execute(
            "SELECT * FROM reports ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset)
        )
        rows = cursor.fetchall()
    return [dict(row) for row in rows]

