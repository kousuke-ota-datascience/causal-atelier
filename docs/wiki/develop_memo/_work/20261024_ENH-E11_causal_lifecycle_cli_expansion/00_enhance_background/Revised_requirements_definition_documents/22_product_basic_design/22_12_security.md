# 22_12_security

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

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


## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。旧要件の具体設計制約を担当領域へ移管。実装検証・ADR承認済みを意味しない。

### 98.1. FR-121（SPLIT）

- 元の設計情報を含む要件：全project-scoped routeでpersisted ProjectMembership role（OWNER/EDITOR/VIEWER）に基づくauthorizationをservice action前に検証する
- 改訂後RD／Legacy Trace：Project内操作を所属Roleに応じて認可し権限外の処理を防止する
- ID：`FR-121`; Status：`ACTIVE`; Implementation：`PARTIAL`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.2. FR-124a（SPLIT）

- 元の設計情報を含む要件：Artifact metadata/downloadでProject境界とsafe content dispositionを検証するcurrent contractを維持する
- 改訂後RD／Legacy Trace：成果物の情報・取得をProject境界内で安全に利用できる
- ID：`FR-124a`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.3. FR-124b（SPLIT）

- 元の設計情報を含む要件：legacy/generic routeを含むArtifact downloadでProjectMembership authorizationを一貫適用する
- 改訂後RD／Legacy Trace：旧経路を含む成果物取得に同じProject権限を適用する
- ID：`FR-124b`; Status：`ACTIVE`; Implementation：`PARTIAL`; [逐条記録](../95_rd04_fr_application_review.md)

### 98.4. NFR-008a（SPLIT）

- 元の設計情報を含む要件：current input validation、path traversal防止、secret非露出等のsafeguardを維持する
- 改訂後RD／Legacy Trace：入力検証と危険なパス・秘密情報の保護を維持する
- ID：`NFR-008a`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../96_rd04_nfr_ar_application_review.md)

### 98.5. AR-020（SPLIT）

- 元の設計情報を含む要件：prediction row / local explanationをpotentially sensitive outputとして扱い、Project roleに応じてdetail exposureを制御する
- 改訂後RD／Legacy Trace：個票予測と局所説明は機微情報になり得るため、利用権限に応じ露出を制限する
- ID：`AR-020`; Status：`ACTIVE`; Implementation：`PARTIAL`; [逐条記録](../96_rd04_nfr_ar_application_review.md)
