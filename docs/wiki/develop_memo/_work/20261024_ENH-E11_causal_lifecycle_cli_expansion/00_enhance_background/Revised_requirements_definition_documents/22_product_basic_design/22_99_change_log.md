# 22_99_change_log

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

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
