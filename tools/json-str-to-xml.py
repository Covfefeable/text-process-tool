from collections.abc import Generator
from typing import Any
import json
import re

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

try:
    from dicttoxml import dicttoxml
except Exception:
    dicttoxml = None  # 延迟在执行时检查依赖是否可用


def _json_to_xml(json_str: str, custom_root: str | None = None) -> str:
    if dicttoxml is None:
        raise RuntimeError("缺少依赖：dicttoxml，请安装后重试")

    data = json.loads(json_str)
    # 根标签：支持自定义，默认 root；做基本合法性校验
    root = (custom_root or "root").strip() or "root"
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_\-\.]*$", root):
        raise ValueError(f"无效的根标签：{root}")

    # 使用较为干净的 XML 输出：不带类型属性，列表项统一为 <item>
    xml_bytes = dicttoxml(data, attr_type=False, item_func=lambda _: "item", custom_root=root)
    return xml_bytes.decode("utf-8")


class JsonStrToXmlTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        json_input = str(tool_parameters.get("json", ""))
        custom_root = tool_parameters.get("custom_root")
        if custom_root is not None:
            custom_root = str(custom_root)

        if json_input.strip() == "":
            yield self.create_text_message("缺少必填参数：json（JSON 字符串）")
            return

        try:
            result_xml = _json_to_xml(json_input, custom_root=custom_root)
            yield self.create_text_message(result_xml)
        except json.JSONDecodeError as e:
            yield self.create_text_message(f"JSON 解析失败：{str(e)}")
        except Exception as e:
            yield self.create_text_message(f"转换失败：{str(e)}")