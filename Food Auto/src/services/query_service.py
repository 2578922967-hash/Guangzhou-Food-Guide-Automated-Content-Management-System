"""
封装各类统计查询与高级 SQL 示例。
"""

from __future__ import annotations

from typing import Any, Iterable

import json
from ..db.connection import get_connection
from . import statistics_service


def _safe_divide(numerator: float | None, denominator: float | None) -> float:
    if not numerator or not denominator:
        return 0.0
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0.0


def star_rating_distribution() -> dict[str, Any]:
    """
    星级分布与评分表现（包含聚合与子查询）。
    """
    sql = """
    WITH filtered AS (
        SELECT
            CASE
                WHEN LOWER(star_level) LIKE 'five%' THEN 'five'
                WHEN LOWER(star_level) LIKE 'quasi%' THEN 'quasi_five'
                WHEN LOWER(star_level) LIKE 'four%' THEN 'four'
                ELSE 'others'
            END AS level_group,
            taste_score,
            environment_score,
            service_score
        FROM restaurants
        WHERE is_active = 1
    ),
    totals AS (
        SELECT COUNT(*) AS total_count FROM filtered
    ),
    level_counts AS (
        SELECT level_group, COUNT(*) AS cnt FROM filtered GROUP BY level_group
    ),
    level_avg AS (
        SELECT
            level_group,
            AVG(taste_score) AS avg_taste,
            AVG(environment_score) AS avg_env,
            AVG(service_score) AS avg_service,
            AVG((environment_score + service_score) / 2.0) AS avg_env_service
        FROM filtered
        GROUP BY level_group
    ),
    overall AS (
        SELECT
            AVG(taste_score) AS avg_taste_overall,
            AVG(environment_score) AS avg_env_overall,
            AVG(service_score) AS avg_service_overall
        FROM filtered
    )
    SELECT
        (SELECT cnt FROM level_counts WHERE level_group = 'five') AS count_five,
        (SELECT cnt FROM level_counts WHERE level_group = 'quasi_five') AS count_quasi,
        (SELECT cnt FROM level_counts WHERE level_group = 'four') AS count_four,
        (SELECT avg_taste FROM level_avg WHERE level_group = 'five') AS avg_taste_five,
        (SELECT avg_env FROM level_avg WHERE level_group = 'five') AS avg_env_five,
        (SELECT avg_service FROM level_avg WHERE level_group = 'five') AS avg_service_five,
        (SELECT avg_taste FROM level_avg WHERE level_group = 'quasi_five') AS avg_taste_quasi,
        (SELECT avg_env FROM level_avg WHERE level_group = 'quasi_five') AS avg_env_quasi,
        (SELECT avg_service FROM level_avg WHERE level_group = 'quasi_five') AS avg_service_quasi,
        (SELECT avg_env_service FROM level_avg WHERE level_group = 'four') AS avg_env_service_four,
        totals.total_count,
        overall.avg_taste_overall,
        overall.avg_env_overall,
        overall.avg_service_overall
    FROM totals, overall;
    """
    with get_connection(read_only=True) as conn:
        row = conn.execute(sql).fetchone()
    data = dict(row or {})

    total = data.get("total_count") or 0
    five = data.get("count_five") or 0
    quasi = data.get("count_quasi") or 0
    four = data.get("count_four") or 0

    # 找出环境评分最高的星级
    env_five = data.get("avg_env_five") or 0.0
    env_quasi = data.get("avg_env_quasi") or 0.0
    env_four = data.get("avg_env_service_four") or 0.0
    
    best_env_level = "Five-Star"
    if env_quasi > env_five and env_quasi > env_four:
        best_env_level = "Quasi-Five-Star"
    elif env_four > env_five and env_four > env_quasi:
        best_env_level = "Four-Star"

    return {
        "percentage_five_star": _safe_divide(five * 100.0, total),
        "percentage_quasi_five": _safe_divide(quasi * 100.0, total),
        "count_four_star": four,
        "avg_taste_five": data.get("avg_taste_five") or 0.0,
        "avg_env_five": data.get("avg_env_five") or 0.0,
        "avg_service_five": data.get("avg_service_five") or 0.0,
        "avg_taste_quasi": data.get("avg_taste_quasi") or 0.0,
        "avg_env_quasi": data.get("avg_env_quasi") or 0.0,
        "avg_service_quasi": data.get("avg_service_quasi") or 0.0,
        "avg_env_service_four_star": data.get("avg_env_service_four") or 0.0,
        "avg_taste_overall": data.get("avg_taste_overall") or 0.0,
        "avg_env_overall": data.get("avg_env_overall") or 0.0,
        "avg_service_overall": data.get("avg_service_overall") or 0.0,
        "total_restaurants": total,
        "best_env_star_level": best_env_level,
    }


