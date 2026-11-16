<!-- ENH-E11 split working copy: not a formal approval. -->
# 23 — overall

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [23_api_interface_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/23_api_interface_design.md) · blob `131467f02222f105a49e6dfdbcec0f49cadb0f41`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 1. 文書の設計粒度

本書は、Ariadneを構成する**interface contract**を、実装内部ではなく利用者・component間の境界として定義する。

本書で確定する事項:

- Browser Navigation Context / route contract
- Web API endpoint、request / response DTO、resource boundary
- Authentication / AuthorizationおよびProject境界
- Worker / Runtime内部interface
- CLI / Python Library interface
- validation / error contract
- idempotency contract
- contract versioning
- interface間で引き渡すidentifier、state、payloadの責務境界

各interface contractでは、該当する範囲で次を明示する。

1. interfaceの目的とauthority
2. endpoint / route / command / callable identity
3. input / request contract
4. output / response contract
5. authentication / authorizationまたはscope boundary
6. state / lifecycle上のprecondition
7. validation / error semantics
8. idempotency / versioning semantics
9. 他interfaceへ引き渡すcontextと、引き渡してはならないstate

本書はDB Entityの属性定義、ORM mapping、class内部構造、algorithm実装詳細を定義しない。それらは`21_logical_data_design.md`、`30_detailed_design.md`またはScientific Core側の詳細contractをauthorityとする。

`Navigation Context`はWeb Appのbrowser interface contractであり、`Web API Endpoint`と同じ種類の設計項目ではない。このため本書では、interface種別を上位階層に置き、Browser / Web API / Runtime / CLIを同一粒度で整理する。

## 2. Interface構成と責務境界

本書のinterface architectureは次のとおりである。

```text
Ariadne Interface Contracts
├─ Browser Navigation Interface
│  └─ route / Navigation Context / browser restoration
├─ Web API Interface
│  ├─ Project / Research Context
│  ├─ Dataset / Analysis View
│  ├─ Analysis Specification
│  ├─ Family-specific analytical interface
│  ├─ Execution
│  ├─ Result / Comparison / Lineage
│  ├─ Annotation / Artifact
│  └─ Frontend Support API
├─ Worker / Runtime Internal Interface
├─ CLI / Library Interface
└─ Cross-cutting Contract Policy
   ├─ Error Model
   ├─ Idempotency
   ├─ Contract Versioning
   └─ Forbidden Interface
```

| Interface種別 | 主な利用者 | Authority / 責務 | 非責務 |
| --- | --- | --- | --- |
| Browser Navigation | Web App / Browser | Project/Analysis route、Navigation Context、deep link、reload/Back/Forward | Domain Resource persistence、Execution lifecycle |
| Web API | Web App / external client | Project-scoped resource/query/command contract | Browser history、UI-local navigation state |
| Worker / Runtime Internal | Worker / Application runtime | Execution claim、lease、Stage runtime、Runner boundary | Public browser/API route |
| CLI / Library | headless user / backend use case | headless scientific execution | Browser navigation metadataへの依存 |
| Cross-cutting policy | 上記すべて | error、idempotency、versioning、禁止境界 | 個別domain operationの意味 |

## 3. 共通Contract規約

### 3.1 API原則

1. Resource IDとProject境界を明示する。
2. `Idempotency-Key`を実装済みのcommand endpointでは、同一commandの再送をidempotency serviceで収束させる。未対応endpointまで一律にidempotentと仮定しない。
3. Analysis Specification、Execution Plan、Family-specific scientific payload、Runner draft等、versioned JSON contractは各contract boundaryでschema versionを持つ。一方、すべてのpersistent entityが直接`schema_version` columnを持つとは仮定しない。
4. validation errorはcurrent error envelopeに従い、必要なfield path / error codeを`details`へ保持する。
5. async execution submissionはExecution identityと受理statusを返す。
6. UI専用のnavigation stateを正本Domain APIへ混入しない。
7. Result payloadとArtifact binary downloadを分離する。
8. Family固有analysis schemaは共通`AnalysisSpecification` envelopeへ埋め込む。
9. analytical Familyのcanonical discriminatorは`AnalysisFamily` / `analysis_family`とし、同義の`family` / `current_family`をpersistent analysis contractへ追加しない。
10. Navigation Stageはpresentation/application metadataであり、Analysis Specification / Execution Plan / Execution / StageExecutionの必須入力にしない。
11. Navigation Stageとruntime `StageType` / `StageExecution`を同一schemaへ統合しない。
12. CLI / Python library / backend use caseによるheadless executionはbrowser navigation metadata interfaceを経由しなくても成立する。
13. UI Stage名を理由として同名execution endpointを1:1で増設しない。
14. UI / application IA変更だけを理由に新しいbackend API/persistence contractを発明しない。必要なinterfaceは本書本文に具体的に記載する。

