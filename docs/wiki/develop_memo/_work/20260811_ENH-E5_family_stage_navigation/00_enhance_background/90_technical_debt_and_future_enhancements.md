# ENH-E5 Technical Debt and Future Enhancements

## 0. PURPOSE

本書は、ENH-E5 preflight alignment auditで **D3: DEFER** と裁定された未実装・部分実装Requirement/Designを、将来のplanningで再評価・promoteできる形で管理する **non-normative planning ledger** である。

本書のsource-of-truthは以下とする。

- `40_operator_workflows/preflight_analysis/remediation_decision_matrix.csv`
- `40_operator_workflows/preflight_analysis/remediation_decision_log.md`
- `40_operator_workflows/preflight_analysis/remediation_decision_freeze_audit.md`

本書はRequirement/Design/Coding/Test contractの正本ではない。Requirementの存在・Level・Status・Deliveryは`10_requirements_definition.md`、current/target設計は`21/22/23/30`、Coding/Test Agent向けcontractは`06/Pxx`および`07`を正本とする。

### 0.1 Scope

- D3 Decision Item: **28件**
- `NOT_IMPLEMENTED`: **15件**
- `PARTIAL`: **13件**
- Root Technical Debt: **17件**
- Derived D3 verification scope: **2件** (`D22-013c`, `D30-018c`)

### 0.2 Decision-freeze note

`remediation_decision_freeze_audit.md` の現在判定は `CONDITIONAL PASS` である。`FR-122 / FR-126 / D10-006a / D10-006b` のD3はlog/matrix間で一致しているが、明示的human approvalが未確認のため、本書では `PENDING_EXPLICIT_APPROVAL` として **provisional trace** する。

これら4件のapprovalが確定した場合、本書のTD-001/TD-002は内容変更なしで`APPROVED`へ移行できる。

---

## 1. MANAGEMENT POLICY

1. **D3はRequirementの消去を意味しない。** Requirement正本では`Requirement Status=DEFERRED`、`Delivery=FUTURE`として保持する。
2. **本書はD3 decisionの派生ledgerであり、decision authorityではない。** D1/D2/D3を変更する場合は、先に`remediation_decision_log.md` / `remediation_decision_matrix.csv`をhuman-reviewed revisionとして更新する。
3. **本書からCoding/Test Agentが不足仕様を補完してはならない。** Future itemを実装対象へpromoteする場合、将来Enhancementのrequirements/design/06/07/Pxxへ仕様を収束させる。
4. **Requirement debtとfuture capabilityを区別する。** 既存Requirement由来の未実装/部分実装と、将来新規capability候補を同一視しない。
5. **Revisit Triggerはplanning guidanceでありnormative requirementではない。** Trigger成立時は新しいpreflightでscope/contract/priorityを再評価する。
6. **TD番号はstable identifierとする。** 欠番は再利用しない。現時点で`TD-016`は未使用であり、意味を推測して割り当てない。
7. `D22-013c / D30-018c`は独立Debtではない。各D3 itemが将来promoteされた際に、そのverification targetをDesign/Test contractへ戻すderived obligationとして扱う。

---

## 2. STATUS / CATEGORY DEFINITIONS

| Category | Meaning |
|---|---|
| UNIMPLEMENTED_REQUIREMENT | D3対象の要求/設計がcurrent implementationに成立していない。 |
| PARTIAL_IMPLEMENTATION | 基礎・断片は存在するが、D3対象substatement全体は成立していない。 |
| IMPLEMENTATION_ANOMALY | Requirementに直接対応しない実装/設計上の将来改善候補。必要時のみ追加する。 |
| FUTURE_ENHANCEMENT | 将来Enhancementで新規にpromoteするcapability候補。本Phase FではD3 root itemを中心に記録する。 |

| Ledger / Approval Status | Meaning |
|---|---|
| DEFERRED | ENH-E5では実装しない。 |
| PENDING_EXPLICIT_APPROVAL | decision contentはmatrix/logと一致するがformal human approval traceが未完。 |
| APPROVED | 会話上の裁定とdecision matrix/logが一致している。 |
| PROMOTED | 将来EnhancementでACTIVE scopeへ移行済み。 |
| RESOLVED | 実装/文書化/要件撤回等によりledger上のopen itemではない。 |

---

## 3. UNIMPLEMENTED REQUIREMENTS

Current D3 rows with `Implementation Status=NOT_IMPLEMENTED`: **15件**。

