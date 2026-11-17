# 23_10_api_project_context


---

## 5. Web API Interface

### 5.1 Project / Research Context API

Project / Research ContextはFamily切替とは独立したProject-scoped resourceである。Project Managementがresource lifecycleを所有し、Family tab操作でresource identityを変更しない。

代表contract:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects` | Project作成 |
| GET | `/projects` | Project一覧 |
| GET | `/projects/{project_id}` | Project取得 |
| PATCH | `/projects/{project_id}` | ACTIVE Project更新 |
| DELETE | `/projects/{project_id}` | Project archive |
| POST | `/projects/{project_id}/research-contexts` | Research Context DRAFT作成 |
| GET | `/projects/{project_id}/research-contexts` | Context一覧 |
| GET | `/projects/{project_id}/research-contexts/{context_id}` | Context取得 |
| PATCH | `/projects/{project_id}/research-contexts/{context_id}` | DRAFT更新 |
| POST | `/projects/{project_id}/research-contexts/{context_id}/fix` | FIXED化 |
| GET | `/projects/{project_id}/research-contexts/{context_id}/usage` | Analysis Specification利用状況とhistorical Family execution/result projectionを返す |

`research-contexts/{context_id}/usage`の現行実装実装は`AnalysisSpecificationOrm`に加え、historical/compatibility read modelである`FamilyExecutionOrm / FamilyResultOrm`を参照する。canonical `Execution / Result`全体の完全なusage indexではないため、そのように一般化しない。

Navigation routeはProject / Research Contextのidentity authorityではない。

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-121`**：全project-scoped routeでpersisted ProjectMembership role（OWNER/EDITOR/VIEWER）に基づくauthorizationをservice action前に検証する


#### 5.1.1 CURRENT API Operation × Source照合（PREP-01）

以下のpathは**相対pathではなくAPIルート全体**。2026-11-17 Source静的照合により、`app.py`が`/api/v1`をrouter prefixとし、`projects.py`が`/projects`を持つことを確認した。Research Contextは`workspace_lifecycle.py`で直接`/projects/{project_id}/research-contexts`を宣言する。HTTP error、Service内部の権限、実行時Responseの完全性は静的Router宣言のみでは確定できない。

**固定Source Blob:**

- `src/ariadne/interfaces/web_api/app.py`：API root `/api/v1`（branch 2026-11-17）。
- `src/ariadne/interfaces/web_api/routers/projects.py`：`6fc9aa297aba3f89d57613a1b1c203f4de071a8c`。
- `src/ariadne/interfaces/web_api/routers/workspace_lifecycle.py`：`eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`。
- `src/ariadne/interfaces/web_api/schemas/__init__.py`：`b2235aed012b954a5b19531f68a9aa2039201781`。

##### 既存Routerの操作表（11件／11件のRoute宣言を観測）

| HTTP | Canonical path (`/api/v1`以降) | Request contract from Router | Success from Router | Source |
| --- | --- | --- | --- | --- |
| POST | `/projects` | `ProjectCreate` body: name 1..200、topic/objective/memo optional | **201**、`ProjectResponse` | projects.py |
| GET | `/projects` | `status: ProjectStatus|None`、default `ACTIVE` | 200（FastAPI既定）、`ProjectListResponse` | projects.py |
| GET | `/projects/{project_id}` | `project_id: str` | 200、`ProjectResponse` | projects.py |
| PATCH | `/projects/{project_id}` | `ProjectUpdate` body: optional name/topic/objective/memo | 200、`ProjectResponse` | projects.py |
| DELETE | `/projects/{project_id}` | `project_id: str`、`X-User-Id` request header（未指定時anonymous） | **204**、empty body | projects.py |
| POST | `/projects/{project_id}/research-contexts` | `ResearchContextCreate` body：context_key、problem_statement、research_questions、significance、hypotheses、decision_context、relations | **201**、`dict[str,Any]`（固定Response Schema未宣言） | workspace_lifecycle.py |
| GET | `/projects/{project_id}/research-contexts` | project_id | 200、`items` list of service results | workspace_lifecycle.py |
| GET | `/projects/{project_id}/research-contexts/{context_id}` | project_id、context_id | 200、Service result dict（固定Response Schema未宣言） | workspace_lifecycle.py |
| PATCH | `/projects/{project_id}/research-contexts/{context_id}` | `ResearchContextPatch` body、exclude_unset | 200、Service result dict（固定Response Schema未宣言） | workspace_lifecycle.py |
| POST | `/projects/{project_id}/research-contexts/{context_id}/fix` | project_id、context_id | 200、Service result dict（固定Response Schema未宣言） | workspace_lifecycle.py |
| GET | `/projects/{project_id}/research-contexts/{context_id}/usage` | project_id、context_id | 200、Service usage dict（固定Response Schema未宣言） | workspace_lifecycle.py |

