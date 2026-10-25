# ENH-E11 — Causal LifecycleのCLI-first拡張

**状態:** 計画段階／Architecture Review・要件／設計の正式承認待ち（2026-10-25）

本ディレクトリはENH-E11のWorkflow資料を格納する。適用規約は`../agentic_enhancement_workflow_template/README.md`と`../agentic_enhancement_workflow_template/README_Appendix_HowToUse.md`。

**本ディレクトリの草案は、Gate 06/07のfreeze、実装着手、canonical 999 PASSを意味しない。**

## 1. 現時点で確認されている方針

- 2026年8月4日のPhase 1〜3必須因果推論手法について、既存Capabilityを再利用しながらENH-E11の実装対象として検討する。
- **新機能**の提供範囲はScientific Core／ローカルCLI／永続的なローカルファイル成果物までとし、Web UI・Web API・Worker・DBとの新規統合は後続へ送る。
- Phase 4のPolicy Evaluation、意思決定自動化、運用監視、driftは対象外。
- [全体追跡Issue #13](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13)を使用する。ただしIssueの完了はGate PASSではない。
- **先行照合の結果:** 9月末のFoundation Gapは、現行Graph／Identification／Eligibility／推定／Diagnostics等で多くが解消済み。Lineage、同一Dataset再利用警告、再現性metadataには一部未充足が残る。DoWhy/FCIは現行要件の未実装ではなく新規Capability候補。

## 2. 文書の配置と実施順序

### 第1段階：構想に先行する調査

| 文書 | 役割と状態 |
|---|---|
| **`00_enhance_background/00_foundation_gap_reconciliation.md`** | **出発点。** 9月末のENH-E11 Foundation Gap 13項目と現行FR/NFR/AR・コード・テスト・過去Gateを照合。ソース照合は完了、現行SHAでの全件テスト再実行は未実施 |

### 第2段階：Workflow所定の正式な計画・承認・要件設計

| 文書 | 役割と状態 |
|---|---|
| `00_enhance_background/01_enhancement_concept_and_requirement_revision_plan.md` | 00の証拠を入力とする構想・対象範囲・リスク・暫定Gate案（DRAFT） |
| `00_enhance_background/02_enhancement_concept_approval_record.md` | Human ownerの正式承認記録。**承認待ち** |
| `00_enhance_background/03_requirements_revision.md` | FR/NFR/ARの意味上の変更案。正本未改定 |
| `00_enhance_background/04_design_revision.md` | 目標Architectureの改定案。未承認 |
| `00_enhance_background/05_requirements_design_consistency_and_traceability_review.md` | Requirement→Design→Gate→ACの整合性（暫定） |
| `00_enhance_background/Revised_requirements_definition_documents/` | 正式承認後の正本Snapshot。**未作成** |
| `00_enhance_background/80_contract_amendment_log.md` | 正式承認・freeze後の変更履歴。現時点で変更なし |

### 第3段階：追加の分析・作業追跡

| 文書 | 役割と状態 |
|---|---|
| `00_enhance_background/06_three_source_reconciliation_matrix.md` | **00を読んだ後**、8月案・9月末案・現行実装・新スコープを比較する草案 |
| `00_enhance_background/07_github_issue_register.md` | GitHub Issue #13〜#24と要件・暫定Gateの対応 |
| `40_operator_workflows/architecture_review/` | Architecture Discovery、目標設計ADR、暫定Gate分割。未承認 |

追加資料06・07は正式文書01〜05を置き換えない。番号は作成順序を機械的に表すものではなく、**00は01の前提**であり、06・07は後続の補助資料とする。

## 3. 今後の進め方

1. **00の事前照合をレビュー**し、残る未充足・証拠不足を把握する。
2. 8月案との三資料比較を詰め、既存再利用・修正・新規Capability・後続送りを分離する。
3. 構想の正式承認とArchitecture Reviewを得る。必要な要件・設計改定を正本に反映する。
4. 承認済みSnapshot、基準SHA、semantic Gate/Work Packageを確定し、Gate別06/07をfreezeする。
5. 実装時に20報告、30独立検証、canonical 999 Decisionを保存する。

**禁止事項:** 承認やGate PASSの証拠を推測で作成しない。テンプレートに項目があるという理由だけで未承認の06/07契約を固定しない。

## 4. 記載言語とファイル名の規則

本文・見出し・表・判断理由は**日本語を基本**とする。統計手法名、ソフトウェア名称、正式なDomain概念、コード上のenum/field名、GitHub Issueの固定見出しなど、日本語訳が不自然または意味を損なうものは英語のまま用いる。Workflowの規定に従い、canonicalファイル名はASCIIかつ技術英語とする。
