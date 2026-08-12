# Ariadne ENH-E5 G05 — Cross-family Convergence and Cross-cutting Completion — Verification

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G05`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `83d33f5c981fa1aa5740e91c30bb969dd6097c42`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 07 verification contract`

## 0. Authority / verification isolation

- 本文書は、このGateを検証する**Test / Audit Agentに対する唯一のnormative verification contract**である。
- Test / Audit Agentは期待挙動を補完するためにGate `06`、`Pxx`、`P00`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repository、candidate diff、test output、migration state、API responseはverification evidenceとして参照してよいが、仕様authorityではない。
- 本文書だけでPASS / FAILを一意に判定できない場合は`BLOCKED_CONTRACT_AMBIGUITY`として報告し、仕様を発明しない。


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
compatibility_reasons[] / reasons[]
direct_comparison_blockers[]
```

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
- Result / Product export create
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


## Gate Acceptance Criteria

- `AC-G05-001`: Comparison response/semantic/direct rulesが本文どおり。
- `AC-G05-002`: same-data confirmatory warningとsource Result evidence propagationが本文どおり。
- `AC-G05-003`: idempotency scope/hash/replay/conflict/concurrency/coverage/exclusionsが本文どおり。
- `AC-G05-004`: retry-safe Artifact identity/hash/reuse/conflict/transaction ruleが本文どおり。
- `AC-G05-005`: Project role matrix、all-route coverage、legacy resource Project derivation、sensitive outputが本文どおり。
- `AC-G05-006`: canonical lineage chain/input/MOTIVATED/no-guess/no-duplicate/Project boundaryが本文どおり。
- `AC-G05-007`: `StageAttempt.effective_random_seed` migration/backfill/deploy/actual seed/retry ruleが本文どおり。
- `AC-G05-008`: `runtime_version_json` exact keysとactual library version。
- `AC-G05-009`: prior Gate PASS evidenceがexecution preconditionとして揃い、embedded protected invariant regressionがgreen。
- `AC-G05-010`: D3/FUTUREをmandatory implementation/testへ追加しない。


## Verification architecture

- comparison: semantic mismatch success response、no quantitative delta/rank、Predictive/Causal direct gates、cross-Family flatten禁止。
- reuse: same dataset despite different AnalysisView、confirmatory warning、source Result evidence/snapshot propagation。
- idempotency: exact command coverage/exclusions、path resource hash、missing/replay/conflict/concurrency。
- Artifact: logical identity、same hash reuse、different hash conflict、retry/restart duplicate 0件。
- authorization: all project-scoped routes、legacy generic resource routes、VIEWER sensitive detail deny。
- lineage: full chain/input、MOTIVATED、no guess、no structural duplicate、Project boundary。
- reproducibility: migration/backfill、deploy order evidence、actual seed、retry same seed、deterministic null、manifest exact keys。
- prior Gate: Fixed Trial Candidate SHAs + PASS reports + protected regression。