### 3.2 Authentication / Authorization

#### 3.2.1 Current request identity

現行実装のFastAPI applicationには共通Bearer/OIDC authentication middlewareは存在しない。

Current request identity contract:

- request correlation: `X-Request-Id`
  - request headerにあればその値を使用する。
  - 未指定時はUUIDを生成する。
  - response headerにも`X-Request-Id`を返す。
- user identity:
  - user identityを必要とするrouterでは`X-User-Id`を読む。
  - 未指定時は`anonymous`を利用する実装がある。
- idempotent command:
  - 対応endpointでは`Idempotency-Key`を受け付ける。

Current interface contractはproduction Authentication方式の成立を前提化しない。`Authorization: Bearer`やproduction OIDCをcurrent implementationとして捏造せず、実装済みauthentication boundaryだけをauthorityとする。

#### 3.2.2 Project role

Project Closure領域のpersisted roleは次の3値である。

- `OWNER`
- `EDITOR`
- `VIEWER`

`ProductClosureService`のrole policy:

```text
READ_ROLES  = OWNER / EDITOR / VIEWER
WRITE_ROLES = OWNER / EDITOR
```

Project作成時は`X-User-Id`（未指定時`anonymous`）をProject ownerとして登録する。

注意事項:

- 全routerがProjectMembership認可を一律に経由するわけではない。
- Current contractではNavigation改修を理由に、未実装の全API統一認可を既存contractとして記述しない。
- Navigation metadataをProject-scoped APIとして追加する場合は、少なくとも既存Project境界を弱めてはならない。


#### 3.2.3 Project authorization coverage

全project-scoped routeはservice action前にProjectMembershipをresolveし、次のmatrixを適用する。

| Action | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- |
| READ | allow | allow | allow |
| WRITE / MUTATE | allow | allow | deny |
| Execution submit/cancel/retry/rerun/revise | allow | allow | deny |
| Export create | allow | allow | deny |
| Membership administration | allow | deny | deny |
| Explicit sensitive output | allow | allow | deny |

Project IDをpathに持たないlegacy/generic resource routeでも、resourceからProjectをresolveして同等のauthorizationを適用する。prediction row / local explanation row/detailはpotentially sensitive outputとし、VIEWERにはaggregate/suppressed responseのみ許可する。configurable sensitive-column policyおよびsystem-level Operator authorizationは`DEFERRED` scopeである。

### 3.3 Response共通規約

#### 3.3.1 Pagination

PaginationはAPIごとにcurrent contractが異なる。`AnalysisViewListResponse`やFamily系list response等には`next_cursor` fieldが存在するが、全list APIが共通cursor query contractを実装しているわけではない。

したがってCurrent contractで共通`?limit=&cursor=&sort=` contractが既に存在するものとして扱わない。新しいNavigation metadata APIがpaginationを必要とする場合は、そのAPI固有contractとして明示する。

#### 3.3.2 Read-only presentation metadata

Navigation metadata等のpresentation-only responseはpersistent Domain Resource responseと区別する。presentation metadataを返すこと自体によって、Analysis Specification / Execution Plan / Execution / StageExecution等のscientific/runtime resourceを生成・更新してはならない。

Analytical Navigation Metadataのcanonical endpoint、schema、catalog authorityは`5.10.2 Analytical Navigation Metadata`および`5.10.3 Catalog source of truth`で定義する。

---

## 90. この文書種別の目的・責務・規範性

- **目的:** Browser/Web API/Worker/CLI/Portの利用者と提供者の間の互換性契約を、観測可能な入出力・検証・失敗として定義する。
- **含む:** Command/operation、request/response、schema version、status/error、backward compatibility、serialization、path/security、timeout/availability、contract test。
- **含まない:** Application内部のclass layout、DB storage実装、推定器の統計手順。
- **E11境界:** 追加はlocal CLIとScientific Port/Artifact Interfaceのみ。既存`/api/v1`に新E11 endpointを追加しない。旧v2 spec/read-backを暗黙更新しない。

**E11追加草案:** [23_09_enh_e11_cli_and_port_interface_draft.md](23_09_enh_e11_cli_and_port_interface_draft.md)
