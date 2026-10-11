"""
模板业务逻辑封装。
"""

from __future__ import annotations

import json
from typing import Any

from ..db.dao import template_dao
from ..templates_seed.data import TEMPLATE_SEED_DATA
from ..utils import validators


def create_or_update_template(payload: dict[str, Any]) -> None:
    """
    新增或更新模板。
    """
    validators.ensure_placeholders(payload)
    template_dao.upsert_template(payload)


def get_template(template_id: int) -> dict[str, Any] | None:
    return template_dao.get_template(template_id)


def list_templates(filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    return template_dao.list_templates(filters)


def delete_template(template_id: int) -> bool:
    return template_dao.delete_template(template_id)


def seed_default_templates(force: bool = False) -> None:
    """
    将模板种子数据写入数据库。
    `force=True` 时会覆盖已有模板。
    """
    if force:
        for record in TEMPLATE_SEED_DATA:
            payload = {
                "template_id": record["template_id"],
                "title": record["title"],
                "keywords": record["keywords"],
                "default_format": record["default_format"],
                "content": record["content"],
                "placeholders_json": json.dumps(record["placeholders"], ensure_ascii=False),
                "sample_output": record.get("sample_output"),
                "version": record.get("version", 1),
            }
            create_or_update_template(payload)
    else:
        template_dao.seed_templates(TEMPLATE_SEED_DATA)