| Decision Item | Source | Deferred Substatement | TD Ref | Requirement Status | Implementation Status | Delivery | Approval |
|---|---|---|---|---|---|---|---|
| FR-021 | FR-021 | Sensitive/use-restriction/description column metadata | TD-006 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| FR-028 | FR-028 | Correlation / association matrix operation | TD-007 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| FR-062 | FR-062 | Automated hyperparameter selection | TD-008 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| FR-110b | FR-110 | Dataset/context/date filter expansion | TD-010 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| FR-118 | FR-118 | Product submit/poll CLI | TD-009 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| FR-122 | FR-122 | General operational audit trail | TD-001 | DEFERRED | NOT_IMPLEMENTED | FUTURE | PENDING_EXPLICIT_APPROVAL |
| FR-126 | FR-126 | Configurable retention/deletion policy | TD-002 | DEFERRED | NOT_IMPLEMENTED | FUTURE | PENDING_EXPLICIT_APPROVAL |
| FR-127b | FR-127 | DB/Worker/Artifact Store component readiness | TD-011 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| FR-128b | FR-128 | Operational size/timeout configuration | TD-004 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| NFR-004 | NFR-004 | General p95 API SLO / performance regression gate | TD-012 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| NFR-017 | NFR-017 | Explicit upload/row/column/memory/timeout hard limits | TD-004 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| NFR-020b | NFR-020 | Object-storage adapter / switching | TD-005 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| D10-005c | D10-005 | Distinct Operator / system-operate authorization | TD-003 | DEFERRED | NOT_IMPLEMENTED | FUTURE | APPROVED |
| D10-006a | D10-006 | General Audit contract | TD-001 | DEFERRED | NOT_IMPLEMENTED | FUTURE | PENDING_EXPLICIT_APPROVAL |
| D10-006b | D10-006 | Retention/deletion contract | TD-002 | DEFERRED | NOT_IMPLEMENTED | FUTURE | PENDING_EXPLICIT_APPROVAL |

---

## 4. PARTIALLY IMPLEMENTED REQUIREMENTS

Current D3 rows with `Implementation Status=PARTIAL`: **13件**。

| Decision Item | Source | Deferred Substatement | TD Ref | Requirement Status | Implementation Status | Delivery | Approval / Note |
|---|---|---|---|---|---|---|---|
| FR-025b | FR-025 | Joint missing-pattern analysis | TD-007 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| FR-026b | FR-026 | Full scatter/box/crosstab surface set | TD-007 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| FR-086b | FR-086 | Per-stage timeout/resource limit persistence | TD-004 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| FR-120b | FR-120 | Systematic canonical schema-example synchronization | TD-013 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| FR-123b | FR-123 | Configurable exposure policy based on sensitive metadata | TD-006 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| NFR-007 | NFR-007 | Metadata/Artifact cross-store failure compensation | TD-014 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| NFR-008c | NFR-008 | Production-grade authentication/system security hardening | TD-015 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| NFR-009b | NFR-009 | Configurable prediction/local-explanation/export minimization | TD-006 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| NFR-010b | NFR-010 | Explicit restart/resume semantics | TD-017 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| NFR-011b | NFR-011 | Comprehensive structured logging + metrics | TD-018 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| D22-003b | D22-003 | Object-storage / broader adapter variants | TD-005 | DEFERRED | PARTIAL | FUTURE | APPROVED |
| D22-013c | D22-013 | Verification surfaces owned by D3 requirements | — | DEFERRED | PARTIAL | FUTURE | DERIVED_D3_VERIFICATION_SCOPE |
| D30-018c | D30-018 | Detailed verification owned by D3 requirements | — | DEFERRED | PARTIAL | FUTURE | DERIVED_D3_VERIFICATION_SCOPE |

### 4.1 Derived verification scope

- `D22-013c`: D3へ送ったcapabilityのverification surfaceをENH-E5のimplemented test architectureとして主張しない。
- `D30-018c`: D3 scopeのdetailed verification targetをENH-E5 acceptanceから外す。
- 将来、対応するTDを`PROMOTED`した時点で、そのRequirementに必要なtest seam / acceptanceを将来Enhancementの`30`および`07`へ再導入する。

---

## 5. IMPLEMENTATION / DESIGN ANOMALIES

現時点のD3 projectionでは、Requirement/Design decisionから独立した`IMPLEMENTATION_ANOMALY`を新規登録していない。

今後、source reviewでRequirementに直接紐づかない改善候補を発見した場合は、以下を最低限記録する。

- anomaly ID / title
- source evidence
- impact
- why not in current Enhancement
- proposed revisit trigger
- related Requirement/Design（存在する場合）

