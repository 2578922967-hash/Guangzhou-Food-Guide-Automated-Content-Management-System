"""
报告输出格式化工具。
"""

from __future__ import annotations

from typing import Iterable, Sequence

from tabulate import tabulate


def format_currency(value: float | int | None) -> str:
    if value is None:
        return "-"
    return f"¥{value:.0f}"


def format_percentage(value: float | None, digits: int = 1) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}%"


def format_rating(value: float | None, scale: int = 10, digits: int = 1) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}/{scale}"


def render_markdown_table(headers: Sequence[str], rows: Iterable[Sequence[str]]) -> str:
    return tabulate(list(rows), headers=headers, tablefmt="github")

