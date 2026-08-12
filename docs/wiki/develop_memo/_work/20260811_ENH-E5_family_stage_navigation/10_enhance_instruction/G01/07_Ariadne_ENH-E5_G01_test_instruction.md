# Ariadne ENH-E5 G01 — URL-driven Family / Stage Navigation Shell — Verification

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G01`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
- 契約状態: `APPROVED / FROZEN`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = APPROVED`
- Document role: `Gate 07 verification contract`

## 0. Authority / verification isolation

- 本文書は、このGateを検証する**Test / Audit Agentに対する唯一のnormative verification contract**である。
- Test / Audit Agentは期待挙動を補完するためにGate `06`、`Pxx`、`P00`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repository、candidate diff、test output、migration state、API responseはverification evidenceとして参照してよいが、仕様authorityではない。
- 本文書だけでPASS / FAILを一意に判定できない場合は`BLOCKED_CONTRACT_AMBIGUITY`として報告し、仕様を発明しない。


### Canonical Navigation Catalog

| family | slug | default_stage_id | stages in deterministic order |
|---|---|---|---|
| `EXPLORATORY` | `exploratory` | `profile` | `profile`, `data-quality`, `distribution`, `relationships`, `comparison`, `findings` |
| `PREDICTIVE` | `predictive` | `setup` | `setup`, `train`, `predict`, `metrics`, `explainability`, `model-management` |
| `CAUSAL` | `causal` | `setup` | `setup`, `discovery`, `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity` |

Canonical metadata response fields:

```text
schema_version = "analysis-navigation/1"
families[].family
families[].slug
families[].label
families[].default_stage_id
families[].stages[].stage_id
families[].stages[].slug
families[].stages[].label
families[].stages[].order
```

Required invariants:

- Family descriptorは`EXPLORATORY / PREDICTIVE / CAUSAL`各1件。
- Family slugはglobalに一意。
- `stage_id / slug`はFamily内で一意。
- `default_stage_id`は当該FamilyのStage内に存在。
- Stage orderはdeterministic。
- `stage_id == slug`をENH-E5 canonical valueとする。
- runtime input/output/status/retry/attempt/leaseをNavigation metadataへ含めない。
- Navigation descriptorをpersistent Domain Resource、Repository、UoWへ登録しない。
- catalogからruntime `StageType / StageDefinition / StageExecution`を生成しない。


### Canonical Route Contract

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}

/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

ENH-E5 `resource_type`:

```text
analysis-specification
execution
result
graph-version
```

Rules:

- explicit Family/Stage deep routeはrouteのStageを保持する。
- generic direct resource linkからdeep routeを構築する場合はresourceからFamilyをderiveし、そのFamily default Stageへ遷移する。
- resource actual Familyとexplicit route Familyが不一致ならexplicit mismatch error。silent normalizationは禁止。
- unknown Family / Stage / resource typeはdeterministic not-found/unsupported error。
- routeはpresentation stateでありResource/Executionへpersistしない。
- direct open / reload / browser back-forwardはURLから同じNavigationContextを復元する。
- legacy routeを残す場合は一方向normalize:
  - `/explore -> /projects/{project_id}/analysis/exploratory/profile`
  - `/predictive -> /projects/{project_id}/analysis/predictive/setup`
  - `/causal -> /projects/{project_id}/analysis/causal/setup`


### Operation Availability Contract

Operation availabilityのcanonical ENH-E5 interface:

```text
GET /projects/{project_id}/operation-availability
```

本endpointはFrontend向けのread-only projectionであり、authorization bypass、scientific validation bypass、Execution commandそのものではない。実commandのauthorization / lifecycle / scientific validationが最終authorityであり、本projectionとの不一致はimplementation defectとして扱う。

#### Canonical operation key set

`operations` mapのkeyは次の3値だけをcanonicalとする。

```text
RUN
EDIT
EXPORT
```

このkey setはclosed setである。ENH-E5で`CREATE / DELETE / CANCEL / RETRY / RERUN / REVISE / DOWNLOAD`等を追加keyとして返してはならない。

