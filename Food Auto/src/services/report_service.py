"""
报告生成服务。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable

from ..config import settings
from ..db.dao import report_dao, template_dao
from ..utils import renderer
from . import query_service

TemplateContextBuilder = Callable[[dict[str, Any]], dict[str, Any]]


class TemplateNotFoundError(RuntimeError):
    pass


class UnsupportedTemplateError(RuntimeError):
    pass


TEMPLATE_BUILDERS: dict[int, TemplateContextBuilder] = {
    1: lambda params: query_service.star_rating_distribution(),
    2: lambda params: query_service.best_value_for_money(
        price_cap=float(params.get("price_cap", 80)),
        top_n=int(params.get("top_n", 5)),
    ),
    4: lambda params: query_service.hidden_gem(params["district"]),
    5: lambda params: query_service.district_food_express(params["district"]),
    6: lambda params: query_service.delivery_picks(
        district=params["district"],
        min_score=float(params.get("min_score", 8.5)),
    ),
    7: lambda params: query_service.statistics_visualization_report(),
}


def _enhance_visualization_html(html_content: str, context: dict[str, Any]) -> str:
    """
    为模板7的HTML添加Chart.js脚本和图表初始化代码。
    """
    # 解析JSON数据字段
    category_labels = context.get("category_labels_json", [])
    category_counts = context.get("category_counts_json", [])
    district_labels = context.get("district_labels_json", [])
    district_counts = context.get("district_counts_json", [])
    price_labels = context.get("price_labels_json", [])
    price_counts = context.get("price_counts_json", [])
    star_labels = context.get("star_labels_json", [])
    star_counts = context.get("star_counts_json", [])
    
    # 确保是列表格式
    if isinstance(category_labels, str):
        category_labels = json.loads(category_labels)
    if isinstance(category_counts, str):
        category_counts = json.loads(category_counts)
    if isinstance(district_labels, str):
        district_labels = json.loads(district_labels)
    if isinstance(district_counts, str):
        district_counts = json.loads(district_counts)
    if isinstance(price_labels, str):
        price_labels = json.loads(price_labels)
    if isinstance(price_counts, str):
        price_counts = json.loads(price_counts)
    if isinstance(star_labels, str):
        star_labels = json.loads(star_labels)
    if isinstance(star_counts, str):
        star_counts = json.loads(star_counts)
    
    # 添加Chart.js CDN和样式
    chart_js_script = """
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
      .chart-container {
        position: relative;
        width: 100%;
        max-width: 800px;
        height: 400px;
        margin: 1rem 0;
      }
      .chart-container canvas {
        max-width: 100%;
        max-height: 100%;
      }
    </style>
    <script>
      document.addEventListener('DOMContentLoaded', function() {
        const Chart = window.Chart;
        if (!Chart) {
          console.error('Chart.js not loaded');
          return;
        }
        
        // 数据
        const categoryLabels = """ + json.dumps(category_labels, ensure_ascii=False) + """;
        const categoryCounts = """ + json.dumps(category_counts, ensure_ascii=False) + """;
        const districtLabels = """ + json.dumps(district_labels, ensure_ascii=False) + """;
        const districtCounts = """ + json.dumps(district_counts, ensure_ascii=False) + """;
        const priceLabels = """ + json.dumps(price_labels, ensure_ascii=False) + """;
        const priceCounts = """ + json.dumps(price_counts, ensure_ascii=False) + """;
        const starLabels = """ + json.dumps(star_labels, ensure_ascii=False) + """;
        const starCounts = """ + json.dumps(star_counts, ensure_ascii=False) + """;
        
        // 初始化Category Chart
        const categoryCanvas = document.getElementById('categoryChart');
        if (categoryCanvas && categoryLabels.length > 0) {
          const categoryCtx = categoryCanvas.getContext('2d');
          new Chart(categoryCtx, {
            type: 'bar',
            data: {
              labels: categoryLabels,
              datasets: [{
                label: 'Number of Restaurants',
                data: categoryCounts,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { display: true }
              },
              scales: {
                y: { beginAtZero: true }
              }
            }
          });
        }
        
        // 初始化District Chart
        const districtCanvas = document.getElementById('districtChart');
        if (districtCanvas && districtLabels.length > 0) {
          const districtCtx = districtCanvas.getContext('2d');
          new Chart(districtCtx, {
            type: 'pie',
            data: {
              labels: districtLabels,
              datasets: [{
                data: districtCounts,
                backgroundColor: [
                  'rgba(255, 99, 132, 0.6)',
                  'rgba(54, 162, 235, 0.6)',
                  'rgba(255, 206, 86, 0.6)',
                  'rgba(75, 192, 192, 0.6)',
                  'rgba(153, 102, 255, 0.6)',
                  'rgba(255, 159, 64, 0.6)',
                  'rgba(199, 199, 199, 0.6)',
                  'rgba(83, 102, 255, 0.6)',
                  'rgba(255, 99, 255, 0.6)',
                  'rgba(99, 255, 132, 0.6)'
                ]
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false
            }
          });
        }
        
        // 初始化Price Chart
        const priceCanvas = document.getElementById('priceChart');
        if (priceCanvas && priceLabels.length > 0) {
          const priceCtx = priceCanvas.getContext('2d');
          new Chart(priceCtx, {
            type: 'line',
            data: {
              labels: priceLabels,
              datasets: [{
                label: 'Number of Restaurants',
                data: priceCounts,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { display: true }
              },
              scales: {
                y: { beginAtZero: true }
              }
            }
          });
        }
        
        // 初始化Star Chart
        const starCanvas = document.getElementById('starChart');
        if (starCanvas && starLabels.length > 0) {
          const starCtx = starCanvas.getContext('2d');
          new Chart(starCtx, {
            type: 'doughnut',
            data: {
              labels: starLabels,
              datasets: [{
                data: starCounts,
                backgroundColor: [
                  'rgba(255, 215, 0, 0.6)',
                  'rgba(192, 192, 192, 0.6)',
                  'rgba(205, 127, 50, 0.6)',
                  'rgba(255, 99, 132, 0.6)',
                  'rgba(54, 162, 235, 0.6)'
                ]
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false
            }
          });
        }
      });
    </script>
    """
    
    # 将脚本添加到HTML末尾
    return html_content + chart_js_script


def _build_context(template_id: int, params: dict[str, Any]) -> dict[str, Any]:
    if template_id not in TEMPLATE_BUILDERS:
        raise UnsupportedTemplateError(f"Unsupported template ID: {template_id}")
    
    # 验证必需参数
    if template_id in [4, 5, 6] and not params.get("district"):
        raise ValueError(f"Template {template_id} requires 'district' parameter")
    
    builder = TEMPLATE_BUILDERS[template_id]
    try:
        return builder(params)
    except KeyError as e:
        missing_param = str(e).strip("'\"")
        raise ValueError(f"Missing required parameter: {missing_param}")
    except Exception as e:
        raise RuntimeError(f"Failed to build template context: {str(e)}")


def _render_outputs(template: dict[str, Any], context: dict[str, Any], template_id: int = None) -> dict[str, Any]:
    content = template["content"]
    rendered_default = renderer.render_text(content, context)
    default_format = template["default_format"]

    outputs = {
        "format": default_format,
        "text": rendered_default,
        "markdown": "",
        "html": "",
    }

    if default_format == "markdown":
        # Markdown 格式：
        # - markdown: 原内容（保留markdown语法）
        # - text: 转换为纯文本（去除markdown语法）
        # - html: 转换为HTML（从markdown渲染）
        outputs["markdown"] = rendered_default
        outputs["text"] = renderer.markdown_to_text(rendered_default)
        outputs["html"] = renderer.markdown_to_html(rendered_default)
    elif default_format == "html":
        # HTML 格式：
        # - html: 原内容（可能增强，如添加Chart.js）
        # - text: 转换为纯文本（去除HTML标签）
        # - markdown: 转换为Markdown格式（从HTML转换）
        html_content = rendered_default
        
        # 如果是模板7（可视化报告），添加Chart.js脚本和初始化代码
        if template_id == 7:
            html_content = _enhance_visualization_html(html_content, context)
        
        outputs["html"] = html_content
        # 从 HTML 提取纯文本（去除标签）
        outputs["text"] = re.sub(r"<[^>]+>", "", rendered_default).strip()
        # 将 HTML 转为 Markdown 格式
        outputs["markdown"] = renderer.html_to_markdown(rendered_default)
    else:  # text format
        # 文本格式：
        # - text: 原内容（纯文本）
        # - markdown: 原内容（如果是纯文本，markdown也是原内容）
        # - html: 从markdown转换（尝试转换，如果包含markdown语法）
        outputs["text"] = rendered_default
        outputs["markdown"] = rendered_default
        # 尝试将文本作为markdown转换（如果没有markdown语法，会原样返回）
        outputs["html"] = renderer.markdown_to_html(rendered_default)

    # 处理标题中的占位符
    title_template = template.get("title") or ""
    if title_template:
        try:
            outputs["title"] = renderer.render_text(title_template, context)
        except renderer.MissingPlaceholderError:
            outputs["title"] = title_template
    else:
        outputs["title"] = "Generated Report"

    outputs["keywords"] = template.get("keywords", "")
    outputs["context"] = context
    return outputs


def generate_report(
    template_id: int,
    params: dict[str, Any],
    *,
    output_format: str | None = None,
    save: bool = False,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """
    生成报告，返回包含 text/markdown/html 的字典。
    """
    template = template_dao.get_template(template_id)
    if not template:
        raise TemplateNotFoundError(f"Template not found: {template_id}")

    context = _build_context(template_id, params)
    rendered = _render_outputs(template, context, template_id=template_id)

    if output_format:
        selected = rendered.get(output_format)
        if selected is None:
            raise ValueError(f"Unsupported output format: {output_format}")
        rendered["selected_format"] = output_format
        rendered["selected_content"] = selected

    if output_path:
        output_file = settings.resolve_path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        content_to_write = rendered["selected_content"] if output_format else rendered["text"]
        output_file.write_text(content_to_write, encoding="utf-8")
        rendered["output_path"] = str(output_file)

    if save:
        payload = {
            "template_id": template_id,
            "title": rendered["title"],
            "params_json": json.dumps(params, ensure_ascii=False),
            "content_text": rendered["text"],
            "content_markdown": rendered["markdown"],
            "content_html": rendered["html"],
        }
        report_id = report_dao.create_report_record(payload)
        rendered["report_id"] = report_id

    return rendered