def best_value_for_money(price_cap: float, top_n: int = 5) -> dict[str, Any]:
    """
    基于味道评分与价格计算性价比。
    """
    query = """
    WITH candidates AS (
        SELECT
            name,
            taste_score,
            environment_score,
            service_score,
            avg_price,
            category,
            business_district,
            recommended_dish_1,
            recommended_dish_2,
            recommended_dish_3,
            (taste_score / NULLIF(avg_price, 0)) AS value_index
        FROM restaurants
        WHERE is_active = 1
          AND avg_price IS NOT NULL
          AND avg_price <= ?
          AND taste_score IS NOT NULL
    ),
    ranked AS (
        SELECT *
        FROM candidates
        WHERE value_index IS NOT NULL
        ORDER BY value_index DESC, taste_score DESC
        LIMIT ?
    ),
    overall AS (
        SELECT
            COUNT(*) AS total_restaurants,
            AVG(taste_score) AS avg_taste,
            AVG(environment_score) AS avg_env,
            AVG(service_score) AS avg_service
        FROM candidates
    )
    SELECT *
    FROM ranked;
    """
    with get_connection(read_only=True) as conn:
        rows = conn.execute(query, (price_cap, top_n * 3)).fetchall()
        overall = conn.execute(
            """
            SELECT
                COUNT(*) AS total_restaurants,
                AVG(taste_score) AS avg_taste,
                AVG(environment_score) AS avg_env,
                AVG(service_score) AS avg_service
            FROM restaurants
            WHERE is_active = 1
              AND avg_price IS NOT NULL
              AND avg_price <= ?
              AND taste_score IS NOT NULL
            """,
            (price_cap,),
        ).fetchone()

    top_rows = [dict(row) for row in rows[:top_n]]
    context: dict[str, Any] = {
        "price_cap": price_cap,
        "top_n": top_n,
        "avg_taste_overall": 0.0,
        "avg_env_overall": 0.0,
        "avg_service_overall": 0.0,
        "total_restaurants": 0,
    }

    if overall:
        context["avg_taste_overall"] = overall["avg_taste"] or 0.0
        context["avg_env_overall"] = overall["avg_env"] or 0.0
        context["avg_service_overall"] = overall["avg_service"] or 0.0
        context["total_restaurants"] = overall["total_restaurants"] or 0

    def get_value(row: Any, key: str) -> Any:
        value = row.get(key)
        if value is None:
            return "N/A"
        return value

    for idx in range(1, top_n + 1):
        row = top_rows[idx - 1] if idx - 1 < len(top_rows) else None
        context[f"restaurant{idx}_name"] = get_value(row, "name") if row else "To be added"
        context[f"value_for_money{idx}"] = float(row["value_index"]) if row and row["value_index"] else 0.0
        context[f"restaurant{idx}_taste_score"] = float(row["taste_score"]) if row and row["taste_score"] else 0.0
        context[f"restaurant{idx}_price"] = float(row["avg_price"]) if row and row["avg_price"] else 0.0
        context[f"restaurant{idx}_rec1"] = get_value(row, "recommended_dish_1") if row else "N/A"
        context[f"restaurant{idx}_rec2"] = get_value(row, "recommended_dish_2") if row else "N/A"

    return context


def _composite_score(row: Any) -> float:
    taste = row["taste_score"] or 0
    env = row["environment_score"] or 0
    service = row["service_score"] or 0
    return float((taste + env + service) / 3.0)


