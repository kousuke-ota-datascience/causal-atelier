# 06 Target Architecture Decision Record

## 1. Metadata

- Prompt: `06_target_architecture_decision_record_prompt.md`
- 前Phase: Architecture Review Phase 01–05、database reinitialization completion decision record
- Repository: `/loc0/bigbrother/repositories/causal-atelier`
- Branch: `refactor/ariadne_mvp_e4`
- HEAD: `a2d499c19e19df16caa7900c1c080743ea702532`
- 調査開始時のworking tree: 既存の ` D deploy/.nfs000000000076202f00000088`、Phase 06 promptは未追跡
- 開始時刻: `2026-08-08T11:24:00Z`
- 終了時刻: `2026-08-08T11:29:00Z`
- Status: `COMPLETED_WITH_HUMAN_DECISIONS`
- 方法: production source、schema、migration、前Phase結果、database decision recordの静的統合。production/schema/test/codeは変更していない。

## 2. Executive Decision Summary

### Recommended Target Architecture

user-visibleなCausal、Exploratory、Predictive分析について、repository-managed Product runtimeのpersistent Executionを一つのcanonical Execution aggregateへ統合する。

共通化するもの:

- `execution_id` とExecution identity
- state、claim、lease、transaction境界
- retry/rerun/revise/cancel semantics
- Result、Artifact、Lineageのownership boundary

一方、scientific workflowの差異は、Execution family discriminator、workflow specification/plan、persistent StageExecution、family-specific runner adapterで保持する。

推奨するauthority分割:

- Execution: 一つのProduct aggregateと一つのlifecycle contract
- StageExecution: canonical workflow全てのfirst-class persistent child
- Result: ExecutionResultとStageResultを意味的に区別しつつ、一つのownership contractで管理
- Artifact metadata: 一つのProduct metadata ownership boundary
- physical Artifact: `ArtifactStorePort`へ委譲
- Lineage: typed persistent relationは構造関係のauthority、generic edgeはtypedで表せない明示関係のauthority、closureはread projection
- legacy runtime/persistence/orchestration: non-canonical。外部利用確認後にbounded retirement/archiveを提案
- shared scientific modules: legacy runtimeとは分離して維持

### Decisions Requiring Human Approval

- unified Product Execution aggregateとpersistent StageExecution contract
- Result/Artifact統合の境界、新metadata tableをENH-E4に含めるか
- generic-only LineageEdge authority policy
- legacy external compatibility assumptionとretirement/archive境界
- Product-only migration/bootstrapをclean-installのtargetとすること

### Decisions Blocked by Evidence

Product targetの核心Decisionはblockedではない。legacy source removalは外部consumerが未確認のため条件付きでblockedである（E4-UNK-024..029）。したがって、本Recordはrepository-local targetと明示的なexternal compatibility gateを提案する。外部consumerが存在しないとは断定しない。

## 3. Current Architecture Problem Statement

### 3.1 Runtime

repository-managed runtimeはProduct API、Product worker、Product migration、Product scientific adapterで構成される。Product CLIはlocal scientific utilityとして別経路を持つ。legacy API/worker/CLIのsource rootは残るが、package/deployment surfaceから除外されている。

その結果、repositoryには複数runtime familyが存在する一方、active Product runtimeは一つだけである。

根拠: Phase 01/05、`pyproject.toml:19-64`、`.dockerignore:14-24`、`Dockerfile:10-20`、`compose.yaml:18-53`。

### 3.2 Execution

Causalは`ExecutionOrm`/`product_execution`、domain/repository UoW、Product worker branchを使う。Exploratory/Predictiveは`FamilyExecutionOrm`/`product_family_execution`、direct service session、family stage、別claim/mutation pathを使う。共有`GenericExecutor`はin-memory stage sequencing/runner infrastructureであり、lifecycle ownerではない。

帰結: user-visible Product analysisに複数のExecution identity、claimer、state mutation、retry semanticsがある。

根拠: Phase 02 E4-OBS-014..032。

### 3.3 Result / Artifact

Causalは`product_result`/`product_artifact`、Familyは`product_family_result`/`product_family_artifact`を使う。Causal Resultはexecution-scoped、Family Resultはexecution+stage-scoped、Family ArtifactはResultなしでも存在できる。repository/ORM persistence方式とretry cleanupも異なる。

帰結: 共通概念としての出力に一つのownership/mutation contractがない。

根拠: Phase 03 E4-OBS-033..041、E4-INF-013..018。

### 3.4 Lineage

Productにはtyped/derived reader、`product_lineage_edge`、hybrid closure、export-synthetic lineageがある。Family serviceはgeneric edgeを書くが、通常のCausal processingではgeneric writeが確認されない。同じsemantic relationがderived/persisted双方に表現され得るが、cross-source reconciliationは確認されない。

帰結: lineage authorityとduplicate representationが曖昧である。

根拠: Phase 04 E4-OBS-042..051、E4-INF-019..025。

### 3.5 Legacy

legacyにはAPI、CLI、execution/control plane、worker、Result/Artifact/ArtifactLineage persistence、旧infrastructureがある。Product/shared production codeから`ariadne.legacy`へのimportは確認されない。一方、`ariadne.causal`、preprocessing等のshared scientific moduleはProductとlegacy双方が利用する。

帰結: legacy orchestrationとshared scientific capabilityを別々に扱う必要がある。legacy directory全体を一括削除すると両者を混同する。

根拠: Phase 05 E4-OBS-052..063、E4-INF-026..032。

### 3.6 Migration

database reinitializationでは、pre-production application dataに保持要件がなく、`product_migrations`だけでProduct clean rebuildが成功した。active databaseはProduct tableのみで、startup後もlegacy migration stateは現れなかった。

帰結: clean target pathについてProduct-only bootstrapは証拠で支持される。ただし外部legacy database/consumerを破棄できることまでは証明しない。

根拠: `database_reinitialization/99_completion_summary_decision_record.md:40-44,183-217,288-371,756-813,1010-1038`。

## 4. Architectural Goals

1. user-visible Product analysisに一つのcanonical persistent Execution architectureを持つ。
2. Causal/Exploratory/PredictiveでExecution identityとlifecycle contractを共通化する。
3. lifecycle orchestrationとscientific workflow executionを分離する。
4. Execution-level/Stage-levelの意味を保った一つのResult/Artifact ownership contractを持つ。
5. physical object storageとmetadata ownershipを分離する。
6. semantic lineage relationごとに一つのauthority ruleを持つ。
7. Product Execution/Result/Artifact/Lineageの恒久的な二重authorityを除去する。
8. shared scientific implementationを保持し、legacy orchestrationをactive authorityにしない。
9. target Product schemaをProduct migration chainだけでbootstrapできる。
10. external compatibilityの仮定を明示し、期限・条件を付ける。

