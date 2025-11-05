from collections.abc import Generator
from typing import Any
import re

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


def _clean_sql_text(text: str) -> str:
    # 去除代码块标记
    cleaned = re.sub(r"(?i)```sql", "", text)
    cleaned = cleaned.replace("```", "")
    # 去除换行（转为空格，避免词粘连）
    cleaned = cleaned.replace("\r", " ").replace("\n", " ")
    # 去除首尾空白
    return cleaned.strip()


class SqlCleanTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        sql_text = str(tool_parameters.get("sql", ""))
        result = _clean_sql_text(sql_text)
        yield self.create_text_message(result)