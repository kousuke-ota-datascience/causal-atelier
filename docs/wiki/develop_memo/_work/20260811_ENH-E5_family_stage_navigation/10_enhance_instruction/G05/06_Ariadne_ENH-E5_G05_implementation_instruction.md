# Ariadne ENH-E5 G05 — Cross-family Convergence and Cross-cutting Completion — Implementation

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G05`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
- 契約状態: `PHASE_K_CONVERGED / EXECUTION_FREEZE_READY`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 06 implementation contract`
- Execution Mode: `SINGLE_EXECUTION`

## 0. Authority / execution isolation

- 本文書は、このGateを実装する**Coding Agentに対する唯一のnormative implementation contract**である。
- Coding Agentは仕様補完のために`00〜30`、ADR、他Gate、他Package、`07`、issue、commit message、外部Webを参照してはならない。
- repositoryはcurrent implementation factと実装方法を調査するsubstrateとして参照してよいが、仕様authorityではない。
- 本文書だけでrequired behavior / boundary / migration / error semanticsを一意に決定できない場合は、探索を広げず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本`06`を期待挙動の補完に利用しない。


## 1. Outcome

cross-cutting D2=`PF-D2-04 / 05 / 06 / 07 / 08 / 10`を完成し、prior Gate candidateを壊さずENH-E5全体を収束させる。

### Scientific Comparability / Reuse Guard

Comparisonは二段階:

```text
semantic_compatible
    ↓
direct_metric_comparable
```

Canonical response fields:

```text
semantic_compatible
direct_metric_comparable
compatibility_reasons[]
direct_comparison_blockers[]
```

External serialized fieldは`compatibility_reasons`に固定する。`reasons`はinternal algorithm termとしてのみ使用可能で、alternative external response fieldとしては使用しない。

Rules:

- same Family / same Result Typeをgeneric direct comparisonの前提とする。
- semantic mismatchはHTTP/application request failureにせず、`semantic_compatible=false`, `direct_metric_comparable=false`, reasonsを返す。
- incompatible caseでquantitative delta/rankを生成しない。
- Predictive semantic key:
  `task_type, prediction target/outcome, prediction unit, prediction time, horizon, deployment/evaluation population semantics`。
- Predictive direct metric:
  same `dataset_version_id` + same TEST-row identity/hash + same metric definition。
- Causal semantic key:
  `treatment/exposure, outcome, estimand, target population`。
- Causal direct quantitative comparison:
  semantic compatibility + same dataset/view/analysis population。
- cross-Family metric/effectを単一scoreへflattenしない。
- same immutable `dataset_version_id`はAnalysisViewが異なってもsame-data。
- Exploratory -> confirmatory same-dataで`EXPLORATORY_REUSE_SAME_DATA` warning。non-blocking。
- source Exploratory Result IDをevidenceとして保持しExecution snapshotへ伝播。


### Command Idempotency

対象はHTTP methodではなくduplicate durable side effect riskで決める。

Web/API transport:

```text
Idempotency-Key
```

Application-layer normalized value may be named `idempotency_key`.

Scope:

```text
(project_id, command_scope, idempotency_key)
```

- canonical semantic request hashへpath上のsemantic resource identityも含める。
- missing required key -> `IDEMPOTENCY_KEY_REQUIRED`。
- same scope/key + same request hash -> stored result/response replay、duplicate side effectなし。
- same scope/key + different request hash -> HTTP 409 `IDEMPOTENCY_CONFLICT`。
- concurrent duplicate requestsはsingle durable side effectへ収束。
- 可能な限りidempotency recordとdomain mutationを同一transactionへ置く。

ENH-E5対象Commandには少なくとも:

- DatasetVersion create
- Execution batch create
- GraphVersion / GraphEditDraft create
- Result export create
- Project Export create
- AnalysisView create
- Exploration execution submit
- Exploratory Result -> AnalysisSpecification DRAFT create
- ResearchContext create
- AnalysisSpecification create / revise
- durable Predictive split-validation
- Predictive Execution submit / rerun / revise
- Annotation / WorkspaceAnnotation create

対象外:

- pure GET / query / compare / preview / validate
- plan-hash natural idempotencyを持つExecutionPlan create
- uniqueness-protected explicit lineage link
- Project create
- state-machine cancel / fix / update

exactly-once executionは保証しない。


### Retry-safe Artifact Materialization

successful Stage outputのlogical identity/object keyは:

```text
Execution + Stage + output slot/ordinal + Artifact type
```

- same logical output + same content hash -> existing durable Artifact reuse。
- same logical output + different content hash -> nondeterministic-output conflict。
- retry/restartでduplicate durable Artifactを作らない。
- Result/Artifact metadata bindingはtransactional commit。
- metadata DBとArtifactStore間general compensationはD3/FUTURE。
- exactly-once executionはclaimしない。


### Project Authorization / Sensitive Output

Persisted Project role:

```text
OWNER
EDITOR
VIEWER
```

Matrix:

- READ: OWNER / EDITOR / VIEWER
- WRITE / MUTATE: OWNER / EDITOR
- Execution submit/cancel/retry/rerun/revise: OWNER / EDITOR
- Export create: OWNER / EDITOR
- Membership administration: OWNER only
- Explicit sensitive output: OWNER / EDITOR
- independent persisted `EXECUTE` roleなし

Coverage:

