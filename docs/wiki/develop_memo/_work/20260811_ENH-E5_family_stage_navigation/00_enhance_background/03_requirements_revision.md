# ENH-E5 要件改定

- 状態: `PHASE_H_UPDATED / CANONICAL_REVISION_PENDING`
- Revised effective requirement target: `Revised_requirements_definition_documents/10_requirements_definition.md`
- Remediation baseline: D1=31 / D2=35 / D3=28
- D2 planning freeze: 11 packages / unresolved=0

## 0. 改定の結論

Phase Iの`10_requirements_definition.md`は、Family/Navigation Stage要求の追加だけでなく、alignment auditで確定したD1/D2/D3を一物一価のcurrent/target Requirementとして再構成する。

原則:

- D1: current implementationをRequirement正本へ訂正する。
- D2: ENH-E5 targetとして`ACTIVE / ENH-E5`へ置く。
- D3: Requirementを削除せず`DEFERRED / FUTURE`として保持する。
- Requirement本文へ時系列説明を混入させない。
- Design Decision Itemの具体化は04/21/22/23/30で行う。

## 1. Requirement table schema

`10_requirements_definition.md`のRequirement一覧は最低限次を持つ。

| Column | Meaning |
|---|---|
| ID | stable Requirement ID |
| Area | Security / UI / Operations / Scientific Integrity等を含む分類 |
| Requirement | 現在有効なRequirement本文 |
| Level | MUST / SHOULD / MUST NOT等 |
| Requirement Status | ACTIVE / DEFERRED / RETIRED |
| Implementation Status | IMPLEMENTED / PARTIAL / NOT_IMPLEMENTED / UNVERIFIED |
| Delivery | BASELINE / ENH-E5 / FUTURE |

`Area`を採用し`Domain`へ変更しない。

## 2. Status assignment rule

### 2.1 D1

```text
Requirement Status = ACTIVE
Implementation Status = IMPLEMENTED
Delivery = BASELINE
```

D1はENH-E5新規実装ではない。current implementationに合わせてRequirement本文を訂正する。

### 2.2 D2

MISMATCH起点:

```text
Requirement Status = ACTIVE
Implementation Status = NOT_IMPLEMENTED
Delivery = ENH-E5
```

PARTIAL_MATCH起点:

```text
Requirement Status = ACTIVE
Implementation Status = PARTIAL
Delivery = ENH-E5
```

### 2.3 D3

MISMATCH起点:

```text
Requirement Status = DEFERRED
Implementation Status = NOT_IMPLEMENTED
Delivery = FUTURE
```

PARTIAL_MATCH起点:

```text
Requirement Status = DEFERRED
Implementation Status = PARTIAL
Delivery = FUTURE
```

D3の詳細理由・future design・revisit triggerは`90_technical_debt_and_future_enhancements.md`へtraceする。

## 3. D1 Requirement-side corrections

以下のDecision Itemに基づき、current implementationと一致するようRequirement本文を訂正する。

### 3.1 Domain / lifecycle / canonical resource

- `FR-002`: `decision_context`をProject direct ownershipとして扱わずResearchContextVersion責務へ訂正。
- `FR-007`: dedicated full ResearchContext複製を必須とせず、current immutable reference/snapshot metadata semanticsへ訂正。
- `FR-090`: Resultへfamily/schema_version/stageを一律direct ownershipさせない。
- `FR-092`: Artifactへfamily/generic schema_versionを一律direct ownershipさせない。
- `NFR-013`: 全entityへgeneric `schema_version` fieldを要求せずversioned contract boundaryでversionを識別する。

### 3.2 Exploratory / scientific capability

- `FR-011`: DatasetVersion registration時のbasic profile必須化を撤回しcurrent schema/shape/hash/profile-summary contractへ訂正。
- `FR-025a`: column missingnessをcurrent baselineとして記述。
- `FR-026a`: current association/bivariate capabilityをbaselineとして記述。
- `FR-048`: 全estimatorへ同一diagnostic setを強制せず、applicable diagnosticを生成するcurrent capabilityへ訂正。
- `FR-068`: model/preprocessor/prediction等のArtifactとmetric/error等のResult payload責務へ訂正。

