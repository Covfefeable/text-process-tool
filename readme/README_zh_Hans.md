## 文本百宝箱（text-process-tool）

**作者：** covfefe  
**版本：** 0.0.1  
**类型：** 工具（Tool）

### 简介

这是一个 Dify 工具插件，提供以下文本处理能力：
- 按标记清理 Markdown 代码块围栏
- 移除 `<think>` 标签及其内容
- 文本转文件（支持 `html`、`txt`、`md/markdown`、`json`、`csv`、`xml`、`sql`）
- JSON 字符串转 XML（支持自定义根标签 `custom_root`）
- XML 转 JSON 字符串

### 工具与参数

- `think-clean`
  - 参数：`text`（必填）
  - 功能：移除文本中的 `<think>...</think>`（大小写不敏感、跨行）

- `markdown-fence-clean`
  - 参数：`marker`（必填）、`text`（必填）
  - 功能：按语言标记移除 Markdown 代码块围栏，保留内部内容

- `text-to-file`
  - 参数：`format`（必填）、`content`（必填）、`filename`（必填）
  - 功能：将文本内容按指定格式生成文件并返回（支持 SDK 的 `save_as`）

- `json-str-to-xml`
  - 参数：`json`（必填）、`custom_root`（可选，默认 `root`）
  - 功能：将 JSON 字符串转换为 XML 文本；根标签可通过 `custom_root` 指定
  - 根标签校验规则：必须以字母或下划线开头，后续可包含字母数字、下划线、连字符和点

- `xml-to-json-str`
  - 参数：`xml`（必填）
  - 功能：将 XML 文本转换为 JSON 字符串

### 使用示例

JSON → XML
```
输入参数：
json = {"user":{"name":"Alice","age":30},"tags":["a","b"]}
custom_root = "MyRoot"

输出：
<MyRoot><user><name>Alice</name><age>30</age></user><tags><item>a</item><item>b</item></tags></MyRoot>
```

XML → JSON
```
输入：
<root><user><name>Alice</name><age>30</age></user><tags><item>a</item><item>b</item></tags></root>

输出：
{
  "root": {
    "user": {"name": "Alice", "age": "30"},
    "tags": {"item": ["a", "b"]}
  }
}
```

### 安装与运行

```
pip install -r requirements.txt
python -m main
```

### 注意事项

- `json-str-to-xml` 的 `custom_root` 非法时会报错（如以数字开头或包含不允许的字符）。
- `xml-to-json-str` 输出的数值通常以字符串形式出现，属于常见行为，如有需要可在上层做类型转换。