##### 共通FieldのCoverageと未検証点

| Field | Coverage | 根拠・未完了 |
| --- | --- | --- |
| Identity / HTTP Method / Path | **DEFINED** | 上記Router Decorator + app prefixで11件 |
| Request | **DEFINED（Router宣言） / NOT_SPECIFIED（後続Service等）** | Project DTO/ResearchContext Modelの宣言は確認。全Field制約、service-level invariantは未検証 |
| Success | **DEFINED（Router宣言） / NOT_SPECIFIED（後続Service等）** | ProjectはPydantic response_model、Research Contextは宣言`dict[str,Any]`。Body実形状の独立確認が必要 |
| Authorization | **NOT_SPECIFIED** | FR-121の期待はOwner要件。Router引数だけから全service pathのrole enforcementを証明しない |
| State and side effects | **NOT_SPECIFIED** | create/update/archive/fixの名称は存在。UoW commit・DRAFT/FIXED前提はServiceの実コードと負例が必要 |
| Error / HTTP code | **NOT_SPECIFIED** | shared Error HandlerがあるがOperation別404/403/409/422の実効対応は未照合 |
| Idempotency / Retry | **NOT_SPECIFIED** | mutationの再送・Idempotency-Key規則を未確認 |
| Compatibility / Version | **DEFINED（prefix） / NOT_SPECIFIED（意味互換）** | `/api/v1` prefixはSource確認。旧v2とLocal E11の意味的互換は個別確認が必要 |
| Test / FR | **DEFINED（Router宣言） / NOT_SPECIFIED（後続Service等）** | FR-121の追跡は本文に存在。Operation別Contract/Negative Testとの1:1追跡は未完 |

**解釈上の制約:** 本表はRouteとDTOのSource突合というPREP-01の部分是正であり、9欄の完成を意味しない。`NOT_SPECIFIED`を暗黙の成功としない。Service/Handler/Testの確認後に最終Contractとする。
 

#### 5.1.2 Router→Application Service→Error Handlerの実装差分（2026-11-17 PREP-01）

**根拠Sourceの範囲（静的照合）**：`routers/projects.py` (blob `6fc9aa297aba3f89d57613a1b1c203f4de071a8c`)、`routers/workspace_lifecycle.py` (`eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`)、`product/application/project_data_service.py` (`639ef15494e6244282b670aa36d53e9beb92e526`)、`product/application/workspace_lifecycle_service.py` (`ee84e914f8bc5136b9f9fee7323814a552a5d68a`)、`web_api/error_handlers.py` (`c8cd02be0aebd1a6e5399098b6594e3f57d06f15`)、`web_api/idempotency.py` (`12ff23e5bf9dd39a5de59a135eef4e874f047505`)。実行時のGateway/OIDC設定は対象外。