## 5. Non-goals

- scientific algorithm/statistical methodの再設計
- numerical correctnessの再検証
- frontend UXの再設計
- 無関係なdataset/auth/deploymentの再設計
- legacy sourceやhistorical migrationの即時削除
- retention requirementが別途承認されない限りのhistorical data migration
- generic plugin architecture
- agentによるADRの自動承認
- 本PhaseでのcodingやGateごとの実装

## 6. Decision Criteria

| Criterion | 意味 |
|---|---|
| Single Source of Truth | lifecycle/relationshipのauthorityが一つであること |
| Semantic Coherence | family/stageの意味を失わないこと |
| Lifecycle Consistency | claim/state/retry/cancelが共通contractであること |
| Persistence Consistency | aggregateとtransaction ownershipが明確なこと |
| Failure Correctness | failure/partial outputが決定的であること |
| Lineage Integrity | 独立した曖昧なauthorityがないこと |
| Auditability | identity、stage、result、artifact、lineageを追跡できること |
| Scientific Preservation | estimator/algorithmを変更しないこと |
| Migration Simplicity | clean bootstrapとdata policyが明確なこと |
| Operational Simplicity | repository-managed runtime familyが一つであること |
| Testability | family固有部分を含む共通contractを検証できること |
| Extensibility | 新familyが新lifecycleを増やさないこと |
| Compatibility Risk | 外部/legacy breakageを明示・gateできること |

## 7. Candidate Architecture Overview

### Candidate A — Causal Executionをcanonicalにする

`product_execution`とdomain/UoWを拡張してFamily execution/stageを吸収する。

### Candidate B — Family Executionをcanonicalにする

`product_family_execution`とdirect service modelを拡張してCausal semanticsを吸収する。

### Candidate C — 新しいunified Execution aggregate

family discriminator、common lifecycle/claim/state contract、persistent StageExecution childを持つ新canonical Product Execution aggregateを定義し、Causal/Family adapterをその背後に置く。

### Candidate D — 二つのpersistent lifecycleを役割明文化して維持する

`product_execution`と`product_family_execution`を独立authorityとして残す。

### Candidate E — external orchestrationのみを共通化する

common lifecycleを外部schedulerへ移し、domain-specific persistenceは複数維持する。

## 8. Candidate Comparison Matrix

| Criterion | A | B | C | D | E | 評価 |
|---|---|---|---|---|---|---|
| Execution authority | 大規模拡張後は可 | 大規模拡張後は可 | **強い** | 弱い | 不明 | Dはdual authorityを残す |
| family/stage fidelity | 弱〜可 | 可 | **強い** | 強い | 不明 | Cは差異を明示できる |
| common claim/state/retry | 可 | 可 | **強い** | 弱い | 不明 | 現状claimerが異なる |
| migration complexity | 可 | 可 | 弱い | 短期は強い | 弱い | Cは移行コスト最大 |
| Result/Artifact alignment | 可 | 可 | **強い** | 弱い | 不明 | Cはownership contractを定義できる |
| lineage authority | 可 | 可 | **強い** | 弱い | 不明 | 別Decisionが必要 |
| scientific preservation | 強い | 強い | **強い** | 強い | 不明 | shared moduleを維持可能 |
| operational simplicity | 可 | 可 | **強い** | 弱い | 弱い | Eはauthorityを増やす |
| testability | 可 | 可 | **強い** | 弱い | 不明 | 共通contractが検証しやすい |
| ENH-E4整合 | 可 | 可 | **強い** | 不可 | 不明 | Dはdual executionを解消しない |
| 推奨 | 不採用 | 不採用 | **推奨** | 却下 | scope外 | — |

Candidate Cを推奨する理由は、問題が単に「どちらのtableがきれいか」ではなく、二つのProduct lifecycle authorityがclaim、stage、result、lineage、mutation semanticsで異なることにある。新aggregateなら現行tableの偶然の境界に依存しないtarget contractを定義できる。移行コストは高いため、人間承認が必要である。

## 9. Recommended Target Architecture

### 9.1 Runtime

```text
Product API / Product CLI adapter
        ↓
Canonical Execution Application Service
        ↓
Canonical Execution repository + Unit of Work
        ↓
Canonical worker claim/lease
        ↓
Family-specific workflow adapter / scientific runner
```

legacy API/worker/CLIはnon-canonical runtime surfaceとする。shared scientific moduleはactive capabilityとして残す。

### 9.2 Execution

一つのcanonical persistent Execution aggregateを使用する。

- user-visible Product analysisごとにglobally uniqueな`execution_id`
- `CAUSAL`、`EXPLORATORY`、`PREDICTIVE`のfamily/type discriminator
- immutable submission/specification snapshot
- 共通state、claim token/lease、timestamp、retry count、terminal outcome
- family固有workflow specification/plan reference
- rerun/revise用のparent/base execution reference
- 一つのrepository/claim abstractionとUoW boundary

これは現行tableのどちらかをそのまま残すという意味ではなく、semantic contractをcanonicalにするという意味である。

### 9.3 Stage

全canonical Executionにpersistent StageExecution childを持たせる。stageにはworkflow固有stage key/type、ordinal/dependency、state、attempt history、timestamp、input/output binding、failure detailを持たせる。

現状ephemeralなCausal stageにも明示的なstage representationを与える。Family workflowは既存stage semanticsをcommon contractの背後に置く。

retry granularity、progress、auditability、Result ownership、failure recoveryに安定したstage boundaryが必要なため、StageExecutionをpersistent first-class entityとする。

### 9.4 Worker

canonical claim mechanismを一つにする。

- repository-level atomic claim
- storageに応じたrow lock/skip-locked相当
- claim tokenとlease expiry
- processing前のclaim commit
- family-neutral state transition
- claim後のfamily adapter dispatch
- terminal state/result/artifactを同じaggregate UoWでcommit
- 長時間処理にはheartbeat/lease renewal contract

Phase 02ではheartbeatの完全な挙動は未確認だが、target invariantとして必要である。

### 9.5 GenericExecutor

`GenericExecutor`はplan validation、stage ordering、binding resolution、runner invocation、in-memory stage outcomeに限定する。

claim、lease、execution identity、transaction commit、retry policy、Result/Artifact persistence、generic lineage authorityは所有しない。

### 9.6 Result

一つのResult ownership contractの下に、意味の異なる二つのlevelを明示する。

- ExecutionResult: canonical Executionに属するfinal/aggregate scientific output
- StageResult: persistent StageExecutionに属するstage scientific output

これは同一概念の重複実装ではなく、異なるsemantic levelである。level/type discriminator、stable ID、execution relation、必要な場合のstage relation、status/payload/diagnostics、cardinalityを明示する。APIはlevel metadata付きのunified Result resourceとして公開してよいが、persistence semanticsを曖昧にしない。

