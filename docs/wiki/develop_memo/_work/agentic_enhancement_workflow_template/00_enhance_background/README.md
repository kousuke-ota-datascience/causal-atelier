# Enhancement Background — Specification

## 0. Purpose

このディレクトリは、enhancementの背景、課題認識、要件改定、設計改定、承認、traceability、およびenhancement開始時点のsnapshotを保存する履歴層である。

## 1. Primary readers

- Human owner / reviewer
- 将来の設計レビュー担当
- 将来のLLMによる背景復元・監査

Coding Agent / Test Agentの通常executionでは、ここを自由探索させない。
必要な差分契約はGate-local 06 / 07へ統合する。

## 2. Standard documents

1. `01_Enhance構想・要件改定計画.md`
2. `02_Enhance構想承認記録.md`
3. `03_要件定義書改定.md`
4. `04_設計書改定.md`
5. `05_要件・設計整合性およびトレーサビリティ確認.md`
6. `Revised_requirements_definition_documents/`

## 3. Architecture-review trigger

以下に該当する場合、`40_operator_workflows/architecture_review/`を`CONDITIONAL MUST`とする。

- runtime entrypoint / lifecycle変更
- authority / ownership変更
- persistence / schema / lineage変更
- legacy path除去・統合
- migration strategy変更
- 複数subsystemを跨ぐcanonical source-of-truth変更

Architecture reviewの成果はこの背景層または正式設計へ反映し、そのうえでGate-local 06 / 07に必要事項を抽出する。

## 4. Boundary

背景・要件・設計文書は上位contractであるが、Agentの実行入口ではない。
Agentに参照例外を認める場合、06 / 07でpath・目的・authority・precedenceを限定する。
