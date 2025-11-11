## テキスト百宝箱（text-process-tool）

**作者：** covfefe  
**バージョン：** 0.0.1
**タイプ：** ツール（Tool）

### 概要

Dify 用のテキスト処理ツールプラグインです。以下の機能を提供します：
- マーカーに応じて Markdown のコードフェンスを削除
- `<think>` タグとその内容を削除
- テキストをファイルへ変換（対応：`html`、`txt`、`md/markdown`、`json`、`csv`、`xml`、`sql`）
- JSON 文字列を XML に変換（`custom_root` でルート要素を指定可能）
- XML を JSON 文字列に変換

### ツールとパラメータ

- `think-clean`
  - パラメータ：`text`（必須）
  - 機能：テキストから `<think>...</think>` を削除（大小文字を区別しない、複数行対応）

- `markdown-fence-clean`
  - パラメータ：`marker`（必須）、`text`（必須）
  - 機能：言語マーカーに基づいてコードフェンスを削除し、内側の内容のみを保持

- `text-to-file`
  - パラメータ：`format`（必須）、`content`（必須）、`filename`（必須）
  - 機能：指定形式のファイルを生成して返却（SDK の `save_as` に対応）

- `json-str-to-xml`
  - パラメータ：`json`（必須）、`custom_root`（任意、既定値 `root`）
  - 機能：JSON 文字列を XML テキストへ変換；ルート要素は `custom_root` で指定可能
  - ルート要素の妥当性：先頭は英字または `_`、以降は英数字、`_`、`-`、`.` を許可

- `xml-to-json-str`
  - パラメータ：`xml`（必須）
  - 機能：XML テキストを JSON 文字列へ変換

### 使用例

JSON → XML
```
入力：
{"user":{"name":"Alice","age":30},"tags":["a","b"]}
custom_root = "MyRoot"

出力：
<MyRoot><user><name>Alice</name><age>30</age></user><tags><item>a</item><item>b</item></tags></MyRoot>
```

XML → JSON
```
入力：
<root><user><name>Alice</name><age>30</age></user><tags><item>a</item><item>b</item></tags></root>

出力：
{
  "root": {
    "user": {"name": "Alice", "age": "30"},
    "tags": {"item": ["a", "b"]}
  }
}
```

### インストールと実行

```
pip install -r requirements.txt
python -m main
```

### 注意事項

- `custom_root` が不正（数字で開始する、許可されない文字を含む等）の場合、エラーになります。
- XML からの値は JSON では文字列として出力されることが一般的です。必要に応じてアプリ側で型変換を行ってください。