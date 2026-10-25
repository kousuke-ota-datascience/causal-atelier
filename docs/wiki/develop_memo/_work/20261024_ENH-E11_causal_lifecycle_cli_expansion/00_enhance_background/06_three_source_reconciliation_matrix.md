# ENH-E11 — 三資料系統の差分照合表（暫定・後続工程用）

**文書区分:** 計画・証跡資料  
**状態:** PRELIMINARY／全機能の固定SHA再テスト未実施  
**前提:** **最初に** `00_foundation_gap_reconciliation.md` による「9月末のFoundation Gap × 現行実装」13項目の照合結果を確認する。本表はその後の比較であり、先行照合を置き換えない。  
**正本の参照:** Implementation Status是正SHA `84c5a624389b233fcb97c656f1c94d177f459c5a`。

## 1. 比較の軸と資料の権限

- **歴史資料A（2026-08-04）:** Phase 1〜3の手法一覧、設計構想、synthetic test案。現行FRではない。
- **歴史資料B（2026年9月末／Notion）:** `ENH-E11 Causal Lifecycle Foundation Gap Completion`、`HANDOFF_DRAFT`。当時は基盤の残差だけを対象とし、Phase 2/3を除外。現行実装との一次照合は**00文書**で行った。
- **現在の基準C:** 現行FR/NFR/ARとsource code、既存テスト、過去の独立999 Gate判定。現行SHAでの再実行は別の証拠とする。
- **最新のオーナー方針:** ENH-E11で8月案Phase 1〜3の必須技術をCLI-onlyに限って再採用する。9月末時点で承認されていたと遡及的に扱わない。

判定分類は`A_CURRENT_REQUIREMENT_GAP`（現行要件の未充足）、`B_NEW_CAPABILITY_CANDIDATE`（新規要件候補）、`C_SUPERSEDED`（既存で解消）、`D_FUTURE_PHASE`（後続）、`E_REJECT`（方針不整合）。複数の意味を持つ行は再利用部分と追加部分を分けて評価する。

## 2. Phase 1：因果推論基盤の差分

| 8月案の機能 | 9月末のENH-E11案 | 現行要件・実装の証拠 | 未充足・今回の計画上の判定 | Issue |
|---|---|---|---|---|
| Causal Questionとversion | 基盤残差候補 | FR-040 IMPLEMENTED、Question/Specのmodelあり | 内容の固定はC。独立したresource versionの採否はB、lineage残差はA | #15 |
| Causal Designの拡張 | 基盤残差候補 | FR-041 IMPLEMENTED | 既存DesignはC。新規CLI-file semanticsが必要なら別途B | #15 |
| DAG/CPDAG/PAGとendpoint | 基盤残差候補 | FR-037 IMPLEMENTED。GraphSemanticsあり | 既存GraphはC。FCIのPAG生成はB | #17 |
| 識別と科学的負結果 | 基盤残差候補 | FR-042/043/046、AR-005/023 IMPLEMENTED | Native Randomized/BackdoorはC。Frontdoor/IV/DoWhyはB | #15、#16 |
| Data Eligibility / gate | 基盤残差候補 | FR-044/045 IMPLEMENTED。型、sample、overlap検査 | 既存判定はC。新手法固有の基準はB | #15、#18〜23 |
| ATE/ATT推定 | 基盤残差候補 | FR-047。Diff/OLS/IPW/AIPWあり | 基本推定はC。SE/CI品質は追加検証が必要 | #19 |
| IPW/IPTW Diagnostics | 基盤残差候補 | FR-048、E9のweight/arm ESS/balance/overlap | 既存重み・診断はC。stabilized/normalizedの命名とCI品質は是正候補 | #19 |
| Placebo/Data Subset Refutation | 基盤残差候補 | FR-049 IMPLEMENTED | C：再実装しない | #16 |
| Random Common Cause/Bootstrap Refutation | 承認された追加方式のみ検討 | 現行Refutation Adapterに方式なし | B：DoWhy等の採用を要件変更で判断 | #16 |
| Adjustment/Clipping Sensitivity | 基盤残差候補 | FR-050 IMPLEMENTED | 既存2軸はC。未測定交絡などの追加はB | #16 |
| Scientific Validation | 基盤残差候補 | FR-044〜046、Scientific testあり | 既存範囲はC。新推定器の手法別検証はB | #15、#24 |
| FCIと潜在交絡 | 追加候補、無条件採用せず | DiscoveryにPC/GES/LiNGAM/NOTEARS。FCIなし | B：PAGのCIRCLE端点を保持 | #17 |
| DoWhy識別 | 追加候補、正式承認なし | 現行のactive DoWhy backendなし | B：正本改定とoptional依存承認が必要 | #16 |
| Provenance/Artifact/Lineage | 基盤残差候補 | FR-054/NFR-001b/NFR-002 PARTIAL、local manifestあり | 現行要件の未充足はA。新規CLI metadataはB | #15、#24 |
| API/Worker/DB統合 | 当時の残差候補 | 現行Productの実行経路あり | 既存機能はC。**新規E11機能の統合はD**（オーナー決定） | #13、#24 |