| 観点・操作 | CURRENT Sourceで観測したこと | REQUIRED（Owner採用Requirement） | 判定 |
| --- | --- | --- | --- |
| Project POST | `create_project`が`ProjectDataService.create_project`の後、`X-User-Id`／anonymousを使い`ProductClosureService.register_project_owner`を呼ぶ | Authenticated principalによるOwner登録／失敗時の整合性 | AUTH/atomicity NOT_VERIFIED |
| Project GET list/get, PATCH | `ProjectDataService`のこれらのmethodにはactor ID・Membership評価の引数がなく、RouterでのMembership認可も観測できない | FR-121: 対象ProjectのOWNER/EDITOR/VIEWERをservice action前に検証 | **CONTRACT_IMPLEMENTATION_GAP（静的）** |
| Project DELETE | `X-User-Id`は`ArchiveProjectCommand.requested_by`へ渡るが、`ProjectDataService.archive_project`はMembership検証を呼んでいない | FR-121: WRITEはOWNER/EDITORのみ | **CONTRACT_IMPLEMENTATION_GAP（静的）** |
| ResearchContext POST/GET/PATCH/FIX/USAGE | `WorkspaceLifecycleService`の各methodは`project_id`や`created_by`を受けるが、`_project/_active_project`はprojectの存在／ARCHIVEDのみ判定。MembershipのRoleは評価していない | FR-121: Actor/Project/Membershipの一致とRole境界 | **CONTRACT_IMPLEMENTATION_GAP（静的）** |
| ResearchContext POST | Routeは`IdempotencyServiceDep`や`Idempotency-Key`を使用せず、Serviceは新versionを作成してcommitする | FR-114a/b、23_51: durable createのIdempotency Keyとreplay semantics | **CONTRACT_IMPLEMENTATION_GAP（静的）** |
| Service error | `EntityNotFound`→404、`ProjectAccessDenied`→403、`ProjectArchived`→409、`InvalidSchema`→422、Request validationは**400** `INVALID_REQUEST` | HTTPごとの型付きError／safe response | Handler mapping DEFINED、Operation別到達はNOT_VERIFIED |
| Version | FastAPI `app.py`が`/api/v1`として公開 | Product v1とE11 Local CLI versionを分離 | Router prefix DEFINED、E11 compatibilityは未実装 |

**評価上の制約：** 実行時Gateway、依存注入override、middlewareまたは運用上の認証機構が追加され得るため、これだけでデプロイ環境の侵害可能性を断定しない。ただし**CURRENT Route→ServiceでOwner Requirementへの実装追跡が成立していない**ことはSourceから検証可能。要求仕様を緩和するのではなく、Product Security backlog（DEC09のGAP-C群／#14との紐付け要精査）と修正責任を切り出す。CLI-onlyのE11新機能を実装することによって本Gapが自動解消したと扱わない。

**独立確認用Negative Test:** 非Member→Project GET/PATCH/DELETEとContext GET/PATCH/FIX/USAGEはdeny、VIEWER→mutation deny、ARCHIVED→mutation 409、missing／same／different Idempotency Key、他ProjectのContext ID、unauthenticated principalのOwner登録を、固定Source／Integration環境で検証。現状はNOT_RUN。

## PREP-01 — Operation別 Request / Response / Errors 詳細（Owner方針 2026-11-17）

対象は**Operation別の入力（path/query/header/body + field type/required/null/constraints）、成功HTTP statusとresponse field、失敗HTTP status/error code/条件**に限定する。すべてのPathは `/api/v1` 以下である。SOURCEで実証できないError到達・Service由来Fieldは推測せず `UNVERIFIED` とする。

共通Error Handlerが処理するDomain/RequestValidationErrorのCURRENT envelope は `{"error":{"code":"…","message":"…","details":{},"request_id":"…"}}`（JSON）、**Notion例のproblem+jsonではない**。RequestValidationErrorは400 `INVALID_REQUEST`、EntityNotFoundは404 `ENTITY_NOT_FOUND`、ProjectArchivedは409 `PROJECT_ARCHIVED`、ProjectAccessDeniedは403 `PROJECT_ACCESS_DENIED`、InvalidSchemaは422 `INVALID_SCHEMA`。これらはHandlerのMappingであり**各Operationが必ずそのエラーを送出するという意味ではない**。Source: `src/ariadne/interfaces/web_api/error_handlers.py`。未捕捉例外やHTTPException等の全error surfaceは別途照合が必要。

