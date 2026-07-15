# Excel to Markdown Converter - スクリプト詳細

## 概要

ExcelファイルをMarkdown形式に変換するPythonスクリプトです。各シートに画像や図形が含まれているかを自動判定し、適切な形式で出力します。

## ファイル構成

```
.bob/skills/excel-to-md/
├── SKILL.md                          # スキル定義ファイル
└── scripts/
    ├── README.md                     # 本ファイル
    ├── excel_to_markdown_with_images.py  # メインスクリプト
    ├── split_excel_sheets.py         # シート分割スクリプト
    └── merge_markdown.py             # Markdownマージスクリプト
```

## 使用方法

### 基本的な使い方

```bash
python excel_to_markdown_with_images.py <Excelファイルパス>
```

### オプション付き

```bash
python excel_to_markdown_with_images.py <Excelファイルパス> [出力Markdownファイルパス] [DPI]
```

## パラメータ詳細

### 必須パラメータ

| パラメータ | 説明 | 例 |
|:---|:---|:---|
| Excelファイルパス | 変換対象のExcelファイル | `"インプット/コーディング規約.xlsx"` |

### オプションパラメータ

| パラメータ | デフォルト | 説明 | 例 |
|:---|:---|:---|:---|
| 出力Markdownファイルパス | 自動生成 | 出力先のMarkdownファイル | `"インプット/コーディング規約.md"` |
| DPI | 250 | 画像変換時の解像度 | `400` |

## 処理フロー

### Step 1: シート判定

各シートに対して、画像・図形の有無を判定します：

```python
def has_images_in_sheet(sheet):
    """
    シートに画像が含まれているかチェック
    
    Returns:
        bool: 画像が含まれている場合True
    """
    shapes_count = sheet.api.Shapes.Count
    return shapes_count > 0
```

### Step 2: 雛形Markdown作成

シート名をh2セクションとした雛形Markdownファイルを作成します：

- **画像・図形なしシート**: `<!-- TODO: シート 'シート名' の内容をここに追加（ExcelをAIで読み取り） -->`
- **画像・図形ありシート**: `<!-- IMAGES: シート 'シート名' の画像をここに追加 -->`

### Step 3: シート分割

Excelファイルを1シートずつ別々のファイルに分割します：

```python
def split_excel_sheets(excel_file, output_dir):
    """
    Excelファイルを1シートずつ別ファイルに分割
    
    Args:
        excel_file: 元のExcelファイルパス
        output_dir: 出力先ディレクトリ
    
    Returns:
        dict: {シート名: 分割ファイルパス}
    """
```

### Step 4: 画像・図形判定

各分割ファイルについて、画像・図形の有無を再確認します。

### Step 5: 画像化

画像・図形ありシートを画像化します：

```python
def convert_sheet_to_images(excel_file, sheet_name, output_dir, dpi=250, show_gridlines=False):
    """
    Excelシートを画像に変換
    
    Args:
        excel_file: Excelファイルパス
        sheet_name: シート名
        output_dir: 出力先ディレクトリ
        dpi: 解像度
        show_gridlines: 枠線表示
    
    Returns:
        list: 生成された画像ファイルのパスリスト
    """
```

### Step 5.5: 画像参照の追加

雛形Markdownの`<!-- IMAGES -->`プレースホルダーを実際の画像パスに置き換えます。

### Step 6: 画像・図形なしシートの記録

画像・図形なしシートをAIによるテキスト抽出対象として記録します。

### Step 7: メタ情報保存

シート情報を`sheet_info.json`に保存します：

```json
[
  {
    "name": "表紙",
    "has_images": true,
    "split_file": "path/to/表紙.xlsx",
    "images": ["path/to/表紙.png"]
  },
  {
    "name": "目次",
    "has_images": false,
    "split_file": "path/to/目次.xlsx",
    "images": []
  }
]
```

## 出力ファイル構造

```
インプット/
├── コーディング規約.xlsx
├── コーディング規約.md          # 最終的なMarkdownファイル
└── コーディング規約_work/        # 作業ディレクトリ
    ├── sheet_info.json                # シート情報
    ├── sheets/                        # 分割されたシート
    │   ├── 表紙.xlsx
    │   ├── 目次.xlsx
    │   └── ...
    ├── 表紙_images/                   # シートごとの画像ディレクトリ
    │   └── 表紙.png
    ├── 目次_images/                   # 画像なしシートも画像化される
    │   └── 目次.png
    └── ...
```

## AIによるテキスト抽出とマージ

### テキスト抽出（AIによる実行）

画像・図形なしシートについて、AIが画像を見てテキストを抽出します：

1. `sheet_info.json`で`has_images: false`のシートを確認
2. 対応する画像ファイル（例：`目次_images/目次.png`）を読み込み
3. 画像からテキストを抽出してMarkdown形式で保存（例：`目次_extracted.md`）

### マージ（スクリプト実行）

抽出したMarkdownを雛形にマージします：

```bash
python merge_markdown.py <雛形Markdownファイル> <シート名> <抽出Markdownファイル>
```

**例**:
```bash
python merge_markdown.py "インプット/コーディング規約.md" "目次" "インプット/コーディング規約_work/目次_extracted.md"
```

## 使用例

### 例1: 基本的な変換

```bash
python excel_to_markdown_with_images.py "インプット/コーディング規約.xlsx"
```

**出力**:
- `インプット/コーディング規約.md`（雛形）
- `インプット/コーディング規約_work/`（作業ディレクトリ）
- `インプット/コーディング規約_work/sheet_info.json`（シート情報）
- `インプット/コーディング規約_work/sheets/`（分割シート）

