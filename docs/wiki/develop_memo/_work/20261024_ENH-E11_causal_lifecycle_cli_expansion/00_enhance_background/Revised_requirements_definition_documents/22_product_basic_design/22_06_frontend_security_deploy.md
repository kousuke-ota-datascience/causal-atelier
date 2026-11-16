<!-- ENH-E11 split working copy: not a formal approval. -->
# 22 — frontend security deploy

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [22_product_basic_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/22_product_basic_design.md) · blob `87196f2f03a7f3367724bc05fb254d1a4d98109e`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 14. Frontend State Design

Frontend stateは次の責務へ分離する。

- server state: API query cache
- Project route state: Project list/registerまたはProject / Project section
- Analysis route state: Project / Family / Navigation Stage / optional resource identity
- Analysis Context selection: Research Context / Dataset Version / Analysis View
- draft state: unsaved form
- authoritative resource state: backend Resource status
- async presentation state: `IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`

Authority rule:

1. Analysis WorkspaceのCurrent ProjectはURL `project_id`をauthorityとしread-only。
2. Current Family / Navigation Stageはcanonical Analysis route / application navigation stateをauthorityとする。
3. Research Context / Dataset Version / Analysis Viewはcurrent Projectと整合するexisting resource/stateだけを復元する。
4. Dataset Version変更でAnalysis Viewが互換でなくなればAnalysis View selectionを解除する。
5. context selection不足だけを理由にFamily / Stage routeを書き換えない。
6. Family / Navigation StageをDB/workspace persistent stateへ昇格させない。
7. Predictive等のdraft inputをStage切替で不必要に破棄しない。
8. Button enablementはclient local stateだけで決定せず、backend validation / operation availabilityを利用する。

Backend action availabilityは最低限`{allowed, reason_code?, message?}`を返し、action visibilityとaction allowedを別conceptとして扱う。


## 15. Security Design

### 15.1 Current request identity

現行実装のWeb APIには共通Bearer/OIDC authentication middlewareは存在しない。request identityが必要なrouterでは`X-User-Id`を読み、未指定時は`anonymous`として扱う実装がある。

Request correlationは`X-Request-Id`をmiddlewareで受理し、未指定時はUUIDを生成してresponse headerへ返す。

したがってCurrent architectureでは、Navigation改修を理由に「production OIDCが既に成立している」と仮定しない。Authentication hardeningは別scopeである。

### 15.2 Project membership

Project Closure領域のProject roleは次の3値である。

- `OWNER`
- `EDITOR`
- `VIEWER`

`ProductClosureService`ではreadを`OWNER / EDITOR / VIEWER`、writeを`OWNER / EDITOR`へ許可する。Project作成時にはrequestの`X-User-Id`をownerとしてmembership登録する。

**全project-scoped route**はservice action前にProject membership authorizationを通す。routerごとの実装差異をauthorization bypassの理由にしてはならない。

Role/action matrix:

| Action | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- |
| READ | allow | allow | allow |
| WRITE / MUTATE | allow | allow | deny |
| Execution mutation | allow | allow | deny |
| Export create | allow | allow | deny |
| Membership admin | allow | deny | deny |
| Explicit sensitive output | allow | allow | deny |

独立`EXECUTE` roleは追加しない。system-level Operator authorizationは`DEFERRED` scopeである。

### 15.3 Artifact / sensitive output

Artifact downloadはcontent hashを検証して返す。Project-scoped closure downloadでは`Content-Disposition`、`Digest`、`X-Content-Type-Options: nosniff`、`Cache-Control: private, no-store`を付与する。

Prediction / local explanation等のsensitive output policyをNavigation Stage名称で緩和しない。

prediction row / local explanation row/detailはpotentially sensitive outputとして扱う。VIEWERにはaggregate/suppressed viewのみ許可し、explicit sensitive detailはOWNER/EDITORに限定する。configurable sensitive-column metadata/policyは`DEFERRED`でありcurrent mandatory designへ含めない。


### 15.4 Command Idempotency / Retry-safe Artifact Commit

Idempotency対象は「全POST/create」ではなく、retryでduplicate durable side effectを生成し得るCommandである。Scopeは`(project_id, command_scope, idempotency_key)`。

- required key missing: `IDEMPOTENCY_KEY_REQUIRED`
- same key + same canonical semantic request: stored response replay、duplicate side effectなし
- same key + different request: HTTP 409 `IDEMPOTENCY_CONFLICT`
- natural idempotency/uniquenessが成立するCommandへheaderを機械的に要求しない
- exactly-once executionは保証しない

Artifact materializationはlogical Execution/Stage/output slot/typeからdeterministic identity/object keyを導出し、same logical output + same content hashはreuse、different content hashはnondeterministic-output conflictとする。Result/Artifact bindingは可能な限りmetadata transaction内でcommitする。cross-store compensationは`DEFERRED` scopeである。



## 16. Deployment

現行実装ではFastAPI Web API、polling Worker、Product persistence DB、ArtifactStore Port（default LocalArtifactStore）が分離されている。Family / Navigation Stage導入のために別runtime execution serviceを新設しない。


## 17. Failure Model

| Failure | 扱い |
| --- | --- |
| Navigation descriptor invalid | startup/query validation error。runtime execution failureへ変換しない |
| Unknown Family / Stage route | explicit 4xx / unsupported state。silent fallbackしない |
| Renderer binding missing | presentation/configuration defectとして検出 |
| Validation rejection | Executionを作成せず4xxまたはREJECTED Command Result |
| Technical runtime stage failure | Stage FAILED、Execution FAILED、既存retry policy |
| Analytical prerequisite unmet | Result/operation availabilityとして表現。Navigation Stage存在自体とは分離 |
| Artifact read integrity failure | `ArtifactHashMismatch`として扱い、破損contentを正常として返さない |
| Client disconnect | server-side Execution継続。cancelは明示Command |


## 18. Schema / Dependency Boundary

- `analysis-specification/1`の既存`analysis_family`を再利用する。
- Navigation Stage fieldをAnalysisSpecificationへ追加しない。
- ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない。
- Product Domainはbrowser route/navigation implementationへ依存しない。
- Scientific / ML / visualization libraryはPort / Adapter背後へ隔離する。
- Capability固有Adapterはcanonical runtime lifecycleを制御しない。
- Navigation metadata/stateについてはDB migrationを行わない。
- Reproducibility contractとして`StageAttempt.effective_random_seed: int | null`を追加するDB migrationを行う。
- `Execution.runtime_version_json`へ`ariadne_code_version / python_version / platform_system / platform_release / machine / libraries`を保存する。


## 19. Test Architecture

Current design concernを次のtest layerへtraceする。

- domain invariant / typed filter / scientific guard → unit/domain test
- persistence / StageAttempt seed / concurrency / idempotency / authorization / lineage → integration test
- route/header/error/response/authorization → API contract test
- Navigation/deep link/history/async state/accessibility → frontend/browser test
- Navigation→runtime import prohibition / optional future dependency prohibition → architecture/static test
- Planner golden / Plan DAG / Runner contract / worker lifecycle → workflow regression
- CLI / library direct execution → headless regression
- Predictive existing setting/spec parity → compatibility regression
- Causal scientific benchmark / Predictive leakage/split/subgroup → scientific test
- Family横断browser E2E

`DEFERRED` concern（general AuditLog、retention、object storage、hard limits、production auth hardening、cross-store compensation等）のtest targetをcurrent mandatory acceptanceへ混ぜない。