---

## 6. FUTURE ENHANCEMENTS

以下はD3 Decision Itemをroot technical-debt/future-enhancement単位へ集約した詳細ledgerである。

### TD-001 — General Operational Audit Trail

- **Category:** `UNIMPLEMENTED_REQUIREMENT`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `PENDING_EXPLICIT_APPROVAL`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `FR-122`, `D10-006a`
- **Source IDs:** `FR-122`, `D10-006`
- **Finding Groups:** `audit_retention`

**Target / debt statement**

作成・更新・archive・execution・cancel・retry・export等のoperational actionを、actor/action/resource/outcomeとともに追跡できる一般Audit contract。

**Current state**

Annotation等の限定的な履歴は存在するが、列挙されたoperational actionを横断するcanonical AuditLog domain/persistence resourceは確認されていない。

**Why deferred from ENH-E5**

Family × Navigation Stage改修の直接依存ではなく、実装するとdomain model、persistence、authorization、export、operationsを横断する基盤設計になるためENH-E5では延期する。

**Impact while deferred**

分析機能自体は成立するが、運用上のactor/action証跡、security forensics、cancel/retry/export等の説明可能性が弱い。Scientific lineageとは別のoperational audit concernである。

**Future design considerations**

- audit eventのcanonical identity、actor、project/resource、action、timestamp、outcome、request/correlation情報を定義する。
- create/update/archive/execute/cancel/retry/export等のaction inventoryと記録境界をfreezeする。
- append-only性、保持、検索、redaction、failure時の扱いを設計する。
- Project authorization / system-level operator modelとの責務境界を明示する。

**Revisit trigger**

- multi-user production運用へ移行するとき。
- security incident調査やoperational accountabilityを正式要件化するとき。
- 監査証跡を必要とする外部運用・組織要件が生じたとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| FR-122 | MISMATCH | NOT_IMPLEMENTED | General operational audit trail | 要求方向は合理的だが横断audit基盤となるためENH-E5では延期する。 |
| D10-006a | MISMATCH | NOT_IMPLEMENTED | General Audit contract | FR-122と同一root decision。 |

### TD-002 — Configurable Retention / Deletion Policy

- **Category:** `UNIMPLEMENTED_REQUIREMENT`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `PENDING_EXPLICIT_APPROVAL`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `FR-126`, `D10-006b`
- **Source IDs:** `FR-126`, `D10-006`
- **Finding Groups:** `audit_retention`

**Target / debt statement**

Metadata、Artifact、logの保持期間・削除policyをresource classごとに管理するlifecycle policy。

**Current state**

Artifact delete等の個別削除処理は存在するが、Metadata / Artifact / logを横断するconfigurable retention/deletion policyは確認されていない。

**Why deferred from ENH-E5**

削除対象、保持期間、cascade/ordering、audit、failure recoveryを含む独立したdata lifecycle設計が必要で、ENH-E5の直接scopeではない。

**Impact while deferred**

長期運用でstorage growth、削除手順の一貫性、policy enforcementの運用負荷が残る。

**Future design considerations**

- resource class別のretention policyとdefault/override semanticsを定義する。
- MetadataとArtifactの削除順序、参照整合、orphan処理を定義する。
- 削除actionのauditabilityとfailure/retry semanticsをTD-001/TD-014と整合させる。
- manual deletionとpolicy-driven deletionの責務境界を定義する。

**Revisit trigger**

- production data lifecycleを正式運用するとき。
- Artifact/Metadata volumeが継続的に増加し自動削除が必要になったとき。
- retention policyを外部運用要件として管理する必要が生じたとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| FR-126 | MISMATCH | NOT_IMPLEMENTED | Configurable retention/deletion policy | 要求方向は合理的だが独立したretention/deletion policy設計が必要。 |
| D10-006b | MISMATCH | NOT_IMPLEMENTED | Retention/deletion contract | FR-126と同一root decision。 |

### TD-003 — System-level Operator Authorization

- **Category:** `UNIMPLEMENTED_REQUIREMENT`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `D10-005c`
- **Source IDs:** `D10-005`
- **Finding Groups:** `authorization`

**Target / debt statement**

Project membershipとは独立したsystem/operator-levelのoperational authorization model。

**Current state**

persisted Project roleはOWNER / EDITOR / VIEWERであり、独立したOperator/system-operate role modelは存在しない。

**Why deferred from ENH-E5**

Project-scoped authorization coverageはENH-E5でD2として補完するが、system-level operatorは別のsecurity/operations concernである。

