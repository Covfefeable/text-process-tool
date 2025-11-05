from collections.abc import Generator
from typing import Any
import re

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


def _remove_think_tags(text: str) -> str:
    # 删除 <think>...</think>，大小写不敏感，跨行匹配，允许空白
    return re.sub(r"(?is)<\s*think\s*>.*?<\s*/\s*think\s*>", "", text)


class ThinkCleanTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        raw_text = str(tool_parameters.get("text", ""))
        result = _remove_think_tags(raw_text)
        yield self.create_text_message(result)