### 9.7 Artifact

Product Artifact metadata ownership contractを一つにする。

- Product-level Artifact metadata authority
- artifact IDとphysical `object_key`を分離
- canonical Execution associationを必須化
- Result/StageExecution associationはoptional
- kind/schema/hash/media/size/metadataを明示
- physical storeは`ArtifactStorePort`
- metadataのcreate/persist/link/deleteは一つのservice/aggregate boundaryが所有
- DBとphysical storeは別resourceであり、commit失敗時はcompensation/reconciliationを定義

Artifact-only stage outputはworkflow contractで明示的に許可する。

### 9.8 Downstream Reuse

canonical referenceはtyped Product IDとする。

- Result reuseはResult IDとtyped relation/role
- Artifact reuseはArtifact IDとmetadata/hash validation
- physical `object_key`はlocatorでありsemantic input identityではない
- DatasetVersion/GraphVersionはtyped domain reference
- family-to-causal reuseはtyped bridgeまたはnormalized input contractを使用する
- content hashはintegrity evidenceでありownership IDの代替ではない

### 9.9 Lineage

明示的なhybrid authority policyを採用する。

1. typed persistent relationshipで表現できるstructural relationはtyped relationをauthorityとする。
2. typed fieldで表現できないgeneric-only relationはgeneric persisted lineageをauthorityとする。
3. closureはread projectionでありauthorityではない。
4. structural relationをgeneric lineageへ独立writeすることをfinal stateでは許可しない。
5. generic-only edgeにはendpoint/project scope/uniqueness/deletion policyを定義する。
6. exportは各edgeがtyped-derivedかgeneric-persistedかを識別できるsnapshotとする。

これはexplicit hybridであり、indefinite dual writeではない。

### 9.10 Legacy

legacy runtime/persistence/orchestrationとshared scientific capabilityを分離する。

- legacy API/CLI/worker: Product runtimeとして`RETIRE_RUNTIME`
- legacy orchestration/domain/persistence/lineage: external compatibility gate後に`ARCHIVE_SOURCE`または`REPLACE_BEFORE_RETIRE`
- `ariadne.causal`、`ariadne.preprocessing`、`ariadne.shared`: independent shared capabilityとして保持
- historical migration: 別Decisionまでarchive/historyとして保持
- compatibility data string: 実際のcontractが必要な期間だけ保持
- “legacy”という名称だけでsourceを削除しない

### 9.11 Migration

canonical target bootstrapは`alembic_product.ini` → `product_migrations`とする。database reinitializationで、legacy migrationを実行せずProduct rebuildが成功した。

現状project contextはpre-productionでapplication-data retention requirementなしと記録している。そのためENH-E4のdefault policyはclean rebuildである。retention requirementが追加された場合は別のhuman-approved migration ADRとする。

### 9.12 CLI

low-level scientific utilityとして明示されたProduct CLIはpersistent Product Execution外に置く。

ただしuser-visibleでauditabilityを約束するCLI analysisはcanonical Execution serviceへsubmitする。CLIがsecond hidden orchestration architectureになってはならない。

## 10. Current Architecture Diagram

```text
Product API ────────┬─> Causal ExecutionService ─> product_execution
                    │                         └─> Product worker branch
                    ├─> ExploratoryService ──> product_family_execution
                    │                         └─> family stages/results/artifacts
                    └─> PredictiveService ───> product_family_execution
                                              └─> family stages/results/artifacts

GenericExecutor: shared in-memory stage sequencing/runner
Result: product_result OR product_family_result
Artifact: product_artifact OR product_family_artifact
Lineage: typed-derived + product_lineage_edge + hybrid closure
Legacy: separate API/CLI/worker/persistence/ArtifactLineage
Scientific: shared ariadne.causal/preprocessing modules
Migration: product_migrations(active) + root migrations(history)
```

## 11. Target Architecture Diagram

```text
Product API / promoted CLI
          │
          v
Canonical Execution Service
          │
          v
Canonical Execution Aggregate
 execution_id + family + state + claim/lease + snapshot
          │
          ├── persistent StageExecution children
          │       └── family workflow adapter / GenericExecutor
          │                         └── shared scientific runner
          ├── ExecutionResult / StageResult
          ├── Product Artifact metadata ──> ArtifactStorePort
          └── typed lineage authority
                    └── generic-only LineageEdge
                              └── closure/export projection

Legacy API/CLI/worker/persistence: retired/archive boundary
Shared scientific modules: retained independently
Bootstrap: product_migrations only
```

## 12. Architecture Decisions

### E4-ADR-001 — Canonical Product runtime

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Product runtimeはrepository-managed、legacy rootはpackage/deploymentから除外。
- Evidence: E4-OBS-052..058、Phase 01、database decision record。
- Decision: Product API、canonical Product worker、Product persistence、promoted Product CLIをcanonical runtime familyとする。legacy runtime rootはnon-canonical。
- Alternatives: 両runtime維持、legacyをcanonical化、external scheduler化。
- Rationale: repository-managed ambiguityを除去し、shared scientific moduleを保持できる。
- Consequences: legacy external compatibilityには明示的gateが必要。
- Risks: 外部consumerがlegacy rootに依存する可能性。
- Human approval required: yes。
- Derived requirements: E4-REQ-001、E4-REQ-002。

### E4-ADR-002 — Unified canonical persistent Execution aggregate

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Causal/Familyでentity/table、claimer、state、mutationが分かれる。
- Evidence: Phase 02 E4-OBS-014..032、E4-INF-012。
- Decision: family discriminatorとworkflow-specific plan/specificationを持つcanonical Execution aggregateを導入する。
- Alternatives: Candidate A、B、D。
- Rationale: Candidate DはENH-E4のdual executionを残す。A/Bは現行tableの偶然の境界をcanonical化する。
- Consequences: 移行/実装コストは大きい。現行tableはfinal stateで独立authorityにできない。
- Risks: aggregateが過度に汎化される可能性。
- Human approval required: yes。
- Derived requirements: E4-REQ-003..006。

### E4-ADR-003 — Common Execution identity and mutation semantics

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: lifecycleごとにretry/rerun/revise semanticsが異なる。
- Evidence: Phase 02/03/04。
- Decision: retryは同じExecution IDで新attempt、rerun/reviseは新Execution ID、reviseはtyped base relationを持つ。cancelはterminal transitionであり、既存成功outputを暗黙削除しない。
- Alternatives: family別ID、retryで新Execution、in-place revise。
- Rationale: attemptと新分析を分離しtraceabilityを保つ。
- Consequences: output retention/cleanup contractが必要。
- Risks: 現行Causal retryの重複挙動は未確定。
- Human approval required: yes。
- Derived requirements: E4-REQ-007..010。

