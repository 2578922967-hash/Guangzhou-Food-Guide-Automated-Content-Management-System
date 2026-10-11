"""
统计数据 API。
"""

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from ...services import statistics_service

bp = Blueprint("statistics", __name__)


@bp.get("/overall")
def get_overall_statistics() -> Any:
    """获取总体统计。"""
    stats = statistics_service.get_overall_statistics()
    return jsonify(stats)


@bp.get("/categories")
def get_category_statistics() -> Any:
    """获取菜系统计。"""
    stats = statistics_service.get_category_statistics()
    return jsonify(stats)


@bp.get("/districts")
def get_district_statistics() -> Any:
    """获取商圈统计。"""
    stats = statistics_service.get_district_statistics()
    return jsonify(stats)


@bp.get("/price-distribution")
def get_price_distribution() -> Any:
    """获取价格分布。"""
    stats = statistics_service.get_price_distribution()
    return jsonify(stats)


@bp.get("/star-levels")
def get_star_level_statistics() -> Any:
    """获取星级统计。"""
    stats = statistics_service.get_star_level_statistics()
    return jsonify(stats)


@bp.get("/top-restaurants")
def get_top_restaurants() -> Any:
    """获取热门餐厅。"""
    limit = request.args.get("limit", default=10, type=int)
    order_by = request.args.get("order_by", default="taste_score")
    order_direction = request.args.get("order_direction", default="DESC")
    
    restaurants = statistics_service.get_top_restaurants(
        limit=limit,
        order_by=order_by,
        order_direction=order_direction
    )
    return jsonify(restaurants)


@bp.get("/dashboard")
def get_dashboard_data() -> Any:
    """获取仪表板数据。"""
    return jsonify({
        "overall": statistics_service.get_overall_statistics(),
        "categories": statistics_service.get_category_statistics(),
        "districts": statistics_service.get_district_statistics(),
        "price_distribution": statistics_service.get_price_distribution(),
        "star_levels": statistics_service.get_star_level_statistics(),
        "top_restaurants": statistics_service.get_top_restaurants(limit=10),
    })

