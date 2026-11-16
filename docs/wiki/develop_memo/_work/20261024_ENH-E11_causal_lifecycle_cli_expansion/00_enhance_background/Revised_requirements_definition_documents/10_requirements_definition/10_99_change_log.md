# 10_99_change_log


---

## 13. CHANGE LOG

### 13.4. ENH-E4 Canonical Execution Architecture Requirements

- canonical Execution lifecycle / StageExecution / Result / Artifact / Lineage authorityをrequirementsへ統合した。
- Family-specific Analysis Specificationとgeneric workflow coreの境界を明確化した。
- FR-001〜FR-128、NFR-001〜NFR-020、AR-001〜AR-020を現行requirements baselineとして継承する。

### 13.5. ENH-E5 Family × Navigation Stage Application Architecture Requirements

- FR-104 / FR-105をProject Workspaceの新navigation architectureに合わせて改定した。
- FR-129〜FR-162を追加し、Family / Navigation Stage、Capability ownership、Navigation / Runtime separation、Family-specific Stage set、互換性とscope境界を定義した。
- NFR-021〜NFR-027、AR-021〜AR-026、Navigation State要件を追加した。
- 既存`AnalysisSpecification.analysis_family`を再利用し、Navigation Stageをpersistent analysis/runtime modelへ追加しないことを明示した。

### 13.6. ENH-E5 Phase I Canonical Convergence

- D1/D2/D3をRequirement lifecycle（Status / Implementation Status / Delivery）へ反映した。
- Phase Gの11 D2 freeze packageをRequirement本文へ具体化した。
- D3を削除せず`DEFERRED / FUTURE`として保持した。
- Navigation endpoint/schema/catalog/default Stage/routeをfrozen contractへ収束した。


### 13.7. Project Management / Analysis Workspace Requirements

Project ManagementとAnalysis Workspaceを別navigation scopeとし、Project routes、Analysis Context、surface ownership、browser restoration、existing analysis surface placementをcurrent requirementへ統合した。

### 13.8. ENH-E10 Predictive Advanced Modeling / XAI Requirements

- FR-061 / FR-068 / FR-069 / FR-071 / FR-161をadvanced model/XAI capabilityに合わせて改定した。
- FR-178〜FR-184、NFR-028、AR-027を追加した。
- LightGBM classifier/regressor、optional dependency isolation、durable fitted-model load contract、SHAP/LIME compatibility/provenance、capability-driven Product integrationをcurrent requirementへ統合した。
- `predictive-analysis-spec/1`、TRAIN-only preprocessing、TEST isolation、Predictive-not-causal、Metrics/Explainability separationを維持した。

### 13.9. ENH-E11事前整合性監査：Implementation Statusの是正（2026-10-24）

ENH-E11の新規技術スコープを定める前に、過去の完了Enhancementで実装・受入済みのcontractと本正本のImplementation Statusを照合した。監査対象の固定SHAは`1207e725990db75b41bb2a398e6963efbeb8383c`（`prototype/ariadne_mvp`）である。本節の変更は**Implementation Statusのみ**であり、Requirement本文、Requirement Status、Delivery、ENH-E11の新規スコープを変更しない。

| 対象ID | 旧 → 新 | 主な判定根拠 |
| --- | --- | --- |
| FR-015 | `NOT_IMPLEMENTED` → `IMPLEMENTED` | AnalysisViewのtyped filter validationと`FILTER_TYPE_MISMATCH`の現行実装・E5 G04テスト |
| FR-032 | `NOT_IMPLEMENTED` → `IMPLEMENTED` | Exploratory Result→Causal/Predictive DRAFT handoff、`MOTIVATED` lineage、E3 integration test（`TZ=UTC`で再実行PASS） |
| FR-067、AR-016 | `NOT_IMPLEMENTED` → `IMPLEMENTED` | untouched TEST subgroup、`sample_count`、1000回のdeterministic percentile bootstrap、E5 G02受入 |
| FR-082、FR-114b | `PARTIAL` / `NOT_IMPLEMENTED` → `IMPLEMENTED` | scoped idempotency authority、semantic request hash、replay/conflict/missing-key handling、E5 G05受入 |
| FR-108 | `NOT_IMPLEMENTED` → `IMPLEMENTED` | Navigation resource deep routeのparse/serialize、resource-family validation、E5 G01およびE7回帰 |
| FR-129〜131、FR-134〜137、FR-140〜143、FR-146〜158、FR-162 | `NOT_IMPLEMENTED` → `IMPLEMENTED` | family-local catalog、URL/history、runtime separation、Family別Stage surface、resource/domain境界。E5 G00〜G05、E7、E8、E9の独立受入記録。ただしFR-144/145はこの集合に含めない |
| FR-132、FR-133、FR-144 | `NOT_IMPLEMENTED` → `PARTIAL` | default stage、immutable catalog、read-only aggregationは存在するが、具体Stage定義の所有者がFamily-specific Capabilityではなくgeneric applicationである |
| FR-138 | `NOT_IMPLEMENTED` → `PARTIAL` | unknown Family/Stageの明示errorは存在するが、利用可能な遷移先の明示提示までの充足根拠が不足 |
| NFR-021、NFR-022、NFR-024〜027 | `NOT_IMPLEMENTED` → `IMPLEMENTED` | navigation/runtime isolation、route determinism、unit/API/E2E separation、ARIA/focusおよびcritical-path分離に関する実装・受入記録 |
| AR-017、AR-021〜026 | `NOT_IMPLEMENTED` → `IMPLEMENTED` | semantic/direct metric comparisonの独立判定、表示順とruntimeの分離、Causal/Predictive/Exploratory意味論の分離 |
| FR-061、FR-068、FR-069、FR-071、FR-161、FR-178〜184、NFR-028、AR-027 | `PARTIAL` / `NOT_IMPLEMENTED` → `IMPLEMENTED` | ENH-E10 G01/G02/G03の最終999 PASS、optional依存・model round-trip・SHAP/LIME・provenance・Frontend統合の現行再実行（42 PASS） |