### E4-ADR-004 — Persistent StageExecution for canonical workflows

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Familyにはpersistent stage、Causalにはpersistent stage writeが確認されない。
- Evidence: Phase 02 E4-OBS-018、021、024、026、E4-UNK-007。
- Decision: canonical Executionすべてにpersistent StageExecution childを持たせる。
- Alternatives: Causal stageをephemeral、Familyだけpersistent。
- Rationale: progress、retry、audit、Result ownership、failure recoveryの共通boundaryになる。
- Consequences: Causal側のpersistenceが増える。
- Risks: schema complexityとmigration cost。
- Human approval required: yes。
- Derived requirements: E4-REQ-011..013。

### E4-ADR-005 — GenericExecutorはworkflow infrastructure

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: GenericExecutorは現在persistence/claim/commitを所有しない。
- Evidence: Phase 02 E4-OBS-026、E4-INF-009。
- Decision: plan/stage sequencingとrunner invocationに限定する。
- Alternatives: lifecycle owner化、family-specific executorの重複。
- Rationale: orchestrationとscientific executionを分離する。
- Consequences: canonical serviceがstate/persistenceを所有する。
- Human approval required: yes。
- Derived requirements: E4-REQ-014。

### E4-ADR-006 — 一つのownership contract下のResult semantic levels

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Causal Resultはexecution-scoped、Family Resultはexecution+stage-scoped。
- Evidence: Phase 03 E4-OBS-033..035、E4-INF-013..014。
- Decision: ExecutionResult/StageResultを明示し、ownership/API contractは一つにする。
- Alternatives: Causal table、Family table、levelなしのResult。
- Rationale: ownership重複を除去しつつsemantic差異を失わない。
- Consequences: level/type/cardinality contractが必要。
- Human approval required: yes。
- Derived requirements: E4-REQ-015..017。

### E4-ADR-007 — 一つのProduct Artifact metadata authorityとphysical store分離

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: causal/family Artifact tableは異なるが、physical store portは共有する。
- Evidence: Phase 03 E4-OBS-035..037、E4-INF-015。
- Decision: metadata ownership contractを一つにし、physical storage boundaryは`ArtifactStorePort`に残す。
- Alternatives: metadata authorityを二つ維持、DB BLOB、object keyをidentity化。
- Rationale: domain ownershipとstorage implementationを分離する。
- Consequences: ResultなしArtifactをfamily contractで明示的に許可できる。
- Human approval required: yes。
- Derived requirements: E4-REQ-018..020。

### E4-ADR-008 — Typed authority + generic-only lineage

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: typed derivation、Family generic write、reconciliationなしのhybrid closureが現状存在する。
- Evidence: Phase 04 E4-OBS-042..051、E4-INF-019..025。
- Decision: structural relationはtyped authority、typedで表せないrelationはgeneric-only authority、closureはprojectionとする。
- Alternatives: derived-only、generic-only、indefinite dual authority。
- Rationale: non-reconstructable relationを保持しながらduplicate authorityを許さない。
- Consequences: 現行Familyのstructural duplicate writeはtransition中に限定し、final stateで除去する。
- Human approval required: yes。
- Derived requirements: E4-REQ-021..025。

### E4-ADR-009 — Legacy runtime retirement/archive boundary

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Product inbound dependencyなし、外部consumer不明、shared scientific codeは独立利用される。
- Evidence: Phase 05 E4-OBS-052..063、E4-INF-026..032。
- Decision: legacy API/CLI/workerをProduct runtimeからretireし、shared scientific moduleは保持する。orchestration/persistence/lineage sourceのarchive/removeはexternal compatibility gate後に行う。
- Alternatives: legacy全体をactive維持、即時全削除、scienceも全移植。
- Rationale: orchestration retirementとcapability preservationを分離する。
- Consequences: source removal前にexternal inventory/approvalが必要。
- Human approval required: yes。
- Derived requirements: E4-REQ-026..029。

### E4-ADR-010 — Product-only canonical migration/bootstrap

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Product migrationだけでclean rebuild成功、retention requirementなし。
- Evidence: database decision recordのDR-02とclean-state verification。
- Decision: target bootstrapは`product_migrations`のみ。root legacy migrationはhistory/archiveとし、pre-production default data policyはclean rebuild。
- Alternatives: 両chain実行、dual-read、historical in-place migration。
- Rationale:実測済みのclean rebuild pathである。
- Consequences: retention requirementが新たに出れば別ADRが必要。
- Human approval required: yes。
- Derived requirements: E4-REQ-030..032。

### E4-ADR-011 — Standalone CLI boundary

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: Product CLIはscientific adapterを直接呼びlocal manifestを書き、Product Executionを永続化しない。
- Evidence: Phase 01/02 E4-OBS-010、011、027。
- Decision: low-level scientific utility CLIはpersistent lifecycle外に残す。user-visibleでaudit可能なCLI analysisはcanonical Executionへsubmitする。
- Alternatives: 全CLIを統合、dual orchestrationを文書化して残す。
- Rationale: utilityとProduct analysisを区別する。
- Consequences: CLI outputは明示的submitなしにProduct Execution/Resultではない。
- Human approval required: yes。
- Derived requirements: E4-REQ-033..034。

### E4-ADR-012 — Compatibility terminologyはconsumedな場合のみarchitectural

- Status: `PROPOSED_FOR_HUMAN_APPROVAL`
- Context: `legacy-product-snapshot/1`等のlegacy-named Product contractがある。
- Evidence: Phase 05 E4-OBS-062、`product/domain/execution.py:15,63-73`。
- Decision: Product validation/data contractが消費する間は保持し、名称だけで`ariadne.legacy` dependencyとは扱わない。renameは別contract decisionで行う。
- Alternatives: 即時rename、legacy-named stringを全てruntime dependencyとみなす。
- Rationale:不要なcompatibility breakを避ける。
- Consequences: terminology debtはtracking対象として残る。
- Human approval required: yes。
- Derived requirements: E4-REQ-035。

## 13. Architecture Invariants

