# ENH-E5 Remediation Decision Log
> **Authority:** 本書はpreflight analysisの意思決定記録であり、Coding/Test Agent向けnormative contractではない。実装仕様は10/21/22/23/30を経て06/Pxxへ、verification requirementは07へ収束させる。
## 1. Decision taxonomy

- **D1 CURRENT_IMPLEMENTATION**: ENH-E4完了実装をcurrent contractとして採用し、文書を実装へ整合させる。
- **D2 E5_TARGET_CHANGE**: E4 targetまたは監査で特定した不足contractをENH-E5変更対象へ昇格する。
- **D3 DEFER**: targetの方向性は保持するがENH-E5では実装せず、将来planning ledgerへ送る。
## 2. Confirmed decisions

### Domain Ownership / Lifecycle

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-002 | FR-002 | **D1** | Project / ResearchContextVersion responsibility ownership | BASELINE |  |
| D10-004 | D10-004 | **D1** | StageExecution CANCELLED transitions | BASELINE |  |

**Rationale summary**

- `FR-002`: Projectのcurrent field ownershipを正とし、decision_contextはResearchContextVersion側の正本として文書を訂正する。
- `D10-004`: sourceで成立するCANCELLED transitionを文書へ反映する純粋なdocumentation drift correction。

### AnalysisView Typed Validation

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-015 | FR-015 | **D2** | AnalysisView filter operator/value × column logical type compatibility validation | ENH-E5 |  |
| D21-005 | D21-005 | **D2** | AnalysisView typed filter constraint | ENH-E5 |  |

**Rationale summary**

- `FR-015`: 既存validatorの局所的なtyped-validation gapをENH-E5で補完する。
- `D21-005`: FR-015と同一root decision。

### Exploratory / Dataset Workflow

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-020 | FR-020 | **D2** | Explore filter/chart state → AnalysisView draft handoff | ENH-E5 |  |
| FR-028 | FR-028 | **D3** | Correlation / association matrix operation | FUTURE | TD-007 |
| FR-032 | FR-032 | **D2** | Exploratory Result → Causal/Predictive AnalysisSpecification draft | ENH-E5 |  |
| FR-011 | FR-011 | **D1** | DatasetVersion registration metadata/profile semantics | BASELINE |  |
| FR-025a | FR-025 | **D1** | Column missingness | BASELINE |  |
| FR-025b | FR-025 | **D3** | Joint missing-pattern analysis | FUTURE | TD-007 |
| FR-026a | FR-026 | **D1** | Existing association/bivariate capability | BASELINE |  |
| FR-026b | FR-026 | **D3** | Full scatter/box/crosstab surface set | FUTURE | TD-007 |
| FR-034 | FR-034 | **D2** | Persist analysis-significant rendering/aggregation/sampling parameters | ENH-E5 |  |

**Rationale summary**

- `FR-020`: Exploratoryから再利用可能なAnalysisView draftへのworkflow continuityをENH-E5で成立させる。
- `FR-028`: Exploratory analytical surface拡張でありENH-E5成立条件ではない。
- `FR-032`: Family間handoffをENH-E5で明示的に成立させる。
- `FR-011`: registration時のbasic profile必須化を撤回しcurrent schema/shape/hash contractを正本とする。
- `FR-025a`: 現実装の列別missingnessをcurrent contractとして維持する。
- `FR-025b`: 追加Exploratory analytical capabilityとして延期する。
- `FR-026a`: 現実装で成立しているassociation capabilityを正本とする。
- `FR-026b`: 追加visualization surfaceはfutureへ送る。
- `FR-034`: Findings/handoffの再構成可能性のため分析意味を変える条件を保存する。

### Security / Privacy

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-021 | FR-021 | **D3** | Sensitive/use-restriction/description column metadata | FUTURE | TD-006 |
| FR-123a | FR-123 | **D2** | Project authorization across preview/artifact/prediction output | ENH-E5 |  |
| FR-123b | FR-123 | **D3** | Configurable exposure policy based on sensitive metadata | FUTURE | TD-006 |
| NFR-008a | NFR-008 | **D1** | Existing input validation/path safeguards | BASELINE |  |
| NFR-008b | NFR-008 | **D2** | Project authorization coverage | ENH-E5 |  |
| NFR-008c | NFR-008 | **D3** | Production-grade authentication/system security hardening | FUTURE | TD-015 |
| NFR-009a | NFR-009 | **D1** | Existing sensitive Result suppression | BASELINE |  |
| NFR-009b | NFR-009 | **D3** | Configurable prediction/local-explanation/export minimization | FUTURE | TD-006 |
| AR-020 | AR-020 | **D2** | Treat local explanation/prediction row as potentially sensitive output | ENH-E5 |  |

