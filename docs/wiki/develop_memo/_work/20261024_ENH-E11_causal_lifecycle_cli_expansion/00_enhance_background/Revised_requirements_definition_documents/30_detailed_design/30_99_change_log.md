# 30_99_change_log


---

## 30. CHANGE LOG

### 30.1 Effective snapshot baseline

Domain/runtime/capability/result/lineage、Family/Navigation Stage catalog、browser navigation、operation availability等のcurrent detailed designをeffective snapshotとして統合した。

### 30.2 Project Management / Analysis Workspace separation

Project ManagementとAnalysis Workspaceを別application/navigation scopeとして定義し、Project routes、resource ownership、Analysis Context、browser restoration、frontend component responsibilityをcurrent detailed designへ統合した。

### 30.3 Analytical surface placement

Causal / Exploratory / Predictiveのanalytical semanticsをNavigation Stage Contentsへ配置した。Exploratory Data Quality、TIME_TREND、CHARTについてbackend semanticsを変更しないcontractを明文化した。

### 30.4 Analysis Stage Content Architecture

Selected ProjectからProject Listへの明示的parent navigation、current Navigation Stageをprimary identityとするStage presentation、Causal Stage responsibility separation、Predictive Stage responsibility separation、Dataset-schema-backed Predictive feature selector、vertical layout/accessibility/history/test seamをcurrent effective detailed design本文へ統合した。

この変更はUI/IA/presentation designの具体化であり、canonical Navigation Stage catalog、API、persistence schema、backend analytical semantics、runtime execution lifecycleを変更しない。

### 30.5 ENH-E10 Predictive Advanced Modeling / XAI

- Model Capability / Explanation Method Capability registry、optional dependency isolation、LightGBM adapterを追加設計した。
- provider-neutral `fitted-model/2`、v1 read compatibility、same-runtime/config reproducibility contractを定義した。
- SHAP_TREE raw-output semantics、LIME_TABULAR local-only + TRAIN explanation referenceを定義した。
- `predictive-capabilities/1`をbackend authorityからadditiveに拡張し、Train / Explainability / Model Managementのconsumer contractを具体化した。
- G01/G02はdeterministic lower-level correctness、G03 Browser E2Eは2 critical product journeyをprimary scopeとする。
