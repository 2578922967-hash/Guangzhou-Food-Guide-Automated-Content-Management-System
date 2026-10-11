"""
模板相关 API。
"""

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from ...services import template_service
from ...utils import renderer

bp = Blueprint("templates", __name__)


@bp.get("/")
def list_templates() -> Any:
    templates = template_service.list_templates()
    return jsonify({"items": templates, "count": len(templates)})


@bp.get("/<int:template_id>")
def get_template(template_id: int) -> Any:
    template = template_service.get_template(template_id)
    if not template:
        return jsonify({"error": "模板不存在"}), 404
    # 解析占位符 JSON 并转换为键名列表
    placeholders_dict = renderer.parse_placeholders(template.get("placeholders_json"))
    template["placeholders"] = list(placeholders_dict.keys()) if placeholders_dict else []
    return jsonify(template)


@bp.put("/<int:template_id>")
def update_template(template_id: int) -> Any:
    payload = request.get_json(force=True)
    payload["template_id"] = template_id
    template_service.create_or_update_template(payload)
    return jsonify({"status": "updated"})


@bp.delete("/<int:template_id>")
def delete_template(template_id: int) -> Any:
    success = template_service.delete_template(template_id)
    if not success:
        return jsonify({"error": "模板不存在"}), 404
    return jsonify({"status": "deleted"})