**Impact while deferred**

system-wide administrative operationを正式に導入するまでは問題を顕在化させないが、将来の運用endpointをProject roleへ誤って載せる余地がある。

**Future design considerations**

- ProjectMembershipとsystem-level principal/roleのauthorityを分離する。
- system operationのaction inventoryとauthorization matrixを定義する。
- audit trail、authentication hardening、operational endpointとの接続を設計する。

**Revisit trigger**

- system-wide administrative endpointを導入するとき。
- multi-tenant / production operationsでProject外の権限境界が必要になったとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| D10-005c | MISMATCH | NOT_IMPLEMENTED | Distinct Operator / system-operate authorization | system-level operator modelは独立security/operations enhancementとして延期する。 |

### TD-004 — Resource Control & Execution Limits

- **Category:** `PARTIAL_IMPLEMENTATION`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `FR-128b`, `NFR-017`, `FR-086b`
- **Source IDs:** `FR-128`, `NFR-017`, `FR-086`
- **Finding Groups:** `resource_control`

**Target / debt statement**

upload / rows / columns / memory / timeout等のhard limitと、execution/stage resource policyのconfiguration・persistence。

**Current state**

timeout validationやworker lease等の断片は存在するが、upload/row/column/memory/timeoutを横断する統一resource policyとper-stage persistenceは成立していない。

**Why deferred from ENH-E5**

timeout scope、hard-limit enforcement、memory isolation、configuration/wiringを含む独立runtime governance設計になるためENH-E5では延期する。

**Impact while deferred**

multi-user/untrusted workloadではresource exhaustionや長時間executionのoperability riskが残る。

**Future design considerations**

- Plan timeout、Stage timeout、Worker lease、HTTP timeout等の異なるtimeout概念を分離して定義する。
- upload size、row count、column count、memory、timeoutのlimit authorityとenforcement layerを定義する。
- memory hard limitに必要なprocess/container isolation等の実装方式を評価する。
- effective resource policyをExecution/Stage snapshotへどの粒度で保存するか定義する。

**Revisit trigger**

- multi-user production、untrusted uploads、worker scalingを開始するとき。
- SLA / resource budgeting / execution sandboxが必要になったとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| FR-128b | MISMATCH | NOT_IMPLEMENTED | Operational size/timeout configuration | resource policyの独立設計が必要なため延期する。 |
| NFR-017 | MISMATCH | NOT_IMPLEMENTED | Explicit upload/row/column/memory/timeout hard limits | 包括的resource control/sandbox設計が必要。 |
| FR-086b | PARTIAL_MATCH | PARTIAL | Per-stage timeout/resource limit persistence | resource control decisionへ統合して延期する。 |

### TD-005 — Object-storage ArtifactStore Adapter

- **Category:** `PARTIAL_IMPLEMENTATION`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `NFR-020b`, `D22-003b`
- **Source IDs:** `NFR-020`, `D22-003`
- **Finding Groups:** `storage_portability`

**Target / debt statement**

既存ArtifactStore Portを維持したまま、Local filesystemとobject storageを切り替えられるadapter/wiring。

**Current state**

ArtifactStore PortとLocalArtifactStoreは存在するが、object-storage adapterと切替configurationは存在しない。

**Why deferred from ENH-E5**

ENH-E5のFamily/Navigation改修には不要で、deployment/storage portabilityとして独立している。

**Impact while deferred**

single-node/local filesystem前提を越えるdeploymentでdurability、shared storage、worker scale-outに制約が残る。

**Future design considerations**

- object key semantics、put/get/delete、visibility/overwrite semanticsをArtifactStore contractと整合させる。
- content hash verification、streaming、failure/retry、backend error mappingを定義する。
- credentials/configuration/dependency injectionの責務を定義する。
- Local/Object-store間でdomain/application contractを変更しないことをacceptanceにする。

**Revisit trigger**

- distributed / multi-worker deploymentへ移行するとき。
- containerized productionでshared durable artifact storageが必要になったとき。
- Artifact durability/scale要件がlocal filesystemを超えたとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| NFR-020b | MISMATCH | NOT_IMPLEMENTED | Object-storage adapter / switching | Portは成立済みだがobject-storage adapterは独立deployment enhancementとして延期する。 |
| D22-003b | PARTIAL_MATCH | PARTIAL | Object-storage / broader adapter variants | future storage portabilityへ送る。 |

### TD-006 — Sensitive Column Metadata & Data-use / Output Policy

