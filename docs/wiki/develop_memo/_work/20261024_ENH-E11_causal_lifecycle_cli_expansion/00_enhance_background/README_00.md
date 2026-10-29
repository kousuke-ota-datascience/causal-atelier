# ENH-E11 — 00_enhance_background：文書の位置付け

**文書区分:** 計画・監査資料の案内  
**状態:** 計画段階／正式承認待ち  
**言語方針:** 本文・見出しは日本語を基本とし、専門用語と識別子は必要に応じて英語を維持する。canonicalファイル名はWorkflow規則に従いASCIIとする。

## 1. 最初に読む文書

**`00_01_foundation_gap_reconciliation.md` — 構想の出発点。**

2026年9月末のENH-E11申し送り（`Causal Lifecycle Foundation Gap Completion`）と2026年10月の現行要件・実装を13項目で照合する。各行についてRequirement Status、ソース、テストの存在、過去の999判定、未充足・新Capability候補を区別する。

続いて**`00_02_foundation_gap_closure_assessment.md`**を読む。前者は9月末構想の13項目を照合する**第1調査**、後者は現行要件に残る4領域について証拠水準・閉鎖条件・E11への帰属未決事項を明示する**第2調査**である。

さらに**`00_03_phase1_to_phase3_reconciliation.md`**で、8月4日Phase 1〜3・上位構想と9月末の判断、現行実装を68項目で照合する（**第3調査**）。

3調査の結果から**`00_04_phase1_to_phase3_cli_scope_proposal.md`**（ステップ4の68項目スコープ案）を策定した。技術審査の**途中経過**は[作業メモ](../working_notes/20261029_cli_scope_review.md)に記録した（68行追跡性PASS、BLOCKER 5件／MAJOR 7件、**CHANGES_REQUIRED**）。作業メモは00層の正式文書ではない。修正と再審査が必要。

**00_01→00_02→00_03→00_04の順で`01_enhancement_concept_and_requirement_revision_plan.md`より前に読む。** 作業メモは指摘事項を確認する際に参照する。設計・実装の承認ではなく、固定SHAでの全テスト再実行もまだ完了していない。

## 2. Workflow所定の正式文書の順序

`01 構想・要件改定計画 → 02 オーナー承認 → 03 要件改定 → 04 設計改定 → 05 要件・設計整合性 → 承認済み正本Snapshot → 80 契約変更履歴`。

**00の事前調査資料を追加しても、Workflow所定の01〜05のファイル名や承認順序は変更しない。**

## 3. 後続の補助資料

- `07_github_issue_register.md`：Issue #13〜#24の追跡と、暫定Gate・要件の対応。
- `40_operator_workflows/architecture_review/`：source-of-truth、Scientific/Local CLI所有権、Gate境界に関する未承認の判断案。

事前調査00_01〜00_03・スコープ案00_04と、別配置の作業メモ・Issue・Operatorの補助資料は、01〜05、承認済み正本、Gate 06/07の正式なauthorityを**代替しない**。

## 4. 現在の承認状態

| 対象 | 状態 |
|---|---|
| 9月末案 × 現行実装のSource Reconciliation | **完了（ソース照合）／新規全件テスト未実施** |
| Foundation Gapの残差確定 | **4領域を登録・証拠水準確定／閉鎖テスト・実装帰属は未決** |
| 8月4日Phase 1〜3構想との三資料照合 | **完了（68行のソース照合）／採否・実装Scopeの承認は未実施** |
| ステップ4：Phase 1〜3・CLI-only実装スコープ案 | **作成完了（68行の採否案・Product Gap境界）／Human owner未承認** |
| ステップ4の技術審査（別配置の作業メモ） | **CHANGES_REQUIRED（BLOCKER 5・MAJOR 7）／正式承認・Gate freeze未実施** |
| CLI-only Phase 1〜3のオーナー方針 | 計画上の方向性を確認済み |
| 正式な構想・要件・設計承認 | **PENDING** |
| Architecture Review | **未完了** |
| 承認済み正本Snapshot | **未作成** |
| Gate 06/07のfreeze | **未実施** |
| 今回の計画に基づくCoding・独立999 PASS | **未実施** |

外部URL、Issue、SHA、過去のGateは根拠の参照先であり、各文書の結論や設計判断そのものを外部参照だけに委ねない。