- `RUN`: analytical executionを開始、または既存Executionを基点に既存のretry/rerun/revise系run-family commandを開始できるかを表すpresentation operation class。
- `EDIT`: mutable analytical resourceを既存mutation contractで編集できるかを表すpresentation operation class。
- `EXPORT`: Resultを既存export contractでexportできるかを表すpresentation operation class。

`RUN`はcanonical `Execution.operation` discriminator (`DISCOVERY / IDENTIFICATION / ESTIMATION / REFUTATION / SENSITIVITY`等)とは別conceptである。Navigation Stage名、runtime StageType、endpoint verbをoperation keyへ1:1転写しない。

Responseは常に3 keyすべてを返す。

```json
{
  "operations": {
    "RUN": {"allowed": false, "reason_code": "SPEC_NOT_FIXED", "message": "Fix the specification first."},
    "EDIT": {"allowed": true},
    "EXPORT": {"allowed": false, "reason_code": "UNSUPPORTED_OPERATION"}
  }
}
```

Operation item contract:

```text
allowed: bool
reason_code?: string
message?: string
```

- `allowed=true`では`reason_code`を返してはならない。`message`は原則返さない。
- `allowed=false`では`reason_code`を必須とする。`message`はoptional human-readable explanationでありFrontend logicの判定材料にしてはならない。
- top-level `operations` mapはrequired。

#### resource_type × operation structural support

`resource_type`は次の4値だけを受理する。

```text
analysis-specification
execution
result
graph-version
```

Structural support matrix:

| resource_type | RUN | EDIT | EXPORT |
| --- | --- | --- | --- |
| `analysis-specification` | supported | supported | unsupported |
| `execution` | supported | unsupported | unsupported |
| `result` | supported | unsupported | supported |
| `graph-version` | supported | supported | unsupported |

意味:

- `analysis-specification/RUN`: FIXED specificationを基点に既存Execution submission contractを利用する。
- `analysis-specification/EDIT`: AnalysisSpecification lifecycleがmutationを許可する場合だけ許可する。
- `execution/RUN`: 既存Execution lifecycleが許可するretry/rerun/revise等のrun-family commandの少なくとも1つへ進める場合に許可する。新しいgeneric run commandを作らない。
- `result/RUN`: 現在のroute/use-caseが既存`input_result_id`を受けるanalytical commandへ対応する場合にのみ候補となる。route/use-case上対応しなければ`UNSUPPORTED_OPERATION`。
- `result/EXPORT`: 既存Result export / Project-scoped export policyへ委譲する。
- `graph-version/RUN`: 現在のroute/use-caseが既存`input_graph_version_id`を受けるcausal commandへ対応する場合にのみ候補となる。
- `graph-version/EDIT`: GraphVersion lifecycleがmutationを許可する場合だけ許可する。

matrixで`unsupported`の組合せはHTTP 200のまま`allowed=false, reason_code=UNSUPPORTED_OPERATION`を返す。

#### Query contract

Query parameter:

```text
resource_type?: string
resource_id?: string
route?: string
```

必須・任意条件:

1. `resource_type`と`resource_id`はpairである。両方指定または両方未指定のみ有効。
2. pairの片方だけを指定したrequestはHTTP 422 / `INVALID_OPERATION_AVAILABILITY_QUERY`。
3. resource pairを指定しない場合、`route`は必須。3 parameterすべて未指定はHTTP 422 / `INVALID_OPERATION_AVAILABILITY_QUERY`。
4. resource pairを指定した場合、`route`はoptional。ただし`result/RUN`または`graph-version/RUN`のようにresourceだけではscientific use-caseを一意に決められないoperationでは、`RUN.allowed=false, reason_code=ROUTE_REQUIRED`とする。
5. `route`はcanonical browser routeをpresentation contextとして渡す。routeはresource identity、authorization identity、scientific truthのauthorityではない。
6. `route`にresource segmentが含まれる場合、その`resource_type/resource_id`はquery pairと一致しなければならない。
7. explicit route Familyとresolved resource Familyが不一致の場合はHTTP 422 / `ROUTE_RESOURCE_FAMILY_MISMATCH`。silent normalizationしない。