- **Category:** `PARTIAL_IMPLEMENTATION`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `FR-021`, `FR-123b`, `NFR-009b`
- **Source IDs:** `FR-021`, `FR-123`, `NFR-009`
- **Finding Groups:** `security_privacy`

**Target / debt statement**

column sensitivity/use restriction metadataと、preview・prediction・local explanation・exportへ伝播するconfigurable exposure/minimization policy。

**Current state**

一部のsensitive Result suppressionは存在するが、column metadata taxonomyと横断的なconfigurable policyは成立していない。

**Why deferred from ENH-E5**

classification、policy propagation、authorization、export/output minimizationを横断するgovernance subsystemになるためENH-E5では延期する。

**Impact while deferred**

高度な機微データ運用では、column単位の明示policyとoutput surface間の一貫した制約を表現できない。

**Future design considerations**

- sensitive/use-restriction/description metadataのschemaとauthorityを定義する。
- metadata inheritance / propagation semanticsを定義する。
- preview、Artifact、prediction row、local explanation、exportへのpolicy適用境界を定義する。
- Project authorizationとconfigurable minimization policyの優先関係を定義する。

**Revisit trigger**

- sensitive-data deploymentを正式サポートするとき。
- column-level governanceやconfigurable export/output restrictionが必要になったとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| FR-021 | MISMATCH | NOT_IMPLEMENTED | Sensitive/use-restriction/description column metadata | 合理的な将来targetだが、data-use policy全体へ波及するためENH-E5では延期する。 |
| FR-123b | PARTIAL_MATCH | PARTIAL | Configurable exposure policy based on sensitive metadata | FR-021のfuture governance targetと統合して延期する。 |
| NFR-009b | PARTIAL_MATCH | PARTIAL | Configurable prediction/local-explanation/export minimization | data-use/sensitive-output governance future targetへ統合する。 |

### TD-007 — Exploratory Analytical Surface Expansion

- **Category:** `PARTIAL_IMPLEMENTATION`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `FR-028`, `FR-025b`, `FR-026b`
- **Source IDs:** `FR-028`, `FR-025`, `FR-026`
- **Finding Groups:** `exploratory_workflow`

**Target / debt statement**

joint missing-pattern analysis、correlation/association matrix、scatter/box/crosstab等のExploratory analytical surface拡張。

**Current state**

列別missingnessや一部association/bivariate operationは存在するが、要求されたmatrixおよびfull visualization surface setは未完成。

**Why deferred from ENH-E5**

ENH-E5のFamily/Navigation成立には既存Exploratory capabilityを再配置すれば足り、追加EDA capabilityは独立enhancementとして扱える。

**Impact while deferred**

Exploratory familyの分析surfaceは限定的なままだが、Family/Stage navigationの成立を阻害しない。

**Future design considerations**

- 各operationのinput schema、supported logical type、output Result contractを定義する。
- missing-pattern / association matrixのsize制御と表示/計算責務を定義する。
- scatter / box / crosstab等のsurfaceと既存association operatorの重複を整理する。

**Revisit trigger**

- Exploratory/EDA capability拡張を次回enhancementの主目的にするとき。
- ユーザー要求としてmatrix/bivariate visualization coverageを拡張するとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| FR-028 | MISMATCH | NOT_IMPLEMENTED | Correlation / association matrix operation | Exploratory analytical surface拡張でありENH-E5成立条件ではない。 |
| FR-025b | PARTIAL_MATCH | PARTIAL | Joint missing-pattern analysis | 追加Exploratory analytical capabilityとして延期する。 |
| FR-026b | PARTIAL_MATCH | PARTIAL | Full scatter/box/crosstab surface set | 追加visualization surfaceはfutureへ送る。 |

### TD-008 — Automated Hyperparameter Selection

- **Category:** `UNIMPLEMENTED_REQUIREMENT`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `FR-062`
- **Source IDs:** `FR-062`
- **Finding Groups:** `predictive_scientific`

**Target / debt statement**

validation partitionまたはcross-validationを用いたautomated hyperparameter/model selection。

**Current state**

Predictive validationはnon-empty automated tuning candidateを明示的にunsupportedとして拒否している。

**Why deferred from ENH-E5**

search strategy、CV semantics、scoring、candidate space、reproducibility、compute costを含む独立model-selection capabilityである。

**Impact while deferred**

Predictive familyではmanual/fixed configuration中心となり、自動model-selection workflowは提供されない。

**Future design considerations**