- 全project-scoped routeはservice action前にProjectMembershipをresolve。
- Project IDをpathに持たないlegacy/generic resource routeもresourceからProjectをderiveして同じauthorization。
- prediction row / local explanation row/detailはpotentially sensitive。
- VIEWERにはaggregate/suppressed representationのみ。
- configurable sensitive-column governanceとsystem/operator authorizationはD3/FUTURE。


### Canonical Lineage

Read chain:

```text
ResearchContextVersion
  -> AnalysisSpecification
  -> ExecutionPlan
  -> Execution
  -> StageExecution
  -> Result
  -> Artifact
```

接続input:

```text
DatasetVersion
AnalysisView
GraphVersion
input Result
base Execution
```

Rules:

- canonical FK/snapshot/ownershipからdeterministically導けるstructural relationはread modelで投影。
- structural relationをgeneric `LineageEdge`へduplicate persistしない。
- `MOTIVATED`等semantic relationはgeneric LineageEdgeへ保存可能。
- `Result --MOTIVATED--> AnalysisSpecification(status=DRAFT)`を保持。
- relationをguessしない。
- Project boundaryを越えない。
- Navigation Stageをpersistent lineage node/edgeへ追加しない。


### Reproducibility Metadata

DB migration:

```text
StageAttempt.effective_random_seed: int | null
```

Migration/runtime rules:

- existing StageAttempt rowsは`null` backfill可能。
- application/runtime deploymentはcolumn存在後に切り替える。
- stochastic Stageはactual effective seedを各attemptへ保存。
- deterministic Stageは`null`。
- same logical Stageのtechnical retryはsame effective seedを再利用し、各attempt rowへ同じseedを明示。
- runner/application boundaryはprocessorがactual seedを永続化できる形で報告。
- `Execution.runtime_version_json`既存JSON fieldを利用し、独立column追加は必須でない。

Exact runtime manifest keys:

```text
ariadne_code_version
python_version
platform_system
platform_release
machine
libraries
```

`libraries`にはactualに利用したregistered scientific/runner dependency versionを保存する。未使用future optional libraryをversion取得目的だけでimportしない。

保証対象はenvironment reconstruction metadataでありbit-for-bit numerical identityではない。


### Prior Gate preservation model

G05はprior Gate specificationを再解釈しない。実行preconditionとしてOperatorが次を提供する:

```text
G00 Fixed Trial Candidate SHA + PASS report
G01 Fixed Trial Candidate SHA + PASS report
G02 Fixed Trial Candidate SHA + PASS report
G03 Fixed Trial Candidate SHA + PASS report
G04 Fixed Trial Candidate SHA + PASS report
```

G05 Coding Agentはそれらの仕様文書を読まない。candidate repositoryとPASS evidenceをpreconditionとして扱い、以下のembedded invariantsを破壊しない:

- Navigation catalog endpoint/schema/default/catalog。
- canonical/deep routeとURL-authoritative navigation。
- Predictive existing spec/settings/runtime compatibility。
- Causal runtime/navigation separation。
- Exploratory typed filter/handoff/provenance。
- Navigation Stage非永続化 / runtime independence。


## Prohibited changes

- `Navigation Stage = Execution Stage`となるmapping、alias、inheritanceを導入しない。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- CLI / Python library / backend execution use caseへCurrent Navigation Stageを必須inputとして追加しない。
- `AnalysisSpecification.analysis_family`と重複するFamily discriminatorを追加しない。
- Predictive existing fieldの削除、rename、default semantics変更を行わない。
- LightGBM / DoWhy / EconMLを追加しない。
- D3 / `DEFERRED / FUTURE` requirementをENH-E5 implementationまたはmandatory acceptanceへ混ぜない。
- testをgreenにする目的のassertion弱体化、削除、skip、xfailを行わない。


## Gate Acceptance Criteria

- `AC-G05-001`: Comparison response/semantic/direct rulesが本文どおり。
- `AC-G05-002`: same-data confirmatory warningとsource Result evidence propagationが本文どおり。
- `AC-G05-003`: Web/API `Idempotency-Key` transport、application `idempotency_key` normalization、scope/hash/replay/conflict/concurrency/coverage/exclusionsが本文どおり。
- `AC-G05-004`: retry-safe Artifact identity/hash/reuse/conflict/transaction ruleが本文どおり。
- `AC-G05-005`: Project role matrix、all-route coverage、legacy resource Project derivation、sensitive outputが本文どおり。
- `AC-G05-006`: canonical lineage chain/input/MOTIVATED/no-guess/no-duplicate/Project boundaryが本文どおり。
- `AC-G05-007`: `StageAttempt.effective_random_seed` migration/backfill/deploy/actual seed/retry ruleが本文どおり。
- `AC-G05-008`: `runtime_version_json` exact keysとactual library version。
- `AC-G05-009`: prior Gate PASS evidenceがexecution preconditionとして揃い、embedded protected invariant regressionがgreen。
- `AC-G05-010`: D3/FUTUREをmandatory implementation/testへ追加しない。


## Coding self-verification

- scientific comparison/reuse guard unit/integration。
- idempotency missing/replay/conflict/concurrent duplicate。
- Artifact retry/restart/concurrent materialization。
- authorization matrix + legacy/generic route。
- lineage projection/semantic edge/Project boundary。
- migration/backfill/runtime manifest/seed retry。
- prior Gate regression evidence。
