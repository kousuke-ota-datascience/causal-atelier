# Enhancement Background

## 0. Purpose

このディレクトリは、エンハンスの背景、課題認識、要件改定、設計改定、承認、
トレーサビリティ、およびエンハンス時点の要件・設計snapshotを保存する履歴層である。

## 1. Primary readers

- 人間
- 将来の設計レビュー担当
- 将来のLLMによる背景復元・監査

Coding Agent / Test Agentの通常作業では参照させない。

## 2. Standard documents

1. `01_Enhance構想・要件改定計画.md`
2. `02_Enhance構想承認記録.md`
3. `03_要件定義書改定.md`
4. `04_設計書改定.md`
5. `05_要件・設計整合性およびトレーサビリティ確認.md`
6. `Revised_requirements_definition_documents/`

## 3. Agent boundary

Coding Agent / Test Agentに必要な差分仕様は、
`10_enhance_instruction/06_...` および `07_...` へ統合する。

背景・要件・設計文書をAgent自身に再探索させない。
