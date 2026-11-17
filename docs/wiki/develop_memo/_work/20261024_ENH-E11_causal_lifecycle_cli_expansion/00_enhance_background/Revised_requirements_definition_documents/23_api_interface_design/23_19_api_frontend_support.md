# 23_19_api_frontend_support — Frontend Support Web API仕様

## 1. API概要

- 対象: Frontend Support のHTTP契約。
- Base path: `/api/v1`。
- 本改訂はOwner採用の**Operation単位Request/Response/Errors定義**を対象とする。実行時PASSや要件変更を含まない。
- Source snapshot: `2068b3b2f8c096d581a0f2d56047c4185c5ac7cc`。CURRENTと未検証事項を分離する。

## 2. エンドポイント一覧

| No. | HTTP | Path | Handler | HTTP Success |
|---:|---|---|---|---|
| 1 | `GET` | `/api/v1/projects/{project_id}/operation-availability` | `operation_availability` | `200` |
| 2 | `GET` | `/api/v1/projects/{project_id}/workspace-state` | `workspace_state` | `200` |
| 3 | `PUT` | `/api/v1/projects/{project_id}/workspace-state` | `update_workspace_state` | `200` |
| 4 | `PUT` | `/api/v1/projects/{project_id}/members/{user_id}` | `set_member_role` | `200` |
| 5 | `GET` | `/api/v1/navigation/analysis` | `get_analysis_navigation` | `200` |

## 3. 共通Error Response形式

CURRENTのDomainError/RequestValidationError Handlerは`application/problem+json`ではなく、以下のJSON envelope。

```json
{"error":{"code":"INVALID_REQUEST","message":"Request validation failed.","details":{},"request_id":"{request_id}"}}
```

共通Handlerに定義されたErrorがすべてのOperationから発生するとは限らない。下表の条件付きErrorはテストPASS済みという意味ではない。

## 4. エンドポイント詳細

### 4.1 `GET /api/v1/projects/{project_id}/operation-availability`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-19-01` |
| Method / Path | `GET /api/v1/projects/{project_id}/operation-availability` |
| Handler | `product_closure.py::operation_availability` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |

**Query parameters**

| 項目 | 型 | default |
|---|---|---|
| `resource_type` | `str \| None` | `None` |
| `resource_id` | `str \| None` | `None` |
| `route` | `str \| None` | `None` |

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: JSON object（Router/Serviceのdict）。

| 項目 | 意味・型 |
|---|---|
| `allowed` | Source返却キー（値の詳細型はService/Schema依存） |


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.2 `GET /api/v1/projects/{project_id}/workspace-state`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-19-02` |
| Method / Path | `GET /api/v1/projects/{project_id}/workspace-state` |
| Handler | `product_closure.py::workspace_state` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: JSON object（Router/Serviceのdict）。

| 項目 | 意味・型 |
|---|---|
| `schema_version` | Source返却キー（値の詳細型はService/Schema依存） |
| `project` | Source返却キー（値の詳細型はService/Schema依存） |
| `current_role` | Source返却キー（値の詳細型はService/Schema依存） |
| `research_context_version_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `dataset_version_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `analysis_view_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `unsaved_draft` | Source返却キー（値の詳細型はService/Schema依存） |
| `updated_at` | Source返却キー（値の詳細型はService/Schema依存） |


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `none`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.3 `PUT /api/v1/projects/{project_id}/workspace-state`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-19-03` |
| Method / Path | `PUT /api/v1/projects/{project_id}/workspace-state` |
| Handler | `product_closure.py::update_workspace_state` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `WorkspaceSelectionUpdate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `research_context_version_id` | `str \| None` | 任意 | 許可 | None |
| `dataset_version_id` | `str \| None` | 任意 | 許可 | None |
| `analysis_view_id` | `str \| None` | 任意 | 許可 | None |
| `unsaved_draft` | `bool \| None` | 任意 | 許可 | None |

**Request JSON例（schema由来の説明用）**

```json
{}
```

#### Response

- HTTP **200**。Response: Service/Router Sourceの返却Object。

| Field | Type | 根拠 |
|---|---|---|
| `schema_version` | `string` | Source上の返却Field |
| `project` | `object` | Source上の返却Field |
| `current_role` | `string` | Source上の返却Field |
| `research_context_version_id` | `string\|null` | Source上の返却Field |
| `dataset_version_id` | `string\|null` | Source上の返却Field |
| `analysis_view_id` | `string\|null` | Source上の返却Field |
| `unsaved_draft` | `boolean` | Source上の返却Field |
| `updated_at` | `datetime\|null` | Source上の返却Field |

