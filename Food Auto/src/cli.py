"""
命令行入口。
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import click

from .config import settings
from .db import connection
from .interface import run_menu
from .services import query_service, report_service, restaurant_service, template_service

LOG_LEVEL = getattr(logging, str(settings.DEFAULT_LOG_LEVEL).upper(), logging.INFO)
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("gz_foodcms.cli")


def _parse_params(param_pairs: tuple[str, ...]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for pair in param_pairs:
        if "=" not in pair:
            raise click.BadParameter(f"参数格式应为 key=value，收到: {pair}")
        key, value = pair.split("=", 1)
        key = key.strip()
        value = value.strip()
        try:
            params[key] = json.loads(value)
        except json.JSONDecodeError:
            params[key] = value
    return params


@click.group()
def cli() -> None:
    """广州美食内容管理系统 CLI。"""


@cli.command()
@click.option("--seed/--no-seed", default=True, help="是否写入模板种子数据")
def init_db(seed: bool) -> None:
    """初始化数据库结构。"""
    connection.init_db()
    click.echo("数据库结构初始化完成。")
    if seed:
        template_service.seed_default_templates(force=False)
        click.echo("模板种子数据已写入。")


@cli.command("import-restaurants")
@click.argument("csv_path", type=click.Path(path_type=Path))
@click.option(
    "--update-existing/--no-update-existing",
    default=True,
    help="冲突时更新已有数据",
)
@click.option("--dry-run", is_flag=True, default=False, help="仅校验，不写入数据库")
@click.option("--encoding", default="utf-8", show_default=True)
def import_restaurants(csv_path: Path, update_existing: bool, dry_run: bool, encoding: str) -> None:
    """从 CSV 文件导入餐厅数据。"""
    result = restaurant_service.bulk_import_from_csv(
        csv_path,
        update_existing=update_existing,
        dry_run=dry_run,
        encoding=encoding,
    )
    click.echo(json.dumps(result, ensure_ascii=False, indent=2))


@cli.command("list-restaurants")
@click.option("--name", help="名称模糊查询")
@click.option("--category", help="菜系")
@click.option("--district", "business_district", help="商圈")
@click.option("--star", "star_level", help="星级")
@click.option("--min-taste", type=float)
@click.option("--min-env", type=float)
@click.option("--min-service", type=float)
@click.option("--min-rating", type=float)
@click.option("--max-price", type=float)
@click.option("--limit", type=int, default=20, show_default=True)
def list_restaurants(
    name: str | None,
    category: str | None,
    business_district: str | None,
    star_level: str | None,
    min_taste: float | None,
    min_env: float | None,
    min_service: float | None,
    min_rating: float | None,
    max_price: float | None,
    limit: int,
) -> None:
    """查询餐厅数据。"""
    filters = {
        "name": name,
        "category": category,
        "business_district": business_district,
        "star_level": star_level,
        "min_taste_score": min_taste,
        "min_environment_score": min_env,
        "min_service_score": min_service,
        "min_rating": min_rating,
        "max_avg_price": max_price,
    }
    result = restaurant_service.search_restaurants(filters, limit=limit)
    click.echo(json.dumps(result, ensure_ascii=False, indent=2))


@cli.command("list-templates")
def list_templates() -> None:
    """查看模板列表。"""
    templates = template_service.list_templates()
    click.echo(json.dumps(templates, ensure_ascii=False, indent=2))


@cli.command("generate-report")
@click.option("--template-id", type=int, required=True)
@click.option("-p", "--param", multiple=True, help="模板参数，格式 key=value，可重复使用")
@click.option("--format", "output_format", type=click.Choice(["text", "markdown", "html"]), default=None)
@click.option("--save/--no-save", default=False, help="是否保存生成记录")
@click.option("--output", "output_path", type=click.Path(path_type=Path), default=None, help="输出文件路径")
def generate_report(
    template_id: int,
    param: tuple[str, ...],
    output_format: str | None,
    save: bool,
    output_path: Path | None,
) -> None:
    """根据模板生成报告。"""
    params = _parse_params(param)
    try:
        result = report_service.generate_report(
            template_id,
            params,
            output_format=output_format,
            save=save,
            output_path=output_path,
        )
    except Exception as exc:
        logger.exception("生成报告失败: %s", exc)
        raise click.ClickException(str(exc)) from exc

    click.echo(json.dumps(result, ensure_ascii=False, indent=2))


@cli.command("analytics-star")
def analytics_star() -> None:
    """示例高级查询：输出按商圈的星级统计。"""
    records = list(query_service.star_level_summary_by_district())
    click.echo(json.dumps(records, ensure_ascii=False, indent=2))


@cli.command("menu")
def menu() -> None:
    """启动交互式文本界面。"""
    run_menu()


def main() -> None:
    cli()


if __name__ == "__main__":
    main()


