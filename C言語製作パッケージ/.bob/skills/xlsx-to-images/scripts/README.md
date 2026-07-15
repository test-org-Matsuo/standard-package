# Excel to Images Converter (Quick Reference)

このファイルは `excel_to_images.py` の実行早見表です。  
運用ルール、使用タイミング、詳細オプションは [SKILL.md](../SKILL.md) を正本として参照してください。

## 基本コマンド

```bash
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイルパス> --font-size 14
```

## よく使うオプション

```bash
# 出力先を指定
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --output <出力ディレクトリ>

# 解像度
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --dpi 200

# 最大幅
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --max-width 2560

# 特定シートのみ
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --sheets "Sheet1" "Sheet2"

# JSON出力
python .bob/skills/xlsx-to-images/scripts/excel_to_images.py <Excelファイル> --json
```

## 一括変換（PowerShell）

```powershell
Get-ChildItem "インプット\ファイル定義書\*.xlsx" | ForEach-Object {
  python .bob/skills/xlsx-to-images/scripts/excel_to_images.py $_.FullName --font-size 14
}
```

## 依存パッケージ

```bash
pip install openpyxl pillow
```

## トラブル時

- `No module named 'PIL'` -> `pip install pillow`
- `No module named 'openpyxl'` -> `pip install openpyxl`
- 文字化け時は `--json` を試す

## 正本ドキュメント

- [SKILL.md](../SKILL.md)
