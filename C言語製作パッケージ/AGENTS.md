# AGENTS.md

## プロジェクト概要

本プロジェクトは、C言語システム保守・開発を対象に、プログラム指示書からテストケース・テストデータ・ソースコードを一貫して生成するためのフレームワークです。

## 一次ソース（最優先参照）

運用時の詳細ルールは以下を正本とし、AGENTS.mdは要約のみを扱います。

1. `.bob/rules/output-standards.md`
   - 成果物形式（TSV等）・配置ルール
2. `.bob/rules/memory.md`
   - セッション記憶

**解釈ルール**:
- AGENTS.md と rules の記載が競合する場合、**rules を優先**すること。
- 詳細手順や例外条件は AGENTS.md に再掲せず、rules を参照すること。

## 絶対遵守ルール（要約版）

- `read_file` の前に必ず `list_files` で存在確認する
- 最終成果物の形式は rules で定義された形式に従う（テスト系はTSV、ソースコード系は `.h`/`.c`）
- セッション記憶を随時記録・更新すること

詳細は以下を参照:
- `.bob/rules/output-standards.md`
- `.bob/rules/memory.md`

セッション記憶の実データ保存先:
- `MEMORY/`
- `MEMORY/knowledge/`
- `MEMORY/reflections/`
- `MEMORY/sessions/`

## 主要スキル

- `c-testcase`: C言語プログラム指示書から単体テストケース（TSV）を生成
- `c-testdata`: 承認済みテストケースから実行可能なテストデータ（TSV）を生成
- `c-implement`: プログラム指示書から変数定義部（`.h`）と関数実装部（`.c`）を生成

### 補助スキル

- `c-instruction`: ソースコードからプログラム指示書を生成
- `assign-testcase-shot`: テストケースにショット番号（ST001, ST002, ...）を割り当て
- `excel-to-md`: ExcelファイルをMarkdown形式に変換
- `xlsx-to-images`: ExcelファイルをシートごとにPNG画像へ変換（大容量ファイルのトークン上限回避用）
- `reflection`: memory.mdルールに従って記憶情報を整理・整合化

## 参照ディレクトリ（導線）

- `インプット/`: プログラム指示書など作業対象の入力ファイル置き場
- `プロンプトテンプレート/`: 各工程の System/User Prompt（`ソースコード/`・`プログラム指示書/` の各サブディレクトリを含む）
- `成果物テンプレート/`: テストケース・テストデータ用テンプレート（TSV形式）
- `セルフチェックリスト/`: 品質観点チェックリスト（Excel）※随時追加
- `参考資産/`: 実績ベースの入力/出力サンプル ※随時追加
- `アウトプット/`: 生成成果物の出力先
- `プロンプトテンプレート/プログラム指示書/`: 指示書生成用テンプレート
- `プロンプトテンプレート/ソースコード/`: ソースコード生成用テンプレート
- `成果物テンプレート/`: 成果物テンプレート
- `セルフチェックリスト/`: 品質観点チェックリスト
- `MEMORY/`: セッション記憶システム

## 専用モード

- `c-testcase-designer`: C言語テストケース設計専用（ルール: `.bob/rules-c-testcase-designer/AGENTS.md`）
- `c-testdata-designer`: C言語テストデータ設計専用（ルール: `.bob/rules-c-testdata-designer/AGENTS.md`）
- `c-implementer`: C言語ソースコード実装専用（ルール: `.bob/rules-c-implementer/AGENTS.md`）

## 運用上の注意

- 長大会話で前提が増えた場合は、新規会話に切り替え、承認済み成果物のみ再投入して継続するようにユーザへ促す。
- 不明点がある場合は推測実装せず、仮定を明示して確認する。
- 具体的な禁止事項・詳細手順・例外条件は必ず rules 側を確認する。

## 関連ドキュメント

- `README.md`: プロジェクト概要、ディレクトリ構成、コマンド一覧
- `AGENTS.md`: 本ファイル（入口・索引）
- `.bob/rules/output-standards.md`: 成果物形式・配置ルール
- `.bob/rules/memory.md`: セッション記憶の運用ルール
- `.bob/rules-c-testcase-designer/AGENTS.md`: C Test Case Designer Mode 専用ルール
- `.bob/rules-c-testdata-designer/AGENTS.md`: C Test Data Designer Mode 専用ルール
- `.bob/rules-c-implementer/AGENTS.md`: C Source Generator Mode 専用ルール
- `MEMORY/README.md`: セッション記憶の構造
- `MEMORY/USAGE_GUIDE.md`: セッション記憶の運用ガイド
- `MEMORY/sessions/index.md`: セッションログ台帳
- `MEMORY/reflections/index.md`: リフレクション台帳