| ID | Invariant | 根拠 |
|---|---|---|
| E4-INV-001 | user-visible Product analysisにはcanonical persistent Execution identityが一つだけ存在する。 | ADR-002 |
| E4-INV-002 | family/typeはworkflow semanticsを変えるが、lifecycle authorityは増やさない。 | ADR-002 |
| E4-INV-003 | retryはExecution identityを保持し、rerun/reviseと区別できる。 | ADR-003 |
| E4-INV-004 | canonical Executionのclaim/state transitionは監査可能である。 | ADR-003/004 |
| E4-INV-005 | worker claim/lease ownershipはcanonical repository/serviceに集約される。 | ADR-002/003 |
| E4-INV-006 | canonical Executionにはpersistent StageExecution childがある。 | ADR-004 |
| E4-INV-007 | GenericExecutorはcanonical lifecycle/Result/Artifact commitを行わない。 | ADR-005 |
| E4-INV-008 | Resultはcanonical Executionに属し、semantic levelを宣言する。 | ADR-006 |
| E4-INV-009 | Artifact metadataには一つのcanonical ownerと別個のphysical locatorがある。 | ADR-007 |
| E4-INV-010 | physical objectとmetadata commitの分離・compensation/reconciliation semanticsが明示される。 | ADR-007 |
| E4-INV-011 | semantic lineage relationごとにauthorityはtypedまたはgeneric-onlyの一つである。 | ADR-008 |
| E4-INV-012 | closure/exportはlineage authorityにならない。 | ADR-008 |
| E4-INV-013 | canonical Product runtimeはretired legacy runtime moduleをimportしない。 | ADR-001/009 |
| E4-INV-014 | shared scientific implementationはlegacy orchestrationなしで利用できる。 | ADR-009 |
| E4-INV-015 | canonical bootstrapはroot legacy migrationを実行しない。 | ADR-010 |
| E4-INV-016 | indefinite dual-write/dual-readをfinal architectureに残さない。 | ADR-008/010 |

## 14. Target Architecture Requirements

| ID | Requirement | ADR | 検証方法 |
|---|---|---|---|
| E4-REQ-001 | repository-managed Product runtime SHALL Product APIとcanonical Product workerをproduction rootとする。 | ADR-001 | static entry/deployment inspection |
| E4-REQ-002 | legacy API/CLI/worker SHALL canonical Product runtimeとして登録されない。 | ADR-001/009 | packaging/deployment contract |
| E4-REQ-003 | user-visible Product analysis SHALL一つのcanonical Execution aggregateを生成する。 | ADR-002 | application/integration test |
| E4-REQ-004 | canonical Execution SHALL family discriminatorを持つ。 | ADR-002 | schema/domain contract |
| E4-REQ-005 | lifecycle state transition SHALL family間で共通contractを持つ。 | ADR-002/003 | state-machine test |
| E4-REQ-006 | claim SHALL一つのrepository/service abstractionでatomic ownership acquisitionを行う。 | ADR-002/003 | concurrent claim test |
| E4-REQ-007 | retry SHALL Execution IDを保持し、attempt/retryを識別可能にする。 | ADR-003 | mutation contract test |
| E4-REQ-008 | rerun SHALL新Execution IDとtyped source relationを作る。 | ADR-003 | rerun lineage test |
| E4-REQ-009 | revise SHALL新Execution IDとtyped base relationを作る。 | ADR-003 | revise lineage test |
| E4-REQ-010 | cancel SHALL prior successful outputを暗黙に変更しない。 | ADR-003 | cancellation contract test |
| E4-REQ-011 | canonical Execution SHALL persistent StageExecution childを持つ。 | ADR-004 | schema/lifecycle test |
| E4-REQ-012 | Stage state/attempt history SHALL runner内部から独立してqueryできる。 | ADR-004/005 | API/repository contract |
| E4-REQ-013 | stage Result/Artifact ownership SHALL executionと必要なstageを識別する。 | ADR-004/006/007 | FK/constraint test |
| E4-REQ-014 | GenericExecutor SHALL claim/commit/retry/canonical persistenceを行わない。 | ADR-005 | architecture test |
| E4-REQ-015 | Result SHALL ExecutionResultまたはStageResult levelを宣言する。 | ADR-006 | schema/domain validation |
| E4-REQ-016 | Result reuse SHALL typed Result IDとrole/contextを使う。 | ADR-006/008 | downstream input contract |
| E4-REQ-017 | Result cardinality SHALL familyごとに明示される。 | ADR-006 | schema/service test |
| E4-REQ-018 | Product Artifact metadata SHALL一つのownership API/service boundaryを持つ。 | ADR-007 | architecture/service contract |
| E4-REQ-019 | physical Artifact bytes SHALL ArtifactStorePort経由で扱い、object keyをsemantic IDにしない。 | ADR-007 | port/contract test |
| E4-REQ-020 | ResultなしArtifactはfamily contractで明示的に許可/拒否する。 | ADR-006/007 | validation test |
| E4-REQ-021 | reconstructableなstructural relationはtyped relationをsole authorityとする。 | ADR-008 | lineage authority test |
| E4-REQ-022 | generic lineageはtypedで表せないrelationまたはapproved user linkに限定する。 | ADR-008 | relation allowlist test |
| E4-REQ-023 | closure/export SHALL lineage source classを保持/表示する。 | ADR-008 | API/export contract |
| E4-REQ-024 | generic-only edge SHALL scope、endpoint policy、uniqueness、deletion behaviorを検証する。 | ADR-008 | persistence/service test |
| E4-REQ-025 | structural lineageをindefinitely dual-writeしない。 | ADR-008 | architecture/reconciliation test |
| E4-REQ-026 | shared scientific module SHALL legacy orchestrationから独立する。 | ADR-009 | import architecture test |
| E4-REQ-027 | legacy runtime retirement前にexternal-consumer decisionを行う。 | ADR-009 | release gate/document review |
| E4-REQ-028 | legacy classification SHALL capability/runtime/persistence/migration/lineageを分ける。 | ADR-009 | inventory review |
| E4-REQ-029 | legacy ArtifactLineage/Result persistence SHALL Product authorityにならない。 | ADR-009 | boundary test |
| E4-REQ-030 | clean Product bootstrap SHALL product_migrationsを使いlegacy chainを実行しない。 | ADR-010 | clean rebuild verification |
| E4-REQ-031 | destructive rebuild前にexisting-data policyを明示する。 | ADR-010 | decision record/release gate |
| E4-REQ-032 | root legacy migrations SHALL別承認がない限りhistory-onlyである。 | ADR-010 | migration review |
| E4-REQ-033 | low-level scientific CLI SHALL second persistent Product lifecycleを暗黙生成しない。 | ADR-011 | CLI contract test |
| E4-REQ-034 | auditable user-visible CLI SHALL canonical Executionへsubmitする。 | ADR-011 | CLI/API contract |
| E4-REQ-035 | legacy-named Product contract SHALL compatibility evidenceなしにrenameしない。 | ADR-012 | contract inventory |

## 15. Implementation Constraints