**Rationale summary**

- `FR-021`: 合理的な将来targetだが、data-use policy全体へ波及するためENH-E5では延期する。
- `FR-123a`: 既存Project authorization boundaryをsensitive output surfaceへ一貫適用する。
- `FR-123b`: FR-021のfuture governance targetと統合して延期する。
- `NFR-008a`: current実装で確認されたsecurity safeguardsを正本とする。
- `NFR-008b`: Authorization root decisionを継承する。
- `NFR-008c`: 独立security enhancementとして延期する。
- `NFR-009a`: current sensitive-output suppressionを正本として維持する。
- `NFR-009b`: data-use/sensitive-output governance future targetへ統合する。
- `AR-020`: row-level outputを既存authorization/sensitive boundaryへ載せる。

### Predictive / Causal Capability Boundaries

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-062 | FR-062 | **D3** | Automated hyperparameter selection | FUTURE | TD-008 |
| FR-048 | FR-048 | **D1** | Estimator-applicable causal diagnostics | BASELINE |  |

**Rationale summary**

- `FR-062`: 独立したmodel selection capability拡張でありENH-E5では延期する。
- `FR-048`: 全estimatorへ同一diagnostic setを強制せず適用可能なdiagnosticを生成するcurrent capability modelを正とする。

### Predictive Subgroup Evaluation

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-067 | FR-067 | **D2** | Subgroup performance + sample size | ENH-E5 |  |
| AR-016 | AR-016 | **D2** | Subgroup metric uncertainty | ENH-E5 |  |

**Rationale summary**

- `FR-067`: evaluation_spec.subgroupsをsemantic no-opにせず既存evaluate contractを完成させる。
- `AR-016`: subgroup metricの誤解を防ぐためsample sizeとuncertaintyを一体で提供する。

### Canonical Result / Artifact / Schema Contract

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-090 | FR-090 | **D1** | Canonical Result ownership/descriptor contract | BASELINE |  |
| FR-092 | FR-092 | **D1** | Canonical Artifact descriptor/ownership contract | BASELINE |  |
| NFR-013 | NFR-013 | **D1** | Versioning at contract boundaries rather than generic field on every entity | BASELINE |  |
| FR-068 | FR-068 | **D1** | Result vs Artifact responsibility for predictive outputs | BASELINE |  |

**Rationale summary**

- `FR-090`: family/schema_version/stageの一律direct ownershipを撤回しcurrent canonical Result modelへ訂正する。
- `FR-092`: family/schema_versionの一律direct ownershipを撤回しcurrent Artifact contractへ訂正する。
- `NFR-013`: 各versioned contract境界でversionを識別するcurrent modelを正とする。
- `FR-068`: model/preprocessor/prediction等のArtifactとmetric/error等のResult payload責務をcurrent canonical modelとして採用する。

### Frontend Navigation / UI State / Accessibility

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-108 | FR-108 | **D2** | Direct/deep resource navigation | ENH-E5 |  |
| FR-110a | FR-110 | **D1** | Existing results filters (family/type/status等) | BASELINE |  |
| FR-110b | FR-110 | **D3** | Dataset/context/date filter expansion | FUTURE | TD-010 |
| FR-118 | FR-118 | **D3** | Product submit/poll CLI | FUTURE | TD-009 |
| FR-107 | FR-107 | **D2** | Backend-authoritative action availability / rejection reason | ENH-E5 |  |
| FR-109 | FR-109 | **D2** | Async UI state taxonomy loading/empty/partial/error/cancel | ENH-E5 |  |
| FR-111 | FR-111 | **D2** | Keyboard/focus/label/contrast accessibility | ENH-E5 |  |
| NFR-012 | NFR-012 | **D2** | Keyboard + non-color state accessibility | ENH-E5 |  |

**Rationale summary**

- `FR-108`: ENH-E5のnavigation architecture改修へ直接含める。
- `FR-110a`: 現実装で成立しているfilter capabilityをcurrent contractとして記述する。
- `FR-110b`: 追加検索surfaceはENH-E5成立条件ではない。
- `FR-118`: current scientific CLIを維持しProduct orchestration CLIは将来拡張へ送る。
- `FR-107`: 新Family/Stage UIでfrontend独自推測を避けるため統一する。
- `FR-109`: ENH-E5 UI改修の直接領域としてstate semanticsを統一する。
- `FR-111`: 新UI surfaceで基本accessibility acceptanceを完成させる。
- `NFR-012`: FR-111と同一root decision。

