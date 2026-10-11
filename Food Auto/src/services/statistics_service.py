"""
数据统计服务。
"""

from __future__ import annotations

from typing import Any

from ..db.connection import get_connection


def get_category_statistics() -> list[dict[str, Any]]:
    """获取菜系统计。"""
    sql = """
        SELECT 
            category,
            COUNT(*) as count,
            AVG(avg_price) as avg_price,
            AVG(taste_score) as avg_taste_score,
            AVG(environment_score) as avg_environment_score,
            AVG(service_score) as avg_service_score
        FROM restaurants
        WHERE is_active = 1
        GROUP BY category
        ORDER BY count DESC
    """
    
    with get_connection(read_only=True) as conn:
        conn.row_factory = lambda c, r: {col[0]: r[idx] for idx, col in enumerate(c.description)}
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
    
    return [dict(row) for row in rows]


def get_district_statistics() -> list[dict[str, Any]]:
    """获取商圈统计。"""
    sql = """
        SELECT 
            business_district,
            COUNT(*) as count,
            AVG(avg_price) as avg_price,
            AVG(taste_score) as avg_taste_score
        FROM restaurants
        WHERE is_active = 1 AND business_district IS NOT NULL AND business_district != ''
        GROUP BY business_district
        ORDER BY count DESC
        LIMIT 20
    """
    
    with get_connection(read_only=True) as conn:
        conn.row_factory = lambda c, r: {col[0]: r[idx] for idx, col in enumerate(c.description)}
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
    
    return [dict(row) for row in rows]


def get_price_distribution() -> list[dict[str, Any]]:
    """获取价格分布。"""
    sql = """
        SELECT 
            CASE
                WHEN avg_price IS NULL OR avg_price = 0 THEN 'Not Set'
                WHEN avg_price < 50 THEN 'Below ¥50'
                WHEN avg_price < 100 THEN '¥50-100'
                WHEN avg_price < 150 THEN '¥100-150'
                WHEN avg_price < 200 THEN '¥150-200'
                WHEN avg_price < 300 THEN '¥200-300'
                ELSE 'Above ¥300'
            END as price_range,
            COUNT(*) as count
        FROM restaurants
        WHERE is_active = 1
        GROUP BY price_range
        ORDER BY 
            CASE price_range
                WHEN 'Not Set' THEN 0
                WHEN 'Below ¥50' THEN 1
                WHEN '¥50-100' THEN 2
                WHEN '¥100-150' THEN 3
                WHEN '¥150-200' THEN 4
                WHEN '¥200-300' THEN 5
                ELSE 6
            END
    """
    
    with get_connection(read_only=True) as conn:
        conn.row_factory = lambda c, r: {col[0]: r[idx] for idx, col in enumerate(c.description)}
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
    
    return [dict(row) for row in rows]


def get_star_level_statistics() -> list[dict[str, Any]]:
    """获取星级统计。"""
    sql = """
        SELECT 
            star_level,
            COUNT(*) as count,
            AVG(taste_score) as avg_taste_score,
            AVG(environment_score) as avg_environment_score,
            AVG(service_score) as avg_service_score
        FROM restaurants
        WHERE is_active = 1 AND star_level IS NOT NULL AND star_level != ''
        GROUP BY star_level
        ORDER BY count DESC
    """
    
    with get_connection(read_only=True) as conn:
        conn.row_factory = lambda c, r: {col[0]: r[idx] for idx, col in enumerate(c.description)}
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
    
    return [dict(row) for row in rows]


def get_overall_statistics() -> dict[str, Any]:
    """获取总体统计。"""
    sql = """
        SELECT 
            COUNT(*) as total_restaurants,
            COUNT(DISTINCT category) as total_categories,
            COUNT(DISTINCT business_district) as total_districts,
            AVG(avg_price) as avg_price,
            AVG(taste_score) as avg_taste_score,
            AVG(environment_score) as avg_environment_score,
            AVG(service_score) as avg_service_score,
            SUM(reviews) as total_reviews,
            MAX(avg_price) as max_price,
            MIN(avg_price) as min_price
        FROM restaurants
        WHERE is_active = 1
    """
    
    with get_connection(read_only=True) as conn:
        conn.row_factory = lambda c, r: {col[0]: r[idx] for idx, col in enumerate(c.description)}
        cursor = conn.execute(sql)
        row = cursor.fetchone()
    
    return dict(row) if row else {}


def get_top_restaurants(
    limit: int = 10,
    order_by: str = "taste_score",
    order_direction: str = "DESC"
) -> list[dict[str, Any]]:
    """获取热门餐厅。"""
    valid_order_fields = {
        "taste_score": "taste_score",
        "environment_score": "environment_score",
        "service_score": "service_score",
        "reviews": "reviews",
        "avg_price": "avg_price",
    }
    
    if order_by not in valid_order_fields:
        order_by = "taste_score"
    
    if order_direction.upper() not in ("ASC", "DESC"):
        order_direction = "DESC"
    
    sql = f"""
        SELECT 
            shop_id,
            name,
            category,
            business_district,
            avg_price,
            taste_score,
            environment_score,
            service_score,
            star_level,
            reviews
        FROM restaurants
        WHERE is_active = 1
        ORDER BY {valid_order_fields[order_by]} {order_direction}
        LIMIT ?
    """
    
    with get_connection(read_only=True) as conn:
        conn.row_factory = lambda c, r: {col[0]: r[idx] for idx, col in enumerate(c.description)}
        cursor = conn.execute(sql, (limit,))
        rows = cursor.fetchall()
    
    return [dict(row) for row in rows]