根拠の主な一次資料：

- [E5 G00](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/30_test_report/G00/Trial01/E5-G00_01__999_gate_decision.md)、[E5 G01 Trial04](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/30_test_report/G01/Trial04/E5-G01_04__999_gate_decision.md)、[E5 G02](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/30_test_report/G02/Trial01/E5-G02_01__999_gate_decision.md)、[E5 G03](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/30_test_report/G03/Trial01/E5-G03_01__999_gate_decision.md)、[E5 G04 Trial02](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/30_test_report/G04/Trial02/E5-G04_02__999_gate_decision.md)、[E5 G05](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/30_test_report/G05/Trial01/E5-G05_01__999_gate_decision.md)
- [E8 G02 Trial02](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260820_ENH-E8_analysis_stage_content_redesign/30_test_report/G02/Trial02/999_GATE_DECISION.md)、[E9 G05](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/G05/Trial01/ENH-E9-G05_01__999_gate_decision.md)
- [E10 G01](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G01/Trial01/ENH-E10_G01_01_999_gate_decision.md)、[E10 G02最終再検証](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G02/Trial01/ENH-E10_G02_01_999_gate_decision_reverification_05.md)、[E10 G03](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/develop_memo/_work/20260926_ENH-10_predictive_advanced_modeling/30_test_report/G03/Trial01/ENH-E10_G03_01_999_gate_decision_ja.md)
- 現行コード・テスト：`src/ariadne/product/application/navigation_catalog.py`、`frontend/navigation_state.js`、`frontend/causal_stage_presentation.js`、`src/ariadne/interfaces/web_api/idempotency.py`、`src/ariadne/capabilities/predictive/`、`tests/product/test_enh_e5_*.py`、`tests/enhancement/enh_e10/`

更新しなかった未充足・未確定の主要事項：

- `FR-020 = NOT_IMPLEMENTED`：手動でAnalysisView DRAFTを作成するData画面やExploratory Result handoffはあるが、Explore stateから直接data-selection semanticsを変換する操作とは同一視しない。
- `FR-145 / NFR-023 = NOT_IMPLEMENTED`、`FR-132 / FR-133 / FR-144 = PARTIAL`：Family-specific Capability ownershipは現在の中央集約catalogと不一致。要件改訂か所有権の移管を別途決める。
- `FR-138 = PARTIAL`：invalid routeを拒否するが、valid transition提示を含む全面充足は未確認。
- `FR-051 / FR-054 / FR-008 / FR-095 / NFR-002 / AR-004 = PARTIAL`：一般的な探索データ再利用警告およびResearchContext→Specification→Plan→Stage→Resultを網羅するcanonical lineageは未完成。
- `FR-034 / FR-072 / FR-086a / FR-087b / FR-107 / FR-109 / FR-111 / FR-121 / FR-123a / FR-124b / NFR-001b / NFR-006b / NFR-008b / NFR-012 / AR-020`等の既存`PARTIAL`は、本監査で全面充足を立証できていないため維持する。`FR-087b`はruntime manifestのscientific library version網羅性、`FR-107`はavailability responseのmessage等に未充足がある。

現行SHAでの限定再実行は、E5対象が**52 PASS / 3 FAIL**（旧Nodeテスト2件のDOM前提、旧依存制約テスト1件のLightGBM optional dependency前提）、E10対象が**42 PASS / 2 non-failing warnings**、科学ベンチマークが**13 PASS**、E9診断関連が**27 PASS**、CLI/E7ナビゲーション関連が**21 PASS**だった。Exploratory handoff E2Eは、非UTCホストでlease日時比較の問題に遭遇したが、`TZ=UTC`では**1 PASS**を確認した。この日時処理は独立した改善候補である。今回、全repository suiteとBrowser E2Eの新規実行はしておらず、過去の999 PASSも各Gateのfrozen scopeに限定される。

従って、本是正は「すべてのE5〜E10要件が完全実装済み」という認定ではない。未充足要件と現行テストの陳腐化を明示的に残した状態で、ENH-E11のBaseline判断へ進むためのImplementation Status snapshotを回復する。

## 13.10. 2026-11-16 RD-03：ENH-E11正式要件条文の発行

- `FR-185〜203`／`NFR-029〜036`／科学的`AR-028〜044`の全44件を`ACTIVE / UNVERIFIED / ENH-E11`として改訂版に発行。
- 既存FR195/NFR36/AR27のID・原文・Statusには変更なし。
- §11のDoWhy/EconML等の除外は**E10時点の意味**へ明確化し、DEC09承認Local E11 Optional Capabilityのみ例外適用。
- E11-A系Architecture候補はScientific ARへ改番しない。68 Scope／41 Method／10 UC、Draft-to-formal IDの監査を[RD-03 Trace](../96_rd03_formal_requirement_traceability.md)へ独立記録。
- Owner SHA最終確認、旧canonicalへの昇格、Independent Architecture、Gate06/07、Science T2/T3、Legalを完了済みと主張しない。