**条件:** ProductClosureService.update_workspace_state→workspace_state。schema_version=workspace-selection/1。projectはproject_id/name/status/topic/objective/memoを含む

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `WorkspaceSelectionUpdate`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.4 `PUT /api/v1/projects/{project_id}/members/{user_id}`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-19-04` |
| Method / Path | `PUT /api/v1/projects/{project_id}/members/{user_id}` |
| Handler | `product_closure.py::set_member_role` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

| 項目 | 型 | 必須 |
|---|---|---|
| `project_id` | string | 必須 |
| `user_id` | string | 必須 |

**Query parameters**

なし

**Headers**

| Header | 仕様 |
|---|---|
| `X-User-Id` | Sourceで参照。認証確立の証拠ではない |

**Request Body / Field定義**

Content-Type: `application/json`、型 `ProjectMemberUpdate`

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `role` | `Literal["OWNER", "EDITOR", "VIEWER"]` | 必須 | 不可 | — |

**Request JSON例（schema由来の説明用）**

```json
{
  "role": "OWNER"
}
```

#### Response

- HTTP **200**。Body schema: JSON object（Router/Serviceのdict）。

| 項目 | 意味・型 |
|---|---|
| `project_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `user_id` | Source返却キー（値の詳細型はService/Schema依存） |
| `role` | Source返却キー（値の詳細型はService/Schema依存） |


#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| 400 | INVALID_REQUEST | 型・必須Field等のRequest検証に失敗 | 共通Handler |
| 404 | ENTITY_NOT_FOUND | 対象がなく、ServiceがEntityNotFoundを送出する場合 | 共通Handler。Operationごとの到達は要確認 |
| 409 | PROJECT_ARCHIVED / RESOURCE_IMMUTABLE / EXECUTION_STATE_CONFLICT | 対象がARCHIVED/FIXEDまたは遷移不適格で該当DomainErrorを送出する場合 | 適用可能なOperationのみ、到達は要確認 |
| 403 | PROJECT_ACCESS_DENIED | Project membership/role不足のためClosure Serviceが拒否 | 共通Handler; gateway認証の保証ではない |

#### 根拠・未検証事項

- Router Source: `product_closure.py`（blob `7cae6a3df8725c3f5263ede17167225175f5968e`）。Request DTO: `ProjectMemberUpdate`、Response Model: `未宣言`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

### 4.5 `GET /api/v1/navigation/analysis`

#### 基本情報

| 項目 | 内容 |
|---|---|
| ID | `API-19-05` |
| Method / Path | `GET /api/v1/navigation/analysis` |
| Handler | `navigation.py::get_analysis_navigation` |
| Success Status | HTTP 200 |

#### Request

**Path parameters**

なし

**Query parameters**

なし

**Headers**

Router固有の必須Header宣言なし

**Request Body / Field定義**

Request JSON Bodyなし（Router未定義）。

#### Response

- HTTP **200**。Body schema: `AnalysisNavigationResponse`。

| 項目（wire） | 型 | 必須 | null | 制約・既定値 |
|---|---|---|---|---|
| `schema_version` | `Literal["analysis-navigation/1"]` | 必須 | 不可 | — |
| `families` | `list[FamilyNavigationResponse]` | 必須 | 不可 | — |

**Response JSON構造例（schema由来の説明用）**

```json
{
  "schema_version": "analysis-navigation/1",
  "families": []
}
```

#### Errors

| HTTP | Error Code | 発生条件 | 根拠・状態 |
|---|---|---|---|
| — | 未確定 | Router固有のErrorを宣言せず | ServiceとHandler詳細照合が必要 |

#### 根拠・未検証事項

- Router Source: `navigation.py`（blob `49bf86edf04828a604c20c247163613422d44315`）。Request DTO: `none`、Response Model: `AnalysisNavigationResponse`。
- 未実行: HTTP Contract Test、Serviceの全Error分岐、認可の実効証明。Source宣言を実行済みと扱わない。

## 5. 検証状況

- Route/Method/Path: 5 件 Source確認。
- Request: Router/Pydanticモデルの静的制約を反映。Response: 型付きモデルは全Fieldを表記。Service無型応答は一部未確定。
- HTTP Contract Test: NOT_RUN。Endpoint詳細の完全性・認可・実行時エラー網羅は未検証。
- 元の`docs/wiki/requirement_definition/`への昇格: NOT_DONE。

