from collections.abc import Generator
from typing import Any
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

try:
    import xmltodict
except Exception:
    xmltodict = None  # 延迟在执行时检查依赖是否可用


def _xml_to_json(xml_str: str) -> str:
    if xmltodict is None:
        raise RuntimeError("缺少依赖：xmltodict，请安装后重试")

    data = xmltodict.parse(xml_str)
    # 直接将字典序列化为字符串，保留中文字符
    return json.dumps(data, ensure_ascii=False, indent=2)


class XmlToJsonStrTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        xml_input = str(tool_parameters.get("xml", ""))

        if xml_input.strip() == "":
            yield self.create_text_message("缺少必填参数：xml（XML 文本）")
            return

        try:
            result_json = _xml_to_json(xml_input)
            yield self.create_text_message(result_json)
        except Exception as e:
            yield self.create_text_message(f"转换失败：{str(e)}")