### 3.3 Frontend / API / operations

- `FR-110a`: current results filters（family/type/status等）をbaselineとして記述。
- `FR-114a`: 「全create API」をidempotency applicability基準にする要求を撤回し、duplicate durable side effect riskを基準とする。
- `FR-120a`: runtime API schemaから生成されるFastAPI OpenAPIをcurrent baselineとして記述。
- `FR-124a`: current project-scoped Artifact download / safe content-disposition contractを記述。
- `FR-127a`: current basic health endpointのみをbaselineとして記述。
- `FR-128a`: current registry/capability based Algorithm/Runner resolutionをbaselineとして記述。
- `NFR-020a`: ArtifactStore Port abstractionはcurrent baseline、object-storage adapterは別Requirementへ分離する。

### 3.4 Reproducibility / reliability / security

- `FR-087a`: current code/runtime/schema snapshot metadataをbaselineとして記述。
- `NFR-001a`: current reproducibility metadataをbaselineとして記述。
- `NFR-006a`: current lease/claim/retry mechanicsをbaselineとして記述。
- `NFR-008a`: current input/path safeguardsをbaselineとして記述。
- `NFR-009a`: current sensitive Result suppressionをbaselineとして記述。
- `NFR-010a`: current API/Worker process separationをbaselineとして記述。
- `NFR-011a`: current request/execution/stage logging identifiersをbaselineとして記述。

Design-only D1 (`D10-004`, `D10-005a`, `D22-001`, `D22-002`, `D22-003a`, `D22-013a`, `D30-018a`)のRequirement波及は04/21/22/23/30と整合させる。

## 4. D2 ENH-E5 Requirements

次のRequirement/ARを`ACTIVE / ENH-E5`として具体化する。

### 4.1 PF-D2-01 — AnalysisView Typed Filter Validation

対象:

- `FR-015`

Requirement intent:

- current operator taxonomyを維持する。
- source Dataset logical type × operator × value compatibilityをvalidationする。
- type mismatch codeは`FILTER_TYPE_MISMATCH`。
- new expression language / full derived-expression static typing / Family-specific typingはENH-E5へ含めない。

### 4.2 PF-D2-02 — Exploratory Handoff & Provenance

対象:

- `FR-020`
- `FR-032`
- `FR-034`

Requirement intent:

- Explore stateからAnalysisView DRAFTへ移すのはdata-selection semantics。
- visualization-only stateはAnalysisViewへ押し込まない。
- Exploratory Resultからcanonical `AnalysisSpecification`をDRAFTとしてpersistできる。
- target FamilyはCAUSAL/PREDICTIVE。
- auto FIX / auto executionは禁止。
- semantic lineage `MOTIVATED`を保持する。
- analysis-significant provenanceを再構成可能にする。

### 4.3 PF-D2-03 — Predictive Subgroup Evaluation

対象:

- `FR-067`
- `AR-016`

Requirement intent:

- evaluation populationはuntouched TEST。
- specified subgroup columnごとに独立sliceする。
- `sample_count`必須。
- uncertaintyはnonparametric percentile bootstrap。
- confidence=0.95、resamples=1000、deterministic seed。
- valid resamples < 200はuncertaintyなし + warning。
- non-computable subgroupで値を捏造しない。

### 4.4 PF-D2-04 — Scientific Comparability & Exploratory-Reuse Guard

対象:

- `AR-017`
- `FR-072`
- `FR-051`
- `AR-004`

Requirement intent:

Comparisonは二段階。

1. semantic compatible
2. direct metric comparable

Predictive semantic key:

- task_type
- target/outcome
- prediction unit
- prediction time
- horizon
- deployment/evaluation population semantics

