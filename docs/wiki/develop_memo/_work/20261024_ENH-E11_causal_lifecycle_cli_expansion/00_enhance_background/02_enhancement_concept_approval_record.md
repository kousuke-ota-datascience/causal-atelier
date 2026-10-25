# ENH-E11 — 構想承認記録

**文書区分:** 計画・意思決定記録  
**承認状態:** **正式な構想承認は未実施**（`PENDING_FULL_CONCEPT_APPROVAL`）  
**承認日時:** 未発行  
**承認権限:** Human owner  
**審査対象:** `01_enhancement_concept_and_requirement_revision_plan.md`  
**事前照合:** `00_foundation_gap_reconciliation.md`  
**追跡:** [GitHub Issue #13](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13)

## 1. 計画の前提として確認されたオーナー方針（Gate承認ではない）

1. ENH-E11では2026年8月4日のPhase 1〜3の必須因果推論Capabilityを実装対象候補とし、既存実装は再利用する。
2. **新機能**の提供範囲はScientific Core、ローカルCLI、永続ローカルファイル成果物に限定する。Web UI/API、Worker、DB統合は後続へ送る。
3. まず9月末のFoundation Gap案と現行実装を照合し、その結果を踏まえて8月構想との差分・正式要件を整理する。
4. Workflowの必須文書に加えてGitHub Issueを使い、Issue→Requirement→Gate→Acceptance Criterionの対応を示す。

## 2. まだ承認されていない事項

- 拡大後の構想名称、必須手法一覧および例外・同等手法。
- 正本§11の外部engine除外の変更、FR/NFR/ARの追加・削除・変更。
- Design/Resultの所有権、optional dependency、CLIファイル契約、科学的許容基準。
- Architecture Review結論、Gate分割、06/07のfreeze、受入用基準SHA。

## 3. 遵守条件

- 新機能のWeb UI/API/Worker/DB統合をENH-E11内で行わない。
- CPDAG/PAG等の不確定性を黙ってDAGへ変換しない。
- 非識別、仮定違反、適格性不足等は科学的statusとして記録し、技術失敗と区別する。
- 既存FR/NFR/ARの意味、現行実装、独立Gate証跡を保護する。
- Issue完了はcanonical 999 PASSを意味しない。

## 4. 明示的な非承認

- 実装Agentの起動、Gate 06/07の固定、受入済みソフトウェアの宣言。
- 審査済みの要件差分がないままの正本書換え。
- Phase 4のPolicy automation、監視、意思決定権限の付与。

## 5. 承認のための残作業

1. 先行照合`00_foundation_gap_reconciliation.md`の証拠と未検証事項を確認する。
2. `06_three_source_reconciliation_matrix.md`、`03_requirements_revision.md`、`04_design_revision.md`を固定SHAに照らして再確認する。
3. Architecture Reviewを完了し、`05_requirements_design_consistency_and_traceability_review.md`を改訂する。
4. Human ownerの正式判断を**実際の日時と根拠**付きで追記する。遡及的に承認済みとしない。
5. 承認後に正本と承認Snapshotを固定し、Gate 06/07を作成する。
