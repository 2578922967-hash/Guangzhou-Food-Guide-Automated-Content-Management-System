"""
报告相关 API。
"""

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from ...services import report_service

bp = Blueprint("reports", __name__)


@bp.post("/generate")
def generate() -> Any:
    try:
        data = request.get_json(force=True)
        template_id = data.get("template_id")
        if not template_id:
            return jsonify({"error": "缺少 template_id 参数"}), 400
        
        params = data.get("params") or {}
        output_format = data.get("format")
        save = bool(data.get("save"))
        
        output = report_service.generate_report(
            template_id,
            params,
            output_format=output_format,
            save=save,
        )
        return jsonify(output)
    except report_service.TemplateNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except report_service.UnsupportedTemplateError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"生成报告失败: {str(e)}"}), 500