Predictive direct metric comparisonではさらに:

- same dataset_version_id
- same TEST-row identity/hash
- same metric definition

Causalはtreatment / outcome / estimand / target populationをsemantic keyとする。

same-dataは同一immutable `dataset_version_id`。

warning code:

`EXPLORATORY_REUSE_SAME_DATA`

non-blocking。

### 4.5 PF-D2-05 — Command Idempotency & Retry-safe Artifact Commit

対象:

- `FR-114b`
- `FR-082`
- `NFR-006b`

Requirement intent:

- 全POSTではなくduplicate durable side effectを生成し得るCommandを対象にする。
- scopeは`(project_id, command_scope, idempotency_key)`。
- missing required key: `IDEMPOTENCY_KEY_REQUIRED`
- same key + different request: HTTP 409 / `IDEMPOTENCY_CONFLICT`
- exactly-once executionは保証しない。
- retry/restartでsuccessful Stage outputのdurable Artifactを重複materializeしない。

### 4.6 PF-D2-06 — Project Authorization & Sensitive Output Boundary

対象:

- `FR-121`
- `FR-123a`
- `FR-124b`
- `NFR-008b`
- `AR-020`

Persisted role:

- OWNER
- EDITOR
- VIEWER

Requirement intent:

- READ: OWNER/EDITOR/VIEWER
- WRITE/MUTATE: OWNER/EDITOR
- membership admin: OWNER only
- explicit sensitive output: OWNER/EDITOR
- prediction/local explanation rowをpotentially sensitive outputとして扱う。
- independent EXECUTE roleを追加しない。

### 4.7 PF-D2-07 — Canonical Lineage Completion

対象:

- `FR-008`
- `FR-054`
- `FR-095`
- `NFR-002`

Read model minimum chain:

```text
ResearchContextVersion
  ↓
AnalysisSpecification
  ↓
ExecutionPlan
  ↓
Execution
  ↓
StageExecution
  ↓
Result
  ↓
Artifact
```

加えてDatasetVersion / AnalysisView / GraphVersion / input Result / base Executionを接続する。

deterministic structural relationをgeneric LineageEdgeへ重複persistしない。

### 4.8 PF-D2-08 — Reproducibility Metadata Completion

対象:

- `FR-086a`
- `FR-087b`
- `NFR-001b`

Requirement intent:

- stochastic Stageのactual seedをStageAttempt単位で保存する。
- `StageAttempt.effective_random_seed: int | null`
- retryでは同じlogical Stage seedを再利用する。
- runtime_version_jsonへcode/python/platform/machine/scientific library versionsを保存する。
- bit-for-bit numerical identityではなくenvironment再構築情報を要件とする。

### 4.9 PF-D2-09 — Frontend Deep Navigation, Action State & Accessibility

対象:

- `FR-108`
- `FR-107`
- `FR-109`
- `FR-111`
- `NFR-012`

Resource deep route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

Async state:

`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`

E5変更surfaceでkeyboard/focus/accessible name/error association/non-color semantics/contrast thresholdを満たす。

### 4.10 PF-D2-11 — Documentation Self-containment

対象:

- `NFR-019`

`10/21/22/23/30`だけでcurrent + E5 target contractを理解可能にする。

NFR-019はPhase I改訂後、`DOC-019-01〜08`を再監査しall PASSになるまで未達とする。

## 5. Family / Navigation Requirements

既存ENH-E5 targetとして追加済みのFamily/Navigation Requirement群は維持する。

- `FR-129〜FR-139`: Family / Navigation Stage / route / global surface boundary
- `FR-140〜FR-143`: Navigation / Runtime separation
- `FR-144〜FR-145`: Capability ownership
- `FR-146〜FR-148`: Exploratory
- `FR-149〜FR-152`: Predictive
- `FR-153〜FR-156`: Causal
- `FR-157〜FR-162`: compatibility / persistence / route / scope boundary

