# 🧠 セッション記憶システム

セッションを跨いで学習・改善するための記憶システム

## 配置方針

- ルール定義: `.bob/rules/memory.md` （このファイル）
- 運用データ: `MEMORY/`

`.bob` 配下には更新頻度の低いルールのみを置き、セッションログや知識ベースなどの高頻度更新ファイルはリポジトリ直下の `MEMORY/` に配置します。

## 記憶システムの構造

記憶システムは3層構造で構成されています：

1. **ログ層** ([`MEMORY/sessions/`](../../MEMORY/sessions/)): セッション内の活動を時系列で記録
2. **リフレクション層** ([`MEMORY/reflections/`](../../MEMORY/reflections/)): セッションから重要な学びを抽出・整理
3. **記憶層** ([`MEMORY/knowledge/`](../../MEMORY/knowledge/)): 次回セッションで参照する知識を保持

詳細は [`MEMORY/README.md`](../../MEMORY/README.md) を参照してください。

## セッション開始時の記憶読み込み

**必須読み込み（毎回）:**
- [`MEMORY/knowledge/persistent.md`](../../MEMORY/knowledge/persistent.md) - プロジェクト固有ルール、技術制約
- [`MEMORY/knowledge/preferences.md`](../../MEMORY/knowledge/preferences.md) - ユーザー設定・好み

**推奨読み込み:**
- [`MEMORY/reflections/`](../../MEMORY/reflections/) 配下の最新3件 - 最近の学び、エラーパターン

**タスクに応じて:**
- [`MEMORY/knowledge/patterns.md`](../../MEMORY/knowledge/patterns.md) - 成功/失敗パターン

## セッション中の記録

以下の情報を [`MEMORY/sessions/YYYY-MM-DD_session-XXX-NNN.md`](../../MEMORY/sessions/) に記録してください：

- **誤り**: 間違った実装アプローチ、誤解した仕様、ツール使用の誤り
- **無駄**: 不要なファイル読み込み、冗長な質問、失敗したアプローチの再試行
- **成功**: 効果的だったアプローチ、問題解決方法
- **ユーザーフィードバック**: 修正指示、好みの表明

**必須ルール:**
- セッションログは各実行の開始時に必ず新規作成すること
- ファイル名は `YYYY-MM-DD_session-XXX-NNN.md` とし、`XXX` は作成対象、 `NNN` は当日既存ファイルの最大番号に `+1` した番号を採番すること
- 既存の終了済みセッションログへ追記してはならない
- タスクが異なる場合は同日でも必ず別ファイルに分けること
- 記載すべき情報を発見したら最優先で記録すること

## セッション終了時の処理

1. セッションログを完成させる
2. エラーまたは新しい学びがある場合、`MEMORY/reflections/YYYY-MM-DD_reflection.md` を生成する
   - ファイル名は上記形式に固定し、タスク名入りなどの独自命名をしてはならない
   - 内容は `MEMORY/USAGE_GUIDE.md` のテンプレートに厳密に従うこと
3. 重要な知識を記憶層に統合

## 命名規則（必須）

### セッションログ

- ファイル名は **`YYYY-MM-DD_session-XXX-NNN.md`** を正とする
- `XXX` は作成対象（例: `flowchart`, `testcase`, `testdata`, `implement`, `reflection`, `precheck` など）
- `NNN` は当日・同一 `XXX` の最大番号に `+1` した3桁連番（`001` 開始）
- `YYYY-MM-DD_session-NNN.md` 形式は使用しない（既存がある場合は順次移行）

### リフレクション

- ファイル名は **`YYYY-MM-DD_reflection.md`** に固定する
- タスク名・PGM-ID などを含む独自命名は禁止

### インデックス

- `MEMORY/sessions/index.md`
- `MEMORY/reflections/index.md`
- 上記2ファイルを台帳の正本として扱う

## 保持・アーカイブルール（必須）

### 対象

- `MEMORY/sessions/` 配下のセッションログ

### 基準

- **3か月より前**（当日基準）のセッションログをアーカイブ対象とする

### 手順

1. 対象ファイル一覧を確定する
2. `MEMORY/archive/sessions/` へ移動する（未作成なら作成）
3. `MEMORY/sessions/` から当該ファイルを除外する
4. `MEMORY/sessions/index.md` を更新する
5. 更新後に整合チェックを実施する

### 禁止事項

- アーカイブ前の直接削除
- index 未更新のまま移動・削除を完了扱いにすること

## index.md 更新ルール（必須）

以下の操作を行った場合、`index.md` 更新を必須とする。

- セッションログ新規作成
- リフレクション新規作成
- 既存ログのファイル名変更
- アーカイブ移動
- ファイル削除（やむを得ない場合のみ）

### 更新内容

- 履歴テーブルの追加・修正・削除
- 統計情報の再計算（件数・エラー数・学習項目数・平均値など）
- 最終更新日の更新

## 整合チェック手順（必須）

記憶メンテナンス時は、開始時と終了時に以下を確認する。

### チェック観点

1. `sessions/index.md` の記載件数と `MEMORY/sessions/` 実ファイル件数が一致している
2. `reflections/index.md` の記載件数と `MEMORY/reflections/` 実ファイル件数が一致している
3. 命名規則違反ファイルが存在しない
   - `sessions`: `YYYY-MM-DD_session-XXX-NNN.md`
   - `reflections`: `YYYY-MM-DD_reflection.md`
4. index に記載されたファイルが実在し、実ファイルの未記載がない
5. アーカイブ実施時、対象ファイルが `MEMORY/archive/sessions/` に存在する

### 完了条件

- 上記チェックで不一致が0件
- 不一致があった場合は、修正内容を反映後に再チェックして0件にする
