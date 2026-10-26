# ENH-E11 — Causal LifecycleのCLI-first拡張

**状態:** 計画段階／Architecture Review・要件／設計の正式承認待ち（2026-10-25）

本ディレクトリはENH-E11のWorkflow資料を格納する。適用規約は`../agentic_enhancement_workflow_template/README.md`と`../agentic_enhancement_workflow_template/README_Appendix_HowToUse.md`。

**本ディレクトリの草案は、Gate 06/07のfreeze、実装着手、canonical 999 PASSを意味しない。**

## 1. 現時点で確認されている方針

- 2026年8月4日のPhase 1〜3必須因果推論手法について、既存Capabilityを再利用しながらENH-E11の実装対象として検討する。
- **新機能**の提供範囲はScientific Core／ローカルCLI／永続的なローカルファイル成果物までとし、Web UI・Web API・Worker・DBとの新規統合は後続へ送る。
- Phase 4のPolicy Evaluation、意思決定自動化、運用監視、driftは対象外。
- [全体追跡Issue #13](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13)を使用する。ただしIssueの完了はGate PASSではない。
- **先行照合の結果:** 9月末のFoundation Gapは、現行Graph／Identification／Eligibility／推定／Diagnostics等で多くが解消済み。Lineage、同一Dataset再利用警告、再現性metadata、Family別NavigationのCapability所有権に未充足が残る。DoWhy/FCIは現行要件の未実装ではなく新規Capability候補。

## 2. 文書の配置と実施順序

### 2.1. 第1段階：構想に先行する調査・スコープ案

| 文書 | 役割と状態 |
|---|---|
| **`00_enhance_background/00_01_foundation_gap_reconciliation.md`** | **第1調査。** 9月末Foundation Gapの13項目を現行FR/NFR/AR・コード・テスト・過去Gateと照合 |
| **`00_enhance_background/00_02_foundation_gap_closure_assessment.md`** | **第2調査。** 第1調査に基づき現行要件の残存Gap4領域と証拠水準・閉鎖条件・E11への帰属未決事項を確定。固定SHAでの全件再実行は未実施 |
| **`00_enhance_background/00_03_phase1_to_phase3_reconciliation.md`** | **第3調査。** 8月4日のPhase 1〜3・A0上位構想、9月末の扱い、現行要件・実装を68行で照合済み。正式な採否とCLI-only実装Scopeは未承認 |
| **`00_enhance_background/00_04_phase1_to_phase3_cli_scope_proposal.md`** | **ステップ4成果物。** 68行に対し再利用・品質検証・新規CLI科学機能・後続送りのスコープ案を整理。**Human ownerの正式承認待ち** |

### 2.2. 第2段階：Workflow所定の正式な計画・承認・要件設計

| 文書 | 役割と状態 |
|---|---|
| `00_enhance_background/01_enhancement_concept_and_requirement_revision_plan.md` | **00_01〜00_03の3件の調査と00_04のスコープ案**を入力とする構想・ユースケース・対象範囲・暫定Gate案（DRAFT） |
| `00_enhance_background/02_enhancement_concept_approval_record.md` | Human ownerの正式承認記録。**承認待ち** |
| `00_enhance_background/03_requirements_revision.md` | FR/NFR/ARの意味上の変更案。正本未改定 |
| `00_enhance_background/04_design_revision.md` | 目標Architectureの改定案。未承認 |
| `00_enhance_background/05_requirements_design_consistency_and_traceability_review.md` | Requirement→Design→Gate→ACの整合性（暫定） |
| `00_enhance_background/Revised_requirements_definition_documents/` | 正式承認後の正本Snapshot。**未作成** |
| `00_enhance_background/80_contract_amendment_log.md` | 正式承認・freeze後の変更履歴。現時点で変更なし |

### 2.3. 第3段階：作業追跡とArchitecture Review

| 文書 | 役割と状態 |
|---|---|
| `00_enhance_background/07_github_issue_register.md` | GitHub Issue #13〜#24と要件・暫定Gateの対応 |
| `40_operator_workflows/architecture_review/` | Architecture Discovery、目標設計ADR、暫定Gate分割。未承認 |

**00_01〜00_03の事前調査と00_04のスコープ案は01より前の根拠・提案資料**であり、Workflowの正式文書01〜05を置き換えない。07はIssue台帳、80は契約変更履歴であり、これらも承認済み要件やGateを代替しない。

## 3. 今後の進め方

1. **00_01→00_02→00_03→00_04をレビュー**し、13項目照合、Gap4領域、8月68項目の差分とCLI-onlyの実装スコープ案を確認する。
2. **00_04のスコープ案の採否・例外をHuman ownerが審査する。** Phase1〜3のMethod群、Negative Control/未観測交絡Sensitivity、A0上位構想だけのATC等、既存Product Gapの別案件帰属を明示して01構想を確定する。
3. 構想の正式承認とArchitecture Reviewを得る。必要な要件・設計改定を正本に反映する。
4. 承認済みSnapshot、基準SHA、semantic Gate/Work Packageを確定し、Gate別06/07をfreezeする。
5. 実装時に20報告、30独立検証、canonical 999 Decisionを保存する。

**禁止事項:** 承認やGate PASSの証拠を推測で作成しない。テンプレートに項目があるという理由だけで未承認の06/07契約を固定しない。

## 4. 記載言語とファイル名の規則

本文・見出し・表・判断理由は**日本語を基本**とする。統計手法名、ソフトウェア名称、正式なDomain概念、コード上のenum/field名、GitHub Issueの固定見出しなど、日本語訳が不自然または意味を損なうものは英語のまま用いる。Workflowの規定に従い、canonicalファイル名はASCIIかつ技術英語とする。

**見出し構造のルール:** 原則として見出しには階層に応じた連番を付け、下位見出しは上位の番号を継承する（例：`## 2. ...` → `### 2.1. ...`、`### 2.2. ...`）。見出しレベルの飛越しと、子見出しが1件しかない階層は作成しない。`#` はWorkflowテンプレートに従う文書タイトル専用の例外とし、`00`の本文は `## 0. INTRODUCTION` を起点とする。
