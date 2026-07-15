---
name: reflection
description: "memory.mdルールに従い、記憶情報（sessions/reflections/knowledge）を整理・整合化"
argument-hint: "<対象日(任意: YYYY-MM-DD)>"
---

# 記憶情報整理スキル

## 概要

`MEMORY/` 配下の session・reflection・knowledge を点検し、必要な更新とクリーンアップを実施します。

## ⚠️ 事前確認（実行前に必ず確認）

1. ルールファイルを読む
   - [`.bob/rules/memory.md`](../../rules/memory.md)
   - [`MEMORY/USAGE_GUIDE.md`](../../../MEMORY/USAGE_GUIDE.md)
2. `read_file` 前の存在確認を徹底する
   - すべての対象ファイルは、`list_files` で存在確認してから読む
3. 対象日の決定
   - 引数がある場合: その日付（`YYYY-MM-DD`）
   - 引数がない場合: 当日

## 実行手順

1. **対象ファイルの収集**
   - `list_files` で以下を確認
     - `MEMORY/sessions/`
     - `MEMORY/reflections/`
     - `MEMORY/knowledge/`
     - `MEMORY/archive/`
   - 続いて `read_file` で以下を読み込む
     - `MEMORY/sessions/index.md`
     - `MEMORY/reflections/index.md`
     - `MEMORY/knowledge/persistent.md`
     - `MEMORY/knowledge/preferences.md`
     - `MEMORY/knowledge/patterns.md`
     - `MEMORY/sessions/*.md`
     - `MEMORY/reflections/*.md`

2. **初期整合チェック（session / reflection / knowledge）**
   - `.bob/rules/memory.md` の「整合チェック手順（必須）」に従って実施する
   - knowledge については `persistent.md` / `preferences.md` / `patterns.md` の重複・矛盾も確認する
   - 不整合を検出したら、修正方針を明示した上で補正する

3. **対象日の reflection 作成・更新**
   - 対象日の session を抽出する
   - `MEMORY/reflections/{対象日}_reflection.md` が未作成の場合:
     - `MEMORY/USAGE_GUIDE.md` のテンプレートに厳密準拠して新規作成
   - 既存の場合:
     - 当日 session の内容を反映し、不足項目を更新
   - 反映対象:
     - 発生した誤り
     - 無駄な作業
     - 成功パターン
     - 次回への引き継ぎ事項
   - `MEMORY/reflections/index.md` の更新要否は `.bob/rules/memory.md` の「index.md 更新ルール（必須）」に従う

4. **knowledge 更新**
   - reflection と session から、`.bob/rules/memory.md` の更新条件に合致する内容を抽出
   - 更新先:
     - `persistent.md`
     - `preferences.md`
     - `patterns.md`
   - 既存記述と衝突する場合:
     - 情報源（session ID / reflection日付）を併記し、最新版に統合
   - 各 knowledge ファイルの最終更新情報を更新

5. **古い session の整理**
   - `.bob/rules/memory.md` の「保持・アーカイブルール（必須）」に従って実施する
   - `MEMORY/archive/sessions/` へ退避し、`index.md` 更新を行う

6. **最終整合チェック**
   - `.bob/rules/memory.md` の「整合チェック手順（必須）」を再実施する
   - reflection と knowledge の参照元に矛盾がないことを追加確認する
   - 最後に変更サマリーを提示
     - 追加 / 更新 / 退避 / 削除ファイル
     - 検出・解消した不整合
     - 残課題（あれば）

## 使用例

```
/reflection
/reflection 2026-04-22
```

## 注意事項
- ルールにない独自テンプレートは使わない
- 命名規則は `.bob/rules/memory.md` を正本とする
- `sessions` は終了済みログへの追記禁止（詳細は `.bob/rules/memory.md`）
- 破壊的変更（削除）は、保持・アーカイブ・index更新ルールに従う