- search strategyとcandidate-space contractを定義する。
- cross-validation / holdout semantics、primary metric、tie-breakingを定義する。
- test-set isolation / leakage preventionとreproducibility snapshotを定義する。
- resource budget / timeoutとの連携をTD-004と整合させる。

**Revisit trigger**

- Predictive model-selection enhancementを実施するとき。
- algorithm registryの拡張と自動選択を同時に扱う必要が生じたとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| FR-062 | MISMATCH | NOT_IMPLEMENTED | Automated hyperparameter selection | 独立したmodel selection capability拡張でありENH-E5では延期する。 |

### TD-009 — Product Orchestration CLI

- **Category:** `UNIMPLEMENTED_REQUIREMENT`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `FR-118`
- **Source IDs:** `FR-118`
- **Finding Groups:** `frontend_navigation_and_state`

**Target / debt statement**

Family別SpecificationをProduct APIへsubmitし、status/resultを取得するheadless Product CLI。

**Current state**

既存CLIはlocal/headless scientific stage実行が中心で、Product submit/poll CLIではない。

**Why deferred from ENH-E5**

ENH-E5ではUI Navigationを改修するが、Product orchestration CLIは直接依存しない。Navigation concernをCLI/library contractへ漏らさない。

**Impact while deferred**

Product workflowのheadless automationはAPIを直接利用する必要がある。

**Future design considerations**

- submit/status/result取得のCLI command surfaceとexit/error semanticsを定義する。
- Product API authentication/authorization/idempotencyとの整合を定義する。
- Navigation StageをCLI contractへ持ち込まないことを明示する。

**Revisit trigger**

- CI/batch/headless product operationを正式サポートするとき。
- UI以外のProduct clientをfirst-class interfaceとして提供するとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| FR-118 | MISMATCH | NOT_IMPLEMENTED | Product submit/poll CLI | current scientific CLIを維持しProduct orchestration CLIは将来拡張へ送る。 |

### TD-010 — Result List Filter Expansion

- **Category:** `UNIMPLEMENTED_REQUIREMENT`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `FR-110b`
- **Source IDs:** `FR-110`
- **Finding Groups:** `frontend_navigation_and_state`

**Target / debt statement**

既存family/type/status等に加え、dataset/context/date等で一覧・比較対象をfilterする機能。

**Current state**

一部filterは存在するが、dataset/context/dateを含む要求surface全体は成立していない。

**Why deferred from ENH-E5**

追加search/filter surfaceはENH-E5のFamily/Navigation成立条件ではない。

**Impact while deferred**

Project内resource量が増えた場合、一覧絞り込みの操作性が低下する可能性がある。

**Future design considerations**

- filterable field、query semantics、combination ruleを定義する。
- API query contractとfrontend stateを一貫させる。
- 必要に応じpagination/indexingへの影響を評価する。

**Revisit trigger**

- large ProjectでResult/Execution inventoryが増え検索性が問題になったとき。
- 一覧/比較UXの改善を独立enhancementとして行うとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| FR-110b | MISMATCH | NOT_IMPLEMENTED | Dataset/context/date filter expansion | 追加検索surfaceはENH-E5成立条件ではない。 |

### TD-011 — Component-level Readiness

- **Category:** `UNIMPLEMENTED_REQUIREMENT`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `FR-127b`
- **Source IDs:** `FR-127`
- **Finding Groups:** `operability`

**Target / debt statement**

APIだけでなくDB、Worker、Artifact Store等を確認するcomponent-level health/readiness contract。

**Current state**

`/health/ready`はbasic statusを返すが、DB/Worker/Artifact Storeのcomponent readinessを検証しない。

**Why deferred from ENH-E5**

正しいreadinessにはcomponent probe、timeout、worker liveness/heartbeat等のoperational contractが必要になる。

**Impact while deferred**

orchestrator/load balancerが依存component failureをreadinessから判定できない。

**Future design considerations**

- livenessとreadinessの意味を分離する。
- DB / Worker / Artifact Store等のprobe responsibilityとtimeoutを定義する。
- degraded / unavailable等のstatus semanticsと外部公開範囲を定義する。

**Revisit trigger**

- production orchestration / container schedulingを導入するとき。
- component failureを自動routing/restart判断へ利用するとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| FR-127b | MISMATCH | NOT_IMPLEMENTED | DB/Worker/Artifact Store component readiness | component readinessは独立operability enhancementとして延期する。 |

### TD-012 — General API Performance SLO & Regression Gate

- **Category:** `UNIMPLEMENTED_REQUIREMENT`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `NFR-004`
- **Source IDs:** `NFR-004`
- **Finding Groups:** `operability`

