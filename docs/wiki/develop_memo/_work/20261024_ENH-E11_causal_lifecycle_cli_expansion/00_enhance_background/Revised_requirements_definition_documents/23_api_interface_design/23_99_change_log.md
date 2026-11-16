# 23_99_change_log

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

---

## 20. CHANGEPOINT

本章はcurrent contract本文の代替ではなく、Enhancementごとの差分サマリを記録する。現在有効なinterface contractは`§1`〜`§9`をauthorityとする。

### 20.2 ENH-E2 Golden Path Interface Expansion

ENH-E2では、Project論理削除、Discovery Analysis Spec、Graph Versionの`designated_outcome_node` / allowed action projection、Graph Edit Draft、Graph Candidate / Comparison、Inference Outcome整合性validation、および対応error codeを追加した。これらのcurrent contractは後続Enhancementで有効なものを本文へ統合済みであり、本節では差分そのものを再定義しない。

### 20.3 ENH-E3 Versioned Workspace / Unified Analysis Interface Expansion

ENH-E3では、versioned Research Context / Analysis View / Analysis Specificationを中心に、Exploratory・Causal・PredictiveのFamily interface、Execution Plan / Execution、Result / Comparison / Lineage、Annotation / Artifact、Operation Availability、Worker interfaceを統合的に拡張した。後続Enhancementで変更されたauthentication、runtime、navigation等のcontractは本文のcurrent definitionをauthorityとし、本節ではENH-E3時点の過去contractを再掲しない。

### 20.4 ENH-E4 Canonical Execution Interface Contract

Canonical persistent Execution identity、generic runtime Stage、Result / Artifact / Lineage authority、headless CLI independenceを有効contractとして保持する。

### 20.5 ENH-E5 Family × Navigation Stage Interface Contract

Family / Navigation Stageをpresentation/application navigation modelとして追加する。`AnalysisFamily`は`EXPLORATORY / CAUSAL / PREDICTIVE`のdomain discriminatorとしてAnalysis Specification / Execution Plan / Executionで利用し、Navigation Stageをpersistent scientific/runtime contractへ追加しない。

Worker interfaceについては、Execution repositoryのlease ownership contractを本文に明示し、存在しないpublic `claim_token` APIや独立Execution/Stage event publish schemaを前提としない設計へ明確化した。

### 20.6 ENH-E5 Phase I Canonical Interface Convergence

- Navigation metadata endpoint/schema/route/resource deep routeをcanonicalにfreezeした。
- typed AnalysisView validation、Exploratory handoff、subgroup output、comparability response、authorization、idempotency、retry-safe Artifact、StageAttempt seedを具体化した。
- Phase G freezeに残っていたcandidate/Architecture Review待ち表現を除去した。


### 20.7 ENH-E7 Project / Analysis Browser Interface Contract

Project routesとAnalysis routesを別navigation authorityとして定義し、Project short-route normalization、Analysis Context composition、direct link / reload / Back / Forward、legacy analytical entry normalizationをcurrent browser interface contractへ統合した。Backend API/persistence contractはUI再配置だけを理由に変更しない。

### 20.8 ENH-E10 Predictive Advanced Modeling / XAI Interface

- `predictive-capabilities/1`をversion-upせずadditive extensionした。
- task defaults、structured model parameter definitions、provider/dependency availability/version、model-method compatibility、global/local supportをbackend authorityから公開する。
- advanced capability unavailable / incompatible / unsupported scopeをstable Predictive validation errorで表現し、silent fallbackしない。
- existing Artifact APIで`fitted-model/2`を扱い、新しいModel Registry APIを追加しない。
