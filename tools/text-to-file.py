from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


MIME_MAP: dict[str, str] = {
    "html": "text/html",
    "txt": "text/plain",
    "md": "text/markdown",
    "markdown": "text/markdown",
    "json": "application/json",
    "csv": "text/csv",
    "xml": "application/xml",
}

EXT_MAP: dict[str, str] = {
    "html": "html",
    "txt": "txt",
    "md": "md",
    "markdown": "md",
    "json": "json",
    "csv": "csv",
    "xml": "xml",
}


def _ensure_filename(filename: str, fmt: str) -> str:
    fmt = fmt.lower()
    ext = EXT_MAP.get(fmt)
    if not ext:
        return filename
    if not filename.lower().endswith(f".{ext}"):
        return f"{filename}.{ext}"
    return filename


def _build_blob(fmt: str, content: str) -> tuple[bytes, str]:
    fmt = fmt.lower()
    mime = MIME_MAP.get(fmt)
    if not mime:
        raise ValueError(f"不支持的文件格式: {fmt}")
    if fmt == "html":
        html_text = (
            "<!DOCTYPE html>\n"
            "<html><head><meta charset=\"utf-8\"></head><body>\n"
            f"{content}\n"
            "</body></html>\n"
        )
        return html_text.encode("utf-8"), mime
    # 其他文本格式直接按原文写入
    return content.encode("utf-8"), mime


class TextToFileTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        fmt = str(tool_parameters.get("format", "")).strip().lower()
        content = str(tool_parameters.get("content", ""))
        filename = str(tool_parameters.get("filename", "")).strip()

        if not fmt:
            yield self.create_text_message("缺少必填参数：format（文件格式）")
            return
        if filename == "":
            yield self.create_text_message("缺少必填参数：filename（文件名）")
            return

        try:
            blob_bytes, mime_type = _build_blob(fmt, content)
            save_as = _ensure_filename(filename, fmt)
            try:
                # 兼容不同 SDK 版本，如果不支持 save_as 则回退
                yield self.create_blob_message(blob=blob_bytes, meta={"mime_type": mime_type}, save_as=save_as)
            except TypeError:
                yield self.create_blob_message(blob=blob_bytes, meta={"mime_type": mime_type})
        except Exception as e:
            yield self.create_text_message(f"生成文件失败：{str(e)}")
            raise e