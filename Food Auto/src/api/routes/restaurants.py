"""
餐厅相关 API。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flask import Blueprint, jsonify, make_response, request

from ...services import export_service, restaurant_service

bp = Blueprint("restaurants", __name__)


@bp.get("/")
def list_restaurants() -> Any:
    filters = {
        "name": request.args.get("name"),
        "category": request.args.get("category"),
        "business_district": request.args.get("business_district"),
        "star_level": request.args.get("star_level"),
        "min_rating": request.args.get("min_rating", type=float),
        "min_taste_score": request.args.get("min_taste_score", type=float),
        "min_environment_score": request.args.get("min_environment_score", type=float),
        "min_service_score": request.args.get("min_service_score", type=float),
        "max_avg_price": request.args.get("max_avg_price", type=float),
        "min_avg_price": request.args.get("min_avg_price", type=float),
    }
    # 移除空值
    filters = {k: v for k, v in filters.items() if v is not None}
    
    # 分页参数
    limit = request.args.get("limit", default=20, type=int)
    offset = request.args.get("offset", default=0, type=int)
    
    # 排序参数
    sort_field = request.args.get("sort_field")
    sort_order = request.args.get("sort_order", default="desc")
    
    # 构建排序字段映射
    order_by = None
    if sort_field:
        valid_sort_fields = {
            "name": "name",
            "avg_price": "avg_price",
            "taste_score": "taste_score",
            "reviews": "reviews",
        }
        if sort_field in valid_sort_fields:
            order_direction = "ASC" if sort_order == "asc" else "DESC"
            order_by = f"{valid_sort_fields[sort_field]} {order_direction}"
    
    # 获取总数
    total_count = restaurant_service.count_restaurants(filters)
    # 获取数据（服务端分页）
    data = restaurant_service.search_restaurants(filters, limit=limit, offset=offset, order_by=order_by)
    
    return jsonify({
        "items": data,
        "count": total_count,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(data) < total_count
    })


@bp.post("/")
def create_restaurant() -> Any:
    payload = request.get_json(force=True)
    restaurant_service.create_restaurant(payload)
    return jsonify({"status": "created"}), 201


@bp.post("/import")
def import_csv() -> Any:
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "未上传文件"}), 400
    temp_path = Path("/tmp") / file.filename
    file.save(temp_path)
    result = restaurant_service.bulk_import_from_csv(temp_path, update_existing=True)
    temp_path.unlink(missing_ok=True)
    return jsonify(result)


@bp.get("/<shop_id>")
def get_restaurant(shop_id: str) -> Any:
    """获取单个餐厅详情。"""
    from ...db.dao import restaurant_dao
    
    restaurant = restaurant_dao.get_by_shop_id(shop_id)
    if not restaurant:
        return jsonify({"error": "餐厅不存在"}), 404
    return jsonify(restaurant)


@bp.put("/<shop_id>")
def update_restaurant(shop_id: str) -> Any:
    """更新餐厅信息。"""
    payload = request.get_json(force=True)
    success = restaurant_service.update_restaurant(shop_id, payload)
    if not success:
        return jsonify({"error": "更新失败"}), 400
    return jsonify({"status": "updated"})


@bp.delete("/<shop_id>")
def delete_restaurant(shop_id: str) -> Any:
    """删除餐厅（软删除）。"""
    success = restaurant_service.soft_delete_restaurant(shop_id)
    if not success:
        return jsonify({"error": "删除失败"}), 400
    return jsonify({"status": "deleted"})


@bp.post("/batch")
def batch_operation() -> Any:
    """批量操作。"""
    payload = request.get_json(force=True)
    operation = payload.get("operation")  # "delete", "update"
    shop_ids = payload.get("shop_ids", [])
    data = payload.get("data", {})  # 用于更新操作
    
    if not shop_ids:
        return jsonify({"error": "未选择餐厅"}), 400
    
    results = []
    for shop_id in shop_ids:
        try:
            if operation == "delete":
                success = restaurant_service.soft_delete_restaurant(shop_id)
                results.append({"shop_id": shop_id, "status": "deleted" if success else "failed"})
            elif operation == "update":
                success = restaurant_service.update_restaurant(shop_id, data)
                results.append({"shop_id": shop_id, "status": "updated" if success else "failed"})
            else:
                results.append({"shop_id": shop_id, "status": "invalid_operation"})
        except Exception as e:
            results.append({"shop_id": shop_id, "status": "error", "error": str(e)})
    
    return jsonify({"results": results})


@bp.get("/export/csv")
def export_csv() -> Any:
    """导出 CSV。"""
    filters = {
        "name": request.args.get("name"),
        "category": request.args.get("category"),
        "business_district": request.args.get("business_district"),
        "star_level": request.args.get("star_level"),
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        csv_data = export_service.export_to_csv(filters)
        response = make_response(csv_data)
        response.headers["Content-Type"] = "text/csv; charset=utf-8"
        response.headers["Content-Disposition"] = "attachment; filename=restaurants.csv"
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.get("/export/excel")
def export_excel() -> Any:
    """导出 Excel。"""
    filters = {
        "name": request.args.get("name"),
        "category": request.args.get("category"),
        "business_district": request.args.get("business_district"),
        "star_level": request.args.get("star_level"),
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        excel_data = export_service.export_to_excel(filters)
        response = make_response(excel_data)
        response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response.headers["Content-Disposition"] = "attachment; filename=restaurants.xlsx"
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


