# ENH-E11 — GitHub Issue台帳と要件・受入の対応（計画版）

**文書区分:** 計画・証跡資料  
**状態:** Issue登録済み／要件・Gate対応は未承認の案  
**Repository:** https://github.com/kousuke-ota-datascience/causal-atelier  
**記載粒度の基準:** [Issue #11](https://github.com/kousuke-ota-datascience/causal-atelier/issues/11)と同様の`Problem / Goal / Proposed Design / Acceptance Criteria / Related / Result / Memo`。  
**作業順序:** 事前調査`00_01_foundation_gap_reconciliation.md`→`00_02_foundation_gap_closure_assessment.md`→`00_03_phase1_to_phase3_reconciliation.md`→スコープ案`00_04_phase1_to_phase3_cli_scope_proposal.md`を01構想策定より**先に**確認する。この台帳のIssue分類は実装承認ではない。

## 1. 登録済みIssue一覧

| Issue | 対象 | 内容 | 暫定Gate | 扱い |
|---|---|---|---|---|
| [#13](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13) | 全体 | Phase 1〜3、CLI-first範囲、承認と子Issueの管理 | 全体／Gate前 | 計画 |
| [#14](https://github.com/kousuke-ota-datascience/causal-atelier/issues/14) | 事前調査 | **完了:** 9月末13項目照合、現行Gap4領域、8月案Phase1〜3＋A0上位68行照合。**スコープ案作成済み・Human承認待ち:** 00_04の68行のR/Q/N/D、Architecture Reviewと正式承認は未完了 | Gate前 | A/B/C/D/E分類・B?未決 |
| [#15](https://github.com/kousuke-ota-datascience/causal-atelier/issues/15) | Phase 1 | Question/Design version、識別・適格性の残差 | G01、G02 | 既存再利用／残差の確認 |
| [#16](https://github.com/kousuke-ota-datascience/causal-atelier/issues/16) | Phase 1 | DoWhy、Frontdoor/IV、Refutation、Sensitivity拡張 | G02、G03 | Optional backend候補 |
| [#17](https://github.com/kousuke-ota-datascience/causal-atelier/issues/17) | Phase 1 | FCI/PAGの端点保持、潜在交絡 | G01 | 新規Discovery候補 |
| [#19](https://github.com/kousuke-ota-datascience/causal-atelier/issues/19) | Phase 1 | IPTW/AIPWの推論・Diagnosticsの科学的妥当性 | G03 | 既存再利用・品質検証 |
| [#18](https://github.com/kousuke-ota-datascience/causal-atelier/issues/18) | Phase 2 | EconML、CATE/HTE、DML/DR/meta/IV+MLと成果物 | G04、G05 | 9月末案では除外、現在の追加候補 |
| [#20](https://github.com/kousuke-ota-datascience/causal-atelier/issues/20) | Phase 3 | Tigramite、PCMCI系、Temporal Graph | G06 | 9月末案では除外 |
| [#21](https://github.com/kousuke-ota-datascience/causal-atelier/issues/21) | Phase 3 | DiD、Event Study、ITS | G07 | 9月末案では除外 |
| [#22](https://github.com/kousuke-ota-datascience/causal-atelier/issues/22) | Phase 3 | Sharp/Fuzzy RDD、IV/LATE | G08 | 9月末案では除外 |
| [#23](https://github.com/kousuke-ota-datascience/causal-atelier/issues/23) | Phase 3 | Synthetic Control、Synthetic DiD | G09 | 9月末案では除外 |
| [#24](https://github.com/kousuke-ota-datascience/causal-atelier/issues/24) | 横断 | CLI schema、Manifest、local artifact、科学的受入 | G05/G10ほか | 共通契約・検証 |

## 2. 作業の依存順序（案）

1. **#14:** 9月末Foundation Gap照合、未解消Gap判定、8月案との68行三資料比較は**ソース照合として完了**。次にB/B?の採否・CLI-only Scopeを審議し、Architecture Review・正式承認へ進む。IssueはGateそのものではない。
2. **#15、#17:** Causal Context/Graphのversion、endpointの不確実性を定義する。
3. **#16、#19:** 承認済みDesignに基づきPhase 1のIdentification/Refutation/推論を検証・拡張する。
4. **#18:** CATE/HTEを独立のestimandとして導入し、EconMLのoptional機能を追加する。
5. **#20:** Temporal Graph/Designを定義。**#21〜23:** 共有契約が承認された後に準実験手法を実装する。Issue数をGate数としない。
6. **#24:** CLI/Manifestの共通契約は手法実装前に確定する。横断的な最終検証は各科学手法の受入後に行う。

この依存順序は承認前の計画であり、Gate 06の`Depends on`やcanonical 999の代替にはならない。

## 3. Issueの記載契約（Issue #11準拠）

すべてのIssueに以下のセクションを置き、**見出し名はIssue #11の英語見出しを維持**する。本文は日本語を基本とする。

1. **Problem:** 現行コード・要件・歴史資料と問題の意味。
2. **Goal:** 科学的に意味のある達成状態。
3. **Proposed Design:** 手法・仮定・parameter・成果物・互換性・科学的負結果・CLI責務。
4. **Acceptance Criteria:** テスト・既知真値・失敗例・証跡で判定可能な条件。
5. **Related:** 正本要件、過去資料、親子Issue、Workflow文書。
6. **Result:** 実装後の実測結果。現状は未着手であり、999判定の代替ではない。
7. **Memo:** 対象外、リスク、承認・運用上の条件。

子Issueは#11のテスト移行全体を再掲する必要はないが、方法別の前提・不変条件・科学的な受入粒度を揃える。

## 4. Issueと正規の受入契約の関係

- **GitHub Issue:** 作業追跡。発行・closeは要件変更承認や科学的受入を意味しない。
- **03 要件改定案:** FR/NFR/ARの意味上の変更と承認記録。
- **04 設計改定案:** ownership、adapter、CLI file、migrationの判断。
- **05 整合性確認:** 要件→設計→Gate→AC→Issueの暫定対応。
- **Gate 06/07:** 審査・承認後に固定する実装／検証契約。
- **20/30/999:** 実装報告、独立検証、canonical Gate判定。

## 5. 明示的な対象外と既存Backlog

- **新規Phase 1〜3手法**のWeb UI/API、Worker、DB統合はE11のIssue対象外。必要性が明確になり、後続Enhancementが承認されてからIssue化する。
- Phase 4のPolicy Evaluation、off-policy evaluation、monitoring、自動意思決定は対象外。
- [Issue #11](https://github.com/kousuke-ota-datascience/causal-atelier/issues/11)のリポジトリ全体のテスト移行は独立・非block扱い。E11はその科学的受入に必要なテストを作成する。
