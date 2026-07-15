---
name: xlsx-to-images
description: "Use this skill when you need to view, analyze, or reference Excel file contents but face token limits or readability issues. Convert Excel sheets to PNG images to visually inspect large spreadsheets, design documents, file definitions, coding standards, or checklists - even when the user doesn't explicitly mention 'convert' or 'image'. Each sheet becomes a separate PNG for easy review. Ideal for: understanding Excel-based specifications, reviewing tabular data visually, or working around token constraints with large .xlsx files. Do NOT use for creating or editing Excel files."
license: Proprietary. LICENSE.txt has complete terms
---

# Excel to Images Converter

## 概要

大容量のExcelファイルをシート毎にPNG画像に変換するツールです。トークン上限を回避し、視覚的にExcelの内容を確認できます。

## 使用タイミング

このスキルは、Excelファイル（.xlsx）の各シートをPNG画像に変換する場合に使用します。

## 基本的な使い方

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイルパス>
```

スクリプトは元のExcelファイルと同じ場所に `<ファイル名>_images` ディレクトリを作成し、各シートをPNG画像として保存します。

## 使用例

### ファイル定義書の変換

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py "インプット/ファイル定義書/ファイル定義書_DCEV006.xlsx"

# 出力: インプット/ファイル定義書/ファイル定義書_DCEV006_images/
#   - Cover Sheet.png
#   - Update History.png
#   - DCEV006(ES部門作業時間月報).png
#   - ...
```

### 設計規約の変換

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py "インプット/A02.07.07 バッチ設計規約.xlsx"
```

### セルフチェックリストの変換

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py "セルフチェックリスト/ソースコードチェックリスト_標準版_ver1.0.0_PGMno.xlsx"
```

## オプション

### 文字サイズの調整（推奨）

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --font-size 14
```

デフォルト: 12
推奨値: 14-16（読みやすさ向上）

### 出力先の指定

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --output <出力ディレクトリ>
```

### 画像解像度の指定

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --dpi 200
```

デフォルト: 150 DPI

### 最大画像幅の指定

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --max-width 2560
```

デフォルト: 1920 ピクセル

### 特定シートのみ変換

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --sheets "Sheet1" "Sheet2"
```

### JSON形式で結果を出力

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --json
```

## 出力構造

```
インプット/ファイル定義書/
├── ファイル定義書_DCEV006.xlsx
└── ファイル定義書_DCEV006_images/
    ├── Cover Sheet.png
    ├── Update History.png
    ├── DCEV006(ES部門作業時間月報).png
    └── ...
```

## 必要なパッケージ

- `openpyxl`: Excelファイルの読み込み
- `Pillow (PIL)`: 画像生成

インストール:
```bash
pip install openpyxl pillow
```

## 制限事項

- 画像、グラフ、マクロは変換されません（セルの値とテキストのみ）
- 複雑な書式（結合セル、条件付き書式など）は簡略化されます
- 非常に大きなシート（1000行以上）は処理に時間がかかる場合があります

## トラブルシューティング

### エラー: `No module named 'PIL'`

```bash
pip install pillow
```

### エラー: `No module named 'openpyxl'`

```bash
pip install openpyxl
```

### 文字化けが発生する場合

Windowsのコンソールでは日本語が正しく表示されない場合があります。`--json` オプションを使用してJSON形式で出力してください。

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --json
```

## 複数ファイルの一括変換

```bash
# PowerShellの場合
Get-ChildItem "インプット\ファイル定義書\*.xlsx" | ForEach-Object { python .bob/skills/xlsx-to-images/scripts/excel_to_images.py $_.FullName --font-size 14 }
```

## 関連スキル

- **xlsx**: Excelファイルの作成・編集・分析に使用
- **xlsx-to-images**: 大容量Excelファイルの読み込みに使用（本スキル）

## 詳細ドキュメント

詳細な使用方法とオプションについては、[scripts/README.md](scripts/README.md)を参照してください。