### ProjectResponse Field Contract（Source: schemas/__init__.py）

`ProjectResponse`: `project_id:string`, `name:string`, `topic/objective/memo:string|null`, `status:string`, `created_at/updated_at:datetime|null`. `ProjectListResponse`: `items:ProjectResponse[]`, `next_cursor:string|null` (default null).

### OP-PROJECT-01 — `POST /projects`

| Key | CURRENT contract |
|---|---|
| Method / path | `POST /api/v1/projects` |
| Success | HTTP **201**, ProjectResponse |
| Request | ProjectCreate JSON body |
| Error (observed handler / reachability) | 400 INVALID_REQUEST; other domain errors UNVERIFIED |

Request fields:

| Field | Type | Required | Nullable | Constraint |
|---|---|---|---|---|
| `name` | string | yes | no | 1..200 characters |
| `topic`, `objective` | string | no | yes | 0..4000 characters |
| `memo` | string | no | yes | 0..8000 characters |

CURRENT: required `name`; optional string fields as above. `X-User-Id` is read as owner identity (defaults to `anonymous`); not a verified authentication mechanism.

### OP-PROJECT-02 — `GET /projects`

| Key | CURRENT contract |
|---|---|
| Method / path | `GET /api/v1/projects` |
| Success | HTTP **200**, ProjectListResponse |
| Request | query: status (ProjectStatus enum or null; default ACTIVE) |
| Error (observed handler / reachability) | 400 INVALID_REQUEST for invalid query; other errors UNVERIFIED |

No JSON request body. Enum literal set: inspect Product ProjectStatus definition before publishing values.

### OP-PROJECT-03 — `GET /projects/{project_id}`

| Key | CURRENT contract |
|---|---|
| Method / path | `GET /api/v1/projects/{project_id}` |
| Success | HTTP **200**, ProjectResponse |
| Request | path project_id:string |
| Error (observed handler / reachability) | 404 ENTITY_NOT_FOUND conditional on domain not-found |

No JSON body.

### OP-PROJECT-04 — `PATCH /projects/{project_id}`

| Key | CURRENT contract |
|---|---|
| Method / path | `PATCH /api/v1/projects/{project_id}` |
| Success | HTTP **200**, ProjectResponse |
| Request | path project_id:string; ProjectUpdate JSON |
| Error (observed handler / reachability) | 400 INVALID_REQUEST; 404 ENTITY_NOT_FOUND if Service raises not-found; other errors UNVERIFIED |

Request fields:

| Field | Type | Required | Nullable | Constraint |
|---|---|---|---|---|
| `name` | string | no | yes | if present non-null length 1..200 |
| `topic`, `objective` | string | no | yes | length <=4000 |
| `memo` | string | no | yes | length <=8000 |

All body fields optional in DTO. Whether explicit null clears a field or denotes unchanged is Service-dependent: UNVERIFIED.

### OP-PROJECT-05 — `DELETE /projects/{project_id}`

| Key | CURRENT contract |
|---|---|
| Method / path | `DELETE /api/v1/projects/{project_id}` |
| Success | HTTP **204**, empty body |
| Request | path project_id:string; X-User-Id header read (default anonymous) |
| Error (observed handler / reachability) | 404 ENTITY_NOT_FOUND / 409 PROJECT_ARCHIVED if raised; authorization enforcement source GAP |

Archive endpoint; request body absent.

### OP-PROJECT-06 — `POST /projects/{project_id}/research-contexts`

| Key | CURRENT contract |
|---|---|
| Method / path | `POST /api/v1/projects/{project_id}/research-contexts` |
| Success | HTTP **201**, dict[str,Any] (no explicit response_model) |
| Request | path project_id:string; ResearchContextCreate JSON |
| Error (observed handler / reachability) | 400 INVALID_REQUEST; 404/409/422 only if raised by Service: UNVERIFIED |

