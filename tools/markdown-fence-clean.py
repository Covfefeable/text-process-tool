from collections.abc import Generator
from typing import Any
import re

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


def _clean_markdown_fence(text: str, marker: str) -> str:
    # 支持两种形式：
    # 1) 多行围栏：```marker + 换行 + 内容 + 换行 + ```
    # 2) 同行围栏：```marker 内容 ```
    # 行为：去除围栏，只保留内部内容；大小写不敏感。
    marker = marker.strip()
    if not marker:
        # 无标记时，移除任意三反引号围栏但保留内容
        cleaned = re.sub(r"(?im)^\s*```\s*$", "", text)
        cleaned = re.sub(r"(?is)```\s*(.*?)```", r"\1", cleaned)
        return cleaned.strip()

    # 统一处理：分别匹配并替换为内容（非贪婪捕获，大小写不敏感）
    # 多行围栏：``` marker [可选附加] \n 内容 \n ```
    pattern_block = rf"(?is)```[ \t]*{re.escape(marker)}[^\n]*\n(.*?)\n?```"
    cleaned = re.sub(pattern_block, r"\1", text)

    # 同行围栏：``` marker 空格 内容 ```
    pattern_inline = rf"(?is)```[ \t]*{re.escape(marker)}[ \t]+(.*?)```"
    cleaned = re.sub(pattern_inline, r"\1", cleaned)

    # 兜底：若仍存在独立围栏行，按行删除开/闭围栏
    pattern_open = rf"(?im)^\s*```\s*{re.escape(marker)}[^\n]*\s*$"
    cleaned = re.sub(pattern_open, "", cleaned)
    cleaned = re.sub(r"(?im)^\s*```\s*$", "", cleaned)
    return cleaned.strip()


class MarkdownFenceCleanTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        marker = str(tool_parameters.get("marker", ""))
        raw_text = str(tool_parameters.get("text", ""))
        result = _clean_markdown_fence(raw_text, marker)
        yield self.create_text_message(result)