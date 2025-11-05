from collections.abc import Generator
from typing import Any
import re

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


def _clean_html_text(text: str) -> str:
    # 仅移除代码块标记（保留原有换行，以便 HTML 可读）
    cleaned = re.sub(r"(?i)```html", "", text)
    cleaned = cleaned.replace("```", "")
    return cleaned.strip()


class HtmlCleanTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        html_text = str(tool_parameters.get("html", ""))
        result = _clean_html_text(html_text)
        yield self.create_text_message(result)