def winter_warmers(district: str) -> dict[str, Any]:
    """
    获取指定商圈的火锅与炖品推荐。
    """
    with get_connection(read_only=True) as conn:
        hotpot_row = conn.execute(
            """
            SELECT *
            FROM restaurants
            WHERE is_active = 1
              AND business_district = ?
              AND (
                    category LIKE '%Hot Pot%' OR category LIKE '%火锅%'
                  )
            ORDER BY (taste_score + environment_score + service_score) DESC
            LIMIT 1
            """,
            (district,),
        ).fetchone()
        stew_row = conn.execute(
            """
            SELECT *
            FROM restaurants
            WHERE is_active = 1
              AND business_district = ?
              AND (
                    category LIKE '%Casserole%' OR category LIKE '%Soup%' OR category LIKE '%煲%'
                  )
            ORDER BY (taste_score + environment_score + service_score) DESC
            LIMIT 1
            """,
            (district,),
        ).fetchone()

    def fallback_row(kind: str) -> dict[str, Any]:
        return {
            "name": f"{kind} restaurant not found",
            "taste_score": 0.0,
            "environment_score": 0.0,
            "service_score": 0.0,
            "avg_price": 0.0,
            "recommended_dish_1": "To be explored",
            "recommended_dish_2": "To be explored",
            "address": "Address not available",
        }

    hotpot = dict(hotpot_row) if hotpot_row else fallback_row("Hot pot")
    stew = dict(stew_row) if stew_row else fallback_row("Soup casserole")

    return {
        "district": district,
        "hotpot_restaurant_name": hotpot.get("name"),
        "hotpot_restaurant_score": _composite_score(hotpot),
        "hotpot_price": hotpot.get("avg_price") or 0,
        "hotpot_rec1": hotpot.get("recommended_dish_1") or "To be explored",
        "hotpot_rec2": hotpot.get("recommended_dish_2") or "To be explored",
        "hotpot_address": hotpot.get("address") or "Address not available",
        "stew_restaurant_name": stew.get("name"),
        "stew_restaurant_score": _composite_score(stew),
        "stew_price": stew.get("avg_price") or 0,
        "stew_rec1": stew.get("recommended_dish_1") or "To be explored",
        "stew_rec2": stew.get("recommended_dish_2") or "To be explored",
        "stew_address": stew.get("address") or "Address not available",
    }


def hidden_gem(district: str) -> dict[str, Any]:
    """
    选取评论数较少但评分高于区域均值的宝藏餐厅。
    """
    sql = """
    WITH district_stats AS (
        SELECT
            AVG((taste_score + environment_score + service_score) / 3.0) AS avg_score,
            AVG(reviews) AS avg_reviews
        FROM restaurants
        WHERE is_active = 1
          AND business_district = ?
    )
    SELECT
        r.*,
        (r.taste_score + r.environment_score + r.service_score) / 3.0 AS composite_score
    FROM restaurants r
    WHERE r.is_active = 1
      AND r.business_district = ?
      AND (SELECT avg_score FROM district_stats) IS NOT NULL
      AND (SELECT avg_reviews FROM district_stats) IS NOT NULL
      AND ((r.taste_score + r.environment_score + r.service_score) / 3.0) >
          (SELECT avg_score FROM district_stats)
      AND r.reviews < (SELECT avg_reviews FROM district_stats)
    ORDER BY composite_score DESC, r.reviews ASC
    LIMIT 1;
    """
    with get_connection(read_only=True) as conn:
        row = conn.execute(sql, (district, district)).fetchone()

    if not row:
        return {
            "district": district,
            "gem_name": "No matching hidden gem found",
            "gem_category": "Various cuisines",
            "gem_score": 0.0,
            "gem_taste": "-",
            "gem_env": "-",
            "gem_service": "-",
            "gem_price": 0.0,
            "gem_rec1": "To be explored",
            "gem_rec2": "To be explored",
            "gem_highlight": "Awaiting discovery",
            "gem_address": "Address not available",
        }

    record = dict(row)
    composite = row["composite_score"] or 0.0
    highlight = f"Only {record.get('reviews', 0)} reviews but high rating"
    return {
        "district": district,
        "gem_name": record.get("name"),
        "gem_category": record.get("category"),
        "gem_score": composite,
        "gem_taste": f"{record.get('taste_score', 0):.1f}",
        "gem_env": f"{record.get('environment_score', 0):.1f}",
        "gem_service": f"{record.get('service_score', 0):.1f}",
        "gem_price": record.get("avg_price") or 0,
        "gem_rec1": record.get("recommended_dish_1") or "To be explored",
        "gem_rec2": record.get("recommended_dish_2") or "To be explored",
        "gem_highlight": highlight,
        "gem_address": record.get("address") or "Address not available",
    }


