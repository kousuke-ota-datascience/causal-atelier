# 23_10_api_project_context

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

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
