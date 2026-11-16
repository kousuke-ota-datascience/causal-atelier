# 22_99_change_log


---

## 20. CHANGE LOG

### 20.4 ENH-E4 Canonical Execution Architecture

canonical Product runtime Execution authority、generic workflow core、persistent StageExecution、Result / Artifact / Lineage authority等の設計を継承する。

### 20.5 ENH-E5 Family × Navigation Stage Application Architecture

Project Workspaceのanalytical navigationをFamily / Family-local Navigation Stageへ再構成する。Navigation taxonomyはPresentation / Application / Capabilityの責務として追加し、Generic Workflow Coreおよびruntime Execution Stageへ依存を逆流させない。

### 20.6 ENH-E5 Phase I Canonical Convergence

- Outbox/nonexistent Port overstatementをD1 current contractへ訂正した。
- Navigation metadata endpoint/schema/route/default Stageをfreezeした。
- typed filter、subgroup、comparability、authorization、idempotency、lineage、reproducibility、frontend accessibilityをD2 targetとして具体化した。
- `StageAttempt.effective_random_seed` migrationを明示し、D3 capabilityをE5 acceptanceから分離した。


### 20.7 ENH-E7 Project Management / Analysis Workspace Basic Architecture

Application IAをProject ManagementとAnalysis Workspaceへ分離し、Project route、Analysis Context、resource ownership、existing Causal/Exploratory/Predictive surface placementをcurrent basic designへ統合した。API/persistence/backend execution semanticsはUI再配置だけを理由に変更しない。

### 20.8 ENH-E7 Product Basic Design Structure Restoration

- ENH-E2で確立していた「文書の設計粒度」「screen/function boundary」「operation / prerequisite / Resource effect / post-state / UI Gate」「画面遷移とlogical context handoff」という基本設計の記載粒度を復元した。
- Top-level IAのconcept authorityは`00_product_concept_memo.md > 3. Ariadne application model`へ集約し、本書ではsurface responsibility、route authority、resource lifecycle ownership、operation/state boundaryを詳細化する責務分離とした。
- Project Management / Analysis Workspace分離、Analysis Context、Family/Navigation Stage、existing capability placement、runtime/capability semanticsは維持した。



### 20.9 ENH-E10 Predictive Advanced Modeling / XAI

- backend Model / Explanation Capability registryをcompatibility・availability authorityとして追加した。
- LightGBM Binary Classification / Regression、`fitted-model/2`、SHAP_TREE、LIME_TABULARのproduct-level responsibilityを定義した。
- optional dependency isolation、no-silent-fallback、same-runtime/config reproducibility、Model Management provenanceをcurrent designへ統合した。
- existing `predictive-analysis-spec/1`、generic execution lifecycle、TRAIN-only preprocessing、TEST isolation、Predictive Stage responsibilityを維持した。


---

## 20.10. ENH-E11 BD-01 Local Causal CLI Architecture（2026-11-16）

- Owner採用済みDEC09のARC09-01〜07を、Local System Boundary、Scientific Pipeline、Local Result/Artifact、Environment/Securityの責務別4文書へ展開。
- 既存Product system図でCLIがWeb APIを通ると解釈され得る混在表記を、Product laneとE11 Local laneへ区別。
- 既存`causal-analysis-spec/2`／Product Worker/DB／Navigation、E9/E10回帰、GAP-C01〜04の非改変条件を維持。
- 実際のCLI`scientific_stage.py`・`ScientificCoreAdapter`・Manifest等を参照したGapをArchitecture Reviewへ記録。独立レビュー・IF/Port/Schema・Science/Legal/Gateは未承認／未実施。
- [BD01 review](../bd01_review/90_architecture_consistency_review.md)、[44 Requirement trace](../bd01_review/91_requirement_architecture_trace.md)、[E11 Canonical promotion rule](../93_enh_e11_canonical_promotion_policy.md)。

### 20.11. 2026-11-16 — BD-01整理：常設設計とフロー型レビューの分離

- 旧`22_20〜22_23`に記載した恒常的設計契約は`22_00`、`22_04`、`22_06`、`22_08`、`22_09`、`22_12〜16`に統合した。
- `22_20〜23`の当初断片は[BD01 source snapshots](../bd01_review/README.md)へ原Blobのまま保全。旧`22_90〜91`の自己レビュー/44要件の割当Traceも`bd01_review/`へ移動。
- `22_product_basic_design/`には将来の正本として継続利用する責務別ファイルのみ置く。原正本`docs/wiki/requirement_definition/`の昇格条件は変更しない。