| ID | Constraint | 理由 | ADR |
|---|---|---|---|
| E4-CON-001 | ENH-E4でscientific algorithmを再実装しない。 | shared capabilityを保全 | ADR-009/011 |
| E4-CON-002 | GenericExecutorをlifecycle ownerにしない。 | current responsibilityと証拠 | ADR-005 |
| E4-CON-003 | Causal/Family tableをfinalの独立authorityとして残さない。 | dual executionを温存するため | ADR-002 |
| E4-CON-004 | physical object keyをsemantic IDにしない。 | metadata/storage分離 | ADR-007 |
| E4-CON-005 | structural lineageをtyped/generic双方へ独立writeしない。 | dual authority防止 | ADR-008 |
| E4-CON-006 | transition dual-read/writeにはowner、期限、exit criteria、reconciliation evidenceを持たせる。 | indefinite dual architecture防止 | ADR-008 |
| E4-CON-007 | canonical Product bootstrapでroot legacy migrationを実行しない。 | clean rebuild evidence | ADR-010 |
| E4-CON-008 | external compatibility decision前にlegacy sourceを削除しない。 | external boundary不明 | ADR-009 |
| E4-CON-009 | terminologyだけを理由にlegacy-named data contractをrenameしない。 | compatibility evidence | ADR-012 |
| E4-CON-010 | direct dependency proofなしにfrontend/auth/datasetを変更しない。 | minimum necessary change | scope |

## 16. Legacy Component Target Classification

| Legacy Component | Proposed Target Status | 理由 |
|---|---|---|
| legacy API | RETIRE_RUNTIME | Product inbound pathなし、non-canonical |
| legacy CLI | RETIRE_RUNTIME | Product CLIと別で、外部利用は未確認 |
| legacy worker | RETIRE_RUNTIME | Product workerがcanonical |
| legacy execution/control plane | ARCHIVE_SOURCE | lifecycle/persistenceが別、外部境界未解決 |
| legacy pipeline | REPLACE_BEFORE_RETIRE | preprocessing/ETL capabilityの確認が必要 |
| legacy discovery | RETAIN_SHARED_CAPABILITY | shared `ariadne.causal`を保持し、legacy orchestrationは保持しない |
| legacy inference/analysis-ready | REPLACE_BEFORE_RETIRE | shared estimatorを保持し、orchestrationを置換 |
| legacy domain/persistence | ARCHIVE_SOURCE | Product clean bootstrapに不要、外部data不明 |
| legacy Artifact/materialization | REPLACE_BEFORE_RETIRE | Product ArtifactStore boundaryへ置換 |
| legacy ArtifactLineage | ARCHIVE_SOURCE | Product lineageとは別authority |
| legacy infrastructure/contracts | ARCHIVE_SOURCE | old namespace/external dependency不明 |
| legacy ETL/catalog | REPLACE_BEFORE_RETIRE | Product equivalentが未確定 |
| `ariadne.causal`/`ariadne.preprocessing`/`ariadne.shared` | RETAIN_SHARED_CAPABILITY | Productとlegacy双方が利用し、legacy orchestrationではない |

全てHuman approvalを要する。これは実行済み変更ではない。

## 17. Lineage Relation Target Classification

| Relation | Current Representation | Proposed Authority | Secondary Representation | 理由 |
|---|---|---|---|---|
| Execution→Result | typed FK + family generic edge | typed | closure projection | structural ownership |
| Result→Artifact | typed FK + family generic edge | typed | closure projection | structural ownership |
| Dataset/View→Execution | typed field + family generic edge | typed | closure projection | input contract |
| Result→Execution input | `input_result_id` + derived/possible generic | typed | closure projection | causal downstream contract |
| Result→GraphVersion | `source_result_id` + derived | typed | closure projection | graph provenance |
| Artifact→DatasetVersion | `source_artifact_id` + derived | typed | closure projection | dataset source |
| Execution revision/base | revision context + predictive generic | typed base relation | generic only if needed | identity relation |
| Artifact→Artifact stage derivation | generic only | generic-only edge | closure projection | typed equivalent未確認 |
| Result→Result SUMMARIZES | generic only | generic-only edge | closure projection | typed relationなし |
| Result/Artifact DOCUMENTS/EVIDENCE_FOR | generic only | generic-only edge | closure/export | non-structural relation |
| user-authored link | generic only | generic-only edge | closure/export | explicit user relation |
| legacy ArtifactLineage | legacy table | Product外のlegacy authority | legacy API projection | separate architecture |

## 18. Execution Mutation Semantics

| Operation | Target identity | Result semantics | Lineage semantics |
|---|---|---|---|
| retry | 同じExecution ID、新しいattempt/retry record | owned incomplete outputをreplaceまたはversion化。暗黙duplicateは禁止 | attempt relationをcontract化。prior success outputは保護 |
| rerun | 新Execution ID | 新Result/Artifact、sourceは保持 | typed RERUN/DERIVED_FROM |
| revise | 新Execution ID、typed base relation | 新snapshot/output、sourceは保持 | typed REVISED_FROM |
| cancel | 同じIDでterminal/cancelled | partial outputのretain/deleteを明示し、prior successを暗黙変更しない | retention ruleなしにhistorical lineageを消さない |

## 19. Data / Migration Policy

### Existing Data Assumption

database decision recordはpre-productionでapplication-data retention requirementなしとする。ただし、これは全環境でdata破棄可能という意味ではない。

### Target Bootstrap

空の永続領域からProduct migrationを適用し、startup前にProduct application rowが0であることを確認する。その後Product startup/functional verificationを行う。

### Migration Chain

canonical chainは`alembic_product.ini` → `product_migrations`。root `alembic.ini` → `migrations`はhistory-onlyで、Product bootstrapから呼ばない。

### Compatibility

retention/external-schema requirementが発見されたらclean-rebuild実装を止め、別のmigration/compatibility ADRを作る。dual migration chainはfinal targetにしない。

## 20. Scientific Capability Preservation

| Capability | Current owner | Target owner | Change allowed? | 根拠 |
|---|---|---|---|---|
| causal discovery | shared `ariadne.causal.discovery` + legacy adapter | shared module + Product workflow adapter | orchestration adapterのみ | E4-OBS-059,060 |
| treatment effect | shared estimator + legacy/Product adapter | shared estimator + canonical workflow | algorithm rewrite不可 | E4-DEP-003 |
| edge weight | shared estimator + legacy analysis-ready | shared estimator + canonical workflow | scientific redesign不可 | E4-DEP-003 |
| preprocessing/feature semantics | shared preprocessing + family adapter | shared module + canonical adapter | contract adaptationのみ | E4-DEP-004 |
| validation/constants | shared module | shared module | 保持 | E4-DEP-005 |
| legacy CompleteJourney orchestration | legacy ETL namespace | canonicalとしない。必要性を別途監査 | Product requirement次第 | E4-UNK-025 |

## 21. Compatibility Boundary

### Repository-local

対象はrepository-local Product compatibilityである。Product sourceは`ariadne.legacy`から独立し、Product-only clean bootstrapをtargetとする。

### External

legacy rootを呼ぶ外部processの有無は不明。source/runtimeをremoveする前に、external compatibilityをENH-E4 scope外とするか、bounded compatibility windowを設けるかをHumanが決める。

