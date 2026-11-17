# 23_01_common_conventions


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

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-120a`**：runtime API schemaから生成されるFastAPI OpenAPIをcurrent API contractとして提供する
- **`FR-120b`（将来拡張・現行提供対象外）**：canonical schema exampleとOpenAPI/exampleをsystematically同期・検証する

## 10. API Operation契約の最低記述粒度（PREP-01 共通規約）

下表の9欄はInterface全体の**広義の整合性監査観点**を示す。ただし、Ownerの2026-11-17決定により、23_10〜23_19の今回優先対象は**Operation別Request／Response／Errorsの詳細仕様**のみとする。残りの観点を今回の各Endpoint詳細節に一律強制しない。既存の承認済み要求・安全性契約は緩和しない。

| 欄 | 必須記載内容 |
| --- | --- |
| Identity | HTTP Method、Path、Operation、Source blob SHA、CURRENT / PROPOSED |
| Request | Path / Query / Body、型、必須性、制約 |
| Success | HTTP Status、Response DTO / Schema、Version |
| Authorization | 認証、ProjectMembership Role、Project Scope |
| State | Lifecycle前提、更新先、Side effect |
| Error | Validation / Domain / Permission / Missing / ConflictのStatus |
| Idempotency | 再送・Retry・no-clobber規則 |
| Compatibility | Legacy v2、Port、Clientへの影響 |
| Evidence | FR/NFR/AR、Contract / Negative Test、Owner approval |

各欄には DEFINED（Sourceまたは承認規範で確定）／INHERITED（共通規範への特定参照）／N_A（理由付き非適用）／NOT_SPECIFIED（未確定）を付す。空欄や例示JSONを完全なSchemaとみなさない。Sourceで確認できないResponse/Errorを推測しない。

この共通規約の追記**だけでは**Operation別Coverageが完了したことにならない。個別23_10〜19と現行Router/DTOのSource突合、負例、レビューは未完として追跡する。


## 11. Web API詳細仕様書の統一構成（Owner採用 2026-11-17）

適用対象は`23_10〜23_19`のHTTP API仕様書（全101 Router Operation）。Browser/Worker/CLI/Scientific Portの`23_20/30/40/41/42`へHTTP書式を強制しない。

| 章 | 必須内容 |
|---|---|
| 1. API概要 | 対象責務、Base path、契約の確認範囲 |
| 2. エンドポイント一覧 | Method、完全Path、Handler、Success HTTP |
| 3. 共通Error形式 | 現行error envelope。`application/problem+json`への無断変換禁止 |
| 4. エンドポイント詳細 | **全Operationごとに**基本情報、Request（Path/Query/Header/Body、型・必須・null・制約）、Response（Status/Body Field/型/例）、Errors（Status/Code/条件）、Source Trace |
| 5. 検証状況 | Source Static CheckとRuntime Contract Testを分離 |
| 6. 既存Domain・設計制約 | 旧版の規範を保持する。旧Route表よりSourceに一致する2章を優先 |
| 7. 改訂記録 | 変更内容・更新日 |

品質ルール：Router/DTO/Serviceが返すFieldを追跡する。`response_model`未宣言でもServiceのreturn dictを点検する。Methodの仮引数をPydanticのFieldに混入させない。Request/Responseの説明用JSONサンプルは実行時成功保証を意味せず、特にFamily Specの `{}` は無条件にvalidとは扱わない。Error Handlerの共有Mappingから個別Operationの到達可能性を推定しない。未確認部分は推測せず検証条件を示す。

**状態:** 10文書の7章構造と101件の操作節はSource静的照合ベースで整備した。Serviceが返す未型付けResponseの残部、Operation固有Error条件、統合Contract Testは未完了であり、PREP-01完了とは判定しない。
