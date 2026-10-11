"""
餐厅数据访问层。
"""

from __future__ import annotations

from typing import Any, Iterable, Sequence

from ..connection import get_connection

RESTAURANT_COLUMNS = [
    "shop_id",
    "name",
    "reviews",
    "avg_price",
    "category",
    "business_district",
    "address",
    "recommended_dish_1",
    "recommended_dish_2",
    "recommended_dish_3",
    "taste_score",
    "environment_score",
    "service_score",
    "star_level",
    "url",
    "is_active",
]


def _row_to_dict(row: Any) -> dict[str, Any]:
    return dict(row) if row is not None else {}


def insert_restaurant(payload: dict[str, Any]) -> None:
    """
    插入单条餐厅记录。
    """
    fields = [field for field in RESTAURANT_COLUMNS if field in payload]
    values = [payload[field] for field in fields]
    placeholders = ", ".join("?" for _ in fields)
    columns = ", ".join(fields)
    sql = f"INSERT INTO restaurants ({columns}) VALUES ({placeholders})"
    with get_connection() as conn:
        conn.execute(sql, values)
        # commit 由上下文管理器自动处理


def bulk_upsert(records: Iterable[dict[str, Any]]) -> tuple[int, int]:
    """
    批量插入或更新餐厅数据。
    返回 (插入数量, 更新数量)。
    """
    insert_count = 0
    update_count = 0
    with get_connection() as conn:
        for payload in records:
            fields = [field for field in RESTAURANT_COLUMNS if field in payload and field != "is_active"]
            assignments = ", ".join(f"{field}=excluded.{field}" for field in fields if field != "shop_id")
            placeholders = ", ".join("?" for _ in RESTAURANT_COLUMNS)
            values = [payload.get(field) for field in RESTAURANT_COLUMNS]
            sql = (
                "INSERT INTO restaurants ("
                + ", ".join(RESTAURANT_COLUMNS)
                + ") VALUES ("
                + placeholders
                + ") ON CONFLICT(shop_id) DO UPDATE SET "
                + assignments
            )
            cursor = conn.execute(sql, values)
            if cursor.rowcount == 1:
                insert_count += 1
            else:
                update_count += 1
        # commit 由上下文管理器自动处理
    return insert_count, update_count


def get_by_shop_id(shop_id: str) -> dict[str, Any] | None:
    with get_connection(read_only=True) as conn:
        cursor = conn.execute("SELECT * FROM restaurants WHERE shop_id = ?", (shop_id,))
        row = cursor.fetchone()
    return _row_to_dict(row) if row else None


def _build_where_clause(filters: dict[str, Any]) -> tuple[str, list[Any]]:
    """构建 WHERE 子句和参数。"""
    conditions: list[str] = []
    params: list[Any] = []

    if name := filters.get("name"):
        conditions.append("name LIKE ?")
        params.append(f"%{name}%")
    if category := filters.get("category"):
        conditions.append("category = ?")
        params.append(category)
    if district := filters.get("business_district"):
        conditions.append("business_district = ?")
        params.append(district)
    if star := filters.get("star_level"):
        conditions.append("star_level = ?")
        params.append(star)
    if filters.get("min_avg_price") is not None:
        conditions.append("avg_price >= ?")
        params.append(filters["min_avg_price"])
    if filters.get("max_avg_price") is not None:
        conditions.append("avg_price <= ?")
        params.append(filters["max_avg_price"])
    if filters.get("min_rating") is not None:
        conditions.append(
            "(taste_score + environment_score + service_score) / 3 >= ?"
        )
        params.append(filters["min_rating"])
    if filters.get("min_taste_score") is not None:
        conditions.append("taste_score >= ?")
        params.append(filters["min_taste_score"])
    if filters.get("min_environment_score") is not None:
        conditions.append("environment_score >= ?")
        params.append(filters["min_environment_score"])
    if filters.get("min_service_score") is not None:
        conditions.append("service_score >= ?")
        params.append(filters["min_service_score"])
    if filters.get("is_active") is not None:
        conditions.append("is_active = ?")
        params.append(int(bool(filters["is_active"])))
    else:
        conditions.append("is_active = 1")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    return where_clause, params


def count_restaurants(filters: dict[str, Any]) -> int:
    """统计符合条件的餐厅数量。"""
    where_clause, params = _build_where_clause(filters)
    sql = f"SELECT COUNT(*) as count FROM restaurants{where_clause}"
    with get_connection(read_only=True) as conn:
        cursor = conn.execute(sql, params)
        row = cursor.fetchone()
    return row["count"] if row else 0


def search(
    filters: dict[str, Any],
    limit: int = 100,
    offset: int = 0,
    order_by: str | None = None,
) -> list[dict[str, Any]]:
    """
    根据过滤条件查询餐厅列表。
    支持字段：name, category, business_district, star_level, min_avg_price, max_avg_price,
    min_rating, min_taste_score, min_environment_score, min_service_score, is_active。
    """
    where_clause, params = _build_where_clause(filters)
    
    base_sql = f"SELECT * FROM restaurants{where_clause}"

    if order_by:
        base_sql += f" ORDER BY {order_by}"

    base_sql += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    with get_connection(read_only=True) as conn:
        cursor = conn.execute(base_sql, params)
        rows = cursor.fetchall()
    return [_row_to_dict(row) for row in rows]


def update(shop_id: str, fields: dict[str, Any]) -> bool:
    """
    更新指定餐厅。返回是否更新成功。
    """
    if not fields:
        return False
    assignments = ", ".join(f"{key} = ?" for key in fields)
    params = list(fields.values()) + [shop_id]
    sql = f"UPDATE restaurants SET {assignments} WHERE shop_id = ?"
    with get_connection() as conn:
        cursor = conn.execute(sql, params)
        # commit 由上下文管理器自动处理
        rowcount = cursor.rowcount
    return rowcount > 0


def soft_delete(shop_id: str) -> bool:
    """
    软删除餐厅。
    """
    return update(shop_id, {"is_active": 0})