## 6. 既存Domain・設計制約（旧仕様本文から保持）

以下は既存のDomain規範・補足情報を保持したもの。重複する旧Route一覧より§2（Source基準）を優先する。改訂前の原本文はGit Blob `c323d8b4d66f1019552fc1ac1e238ccf93f858dc`で追跡可能。

### Frontend Support API

#### Operation Availability

Operation availabilityのcanonical current interface:

```text
GET /projects/{project_id}/operation-availability
```

本endpointはFrontend向けのread-only projectionであり、authorization bypass、scientific validation bypass、Execution commandそのものではない。実commandのauthorization / lifecycle / scientific validationが最終authorityであり、本projectionとの不一致はimplementation defectとして扱う。

##### Canonical operation key set

`operations` mapのkeyは次の3値だけをcanonicalとする。

```text
RUN
EDIT
EXPORT
```

このkey setはclosed setである。Current contractで`CREATE / DELETE / CANCEL / RETRY / RERUN / REVISE / DOWNLOAD`等を追加keyとして返してはならない。

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

##### resource_type × operation structural support

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

##### Query contract

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

##### Authorization class

endpoint自体のreadにはProject-scoped `READ` authorizationを適用する。ProjectMembershipをresolveできない、またはREAD不可の場合はHTTP 403 / `PROJECT_ACCESS_DENIED`でrequest全体を拒否する。

各canonical operationのauthorization class:

| operation | authorization class | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- | --- |
| `RUN` | `EXECUTION_MUTATION` | allow | allow | deny |
| `EDIT` | `WRITE_MUTATE` | allow | allow | deny |
| `EXPORT` | `EXPORT_CREATE` | allow | allow | deny |

Structural support判定後、scientific/domain prerequisite判定前にoperation authorizationを評価する。structurally supported operationでrole不足の場合、HTTP 200のoperation itemとして`allowed=false, reason_code=PROJECT_ACCESS_DENIED`を返す。

##### Scientific/domain prerequisite authority

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

##### Unknown resource / unsupported operation semantics

- unknown `resource_type`: HTTP 422 / `UNSUPPORTED_RESOURCE_TYPE`。
- known `resource_type` + `resource_id`が当該Project内で解決できない場合（別ProjectのIDを含む）: HTTP 404 / `ENTITY_NOT_FOUND`。cross-project existenceを開示しない。
- malformed/unknown canonical route: HTTP 422 / `INVALID_NAVIGATION_ROUTE`。
- route/resource Family mismatch: HTTP 422 / `ROUTE_RESOURCE_FAMILY_MISMATCH`。
- structural matrixまたはroute/use-case上unsupportedなcanonical operation: HTTP 200、`allowed=false, reason_code=UNSUPPORTED_OPERATION`。
- responseは非canonical operation keyを返してはならない。内部実装でunknown operation keyが要求された場合はfail closedし、configuration/programming defectとして扱う。

##### reason_code taxonomy

Current Operation Availabilityのoperation item `reason_code`は次のclosed vocabularyとする。

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

current implementationでad-hoc reason codeを追加してはならない。新しいcodeが必要な場合はcanonical design amendmentを先に行う。

Stage visibilityとaction availabilityは別contractとする。`allowed=false`をStage自体の非表示で表現することを基本挙動にしない。
#### Analytical Navigation Metadata

Capability-owned Family / Navigation Stage catalogのcanonical endpoint:

```http
GET /api/v1/navigation/analysis
```

Response schemaは`analysis-navigation/1`。

Responsibility:

- supported Family identity
- Family slug / display label
- Family-local Navigation Stage ID / slug / display label / order
- Family default Stage
- metadata schema version

Non-responsibility:

- Execution Plan生成
- Runner selection
- StageExecution status
- Analysis Specification mutation
- persistent current navigation state
- Family-specific analytical result payload

Catalog source of truthは**backend read-only metadata endpoint**へfreeze済みである。Family Capability descriptorをapplication/interface aggregatorが集約し、Frontendはfull catalogをduplicate ownershipしない。Execution Agentが別方式へ変更してはならない。

#### Catalog source of truth

Concrete Navigation Stage catalogはFamily Capabilityが所有する。Frontend rendererは`(family, stage_id) -> surface` bindingを保持できるが、stage label/order/defaultのfull catalogを独自に二重管理しない。

## 7. 改訂記録

- 2026-11-17: 全23_10〜23_19共通フォーマットへ再構成。Request/Response/ErrorsをOperation別に記載し、Source確認と未検証を分離。