### Data formats

`legacy-product-snapshot/1`等はProduct domain/schema/testが消費する間だけ保持する。これはruntime package dependencyの証明ではない。

### API/CLI

legacy API/CLIはcanonical Product endpointではない。外部に約束されたlegacy API/CLIがある場合は、別のcompatibility decisionとexit dateが必要である。

## 22. Risks

| Risk | 原因 | 影響 | Mitigation/Verification |
|---|---|---|---|
| unified aggregateの過汎化 | family差を一schemaへ押し込む | semantic loss | family workflow/stage contractを明示 |
| migration complexity | current tableが分離 | implementation defect | target schemaを別設計しclean rebuildを検証 |
| retry semantics変更 | lifecycleごとにcleanupが違う | output duplicate/loss | coding前にattempt/result retention testを定義 |
| lineage duplicate | Family generic writeとtyped derivationの重複 | stale/conflict graph | bounded transitionとreconciliation |
| external legacy breakage | external consumer不明 | compatibility failure | retirement前external inventory gate |
| shared science削除 | Product/legacy双方がshared moduleを利用 | scientific regression | shared moduleを保持しimport test |
| artifact orphan | DB/object storeが別resource | leak/missing object | compensation/reconciliation |
| data policy誤認 | retention evidenceが変わる | irreversible loss | reset前にdata policyを承認 |
| CLI semantics誤認 | utilityとuser-visible analysisの混同 | hidden lifecycle | CLI purposeを分類 |

## 23. Human Decisions Required

| ID | Question | Options | Recommendation | Evidence | Blocking |
|---|---|---|---|---|---|
| HD-001 | unified canonical Execution aggregateを承認するか | A/B/C/D | C | Phase 02、ADR-002 | implementationに対してyes |
| HD-002 | Causalにもpersistent StageExecutionを導入するか | A/B/C | all canonical workflows | E4-UNK-007、ADR-004 | schemaに対してyes |
| HD-003 | Result semantic-level modelを承認するか | unified/levelled | levelled + one ownership | Phase 03 | Result designに対してyes |
| HD-004 | typed + generic-only lineage authorityを承認するか | derived/generic/hybrid | explicit hybrid | Phase 04 | lineage designに対してyes |
| HD-005 | external legacy compatibilityをENH-E4 scope外とするか | yes/no/window | yesをdefault提案、要確認 | E4-UNK-024..029 | legacy retirementに対してyes |
| HD-006 | Product-only clean bootstrapとhistorical migrationなしを承認するか | clean/migrate/dual | pre-productionではclean | database decision | destructive policyに対してyes |
| HD-007 | standalone Product CLIをutility boundaryとするか | utility/integrated | utility。ただしauditable useはExecutionへ | Phase 01/02 | coreにはno |

## 24. ADR Dependency Graph

```text
ADR-001 runtime
   ├── ADR-002 unified Execution
   │      ├── ADR-003 identity/state/mutation
   │      ├── ADR-004 persistent StageExecution
   │      └── ADR-005 GenericExecutor boundary
   ├── ADR-006 Result
   │      └── ADR-007 Artifact
   ├── ADR-008 Lineage
   ├── ADR-009 Legacy
   ├── ADR-010 Migration
   ├── ADR-011 CLI boundary
   └── ADR-012 terminology
```

## 25. Traceability Matrix

| Evidence | ADR | Invariant | Requirement | Implementation area |
|---|---|---|---|---|
| Phase 02 E4-OBS-014..032 | ADR-001..005 | INV-001..007 | REQ-001..014 | execution/service/repository/worker/stage |
| Phase 03 E4-OBS-033..041 | ADR-006..007 | INV-008..010 | REQ-015..020 | Result/Artifact aggregate/store |
| Phase 04 E4-OBS-042..051 | ADR-008 | INV-011..012,016 | REQ-021..025 | lineage/closure/export |
| Phase 05 E4-OBS-052..063 | ADR-001,009,012 | INV-013..014 | REQ-001,002,026..029,035 | package/deploy/shared/legacy |
| database DR-02/clean rebuild | ADR-010 | INV-015 | REQ-030..032 | migration/bootstrap/data policy |
| Phase 01 E4-OBS-010..013 | ADR-001,011 | INV-001,013 | REQ-001,033,034 | CLI/runtime |
| E4-UNK-024..029 | ADR-009,012 | INV-013,014 | REQ-027,035 | external compatibility gate |

## 26. Implementation Area Impact

| Area | Requirements | Expected change type |
|---|---|---|
| Product execution domain/application | REQ-003..010 | unified lifecycle contractとadapter |
| Product persistence/schema | REQ-004,011,013,015,017,018 | target aggregate/result/artifact schema |
| repository/UoW | REQ-006,012 | common claim/transaction abstraction |
| worker runner | REQ-006,010,012,014 | canonical claim/dispatch/terminal boundary |
| family workflow adapter | REQ-004,011,014,020 | existing workflowを新lifecycleへadapter |
| Result/Artifact service | REQ-015..020 | ownership/cardinality/reference contract |
| lineage/closure/export | REQ-021..025 | authority split/source labeling |
| packaging/deployment | REQ-001,002,026 | Product-only surface維持 |
| shared scientific module | REQ-026 | 保持。algorithm rewriteなし |
| legacy/migration | REQ-027..032 | bounded retirement/archive decision |
| CLI | REQ-033..035 | utility/user-visible boundary |
| tests | 全requirement | architecture/state/lineage/migration/compatibility verification |

## 27. Rejected Alternatives

### Alternative A — Product Execution lifecycleを二つ維持

- 検討理由: 即時変更が最小。
- 非推奨理由: claim/state/retry/result/lineage authorityが二つ残り、ENH-E4目的に反する。
- 根拠: Phase 02。

### Alternative B — Causal table/modelをcanonical化

- 検討理由: domain/repository/UoWが成熟している。
- 非推奨理由: family stage semantics、artifact-only output、workflow-specific stateを無理に押し込む。
- 根拠: Phase 03 E4-OBS-034..035。

### Alternative C — Family table/modelをcanonical化

- 検討理由: persistent stageとfamily workflowを既に持つ。
- 非推奨理由: CausalのResult/input/graph relationとrepository abstractionが異なる。
- 根拠: Phase 03/04。

### Alternative D — derived-only lineage

- 検討理由: structural Product relationの多くはtyped relationから再構築できる。
- 非推奨理由: Predictive stage/artifact、model-card、user-authored relationは完全再構築できない。
- 根拠: Phase 04 E4-INF-022。

### Alternative E — 全lineageをgeneric persisted authority

- 検討理由: common graph representation。
- 非推奨理由: normal Causal processingにgeneric writeがなく、typed FK integrityを下げる。
- 根拠: Phase 04 E4-OBS-048、E4-OBS-057。

