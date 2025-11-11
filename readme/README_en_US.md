## Text Process Tool (text-process-tool)

**Author:** covfefe  
**Version:** 0.0.1
**Type:** Tool

### Overview

This is a Dify tool plugin providing text utilities:
- Clean Markdown code fences by language marker
- Strip `<think>` tags and their content
- Convert text to files (`html`, `txt`, `md/markdown`, `json`, `csv`, `xml`, `sql`)
- Convert JSON string to XML (supports custom root via `custom_root`)
- Convert XML to JSON string

### Tools & Parameters

- `think-clean`
  - Params: `text` (required)
  - Function: remove `<think>...</think>` from text (case-insensitive, multiline)

- `markdown-fence-clean`
  - Params: `marker` (required), `text` (required)
  - Function: strip code fences by marker, keep inner content

- `text-to-file`
  - Params: `format` (required), `content` (required), `filename` (required)
  - Function: generate a file in given format and return it (supports SDK `save_as`)

- `json-str-to-xml`
  - Params: `json` (required), `custom_root` (optional, default `root`)
  - Function: convert a JSON string to XML; root tag can be customized by `custom_root`
  - Root tag validation: must start with a letter or `_`, followed by letters, digits, `_`, `-`, or `.`

- `xml-to-json-str`
  - Params: `xml` (required)
  - Function: convert XML text to JSON string

### Examples

JSON → XML
```
Input:
{"user":{"name":"Alice","age":30},"tags":["a","b"]}
custom_root = "MyRoot"

Output:
<MyRoot><user><name>Alice</name><age>30</age></user><tags><item>a</item><item>b</item></tags></MyRoot>
```

XML → JSON
```
Input:
<root><user><name>Alice</name><age>30</age></user><tags><item>a</item><item>b</item></tags></root>

Output:
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

### Notes

- If `custom_root` is invalid (e.g., starts with a digit or contains disallowed chars), an error is returned.
- Values from XML typically appear as strings in JSON; convert types as needed in your application.