def district_food_express(district: str) -> dict[str, Any]:
    """
    区域概览，展示主流菜系与代表餐厅。
    """
    sql_primary = """
    WITH district_restaurants AS (
        SELECT *
        FROM restaurants
        WHERE is_active = 1
          AND business_district = ?
    ),
    ranked_categories AS (
        SELECT
            category,
            COUNT(*) AS cnt,
            ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rn
        FROM district_restaurants
        GROUP BY category
    )
    SELECT
        (SELECT AVG(avg_price) FROM district_restaurants) AS avg_price,
        (SELECT category FROM ranked_categories WHERE rn = 1) AS primary_category,
        (SELECT category FROM ranked_categories WHERE rn = 2) AS secondary_category
    ;
    """
    sql_top_restaurants = """
    SELECT
        name,
        (taste_score + environment_score + service_score) / 3.0 AS composite_score
    FROM restaurants
    WHERE is_active = 1
      AND business_district = ?
    ORDER BY composite_score DESC
    LIMIT 2;
    """
    with get_connection(read_only=True) as conn:
        conn.row_factory = lambda c, r: {col[0]: r[idx] for idx, col in enumerate(c.description)}
        primary = conn.execute(sql_primary, (district,)).fetchone()
        top_rows = conn.execute(sql_top_restaurants, (district,)).fetchall()

    primary_category = primary["primary_category"] if primary else None
    secondary_category = primary["secondary_category"] if primary else None
    avg_price = primary["avg_price"] if primary else None

    # 计算主流菜系占比
    primary_count = 0
    total_in_district = 0
    if primary_category:
        sql_count = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN category = ? THEN 1 ELSE 0 END) as primary_count
        FROM restaurants
        WHERE is_active = 1 AND business_district = ?
        """
        with get_connection(read_only=True) as conn:
            conn.row_factory = lambda c, r: {col[0]: r[idx] for idx, col in enumerate(c.description)}
            count_row = conn.execute(sql_count, (primary_category, district)).fetchone()
            if count_row:
                total_in_district = count_row.get("total") or 0
                primary_count = count_row.get("primary_count") or 0
    
    primary_category_percentage = _safe_divide(primary_count * 100.0, total_in_district) if total_in_district > 0 else 0.0

    context = {
        "district": district,
        "most_common_category": primary_category or "Diverse cuisines",
        "most_common_category_percentage": primary_category_percentage,
        "distinct_category": secondary_category or "Regional selections",
        "avg_price_district": avg_price or 0.0,
    }

    for idx, row in enumerate(top_rows[:2], start=1):
        context[f"restaurant{idx}_name"] = row["name"]
        context[f"restaurant{idx}_score"] = row["composite_score"] or 0.0

    if len(top_rows) < 2:
        for idx in range(len(top_rows) + 1, 3):
            context[f"restaurant{idx}_name"] = "To be added"
            context[f"restaurant{idx}_score"] = 0.0

    return context


def delivery_picks(district: str, min_score: float = 8.0, limit: int = 3) -> dict[str, Any]:
    """
    选择综合评分高于阈值的外卖友好餐厅。
    """
    sql = """
    WITH candidate AS (
        SELECT
            *,
            (taste_score + environment_score + service_score) / 3.0 AS composite_score
        FROM restaurants
        WHERE is_active = 1
          AND business_district = ?
          AND (taste_score + environment_score + service_score) / 3.0 >= ?
          AND reviews >= (
                SELECT COALESCE(AVG(reviews), 0)
                FROM restaurants
                WHERE is_active = 1
                  AND business_district = ?
          )
    )
    SELECT *
    FROM candidate
    ORDER BY composite_score DESC, reviews DESC
    LIMIT ?;
    """
    with get_connection(read_only=True) as conn:
        rows = conn.execute(sql, (district, min_score, district, limit)).fetchall()

    context = {
        "district": district,
        "min_score": min_score,
    }

    taste_scores: list[float] = []
    service_scores: list[float] = []

    for idx in range(1, limit + 1):
        row = rows[idx - 1] if idx - 1 < len(rows) else None
        if row:
            taste_scores.append(row["taste_score"] or 0.0)
            service_scores.append(row["service_score"] or 0.0)
            context[f"restaurant{idx}_name"] = row["name"]
            context[f"restaurant{idx}_score"] = row["composite_score"] or 0.0
            context[f"restaurant{idx}_category"] = row["category"] or "General cuisine"
            context[f"restaurant{idx}_price"] = row["avg_price"] or 0.0
            context[f"restaurant{idx}_rec1"] = row["recommended_dish_1"] or "Signature dish"
            context[f"restaurant{idx}_rec2"] = row["recommended_dish_2"] or "Recommended dish"
        else:
            context[f"restaurant{idx}_name"] = "To be added"
            context[f"restaurant{idx}_score"] = 0.0
            context[f"restaurant{idx}_category"] = "Various cuisines"
            context[f"restaurant{idx}_price"] = 0.0
            context[f"restaurant{idx}_rec1"] = "To be explored"
            context[f"restaurant{idx}_rec2"] = "To be explored"

    context["avg_taste_score"] = sum(taste_scores) / len(taste_scores) if taste_scores else 0.0
    context["avg_service_score"] = sum(service_scores) / len(service_scores) if service_scores else 0.0

    return context


def star_level_summary_by_district() -> Iterable[dict[str, Any]]:
    """
    额外的高级查询示例：按商圈统计不同星级分布与平均价位。
    """
    sql = """
    SELECT
        business_district,
        star_level,
        COUNT(*) AS store_count,
        AVG(avg_price) AS avg_price
    FROM restaurants
    WHERE is_active = 1
    GROUP BY business_district, star_level
    ORDER BY business_district, store_count DESC;
    """
    with get_connection(read_only=True) as conn:
        rows = conn.execute(sql).fetchall()
    for row in rows:
        yield dict(row)


def statistics_visualization_report() -> dict[str, Any]:
    """
    生成包含可视化图表的统计报告。
    """
    # 获取所有统计数据
    overall = statistics_service.get_overall_statistics()
    categories = statistics_service.get_category_statistics()[:10]  # Top 10
    districts = statistics_service.get_district_statistics()[:10]  # Top 10
    price_dist = statistics_service.get_price_distribution()
    star_levels = statistics_service.get_star_level_statistics()
    top_restaurants = statistics_service.get_top_restaurants(limit=10)
    
    # 准备图表数据
    category_labels = [cat["category"] for cat in categories]
    category_counts = [cat["count"] for cat in categories]
    category_avg_prices = [cat["avg_price"] or 0 for cat in categories]
    
    district_labels = [d["business_district"] for d in districts]
    district_counts = [d["count"] for d in districts]
    
    price_labels = [p["price_range"] for p in price_dist]
    price_counts = [p["count"] for p in price_dist]
    
    star_labels = [s["star_level"] for s in star_levels]
    star_counts = [s["count"] for s in star_levels]
    
    # 计算各项统计数据
    total_restaurants = overall.get("total_restaurants") or 0
    total_categories = overall.get("total_categories") or 0
    total_districts = overall.get("total_districts") or 0
    avg_price = overall.get("avg_price") or 0.0
    avg_taste = overall.get("avg_taste_score") or 0.0
    avg_env = overall.get("avg_environment_score") or 0.0
    avg_service = overall.get("avg_service_score") or 0.0
    total_reviews = overall.get("total_reviews") or 0
    
    # 将列表转换为JSON字符串以便在模板中使用
    return {
        "total_restaurants": total_restaurants,
        "total_categories": total_categories,
        "total_districts": total_districts,
        "avg_price": avg_price,
        "avg_taste_score": avg_taste,
        "avg_environment_score": avg_env,
        "avg_service_score": avg_service,
        "total_reviews": total_reviews,
        # 图表数据（JSON格式字符串，供前端Chart.js使用）
        "category_labels_json": json.dumps(category_labels, ensure_ascii=False),
        "category_counts_json": json.dumps(category_counts, ensure_ascii=False),
        "category_avg_prices_json": json.dumps(category_avg_prices, ensure_ascii=False),
        "district_labels_json": json.dumps(district_labels, ensure_ascii=False),
        "district_counts_json": json.dumps(district_counts, ensure_ascii=False),
        "price_labels_json": json.dumps(price_labels, ensure_ascii=False),
        "price_counts_json": json.dumps(price_counts, ensure_ascii=False),
        "star_labels_json": json.dumps(star_labels, ensure_ascii=False),
        "star_counts_json": json.dumps(star_counts, ensure_ascii=False),
    }


