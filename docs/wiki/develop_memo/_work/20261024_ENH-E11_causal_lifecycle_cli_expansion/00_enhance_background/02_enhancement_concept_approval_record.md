# ENH-E11 — 構想承認記録

**文書区分:** 計画・意思決定記録  
**承認状態:** **正式な構想承認は未実施**（`PENDING_FULL_CONCEPT_APPROVAL`）  
**承認日時:** 未発行  
**承認権限:** Human owner  
**審査対象:** `01_enhancement_concept_and_requirement_revision_plan.md`  
**事前調査・スコープ案・技術審査:** `00_01_foundation_gap_reconciliation.md` → `00_02_foundation_gap_closure_assessment.md` → `00_03_phase1_to_phase3_reconciliation.md` → `00_04_phase1_to_phase3_cli_scope_proposal.md`  
**途中レビュー（非正規の作業メモ）:** [20261029_cli_scope_review.md](../working_notes/20261029_cli_scope_review.md)（**CHANGES_REQUIRED**）  
**追跡:** [GitHub Issue #13](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13)

## 1. 計画の前提として確認されたオーナー方針（Gate承認ではない）

1. ENH-E11では2026年8月4日のPhase 1〜3の必須因果推論Capabilityを実装対象候補とし、既存実装は再利用する。
2. **新機能**の提供範囲はScientific Core、ローカルCLI、永続ローカルファイル成果物に限定する。Web UI/API、Worker、DB統合は後続へ送る。
3. まず9月末のFoundation Gap案と現行実装を照合し、その結果を踏まえて8月構想との差分・正式要件を整理する。
4. Workflowの必須文書に加えてGitHub Issueを使い、Issue→Requirement→Gate→Acceptance Criterionの対応を示す。
5. **Negative Controlの機能原則（2026-11-01の明示方針）:** 「適切なNegative Controlを指定できる研究に対し、科学的に解釈可能な反証分析を提供する」。全分析にNegative Controlの実行を義務付けない。方法実装案は[作業メモ](../working_notes/20261101_negative_control_implementation_plan.md)に記録し、**Method・正本FR/AC・Gateの正式承認と区別する**。

6. **SR-02外部Backendのオーナー方針（2026-11-01）:** **A採用＝Python 3.12／Linux基準**、**B採用＝DoWhy・EconML・Tigramiteを機能別optional依存**、**C採用＝Phase1〜3の列挙Methodを維持し、実装不能な場合は根拠付きで再審議**、**E採用＝実証された採用versionをlock＋科学Benchmarkで固定**。
7. **D採用＝個別SIで顧客環境へ構築・納入、現時点でSaaSは想定しない。** Tigramiteを使用する場合、実際の納入物と結合・提供形態に即してGPLv3適合性を**顧客納入前に審査する方針**を採用。PCMCI／PCMCI+／LPCMCIの利用場面は[SR-02技術メモ](../working_notes/20261101_external_backend_policy_temporal_scenarios.md)で精査。**D方針の採用は個別納入の法的適合性を認定するものではない**。

8. **SR03-D02 Frontdoor（2026-11-01の明示判断）:** **Phase1では識別だけでなく数値推定Capabilityも含める**。識別だけを完了条件としない。ただし推定器の線形性等の追加仮定、数値的実行可能性、CI、科学Benchmarkは未承認・未検証。LATE初期推定器については次項の個別判断で**A＋Bを採用**。[選択肢・科学的制約](../working_notes/20261101_sr03_late_estimator_options_econml_inference_review.md)を参照。

9. **SR03-D03 LATE（2026-11-01の明示判断）:** **Phase3初期提供はA＝二値Z・二値AのWald比を基準、B＝2SLSにも対応する構成を採用**。**C＝条件付きIV向けDR／効率的LATEは追加審議**であり今回の採用範囲ではない。LATEの対象は独立性・除外制約・関連性・単調性等を仮定した**complier**であり、一般ATEや連続TのIV heterogeneous effectと混同しない。2SLSの共変量・複数IV拡張はEstimandと仮定の適合を別審査。**弱IV時のFirst Stage診断・通常CIの限界・Anderson–Rubin等の頑健推論の設計は必須検討だが、具体的推論アルゴリズム／閾値／科学Gateの採用は未完了**（[科学契約・検討メモ](../working_notes/20261101_sr03_identification_estimand_estimator_contract_review.md)）。

## 2. まだ承認されていない事項

- 拡大後の構想名称、必須手法一覧および例外・同等手法。
- 正本§11の外部engine除外の変更、FR/NFR/ARの追加・削除・変更。
- Design/Resultの所有権、**optional依存の具体的version・実効API・CLIファイル契約**、科学的許容基準。A/B/C/D/Eの基本方針は採用済み。
- **Tigramiteを含む個別SI納入物のGPLv3適合性**（配布前評価方針は採用済み。個別の組合せ・納入主体・対応ソース義務等は未判定）。
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

1. 先行調査の`00_01_foundation_gap_reconciliation.md`→`00_02_foundation_gap_closure_assessment.md`→`00_03_phase1_to_phase3_reconciliation.md`を確認し、`00_04_phase1_to_phase3_cli_scope_proposal.md`の68行と[作業メモ](../working_notes/20261029_cli_scope_review.md)の**SR-01〜12を是正・再審査**した結果を確認する。
2. `00_04_phase1_to_phase3_cli_scope_proposal.md`にあるATC/matching等の後続送り、**§2.3の観測NCE/NCO・OLS partial R²候補の採否・適用限界（[方法検討メモ](../working_notes/20261101_negative_control_unobserved_confounding_method_review.md)）**、外部Libraryの同等代替、Product GAP-C01〜04の帰属を**項目単位で明示承認または差戻し**したうえで、`03_requirements_revision.md`、`04_design_revision.md`を固定SHAに照らして再確認する。
3. Architecture Reviewを完了し、`05_requirements_design_consistency_and_traceability_review.md`を改訂する。
4. Human ownerの正式判断を**実際の日時と根拠**付きで追記する。遡及的に承認済みとしない。
5. 承認後に正本と承認Snapshotを固定し、Gate 06/07を作成する。