resource未指定時semantics:

- `route`だけを指定したrequestは有効である。
- Backendはrouteからresource IDを推測・自動選択してはならない。
- concrete resourceを必要とするcanonical operationは`allowed=false, reason_code=RESOURCE_REQUIRED`を返す。
- operation availability queryを理由にAnalysisSpecification / Execution / Result / GraphVersionを生成・変更してはならない。

#### Authorization class

endpoint自体のreadにはProject-scoped `READ` authorizationを適用する。ProjectMembershipをresolveできない、またはREAD不可の場合はHTTP 403 / `PROJECT_ACCESS_DENIED`でrequest全体を拒否する。

各canonical operationのauthorization class:

| operation | authorization class | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- | --- |
| `RUN` | `EXECUTION_MUTATION` | allow | allow | deny |
| `EDIT` | `WRITE_MUTATE` | allow | allow | deny |
| `EXPORT` | `EXPORT_CREATE` | allow | allow | deny |

Structural support判定後、scientific/domain prerequisite判定前にoperation authorizationを評価する。structurally supported operationでrole不足の場合、HTTP 200のoperation itemとして`allowed=false, reason_code=PROJECT_ACCESS_DENIED`を返す。

#### Scientific/domain prerequisite authority

scientific/domain prerequisiteのauthorityは**実際のcommandを検証するApplication/Domain policy / validator / lifecycle service**である。Operation Availability専用にscientific ruleを複製してはならない。

最低限、次のauthority境界を維持する。

- AnalysisSpecification lifecycle / validation: specification domain/application validator。
- GraphVersion lifecycle / validation: graph domain/application validator。
- Execution retry/rerun/revise可否: Execution lifecycle/application service。
- Causal input prerequisite (`input_graph_version_id / input_result_id`, identification prerequisite等): causal planner/use-case validation + persisted Result/Lineage。
- Result exportability: Result / output ownership / export policy。
- Project role: persisted ProjectMembership policy。

Evaluation order:

```text
query validation
  -> Project READ authorization
  -> resource resolution / project boundary
  -> resource_type × operation structural support
  -> per-operation authorization
  -> lifecycle mutability/state
  -> scientific/domain prerequisite
  -> allowed=true
```

Frontend、browser route、Navigation Stage visibilityはscientific/domain prerequisite authorityではない。

#### Unknown resource / unsupported operation semantics

- unknown `resource_type`: HTTP 422 / `UNSUPPORTED_RESOURCE_TYPE`。
- known `resource_type` + `resource_id`が当該Project内で解決できない場合（別ProjectのIDを含む）: HTTP 404 / `ENTITY_NOT_FOUND`。cross-project existenceを開示しない。
- malformed/unknown canonical route: HTTP 422 / `INVALID_NAVIGATION_ROUTE`。
- route/resource Family mismatch: HTTP 422 / `ROUTE_RESOURCE_FAMILY_MISMATCH`。
- structural matrixまたはroute/use-case上unsupportedなcanonical operation: HTTP 200、`allowed=false, reason_code=UNSUPPORTED_OPERATION`。
- responseは非canonical operation keyを返してはならない。内部実装でunknown operation keyが要求された場合はfail closedし、configuration/programming defectとして扱う。

#### reason_code taxonomy

ENH-E5 Operation Availabilityのoperation item `reason_code`は次のclosed vocabularyとする。

