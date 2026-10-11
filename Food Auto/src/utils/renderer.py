"""
模板渲染工具。
"""

from __future__ import annotations

import json
import re
from string import Formatter
from typing import Any, Mapping

import markdown

try:
    import html2text
except ImportError:
    html2text = None


class MissingPlaceholderError(KeyError):
    """
    占位符缺失异常。
    """


class StrictFormatter(Formatter):
    """
    对 str.format 进行包装，当占位符缺失时抛出异常。
    """

    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            if key in kwargs:
                return kwargs[key]
            raise MissingPlaceholderError(key)
        return super().get_value(key, args, kwargs)


def render_text(template: str, context: Mapping[str, Any]) -> str:
    formatter = StrictFormatter()
    return formatter.format(template, **context)


def markdown_to_html(md_text: str) -> str:
    return markdown.markdown(md_text, extensions=["extra", "tables", "sane_lists"])


def markdown_to_text(md_text: str) -> str:
    """
    将Markdown文本转换为纯文本，去除所有Markdown语法标记。
    
    移除的标记包括：
    - 标题标记 (#, ##, etc.)
    - 粗体 (**text**, __text__)
    - 斜体 (*text*, _text_)
    - 代码块 (```...```, `...`)
    - 链接 ([text](url))
    - 图片 (![alt](url))
    - 列表标记 (-, *, +, 1.)
    - 引用 (>)
    - 水平线 (---, ***)
    """
    text = md_text
    
    # 移除代码块（```...```）
    text = re.sub(r'```[\s\S]*?```', '', text)
    
    # 移除行内代码（`...`）
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # 移除图片（![alt](url)）
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)
    
    # 移除链接（[text](url)），保留文本
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # 移除粗体（**text** 或 __text__）
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    
    # 移除斜体（*text* 或 _text_），但要注意不要误删粗体
    text = re.sub(r'(?<!\*)\*([^\*]+?)\*(?!\*)', r'\1', text)
    text = re.sub(r'(?<!_)_([^_]+?)_(?!_)', r'\1', text)
    
    # 移除标题标记（#, ##, etc.）
    text = re.sub(r'^#{1,6}\s+(.+)$', r'\1', text, flags=re.MULTILINE)
    
    # 移除列表标记（-, *, +, 1.）
    text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[\s]*\d+\.\s+', '', text, flags=re.MULTILINE)
    
    # 移除引用标记（>）
    text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
    
    # 移除水平线（---, ***）
    text = re.sub(r'^[-*]{3,}$', '', text, flags=re.MULTILINE)
    
    # 移除多余的空行（连续3个以上空行变为2个）
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 清理首尾空白
    text = text.strip()
    
    return text


def html_to_markdown(html_text: str) -> str:
    """
    将HTML文本转换为Markdown格式。
    使用html2text库进行转换。
    """
    if html2text is None:
        # 如果html2text未安装，使用简单的替换方法
        return _html_to_markdown_simple(html_text)
    
    # 使用html2text进行转换
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # 不限制行宽
    h.unicode_snob = True
    h.mark_code = True
    
    # 转换HTML到Markdown
    md_text = h.handle(html_text)
    return md_text.strip()


def _html_to_markdown_simple(html_text: str) -> str:
    """
    简单的HTML到Markdown转换（备用方案，不依赖外部库）。
    只处理基本的HTML标签。
    """
    text = html_text
    
    # 移除script和style标签及其内容
    text = re.sub(r'<script[\s\S]*?</script>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<style[\s\S]*?</style>', '', text, flags=re.IGNORECASE)
    
    # 转换标题
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<h6[^>]*>(.*?)</h6>', r'###### \1', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 转换粗体
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 转换斜体
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 转换链接
    text = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 转换图片
    text = re.sub(r'<img[^>]*alt=["\']([^"\']*)["\'][^>]*src=["\']([^"\']*)["\'][^>]*>', r'![\1](\2)', text, flags=re.IGNORECASE)
    
    # 转换段落
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 转换列表项
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 转换换行
    text = re.sub(r'<br[^>]*/?>', '\n', text, flags=re.IGNORECASE)
    
    # 移除所有剩余的HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 解码HTML实体
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    
    # 清理多余的空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def parse_placeholders(placeholders: str | dict[str, Any] | None) -> dict[str, Any]:
    if placeholders is None:
        return {}
    if isinstance(placeholders, dict):
        return placeholders
    try:
        return json.loads(placeholders)
    except json.JSONDecodeError:
        return {}

