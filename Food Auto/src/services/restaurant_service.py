"""
餐厅业务逻辑。
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Any, Iterable

from ..config import settings
from ..db.dao import restaurant_dao
from ..utils import validators

logger = logging.getLogger(__name__)


def create_restaurant(payload: dict[str, Any]) -> None:
    record = validators.normalize_restaurant_record(payload)
    restaurant_dao.insert_restaurant(record)


def bulk_import_from_csv(
    csv_path: Path,
    *,
    update_existing: bool = True,
    dry_run: bool = False,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """
    从 CSV 导入餐厅数据。
    返回导入统计。
    """
    csv_path = settings.resolve_path(csv_path)
    inserted = 0
    updated = 0
    skipped = 0
    errors: list[str] = []
    records: list[dict[str, Any]] = []

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV 文件不存在: {csv_path}")

    with open(csv_path, "r", encoding=encoding) as fh:
        reader = csv.DictReader(fh)
        for idx, row in enumerate(reader, start=2):  # 包含表头
            try:
                record = validators.normalize_restaurant_record(row)
                records.append(record)
            except ValueError as exc:
                logger.warning("第 %s 行数据校验失败: %s", idx, exc)
                errors.append(f"第 {idx} 行: {exc}")
                skipped += 1

    if dry_run:
        return {
            "inserted": 0,
            "updated": 0,
            "skipped": skipped,
            "errors": errors,
            "dry_run": True,
            "total": len(records),
        }

    if records:
        if update_existing:
            inserted, updated = restaurant_dao.bulk_upsert(records)
        else:
            for record in records:
                try:
                    restaurant_dao.insert_restaurant(record)
                    inserted += 1
                except Exception as exc:  # sqlite3.IntegrityError
                    logger.warning("插入失败（可能重复）: %s", exc)
                    errors.append(str(exc))
                    skipped += 1

    return {
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped,
        "errors": errors,
        "dry_run": False,
        "total": len(records),
    }


def search_restaurants(
    filters: dict[str, Any], 
    limit: int = 100, 
    offset: int = 0,
    order_by: str | None = None
) -> list[dict[str, Any]]:
    return restaurant_dao.search(filters, limit=limit, offset=offset, order_by=order_by)


def count_restaurants(filters: dict[str, Any]) -> int:
    """统计符合条件的餐厅数量。"""
    return restaurant_dao.count_restaurants(filters)


def update_restaurant(shop_id: str, fields: dict[str, Any]) -> bool:
    clean_fields = validators.normalize_restaurant_record(fields, partial=True)
    return restaurant_dao.update(shop_id, clean_fields)


def soft_delete_restaurant(shop_id: str) -> bool:
    return restaurant_dao.soft_delete(shop_id)


def list_top_value_for_money(
    *,
    price_cap: float,
    top_n: int = 5,
) -> list[dict[str, Any]]:
    filters = {"max_avg_price": price_cap, "is_active": True}
    restaurants = restaurant_dao.search(filters, limit=top_n * 3, order_by="(taste_score / NULLIF(avg_price, 0)) DESC")

    result = []
    for row in restaurants:
        price = row.get("avg_price") or 0
        taste = row.get("taste_score") or 0
        value_index = taste / price if price else 0
        row["value_index"] = round(value_index, 2)
        result.append(row)
        if len(result) >= top_n:
            break
    return result