**Target / debt statement**

通常一覧・詳細APIのp95 performance SLOと、重い処理のasync境界を検証するperformance acceptance。

**Current state**

p95 <= 2秒を保証するbenchmark environment、測定contract、regression gateは確認されていない。

**Why deferred from ENH-E5**

SLOをnormativeにするにはworkload、dataset size、concurrency、warm/cold、測定方法を先に定義する必要がある。

**Impact while deferred**

general product API performanceの定量的regression acceptanceがない。

**Future design considerations**

- 代表workload、dataset size、concurrency、warm/cold条件を定義する。
- measurement window、percentile算出、environment、pass/fail thresholdをfreezeする。
- 同期/非同期境界とperformance regression testを定義する。

**Revisit trigger**

- production SLA/SLOを設定するとき。
- performance regressionをrelease gateへ組み込むとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| NFR-004 | MISMATCH | NOT_IMPLEMENTED | General p95 API SLO / performance regression gate | benchmark environment等を伴う独立performance workとして延期する。 |

### TD-013 — Canonical Schema Example Synchronization

- **Category:** `PARTIAL_IMPLEMENTATION`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `FR-120b`
- **Source IDs:** `FR-120`
- **Finding Groups:** `architecture_overstatement`

**Target / debt statement**

OpenAPI/runtime schemaとcanonical Schema exampleを体系的に同期・検証する仕組み。

**Current state**

FastAPIによるOpenAPI生成は存在するが、canonical example全体のsystematic synchronizationは成立していない。

**Why deferred from ENH-E5**

ENH-E5のdirect dependencyではなく、documentation/API toolingとして独立して改善できる。

**Impact while deferred**

example driftをCIで網羅的に検出できず、外部利用者向けexampleの信頼性が手作業に依存する。

**Future design considerations**

- canonical exampleのauthorityと配置を定義する。
- runtime/schema validationでexampleをCI検証する。
- OpenAPI exampleとhandwritten documentation exampleの重複authorityを排除する。

**Revisit trigger**

- 外部API consumer / SDK / integration documentationを正式提供するとき。
- schema example driftが継続的なmaintenance issueになったとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| FR-120b | PARTIAL_MATCH | PARTIAL | Systematic canonical schema-example synchronization | 全exampleの同期/検証基盤はENH-E5のdirect dependencyではない。 |

### TD-014 — Metadata / Artifact Cross-store Failure Compensation

- **Category:** `PARTIAL_IMPLEMENTATION`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `NFR-007`
- **Source IDs:** `NFR-007`
- **Finding Groups:** `worker_reliability`

**Target / debt statement**

Metadata transactionとArtifact write/deleteの跨ぎ失敗に対する補償・再試行protocol。

**Current state**

Metadata transactionとArtifact storageは存在するが、cross-store failureを一貫して補償するcomplete protocolは成立していない。

**Why deferred from ENH-E5**

transaction boundaryを跨ぐfailure state、orphan cleanup、retry/idempotencyを設計する独立reliability workになる。

**Impact while deferred**

特定failure timingでmetadata/artifactのorphanまたは不整合を手動回復する可能性が残る。

**Future design considerations**

- write/commit orderingとfailure-state taxonomyを定義する。
- orphan Artifact / dangling metadataの検出・cleanup semanticsを定義する。
- retry/idempotencyとcompensation actionをNFR-006b/TD-005/TD-002と整合させる。

**Revisit trigger**

- object storageやdistributed workerへ拡張するとき。
- cross-store failureの実運用incidentが発生したとき。
- durability/consistencyをproduction acceptanceとして強化するとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| NFR-007 | PARTIAL_MATCH | PARTIAL | Metadata/Artifact cross-store failure compensation | 独立したcross-store compensation protocolとして延期する。 |

### TD-015 — Production-grade Authentication / System Security Hardening

- **Category:** `PARTIAL_IMPLEMENTATION`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `NFR-008c`
- **Source IDs:** `NFR-008`
- **Finding Groups:** `security_privacy`

**Target / debt statement**

既存validation/path safeguardおよびProject authorizationを越えたproduction-grade authentication/system security hardening。

**Current state**

入力validation/path safeguard等は一部存在するが、production-grade authentication/system security configurationを包括的に成立させてはいない。

**Why deferred from ENH-E5**

authentication provider、security boundary、secret/configuration、threat modelを含む独立security enhancementである。

**Impact while deferred**

現在のdeployment前提を超えてinternet-facing/multi-user productionへ移行する際に追加hardeningが必要。

**Future design considerations**