### Command Idempotency

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-114a | FR-114 | **D1** | Create APIであること自体をidempotency applicability基準にする要求 | BASELINE |  |
| FR-114b | FR-114 | **D2** | Idempotency-required Command APIでIdempotency-Keyを受理 | ENH-E5 |  |
| FR-082 | FR-082 | **D2** | Command idempotency semantics/coverage | ENH-E5 |  |

**Rationale summary**

- `FR-114a`: HTTP createか否かではなく重複side effectリスクを基準にRequirementを訂正する。
- `FR-114b`: 既存mechanismのcoverageを必要なCommandへ統一する。
- `FR-082`: FR-114bと同一root decision。

### Audit / Retention

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-122 | FR-122 | **D3** | General operational audit trail | FUTURE | TD-001 |
| FR-126 | FR-126 | **D3** | Configurable retention/deletion policy | FUTURE | TD-002 |
| D10-006a | D10-006 | **D3** | General Audit contract | FUTURE | TD-001 |
| D10-006b | D10-006 | **D3** | Retention/deletion contract | FUTURE | TD-002 |

**Rationale summary**

- `FR-122`: 要求方向は合理的だが横断audit基盤となるためENH-E5では延期する。
- `FR-126`: 要求方向は合理的だが独立したretention/deletion policy設計が必要。
- `D10-006a`: FR-122と同一root decision。
- `D10-006b`: FR-126と同一root decision。

### Operability / Health / Performance

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-127a | FR-127 | **D1** | Existing basic health endpoint | BASELINE |  |
| FR-127b | FR-127 | **D3** | DB/Worker/Artifact Store component readiness | FUTURE | TD-011 |
| NFR-004 | NFR-004 | **D3** | General p95 API SLO / performance regression gate | FUTURE | TD-012 |

**Rationale summary**

- `FR-127a`: 現存するbasic health contractのみcurrent contractとして記述する。
- `FR-127b`: component readinessは独立operability enhancementとして延期する。
- `NFR-004`: benchmark environment等を伴う独立performance workとして延期する。

### Resource Configuration / Resource Control

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-128a | FR-128 | **D1** | Registry-based Algorithm / Runner management | BASELINE |  |
| FR-128b | FR-128 | **D3** | Operational size/timeout configuration | FUTURE | TD-004 |
| NFR-017 | NFR-017 | **D3** | Explicit upload/row/column/memory/timeout hard limits | FUTURE | TD-004 |
| FR-086b | FR-086 | **D3** | Per-stage timeout/resource limit persistence | FUTURE | TD-004 |

**Rationale summary**

- `FR-128a`: current registry/capability resolutionを正本とし外部config loadingをmandatory contractとしない。
- `FR-128b`: resource policyの独立設計が必要なため延期する。
- `NFR-017`: 包括的resource control/sandbox設計が必要。
- `FR-086b`: resource control decisionへ統合して延期する。

### Storage Portability

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| NFR-020a | NFR-020 | **D1** | ArtifactStore Port abstraction | BASELINE |  |
| NFR-020b | NFR-020 | **D3** | Object-storage adapter / switching | FUTURE | TD-005 |
| D22-003a | D22-003 | **D1** | Current implemented Port/Adapter boundary | BASELINE |  |
| D22-003b | D22-003 | **D3** | Object-storage / broader adapter variants | FUTURE | TD-005 |

**Rationale summary**

- `NFR-020a`: current ArtifactStore Port abstractionを正本として維持する。
- `NFR-020b`: Portは成立済みだがobject-storage adapterは独立deployment enhancementとして延期する。
- `D22-003a`: sourceで確認されたLocalArtifactStore/scientific-core等の境界だけをcurrent designに記載する。
- `D22-003b`: future storage portabilityへ送る。

### Scientific Comparability / Exploratory-to-Confirmatory Guard

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| AR-017 | AR-017 | **D2** | Semantic result comparability | ENH-E5 |  |
| FR-051 | FR-051 | **D2** | Prior exploratory use warning before confirmatory estimation | ENH-E5 |  |
| FR-072 | FR-072 | **D2** | Predictive comparison semantic guard | ENH-E5 |  |
| AR-004 | AR-004 | **D2** | Same-data exploratory→confirmatory warning + lineage | ENH-E5 |  |