Request fields:

| Field | Type | Required | Nullable | Constraint |
|---|---|---|---|---|
| `context_key` | string | yes | no | no Field constraint in router DTO |
| `problem_statement` | string | no | no | default empty string |
| `research_questions`, `hypotheses` | array[string] | no | no | default [] |
| `significance` | string | no | yes | default null |
| `decision_context` | object | no | no | default {} |
| `relations` | array[object(string)] | no | no | default [] |

X-User-Id defaults anonymous. Exact Service output keys require Service inspection; cannot claim fixed JSON schema.

### OP-PROJECT-07 — `GET /projects/{project_id}/research-contexts`

| Key | CURRENT contract |
|---|---|
| Method / path | `GET /api/v1/projects/{project_id}/research-contexts` |
| Success | HTTP **200**, object: items=service list |
| Request | path project_id:string |
| Error (observed handler / reachability) | 404 ENTITY_NOT_FOUND etc conditional; operation mappings UNVERIFIED |

Elements of items not response_model typed in Router. No JSON body.

### OP-PROJECT-08 — `GET /projects/{project_id}/research-contexts/{context_id}`

| Key | CURRENT contract |
|---|---|
| Method / path | `GET /api/v1/projects/{project_id}/research-contexts/{context_id}` |
| Success | HTTP **200**, dict[str,Any] from Service |
| Request | path project_id:string; context_id:string |
| Error (observed handler / reachability) | 404 ENTITY_NOT_FOUND / 422 PROJECT_BOUNDARY_VIOLATION if raised; UNVERIFIED |

Fields UNVERIFIED; no declared response_model.

### OP-PROJECT-09 — `PATCH /projects/{project_id}/research-contexts/{context_id}`

| Key | CURRENT contract |
|---|---|
| Method / path | `PATCH /api/v1/projects/{project_id}/research-contexts/{context_id}` |
| Success | HTTP **200**, dict[str,Any] from Service |
| Request | path project_id:string; context_id:string; ResearchContextPatch JSON |
| Error (observed handler / reachability) | 400 INVALID_REQUEST; 404 ENTITY_NOT_FOUND / 409 RESOURCE_IMMUTABLE if emitted; mapping UNVERIFIED |

Request fields:

| Field | Type | Required | Nullable |
|---|---|---|---|
| `problem_statement`, `significance` | string | no | yes |
| `research_questions`, `hypotheses` | array[string] | no | yes |
| `decision_context` | object | no | yes |
| `relations` | array[object(string)] | no | yes |

Body sent via `model_dump(exclude_unset=True)`: omitted and explicit null distinguishable. Exact Service response fields UNVERIFIED.

### OP-PROJECT-10 — `POST /projects/{project_id}/research-contexts/{context_id}/fix`

| Key | CURRENT contract |
|---|---|
| Method / path | `POST /api/v1/projects/{project_id}/research-contexts/{context_id}/fix` |
| Success | HTTP **200**, dict[str,Any] from Service |
| Request | path project_id:string; context_id:string; no JSON body |
| Error (observed handler / reachability) | 404 ENTITY_NOT_FOUND / 409 RESOURCE_IMMUTABLE if emitted; mapping UNVERIFIED |

FIX transition side effects and Service response shape require Source review.

### OP-PROJECT-11 — `GET /projects/{project_id}/research-contexts/{context_id}/usage`

| Key | CURRENT contract |
|---|---|
| Method / path | `GET /api/v1/projects/{project_id}/research-contexts/{context_id}/usage` |
| Success | HTTP **200**, dict[str,Any] from Service |
| Request | path project_id:string; context_id:string |
| Error (observed handler / reachability) | 404 ENTITY_NOT_FOUND if raised; mapping UNVERIFIED |

Historical Family execution/result projection; not canonical full usage. Exact keys UNVERIFIED.