これらはPhase G PF-D2-11のexact Navigation architectureと矛盾しないようPhase Iで本文を更新する。

## 6. D3 Deferred Requirements

以下はENH-E5では実装しない。正本から削除してはならない。

| Decision Item | Deferred requirement | TD |
|---|---|---|
| FR-021 | sensitive/use-restriction/description column metadata | TD-006 |
| FR-028 | correlation / association matrix operation | TD-007 |
| FR-062 | automated hyperparameter selection | TD-008 |
| FR-110b | dataset/context/date filter expansion | TD-010 |
| FR-118 | Product submit/poll CLI | TD-009 |
| FR-122 | general operational audit trail | TD-001 |
| FR-126 | configurable retention/deletion policy | TD-002 |
| FR-127b | DB/Worker/ArtifactStore component readiness | TD-011 |
| FR-128b | operational size/timeout configuration | TD-004 |
| NFR-004 | general p95 API SLO/performance regression gate | TD-012 |
| NFR-017 | explicit upload/row/column/memory/timeout hard limits | TD-004 |
| NFR-020b | object-storage adapter/switching | TD-005 |
| FR-025b | joint missing-pattern analysis | TD-007 |
| FR-026b | full scatter/box/crosstab surface set | TD-007 |
| FR-086b | per-stage timeout/resource limit persistence | TD-004 |
| FR-120b | systematic canonical schema-example synchronization | TD-013 |
| FR-123b | configurable exposure policy based on sensitive metadata | TD-006 |
| NFR-007 | metadata/artifact cross-store compensation | TD-014 |
| NFR-008c | production-grade authentication/security hardening | TD-015 |
| NFR-009b | configurable prediction/local-explanation/export minimization | TD-006 |
| NFR-010b | explicit restart/resume semantics | TD-017 |
| NFR-011b | comprehensive structured logging + metrics | TD-018 |

Design-only D3 (`D10-005c`, `D10-006a`, `D10-006b`, `D22-003b`, `D22-013c`, `D30-018c`)は04/21/22/23/30からENH-E5 current targetを除外し90へtraceする。

## 7. Logical splitを維持するRequirement

次は単一IDのstatementをcurrent baselineとfuture/targetへ論理分割して扱う。Phase Iで再結合して曖昧化しない。

- `FR-110a / FR-110b`
- `FR-114a / FR-114b`
- `FR-127a / FR-127b`
- `FR-128a / FR-128b`
- `NFR-020a / NFR-020b`
- `FR-025a / FR-025b`
- `FR-026a / FR-026b`
- `FR-086a / FR-086b`
- `FR-087a / FR-087b`
- `FR-120a / FR-120b`
- `FR-123a / FR-123b`
- `FR-124a / FR-124b`
- `NFR-001a / NFR-001b`
- `NFR-006a / NFR-006b`
- `NFR-008a / NFR-008b / NFR-008c`
- `NFR-009a / NFR-009b`
- `NFR-010a / NFR-010b`
- `NFR-011a / NFR-011b`

## 8. 廃止するRequirement表現

Requirement本文から次を除去する。

- 「ENH-E4ではMUSTではない」「今回はMUST」等の時点依存表現
- current実装に存在しないcapabilityをIMPLEMENTEDと読める表現
- D3をcurrent targetとして読める表現
- 「既存設計参照」「E4参照」「G00で決める」等の外部normative delegation
- Navigation Stage = Execution Stageを示唆する表現
- Navigation stateのDB/AnalysisSpecification persistenceを要求する表現
- Predictive既存field削除/rename/default semantics変更を許容する表現

## 9. Acceptanceへの接続

Phase IでRequirementsをcanonical snapshotへ反映した後:

```text
10
 ↓
21 / 22 / 23 / 30
 ↓
NFR-019 re-audit
 ↓ PASS
06 / Pxx
07
```

Execution Agentが本planning文書やpreflightを直接読んでscopeを補完する運用は行わない。
