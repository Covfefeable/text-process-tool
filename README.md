## text-process-tool

**Author:** covfefe  
**Version:** 0.0.1
**Type:** tool

### Description

Tool plugin for Dify providing:
- Clean Markdown code fences by marker
- Strip `<think>` tags
- Convert text to files (`html`, `txt`, `md`, `json`, `csv`, `xml`, `sql`)
- Convert JSON string to XML (supports custom root via `custom_root`)
- Convert XML to JSON string

### Tools

- `think-clean`: remove `<think>...</think>` from text
- `markdown-fence-clean`: strip code fences by language marker
- `text-to-file`: parameters: `format`, `content`, `filename`
- `json-str-to-xml`: parameters: `json`, optional `custom_root`; returns XML text
- `xml-to-json-str`: parameter: `xml`; returns JSON string

### Examples

JSON → XML
```
Input JSON:
{"user":{"name":"Alice","age":30},"tags":["a","b"]}

Optional param: custom_root = "MyRoot"

Output XML:
<MyRoot><user><name>Alice</name><age>30</age></user><tags><item>a</item><item>b</item></tags></MyRoot>
```

XML → JSON
```
Input XML:
<root><user><name>Alice</name><age>30</age></user><tags><item>a</item><item>b</item></tags></root>

Output JSON:
{
  "root": {
    "user": {"name": "Alice", "age": "30"},
    "tags": {"item": ["a", "b"]}
  }
}
```

### Install & Run

```
pip install -r requirements.txt
python -m main
```

For Chinese documentation, see `readme/README_zh_Hans.md`.