- authentication authorityとprincipal lifecycleを定義する。
- Project authorization / system Operator authorizationとの接続を定義する。
- security-sensitive configuration/secret handlingとroute coverageを監査可能にする。
- production threat modelに基づくacceptanceを定義する。

**Revisit trigger**

- internet-facingまたはmulti-user productionへ移行するとき。
- external identity provider等とのintegrationが必要になったとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| NFR-008c | PARTIAL_MATCH | PARTIAL | Production-grade authentication/system security hardening | 独立security enhancementとして延期する。 |

### TD-017 — Worker Restart / Resume Semantics

- **Category:** `PARTIAL_IMPLEMENTATION`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `NFR-010b`
- **Source IDs:** `NFR-010`
- **Finding Groups:** `worker_reliability`

**Target / debt statement**

API/Worker process separationの上で、worker restart時のexecution interruption / retry / resume可否を明示するcontract。

**Current state**

APIとWorkerは分離され、lease/claim/retryの基盤はあるが、restart/resume semantics全体は明示されていない。

**Why deferred from ENH-E5**

長時間job recovery、stage state、lease expiry、resume/restart classificationを含む独立worker reliability設計になる。

**Impact while deferred**

worker restart後に何が自動回復し、何がretry/restartを必要とするかのoperational predictabilityが限定的。

**Future design considerations**

- Stageごとのresumable / restartable / terminal classificationを定義する。
- lease expiry、claim recovery、retry counter、artifact commitとの整合を定義する。
- user-visible statusとrecovery actionを定義する。
- restart/recovery integration testを追加する。

**Revisit trigger**

- long-running production jobが増えるとき。
- worker rolling restart / autoscalingを正式運用するとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| NFR-010b | PARTIAL_MATCH | PARTIAL | Explicit restart/resume semantics | 独立worker reliability enhancementとして延期する。 |

### TD-018 — Comprehensive Structured Logging & Metrics

- **Category:** `PARTIAL_IMPLEMENTATION`
- **Ledger Status:** `DEFERRED`
- **Decision Approval:** `APPROVED`
- **Delivery:** `FUTURE`
- **Source Decision Items:** `NFR-011b`
- **Source IDs:** `NFR-011`
- **Finding Groups:** `worker_reliability`

**Target / debt statement**

request / execution / stage correlationを保ったstructured logとoperational metricsの統一contract。

**Current state**

request/execution/stage identifiers等のlogging contextは存在するが、structured schemaとmetrics coverageは全体で統一されていない。

**Why deferred from ENH-E5**

observability schema、metric semantics、redaction、cardinality等を横断的に決める必要があるため独立enhancementとする。

**Impact while deferred**

production troubleshooting、capacity analysis、SLO monitoringの自動化が限定的。

**Future design considerations**

- structured log field schemaとcorrelation semanticsを定義する。
- execution/stage/APIのmetric inventory、unit、labels/cardinalityを定義する。
- sensitive data redactionとlogging boundaryを定義する。
- performance/readiness/auditとの重複を整理する。

**Revisit trigger**

- production observabilityを正式運用するとき。
- SLO / alerting / incident responseを導入するとき。

**Source trace**

| Decision Item | Original Alignment | Impl. Status | Deferred Substatement | D3 rationale |
|---|---|---|---|---|
| NFR-011b | PARTIAL_MATCH | PARTIAL | Comprehensive structured logging + metrics | observability overhaulとして延期する。 |

---

## 7. RESOLVED / PROMOTED ITEMS

現時点ではなし。

将来itemをpromoteする場合、元entryを削除せず以下を記録する。

- new status: `PROMOTED` または `RESOLVED`
- promoted delivery / Enhancement ID
- new Requirement/Design IDs
- promotion decision date / record
- implementation/test completion evidence

---

## 8. CHANGE LOG

| Date | Revision | Change |
|---|---|---|
| 2026-08-12 | Initial | `remediation_decision_matrix.csv`のD3 28件を17 root TDへ収束。derived test-scope 2件を別管理。Freeze auditのconditional approval stateを反映。 |

---

## APPENDIX A. D3 TRACEABILITY CHECK

- D3 source rows: **28**
- Section 3 NOT_IMPLEMENTED rows: **15**
- Section 4 PARTIAL rows: **13**
- Root TD referenced rows: **26**
- Derived rows without standalone TD: **2** (`D22-013c`, `D30-018c`)
- Unmapped D3 rows: **0**

このappendixはledger generation時のcompleteness checkであり、remediation decision自体のauthorityではない。
