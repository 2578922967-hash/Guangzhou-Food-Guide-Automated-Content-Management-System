"""
数据校验与类型转换工具。
"""

from __future__ import annotations

from typing import Any

CSV_FIELD_ALIASES = {
    "Name": "name",
    "Restaurant Name": "name",
    "Reviews": "reviews",
    "Avg price (RMB)": "avg_price",
    "Avg price": "avg_price",
    "Category": "category",
    "Cuisine Type": "category",
    "Business district": "business_district",
    "Business District": "business_district",
    "Address": "address",
    "Recommendation 1": "recommended_dish_1",
    "Recommendation 2": "recommended_dish_2",
    "Recommendation 3": "recommended_dish_3",
    "Taste score": "taste_score",
    "Taste Score": "taste_score",
    "Environment score": "environment_score",
    "Environment Score": "environment_score",
    "Service score": "service_score",
    "Service Score": "service_score",
    "Star level": "star_level",
    "Star Level": "star_level",
    "Shop ID": "shop_id",
    "ShopId": "shop_id",
    "URL": "url",
}


REQUIRED_RESTAURANT_FIELDS = {
    "shop_id",
    "name",
    "category",
    "star_level",
}

FLOAT_FIELDS = {
    "avg_price",
    "taste_score",
    "environment_score",
    "service_score",
}

INT_FIELDS = {
    "reviews",
}

STRING_FIELDS = {
    "name",
    "category",
    "business_district",
    "address",
    "shop_id",
    "recommended_dish_1",
    "recommended_dish_2",
    "recommended_dish_3",
    "star_level",
    "url",
}


def _coerce_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        raise ValueError(f"无效的整数值: {value}")


def _coerce_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"无效的浮点数值: {value}")


def normalize_restaurant_record(raw: dict[str, Any], *, partial: bool = False) -> dict[str, Any]:
    """
    将原始记录转换为数据库兼容格式。
    """
    mapped: dict[str, Any] = {}
    for key, value in raw.items():
        canonical = CSV_FIELD_ALIASES.get(key, key)
        mapped[canonical] = value

    record: dict[str, Any] = {}

    # 去除前后空白
    trimmed = {key: (value.strip() if isinstance(value, str) else value) for key, value in mapped.items()}

    if not partial:
        missing = [field for field in REQUIRED_RESTAURANT_FIELDS if not trimmed.get(field)]
        if missing:
            raise ValueError(f"缺少必填字段: {', '.join(missing)}")

    for field in STRING_FIELDS:
        if field in trimmed and trimmed[field] != "":
            record[field] = trimmed[field]
    for field in FLOAT_FIELDS:
        if field in trimmed:
            record[field] = _coerce_float(trimmed[field])
    for field in INT_FIELDS:
        if field in trimmed:
            record[field] = _coerce_int(trimmed[field])

    record.setdefault("reviews", 0)
    record.setdefault("is_active", 1)

    return record


def ensure_placeholders(payload: dict[str, Any]) -> None:
    """
    校验模板必填字段。
    """
    if "template_id" not in payload:
        raise ValueError("模板必须包含 template_id")
    if "content" not in payload:
        raise ValueError("模板必须包含 content")
    placeholders = payload.get("placeholders") or payload.get("placeholders_json")
    if placeholders is None:
        raise ValueError("模板必须定义占位符说明 placeholders")

