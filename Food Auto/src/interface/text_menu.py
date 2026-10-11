"""
命令行文本界面。
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from ..config import settings
from ..services import query_service, report_service, restaurant_service, template_service
from ..utils import validators

MENU_TEXT = """
== 广州美食指南内容管理系统 ==
1. 数据管理
   ├─ 1.1 导入数据
   ├─ 1.2 查询餐厅
   └─ 1.3 添加餐厅
2. 模板管理
   ├─ 2.1 查看模板列表
   └─ 2.2 编辑模板
3. 报告生成
   ├─ 3.1 星级分布分析
   ├─ 3.2 性价比推荐
   └─ 3.3 冬季暖食指南
4. 系统设置
   ├─ 4.1 数据库备份
   └─ 4.2 日志查看
Q. 退出系统
"""


def clear_screen() -> None:
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def prompt(message: str) -> str:
    try:
        return input(message).strip()
    except EOFError:
        return ""


def pause(message: str = "按回车键继续...") -> None:
    try:
        input(message)
    except EOFError:
        pass


def handle_import_data() -> None:
    clear_screen()
    print("=== 导入餐厅数据 ===")
    path = prompt("请输入 CSV 文件路径：")
    if not path:
        print("未输入路径，操作取消。")
        pause()
        return
    csv_path = Path(path)
    dry_run = prompt("是否仅校验数据? (y/N)：").lower() == "y"
    update_existing = prompt("遇到重复是否更新? (Y/n)：").lower() not in {"n", "no"}
    encoding = prompt("CSV 编码（默认 utf-8）：") or "utf-8"
    try:
        result = restaurant_service.bulk_import_from_csv(
            csv_path,
            update_existing=update_existing,
            dry_run=dry_run,
            encoding=encoding,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(f"导入失败：{exc}")
    pause()


def handle_query_restaurants() -> None:
    clear_screen()
    print("=== 查询餐厅 ===")
    filters: dict[str, Any] = {}
    if name := prompt("名称关键字（可空）："):
        filters["name"] = name
    if category := prompt("菜系（可空）："):
        filters["category"] = category
    if district := prompt("商圈（可空）："):
        filters["business_district"] = district
    if star := prompt("星级（可空，如 Five-Star Merchant）："):
        filters["star_level"] = star
    if max_price := prompt("最高人均价格（可空）："):
        filters["max_avg_price"] = float(max_price)
    if min_rating := prompt("最低综合评分（可空）："):
        filters["min_rating"] = float(min_rating)
    try:
        results = restaurant_service.search_restaurants(filters, limit=50)
        print(f"共返回 {len(results)} 条记录：")
        for idx, item in enumerate(results, start=1):
            print(f"{idx}. {item.get('name')} | {item.get('category')} | ¥{item.get('avg_price')}")
    except Exception as exc:
        print(f"查询失败：{exc}")
    pause()


def handle_add_restaurant() -> None:
    clear_screen()
    print("=== 添加餐厅 ===")
    payload: dict[str, Any] = {}
    for field in (
        "shop_id",
        "name",
        "category",
        "star_level",
        "business_district",
        "address",
        "avg_price",
        "reviews",
        "taste_score",
        "environment_score",
        "service_score",
        "recommended_dish_1",
        "recommended_dish_2",
        "recommended_dish_3",
        "url",
    ):
        value = prompt(f"{field}: ")
        if value:
            payload[field] = value
    try:
        clean = validators.normalize_restaurant_record(payload)
        clean["shop_id"] = payload["shop_id"]
        clean["name"] = payload["name"]
        clean["category"] = payload["category"]
        clean["star_level"] = payload["star_level"]
        restaurant_service.create_restaurant(clean)
        print("餐厅添加成功。")
    except Exception as exc:
        print(f"添加失败：{exc}")
    pause()


def handle_view_templates() -> None:
    clear_screen()
    print("=== 模板列表 ===")
    templates = template_service.list_templates()
    for tpl in templates:
        print(f"[{tpl['template_id']}] {tpl['title']} ({tpl['default_format']})")
    pause()


def handle_edit_template() -> None:
    clear_screen()
    print("=== 编辑模板 ===")
    template_id = prompt("请输入模板 ID：")
    if not template_id.isdigit():
        print("模板 ID 需为数字。")
        pause()
        return
    template = template_service.get_template(int(template_id))
    if not template:
        print("未找到模板。")
        pause()
        return
    print(f"当前模板标题：{template['title']}")
    new_title = prompt("新的标题（回车保持不变）：") or template["title"]
    new_keywords = prompt("新的关键词（逗号分隔，回车保持不变）：") or template.get("keywords", "")
    print("当前模板内容如下：")
    print(template["content"])
    print("请输入新的模板内容，结束后输入单独的 '.' 结束：")
    lines: list[str] = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        lines.append(line)
    new_content = "\n".join(lines) if lines else template["content"]
    payload = {
        "template_id": int(template_id),
        "title": new_title,
        "keywords": new_keywords,
        "default_format": template["default_format"],
        "content": new_content,
        "placeholders": json.loads(template["placeholders_json"]),
        "sample_output": template.get("sample_output"),
    }
    try:
        template_service.create_or_update_template(payload)
        print("模板更新成功。")
    except Exception as exc:
        print(f"模板更新失败：{exc}")
    pause()


def handle_report_star() -> None:
    clear_screen()
    print("=== 星级分布分析 ===")
    try:
        result = report_service.generate_report(1, {}, output_format="markdown")
        print(result["selected_content"])
    except Exception as exc:
        print(f"生成失败：{exc}")
    pause()


def handle_report_value() -> None:
    clear_screen()
    print("=== 性价比推荐 ===")
    price_cap = float(prompt("请输入预算上限（元）：") or "80")
    top_n = int(prompt("推荐数量（默认 5）：") or "5")
    try:
        result = report_service.generate_report(
            2,
            {"price_cap": price_cap, "top_n": top_n},
            output_format="markdown",
        )
        print(result["selected_content"])
    except Exception as exc:
        print(f"生成失败：{exc}")
    pause()


def handle_report_winter() -> None:
    clear_screen()
    print("=== 冬季暖食指南 ===")
    district = prompt("请输入商圈名称：")
    if not district:
        print("商圈不能为空。")
        pause()
        return
    try:
        result = report_service.generate_report(
            3,
            {"district": district},
            output_format="text",
        )
        print(result["selected_content"])
    except Exception as exc:
        print(f"生成失败：{exc}")
    pause()


def handle_report_hidden() -> None:
    clear_screen()
    print("=== 隐藏宝藏店铺 ===")
    district = prompt("请输入商圈名称：")
    if not district:
        print("商圈不能为空。")
        pause()
        return
    try:
        result = report_service.generate_report(
            4,
            {"district": district},
            output_format="markdown",
        )
        print(result["selected_content"])
    except Exception as exc:
        print(f"生成失败：{exc}")
    pause()


def handle_report_district() -> None:
    clear_screen()
    print("=== 商圈美食速递 ===")
    district = prompt("请输入商圈名称：")
    if not district:
        print("商圈不能为空。")
        pause()
        return
    try:
        result = report_service.generate_report(
            5,
            {"district": district},
            output_format="html",
        )
        print(result["selected_content"])
    except Exception as exc:
        print(f"生成失败：{exc}")
    pause()


def handle_report_delivery() -> None:
    clear_screen()
    print("=== 外卖优选 ===")
    district = prompt("请输入商圈名称：")
    if not district:
        print("商圈不能为空。")
        pause()
        return
    min_score_input = prompt("最低综合评分（默认 8.5）：") or "8.5"
    try:
        min_score = float(min_score_input)
    except ValueError:
        print("请输入合法的数值。")
        pause()
        return
    try:
        result = report_service.generate_report(
            6,
            {"district": district, "min_score": min_score},
            output_format="markdown",
        )
        print(result["selected_content"])
    except Exception as exc:
        print(f"生成失败：{exc}")
    pause()


def handle_backup() -> None:
    clear_screen()
    print("=== 数据库备份 ===")
    backup_dir = settings.OUTPUT_DIR / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / f"gz_foodcms-{timestamp}.db"
    try:
        shutil.copy2(settings.DB_PATH, backup_path)
        print(f"备份成功：{backup_path}")
    except Exception as exc:
        print(f"备份失败：{exc}")
    pause()


def handle_view_logs() -> None:
    clear_screen()
    print("=== 查看日志 ===")
    log_file = settings.LOG_DIR / "app.log"
    if not log_file.exists():
        print("暂无日志文件。")
    else:
        content = log_file.read_text(encoding="utf-8")[-2000:]
        print(content)
    pause()


MAIN_ACTIONS = {
    "1": ("数据管理", {
        "1": ("导入数据", handle_import_data),
        "2": ("查询餐厅", handle_query_restaurants),
        "3": ("添加餐厅", handle_add_restaurant),
    }),
    "2": ("模板管理", {
        "1": ("查看模板列表", handle_view_templates),
        "2": ("编辑模板", handle_edit_template),
    }),
    "3": ("报告生成", {
        "1": ("星级分布分析", handle_report_star),
        "2": ("性价比推荐", handle_report_value),
        "3": ("冬季暖食指南", handle_report_winter),
        "4": ("隐藏宝藏店铺", handle_report_hidden),
        "5": ("商圈美食速递", handle_report_district),
        "6": ("外卖优选", handle_report_delivery),
    }),
    "4": ("系统设置", {
        "1": ("数据库备份", handle_backup),
        "2": ("日志查看", handle_view_logs),
    }),
}


def run_menu() -> None:
    """
    文本菜单主循环。
    """
    while True:
        clear_screen()
        print(MENU_TEXT)
        choice = prompt("请选择功能 [1-4 或 Q]: ").lower()
        if choice in {"q", "quit", "exit"}:
            print("感谢使用，再见！")
            pause()
            clear_screen()
            return
        if choice not in MAIN_ACTIONS:
            print("无效选择。")
            pause()
            continue
        section_name, sub_actions = MAIN_ACTIONS[choice]
        while True:
            clear_screen()
            print(f"=== {section_name} ===")
            for key, (label, _) in sub_actions.items():
                print(f"{choice}.{key} {label}")
            print("B. 返回上一级")
            sub_choice = prompt("请选择功能：").lower()
            if sub_choice in {"b", "back"}:
                break
            if sub_choice not in sub_actions:
                print("无效选择。")
                pause()
                continue
            _, handler = sub_actions[sub_choice]
            handler()