### Alternative F — legacy sourceを即時全削除

- 検討理由: Product inbound importがなく、Product-only clean rebuildが成功。
- 非推奨理由: external consumerとshared-scientific usageが未確定。
- 根拠: Phase 05 E4-UNK-024..029。

## 28. Remaining Unknowns

| ID | Targetへの影響 | Blocking | Handling |
|---|---|---|---|
| E4-UNK-009 | causal retry output retention | retry実装にはyes | coding前にsemanticsを決定 |
| E4-UNK-012 | family Artifact reuse | downstream contract | core targetはblockしないがadapter前に確認 |
| E4-UNK-014 | object backend/GC | Artifact operation | store contract/reconciliationで補う |
| E4-UNK-015 | legacy cleanup | archive/removal safety | external/retention review |
| E4-UNK-016..022 | external lineage/export details | transition/compatibility | contract/test review |
| E4-UNK-023 | legacy namespace executable status | archive approach | source/package review |
| E4-UNK-024..029 | external legacy/data/compatibility | retirement/data destruction | legacy removalにはyes |
| E4-UNK-005..008 | schema intent、lease、Causal stage、legacy retry | detailed implementation | corresponding invariantを先に定義 |

## 29. New Facts

Phase 06で追加のrepository factは確認していない。database reinitialization evidenceは既存decision recordとして利用した。

## 30. New Inferences

- E4-INF-033: Candidate Cだけが、Causal/Family semanticsを消さずにProductの複数Execution authorityを解消できる。
- E4-INF-034: persistent StageExecutionはFamilyの現行semanticsを保ちつつCausalのobservability gapを閉じる最小共通boundaryである。
- E4-INF-035: explicit hybrid lineageは、typed structural relationとgeneric-only relationのauthorityを重複させない場合にのみ成立する。
- E4-INF-036: Product-only clean bootstrapは現在のpre-production contextには有効だが、全historical data policyではない。
- E4-INF-037: legacy retirementはrepository-managed runtimeには提案できるが、source/data removalはexternal consumer不明のため条件付きである。

## 31. Decision Quality Check

1. authoritative Product persistent Execution lifecycleは一つか: **現状NO、target YES**。ADR-002で解消する。
2. 同じsemantic Resultに複数authorityが残るか: **target NO**。ExecutionResult/StageResultはsemantic levelとして明示する。
3. 同じsemantic Artifactに複数metadata authorityが残るか: **target NO**。metadata ownerを一つにする。
4. 一つのsemantic lineage relationに二つの独立authorityが残るか: **target NO**。typed structuralとgeneric-onlyを分離する。
5. active Productがretired legacy runtimeに依存するか: **現状NO_PATH_CONFIRMED、target NO**。
6. target bootstrapはlegacy migrationを必要とするか: **NO**。
7. shared scientific implementationは保持されるか: **YES**。
8. dual-read/writeはtemporary boundedか: **YES**。final stateでは一つのauthorityにする。
9. Decisionはprior evidenceへtraceできるか: **YES**。
10. external compatibility assumptionは明示されているか: **YES**。E4-UNK-024..029とHD-005に記録した。

## 32. Recommendation

`READY_FOR_HUMAN_APPROVAL`。

architectural directionはreview可能である。ただしSection 23のhuman decisionsを承認するまで、implementationは開始しない。legacy source/runtime removalとdestructive data policyはexternal compatibility/retention decisionの後に限る。

## 33. Completion Status

`COMPLETED_WITH_HUMAN_DECISIONS`。

# 53. Mandatory Decision Quality Requirements

## Q1

**YES（target案）。** user-visible Product analysisは一つのcanonical persistent Execution aggregateを持つ。現行Causal/Family dualityはtargetではない。

## Q2

**YES。** canonical Executionはidentity、state、claim、retry/rerun/revise、persistence、terminal outcomeを所有する。scientific workflowはfamily固有plan/stage/runnerを所有する。

## Q3

**YES。** Result semanticsはcurrent table nameではなくExecutionResult/StageResultとして定義する。

## Q4

**YES。** Artifact metadata ownershipは一つ、physical objectは`ArtifactStorePort`に分離する。

## Q5

**YES。** relationごとにtypedまたはgeneric-onlyの一つをauthorityとする。

## Q6

**YES。** generic `LineageEdge`はtypedで表せないrelationとuser-authored relationのstoreであり、全relationの曖昧なauthorityではない。

## Q7

**YES。** Causal/Familyの現行persistent lifecycleをcanonical aggregateへ統合し、どちらもfinalで独立authorityとして残さない。

## Q8

**YES。** 全canonical Executionにpersistent StageExecutionを持たせる。

## Q9

**YES。** retryは同一Execution IDの新attempt、rerun/reviseは新IDとtyped source/base relationとする。

## Q10

**YES。** legacy orchestration/persistence/runtimeと`ariadne.causal`/`ariadne.preprocessing`/`ariadne.shared`を分離する。

## Q11

**YES。** 現行pre-production database recordはProduct-only clean bootstrapとretentionなしを支持する。ただしretention requirementが変わればdestructive implementationをblockする。

## Q12

**YES。** indefinite dual-write/readはtargetにしない。transitionが必要なら期限、exit criteria、reconciliationを持たせる。

# 54. Prohibited Conclusions

本Recordはhuman approvalのための提案である。code/schema/migration/test変更、legacy削除、data破棄、Gate実行を許可しない。外部consumerが存在しないとも断定しない。

# 55. Completeness Criteria

C1 Phase 01–05 resultを読んだ: PASS  
C2 database reinitialization evidenceを読んだ: PASS  
C3 current problem statement: PASS  
C4 candidate比較: PASS  
C5 canonical Execution: PASS  
C6 identity/state/mutation: PASS  
C7 worker claim: PASS  
C8 StageExecution policy: PASS  
C9 GenericExecutor責務: PASS  
C10 Result ownership: PASS  
C11 Artifact ownership: PASS  
C12 downstream reuse: PASS  
C13 lineage authority: PASS  
C14 generic-only lineage: PASS  
C15 legacy policy: PASS  
C16 shared scientific separation: PASS  
C17 external boundary: PASS  
C18 migration/data policy: PASS  
C19 CLI policy: PASS  
C20 compatibility terminology: PASS  
C21 ADR/invariant/requirement: PASS  
C22 traceability: PASS  
C23 rejected alternatives: PASS  
C24 risks: PASS  
C25 human decisions: PASS  
C26 code変更なし: PASS  
C27 Gate decompositionなし: PASS

# 56. Final Self-Check

生成後に以下のみ実行する:

```text
git status --short
git diff --stat
git diff -- docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/architecture_review/06_target_architecture_decision_record_result.md
```

既存の `deploy/.nfs000000000076202f00000088` 変更は保持する。