**Rationale summary**

- `AR-017`: same family/typeだけでなくTask/Estimand/Outcome等のsemantic comparability guardを完成させる。
- `FR-051`: 探索後推論guardをFamily handoffと一貫して完成させる。
- `FR-072`: AR-017と同一root decision。
- `AR-004`: FR-051と同一root decision。

### Authorization Model

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| D10-005a | D10-005 | **D1** | Project role taxonomy OWNER/EDITOR/VIEWER | BASELINE |  |
| D10-005b | D10-005 | **D2** | Uniform Project-scoped authorization across routers | ENH-E5 |  |
| D10-005c | D10-005 | **D3** | Distinct Operator / system-operate authorization | FUTURE | TD-003 |
| FR-121 | FR-121 | **D2** | Uniform Project-scoped authorization | ENH-E5 |  |
| FR-124a | FR-124 | **D1** | Existing project-scoped artifact download + safe content disposition | BASELINE |  |
| FR-124b | FR-124 | **D2** | Uniform artifact-route authorization coverage | ENH-E5 |  |

**Rationale summary**

- `D10-005a`: persisted current role taxonomyを正本とする。
- `D10-005b`: 既存ProjectMembership authorization boundaryの適用漏れをENH-E5で解消する。
- `D10-005c`: system-level operator modelは独立security/operations enhancementとして延期する。
- `FR-121`: D10-005bと同一root decision。
- `FR-124a`: 現実装で成立しているdownload contractを正本とする。
- `FR-124b`: D10-005b/FR-121と同一root decision。

### Architecture / API Documentation Correction

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| D22-001 | D22-001 | **D1** | Outbox as current runtime component | BASELINE |  |
| D22-002 | D22-002 | **D1** | Runner/Auth/Event Ports as current implemented Ports | BASELINE |  |
| FR-120a | FR-120 | **D1** | OpenAPI generated from runtime API schema | BASELINE |  |
| FR-120b | FR-120 | **D3** | Systematic canonical schema-example synchronization | FUTURE | TD-013 |

**Rationale summary**

- `D22-001`: current implementationに存在しないOutboxをcurrent architectureから除去する。
- `D22-002`: sourceで確認されたPort setだけをcurrent architectureに記載する。
- `FR-120a`: current FastAPI OpenAPI generationを正本として維持する。
- `FR-120b`: 全exampleの同期/検証基盤はENH-E5のdirect dependencyではない。

### Reproducibility / Execution Snapshot

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-007 | FR-007 | **D1** | Execution context snapshot semantics | BASELINE |  |
| FR-086a | FR-086 | **D2** | Effective random seed persistence for stochastic stages | ENH-E5 |  |
| FR-087a | FR-087 | **D1** | Code/runtime/schema snapshot metadata | BASELINE |  |
| FR-087b | FR-087 | **D2** | Effective library version capture | ENH-E5 |  |
| NFR-001a | NFR-001 | **D1** | Current reproducibility snapshot/code/runtime metadata | BASELINE |  |
| NFR-001b | NFR-001 | **D2** | Seed/library-environment reproducibility coverage | ENH-E5 |  |

**Rationale summary**

- `FR-007`: 完全なResearchContext object複製を必須にせずcurrent immutable references/snapshot metadataを正本とする。
- `FR-086a`: 再現性の直接入力であるeffective seedを保存する。
- `FR-087a`: current execution snapshot metadataを正本とする。
- `FR-087b`: 再現性coverageを完成させるためlibrary environmentを明示記録する。
- `NFR-001a`: 現実装で成立する再現性metadataを正本とする。
- `NFR-001b`: FR-086a/FR-087bの上位NFRとしてcoverageを完成させる。

### Lineage / Traceability

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| FR-008 | FR-008 | **D2** | Canonical Context usage index to Analysis/Result | ENH-E5 |  |
| FR-054 | FR-054 | **D2** | Causal upstream lineage completeness | ENH-E5 |  |
| FR-095 | FR-095 | **D2** | Result lineage to Context/Dataset/View/Spec/Plan/Stage/Artifact | ENH-E5 |  |
| NFR-002 | NFR-002 | **D2** | Complete Result traceability to Project/Context/Dataset/Spec/Execution/Artifact | ENH-E5 |  |

**Rationale summary**