**注意:** 上記のFoundation実装状態の詳細なソース・テスト・999証拠は先行`00_foundation_gap_reconciliation.md`を正とする。本表の「C」は個別Capabilityの既存範囲だけを指す。

## 3. Phase 2：CATE/HTE（9月末案では明示的に除外、現在は実装候補）

| 8月案の機能 | 9月末判断 | 現行実装 | 差分・分類 | Issue |
|---|---|---|---|---|
| 第一級CATE/HTE estimand | 後続へ送る | 現行SpecのestimandはATE/ATTのみ | B：意味上の新規契約 | #18 |
| LinearDML / CausalForestDML | 後続 | 現行Estimator registryなし | B：optional EconML等 | #18 |
| DRLearner / ForestDRLearner | 後続 | AIPWはあるがDRLearnerではない | B：推定器と結果が異なる | #18 |
| S/T/X Learner | 後続 | 第一級Causal Estimatorとして未確認 | B | #18 |
| DRIV / IV+ML | 後続 | IV+ML Adapterなし | B：Phase 1の識別・Phase 3 LATEと分離 | #18 |
| Cross-fitting、nuisance/final/split | 後続 | AIPWに部分的cross-fittingあり | 既存再利用C＋新規Contract B | #18、#24 |
| CATE support/overlap/calibration/stability | 後続 | E9の汎用診断はあるがCATE専用なし | B | #18、#24 |
| 個体別CATE Parquet・policy-ready file | 後続 | CLI専用CATE Artifactなし | B：Policy実行ではない | #18、#24 |

## 4. Phase 3：時系列因果と準実験（9月末案では除外）

| 8月案の機能 | 9月末判断 | 現行実装 | 差分・分類 | Issue |
|---|---|---|---|---|
| PCMCI/PCMCI+/LPCMCIとCI registry | 後続 | Tigramite登録なし | B | #20 |
| TemporalDesign / TIME_SERIES_GRAPH | 後続 | 現行GraphTypeは時系列専用型なし | B | #20 |
| DiD / Event Study | 後続 | Causal CLIに専用Design/Estimatorなし | B | #21 |
| Interrupted Time Series | 後続 | 専用推定器なし | B | #21 |
| Sharp/Fuzzy RDD | 後続 | 専用推定器なし | B | #22 |
| IV/LATE/weak-IV | 後続 | Backdoorと別のDesign推定器なし | B | #22 |
| Synthetic Control / Synthetic DiD | 後続 | donor-based推定器なし | B | #23 |
| 手法固有の診断とbenchmark | 後続 | 汎用Diagnosticsだけでは不足 | B | #21〜24 |
| RPCMCI/J-PCMCI+ | 非必須の8月拡張点 | 対応なし | D | #13 |
| Policy Evaluation/監視/drift | Phase 4／将来 | E11のCLI対象外 | D | #13 |

## 5. 検証証跡と確定条件

**本表は現行SHAでのテスト合格証明ではない。** Issue #14の全体完了には、行単位のFR/NFR/AR、コードの関数/ファイル、Unit/Integration/Scientific Benchmark、過去の999（存在すれば）、新規再実行を対応付ける。見つからない999は`NOT_LOCATED`と記す。`IMPLEMENTED`／`PARTIAL`／`ABSENT`、`TEST_EXISTS`、`HISTORICAL_ACCEPTED`、`RERUN_PASS/FAIL/BLOCKED`は区別する。

## 6. 承認を要する設計上の衝突

1. 正本§11は未承認DoWhy/EconMLを対象外とする。追加前にsemantic requirementの変更を承認する。
2. 9月末`HANDOFF_DRAFT`はPhase 2/3を後続へ送っていた。最新の方針で再採用した事実は正式構想承認に記録し、歴史を書き換えない。
3. `causal-analysis-spec/2`はATE/ATTと特定手法に限定。旧schemaを黙って拡張せず、版管理を伴う契約とする。
4. Product DBのlineageとDB-free CLI Manifestを同じ永続Resourceと扱わない。
5. Phase 1識別IV、Phase 2 IV+ML、Phase 3 LATEは別々の科学的契約・テストが必要。

**現時点の扱い:** この三資料比較は後続工程の**暫定案**。先行する9月末13項目のSource Reconciliationの完了を、Phase 1〜3の正式実装承認と取り違えない。
