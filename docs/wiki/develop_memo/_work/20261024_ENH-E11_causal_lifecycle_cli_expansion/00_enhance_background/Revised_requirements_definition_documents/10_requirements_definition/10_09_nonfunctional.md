<!-- ENH-E11 split working copy: not a formal approval. -->
# 10 — nonfunctional

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [10_requirements_definition.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/10_requirements_definition.md) · blob `40b83f29c67b4a39f6db5393be7534c5e892d656`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 6. 非機能要件

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-001a | 再現性 | current snapshot、code/runtime metadata、seed、schema identity等の再現性情報を保持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-001b | 再現性 | actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-002 | 追跡可能性 | canonical lineage read modelでResearchContextVersion→AnalysisSpecification→ExecutionPlan→Execution→StageExecution→Result→Artifactを追跡し、DatasetVersion/AnalysisView/GraphVersion/input Result/base Executionも接続する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-003 | 決定性 | Canonical JSONとhash生成はfield順やprocessに依存しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-004 | 応答性能 | 通常一覧・詳細APIの95 percentile 2秒等のgeneral performance SLOとregression gateを定義する | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-005 | 拡張性 | 新Analysis Familyを既存Executor変更なしにRegistry追加できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-006a | 信頼性 | current claim/lease/retry mechanicsでExecution/Stage lifecycleを安全に再試行できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-006b | 信頼性 | retry/restartでsuccessful Stage outputのduplicate durable Artifact materializationを防止する。exactly-once executionは保証しない | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-007 | 整合性 | Metadata transactionとArtifact writeのcross-store failure compensationを定義する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-008a | 安全性 | current input validation、path traversal防止、secret非露出等のsafeguardを維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-008b | 安全性 | 全project-scoped routeへProjectMembership authorizationを一貫適用する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-008c | 安全性 | production-grade authentication/security hardeningを完成させる | — | DEFERRED | PARTIAL | FUTURE |
| NFR-009a | Privacy | current sensitive Result suppressionを維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-009b | Privacy | prediction/local explanation/exportのconfigurable minimization policyを提供する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-010a | 可用性 | API processとWorker processを分離するcurrent deployment boundaryを維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-010b | 可用性 | Worker restart後の明示的resume/recovery semanticsを定義する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-011a | 観測性 | current request/execution/stage correlation identifiersをlogへ出力する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-011b | 観測性 | comprehensive structured logging、metrics、operational telemetryを提供する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-012 | Accessibility | current surfaceの主要操作をkeyboardで実行でき、focus/name/error/non-color/contrast semanticsを満たす | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-013 | Schema evolution | schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-014 | 互換性 | `causal-analysis-spec/2`の正規contractおよび保存済みCausal Resultをschema versionに従って読取可能に保つ | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-015 | Testability | Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-016 | Scientific transparency | 仮定、warning、negative result、limitationを省略せず表示する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-017 | Resource control | upload size、row/column count、memory、timeout等にexplicit operational hard limitを定義する | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-018 | Dependency direction | Product DomainからWeb Framework、ORMおよびlegacy packageへ依存しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-019 | Documentation | `00/10/21/22/23/30`だけでcurrent product concept / requirement / logical model / design / interface contractを自己完結して理解できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-020a | 移植性 | Artifact storageを`ArtifactStore` Port abstraction越しに利用する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-020b | 移植性 | Local filesystemに加えobject storage adapterを提供し、Port越しに切替可能にする | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-021 | Navigation separation | Navigation concernの変更がruntime execution lifecycleへ不要に伝播しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-022 | Navigation determinism | 同一Project / Family / Stage routeは同一navigation stateへdeterministicに復元される | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-023 | Maintainability | Family-specific Navigation Stage catalogをCapability ownershipで局所化する | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| NFR-024 | Testability | Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-025 | Portability | CLI / library executionがWeb UI route、tab/sidebar state、NavigationStageDescriptorへ依存しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-026 | Accessibility | Current Family / Stageを色だけでなくsemantic active state、label、focus等でも識別できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-027 | Performance | navigation metadata取得・renderingがanalysis executionのcritical pathへ不要なI/Oまたはblocking dependencyを追加しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-028 | Dependency isolation | optional analytical engineのimport/availability failureをcore process startup failureへ伝播させず、capability discovery/selection時に局所化してstable unavailable state/errorとして報告する | — | ACTIVE | IMPLEMENTED | ENH-E10 |