| reason_code | class | meaning |
| --- | --- | --- |
| `PROJECT_ACCESS_DENIED` | authorization | roleが当該operationを許可しない |
| `UNSUPPORTED_OPERATION` | structural | resource type / route use-caseがoperationを提供しない |
| `RESOURCE_REQUIRED` | query/context | concrete resourceが必要だが指定されていない |
| `ROUTE_REQUIRED` | query/context | resourceだけではRUN use-caseを一意に決められない |
| `RESOURCE_IMMUTABLE` | lifecycle | resource lifecycleがEDIT等のmutationを許可しない |
| `SPEC_NOT_FIXED` | lifecycle/domain | AnalysisSpecificationがRUN可能なfixed stateでない |
| `GRAPH_NOT_FIXED` | lifecycle/domain | GraphVersionがRUN inputとしてfixed stateでない |
| `IDENTIFICATION_REQUIRED` | scientific | estimation等に必要なidentification prerequisiteが未成立 |
| `INPUT_GRAPH_REQUIRED` | scientific | current commandに必要なGraphVersion inputがない |
| `INPUT_RESULT_REQUIRED` | scientific | current commandに必要なResult inputがない |
| `EXECUTION_STATE_NOT_RUNNABLE` | lifecycle | Executionに利用可能なrun-family transitionがない |
| `RESULT_NOT_EXPORTABLE` | lifecycle/domain | Result/export policyがexportを許可しない |
| `DOMAIN_PREREQUISITE_NOT_SATISFIED` | domain | 上記個別codeへ分類できない既存domain prerequisiteが未成立 |

Request-level error codeは次を使用する。

```text
INVALID_OPERATION_AVAILABILITY_QUERY
UNSUPPORTED_RESOURCE_TYPE
ENTITY_NOT_FOUND
PROJECT_ACCESS_DENIED
INVALID_NAVIGATION_ROUTE
ROUTE_RESOURCE_FAMILY_MISMATCH
```

ENH-E5実装でad-hoc reason codeを追加してはならない。新しいcodeが必要な場合はcanonical design amendmentを先に行う。

Stage visibilityとaction availabilityは別contractとする。`allowed=false`をStage自体の非表示で表現することを基本挙動にしない。
## Gate Acceptance Criteria

- `AC-G01-001`: canonical Stage/resource routesとresource typesがexact。
- `AC-G01-002`: URL/application stateがcurrent Family/Stage authorityでDB persistenceなし。
- `AC-G01-003`: explicit deep route、generic resource link、Family mismatch、unknown Family/Stageのrulesが本文どおり。
- `AC-G01-004`: legacy routeを保持する場合は本文の一方向mappingのみ。
- `AC-G01-005`: Family clickはtarget Family default Stageへ、Stage clickはFamilyを維持してselected Stageへ遷移。
- `AC-G01-006`: frontend full catalog duplicate ownershipなし。renderer missing/catalog invariant failureをsilent fallbackしない。
- `AC-G01-007`: operation availability endpoint/queryとtop-level `operations` map + `{allowed, reason_code?, message?}` item contractを利用し、Stage visibilityとaction availabilityを分離。
- `AC-G01-008`: async presentation state=`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`。
- `AC-G01-009`: E5変更surfaceはkeyboard、deterministic focus、accessible name、error association、non-color semantics、required contrastを満たす。


## Verification architecture

- unit: route parse/serialize/normalize、mismatch/unknown。
- API/integration: catalog consumption、operation availability endpoint/query/response。
- browser: Family click default Stage、sidebar current Family/order、explicit deep route、generic resource deep link、reload/back-forward。
- negative: renderer missing/catalog invalid、`allowed=false`でStage hiddenにしない、silent normalization禁止。
- accessibility: keyboard/focus/accessible name/error/non-color/contrast。
- static: frontend full catalog duplicate ownership、Navigation->runtime Stage生成依存が0件。

## Change Log

### 2026-08-12 — AMEND-001

G01/P02 Trial01 で検出された Operation Availability Contract ambiguity の remediation に伴い、Gate 07 verification contract を canonical design / P02 execution contract と再収束した。

- Amendment type: `CONTRACT_DEFECT_CORRECTION`
- ENH-E5 scope change: `NO`
- G01 semantic claim change: `NO`
- Verification intent change: `NO`
- Contract clarification/completion: `YES`
- Trigger evidence: `20_implementation_reports/G01/Trial01/packages/E5-G01_01_P02__status.md`
- Detection commit: `e5035b7e9d6d954eaba9373a27b564ce070821a7`
- Amendment ledger: `00_enhance_background/80_contract_amendment_log.md#amend-001-g01-operation-availability-contract-completion`
