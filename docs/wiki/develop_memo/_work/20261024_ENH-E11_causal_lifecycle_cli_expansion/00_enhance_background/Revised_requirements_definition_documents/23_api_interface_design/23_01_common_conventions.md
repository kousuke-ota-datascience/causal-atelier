# 23_01_common_conventions

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

---

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
