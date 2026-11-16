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


## 5.1.1 CURRENT API Operation × Source照合（PREP-01）

以下のpathは**相対pathではなくAPIルート全体**。2026-11-17 Source静的照合により、`app.py`が`/api/v1`をrouter prefixとし、`projects.py`が`/projects`を持つことを確認した。Research Contextは`workspace_lifecycle.py`で直接`/projects/{project_id}/research-contexts`を宣言する。HTTP error、Service内部の権限、実行時Responseの完全性は静的Router宣言のみでは確定できない。

**固定Source Blob:**

- `src/ariadne/interfaces/web_api/app.py`：API root `/api/v1`（branch 2026-11-17）。
- `src/ariadne/interfaces/web_api/routers/projects.py`：`6fc9aa297aba3f89d57613a1b1c203f4de071a8c`。
- `src/ariadne/interfaces/web_api/routers/workspace_lifecycle.py`：`eb90bd940fc7a35b84cda0e3fa58235a738cb0a1`。
- `src/ariadne/interfaces/web_api/schemas/__init__.py`：`b2235aed012b954a5b19531f68a9aa2039201781`。

### 既存Routerの操作表（11件／11件のRoute宣言を観測）

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

### 共通FieldのCoverageと未検証点

| Field | Coverage | 根拠・未完了 |
| --- | --- | --- |
| Identity / HTTP Method / Path | **DEFINED** | 上記Router Decorator + app prefixで11件 |
| Request | **PARTIALLY DEFINED** | Project DTO/ResearchContext Modelの宣言は確認。全Field制約、service-level invariantは未検証 |
| Success | **PARTIALLY DEFINED** | ProjectはPydantic response_model、Research Contextは宣言`dict[str,Any]`。Body実形状の独立確認が必要 |
| Authorization | **NOT_SPECIFIED** | FR-121の期待はOwner要件。Router引数だけから全service pathのrole enforcementを証明しない |
| State and side effects | **NOT_SPECIFIED** | create/update/archive/fixの名称は存在。UoW commit・DRAFT/FIXED前提はServiceの実コードと負例が必要 |
| Error / HTTP code | **NOT_SPECIFIED** | shared Error HandlerがあるがOperation別404/403/409/422の実効対応は未照合 |
| Idempotency / Retry | **NOT_SPECIFIED** | mutationの再送・Idempotency-Key規則を未確認 |
| Compatibility / Version | **INHERITED+UNVERIFIED** | `/api/v1` prefixはSource確認。旧v2とLocal E11の意味的互換は個別確認が必要 |
| Test / FR | **PARTIALLY DEFINED** | FR-121の追跡は本文に存在。Operation別Contract/Negative Testとの1:1追跡は未完 |

**解釈上の制約:** 本表はRouteとDTOのSource突合というPREP-01の部分是正であり、9欄の完成を意味しない。`NOT_SPECIFIED`を暗黙の成功としない。Service/Handler/Testの確認後に最終Contractとする。