### 例2: 出力先を指定

```bash
python excel_to_markdown_with_images.py "インプット/コーディング規約.xlsx" "インプット/コーディング規約.md"
```

**出力**:
- `インプット/コーディング規約.md`
- `インプット/コーディング規約_work/`（作業ディレクトリは元ファイルと同じ場所）

### 例3: 高解像度で変換

```bash
python excel_to_markdown_with_images.py "インプット/コーディング規約.xlsx" "インプット/コーディング規約.md" 400
```

**出力**:
- `インプット/コーディング規約.md`
- `インプット/コーディング規約_work/`（400 DPIの高品質画像）

### 例4: 完全なワークフロー

```bash
# Step 1-7: 雛形Markdown作成とシート分割
python excel_to_markdown_with_images.py "インプット/コーディング規約.xlsx"

# AIによるテキスト抽出（手動）
# - sheet_info.jsonで has_images: false のシートを確認
# - 画像を見てテキストを抽出し、Markdown形式で保存

# マージ
python merge_markdown.py "インプット/コーディング規約.md" "目次" "インプット/コーディング規約_work/目次_extracted.md"
```

## 生成されるMarkdownの例

### 雛形Markdown（Step 1-7完了後）

```markdown
# コーディング規約

## 表紙

![表紙](コーディング規約_work\表紙_images\表紙.png)

## 目次

<!-- TODO: シート '目次' の内容をここに追加（ExcelをAIで読み取り） -->

## 1.コード

![1.コード](コーディング規約_work\1._images\1..png)

## 改定履歴

![改定履歴](コーディング規約_work\改定履歴_images\改定履歴.png)
```

### 最終Markdown（マージ後）

```markdown
# コーディング規約

## 表紙

![表紙](コーディング規約_work\表紙_images\表紙.png)

## 目次

### 目次

| 大項目 | 中項目 | 小項目 |
|:---|:---|:---|
| 1. プログラミング | 1.1 コーディング基準 | 1.1.1 使用文字 |
| | | 1.1.2 引用符 |

## 1.プログラミング

![1.プログラミング](コーディング規約_work\1.プログラミング_images\1.プログラミング.png)

## 改定履歴

![改定履歴](コーディング規約_work\改定履歴_images\改定履歴.png)
```

## エラーハンドリング

### ファイルが見つからない場合

```python
if not excel_path.exists():
    raise FileNotFoundError(f"Excelファイルが見つかりません: {excel_file}")
```

### Excel起動エラー

```python
try:
    app = xw.App(visible=False)
    wb = app.books.open(str(excel_path.absolute()))
except Exception as e:
    print(f"Excelファイルを開けませんでした: {e}")
```

## パフォーマンス

### 処理時間の目安

| シート数 | ページ数 | DPI | 処理時間 |
|:---|:---|:---|:---|
| 5 | 10 | 250 | 約30秒 |
| 10 | 20 | 250 | 約60秒 |
| 5 | 10 | 400 | 約45秒 |

### ファイルサイズの目安

| DPI | 1ページあたり | 10ページ合計 |
|:---|:---|:---|
| 200 | 約500KB | 約5MB |
| 250 | 約800KB | 約8MB |
| 400 | 約2MB | 約20MB |

## トラブルシューティング

### エラー: `No module named 'xlwings'`

**原因**: xlwingsがインストールされていない

**解決方法**:
```bash
pip install xlwings
```

### エラー: `No module named 'fitz'`

**原因**: PyMuPDFがインストールされていない

**解決方法**:
```bash
pip install PyMuPDF
```

### エラー: `Excelが起動しません`

**原因**: Microsoft Excelがインストールされていない

**解決方法**: Microsoft Excelをインストールしてください

### 画像が不鮮明

**原因**: DPI設定が低い

**解決方法**: DPI値を上げて再変換
```bash
python excel_to_markdown_with_images.py <Excelファイル> <出力先> 400
```

### ファイルサイズが大きすぎる

**原因**: DPI設定が高い

**解決方法**: DPI値を下げて再変換
```bash
python excel_to_markdown_with_images.py <Excelファイル> <出力先> 200
```

### シート名に特殊文字が含まれる

**原因**: ファイル名に使用できない文字（`/`, `\`, `:`）がシート名に含まれている

**解決方法**: スクリプトが自動的に`_`に置換します
```python
safe_sheet_name = sheet_name.replace('/', '_').replace('\\', '_').replace(':', '_')
```

### マージが失敗する

**原因**: TODOコメントが見つからない、またはシート名が一致しない

**解決方法**:
1. 雛形Markdownファイルが存在するか確認
2. シート名が正確か確認（大文字・小文字、スペースも含めて完全一致）
3. 抽出Markdownファイルが存在するか確認

## 制限事項

1. **Windows専用**: Microsoft Excelが必要なため、Windowsでのみ動作
2. **シート名の制限**: 特殊文字は自動的に置換される
3. **複数ページ**: 大きなシートは複数ページの画像になる
4. **書式の簡略化**: 複雑な書式は変換時に簡略化される場合がある
5. **テキスト抽出**: 画像・図形なしシートのテキスト抽出はAIが手動で実施

## 依存関係

```
xlwings>=0.24.0
PyMuPDF>=1.18.0
```

## 関連ドキュメント

- [.bob/skills/excel-to-md/SKILL.md](../SKILL.md): スキル定義ファイル
- [.bob/skills/xlsx-to-images/SKILL.md](../../xlsx-to-images/SKILL.md): Excel→画像変換スキル