- `FR-008`: 既存lineage/read-modelを拡張しContext usageのtraceabilityを完成させる。
- `FR-054`: Question/Design/Graph/Eligibility/upstream Resultへの意味的traceabilityを完成させる。
- `FR-095`: 既存lineageをSpec/Plan/Stage chainまで完成させる。
- `NFR-002`: FR-008/054/095と整合してtraceabilityを完成させる。

### Worker Reliability / Consistency / Observability

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| NFR-006a | NFR-006 | **D1** | Current lease/claim/retry mechanics | BASELINE |  |
| NFR-006b | NFR-006 | **D2** | Idempotent Artifact commit across retry/restart | ENH-E5 |  |
| NFR-007 | NFR-007 | **D3** | Metadata/Artifact cross-store failure compensation | FUTURE | TD-014 |
| NFR-010a | NFR-010 | **D1** | API/Worker process separation | BASELINE |  |
| NFR-010b | NFR-010 | **D3** | Explicit restart/resume semantics | FUTURE | TD-017 |
| NFR-011a | NFR-011 | **D1** | Existing request/execution/stage logging identifiers | BASELINE |  |
| NFR-011b | NFR-011 | **D3** | Comprehensive structured logging + metrics | FUTURE | TD-018 |

**Rationale summary**

- `NFR-006a`: current worker lease/claim/retry contractを正本とする。
- `NFR-006b`: 再実行時の重複副作用防止をENH-E5で補完する。
- `NFR-007`: 独立したcross-store compensation protocolとして延期する。
- `NFR-010a`: current process separationを正本とする。
- `NFR-010b`: 独立worker reliability enhancementとして延期する。
- `NFR-011a`: current logging contextを正本とする。
- `NFR-011b`: observability overhaulとして延期する。

### Test Architecture

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| D22-013a | D22-013 | **D1** | Existing core test architecture | BASELINE |  |
| D22-013b | D22-013 | **D2** | Verification surfaces for D2 requirements | ENH-E5 |  |
| D22-013c | D22-013 | **D3** | Verification surfaces owned by D3 requirements | FUTURE |  |
| D30-018a | D30-018 | **D1** | Existing detailed contract tests | BASELINE |  |
| D30-018b | D30-018 | **D2** | Detailed verification for D2 requirements | ENH-E5 |  |
| D30-018c | D30-018 | **D3** | Detailed verification owned by D3 requirements | FUTURE |  |

**Rationale summary**

- `D22-013a`: current domain/workflow/API/scientific testsを正本として記述する。
- `D22-013b`: 今回D2としたRequirementのverificationを07へ追加するderived decision。
- `D22-013c`: D3へ送ったcapabilityのacceptanceをENH-E5に要求しないderived decision。
- `D30-018a`: current verified test seamsを正本として記述する。
- `D30-018b`: D2 requirementsに必要なtest seamsを30/07へ追加するderived decision。
- `D30-018c`: D3 scopeのtest targetはENH-E5から外すderived decision。

### NFR-019 Documentation Self-Containment

| Decision Item | Source | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|---|
| NFR-019 | NFR-019 | **D2** | Documentation self-containment | ENH-E5 |  |

**Rationale summary**

- `NFR-019`: 現行v5はPARTIAL_MATCH/FAIL。正本文書10/21/22/23/30だけでcurrent+E5 targetを理解可能にするdocumentation remediationを行う。

## 3. Unresolved planning decisions before Coding contract freeze

- Subgroup uncertainty contract: estimator / interval / confidence level / undefined-metric handling.
- Idempotency: mutation/command inventory, applicability matrix, scope, same-key/same-body, same-key/different-body, transaction/concurrency semantics.
- Authorization: endpoint/action matrix for OWNER/EDITOR/VIEWER and exact mutation semantics.
- Semantic comparability: Family別comparability keyとincompatible comparison error/warning semantics.
- Reproducibility: stochastic seed capture scope and library/environment version capture contract.
- Lineage: canonical trace path/read-model for Context/Spec/Plan/Stage/upstream Result.
- FR-034: persistence対象とするanalysis-significant rendering/aggregation/sampling parameters.
- NFR-006b: retry/restart時のArtifact commit idempotency/commit boundary.

## 4. Downstream rule

D1/D2/D3は本書で履歴を保持するが、Agentは本書から仕様を補完してはならない。D2の未確定事項はpreflightでfreezeし、10/21/22/23/30へ反映した後、NFR-019をPASSさせてから06/Pxx・07へ収束する。
