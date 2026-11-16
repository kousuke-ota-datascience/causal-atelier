# 22_12_security

**Status:** `BD01_E11_BASIC_DESIGN_REVISED / OWNER_POLICY_APPROVED / INDEPENDENT_REVIEW_PENDING`. Original chapter and source provenance retained; DD physical coverage remains partial.  
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



### 15.5. Local CLIのセキュリティ境界

| Trust boundary | Required behavior | Open contract |
|---|---|---|
| CLI runner identity | 実行主体はlocal OS実行者。Product `X-User-Id`/Project Roleを強制前提としない | OS user/privilege model and delegation |
| Input Path | Root/path allowlist、traversal・symlink escapeを拒否 | canonical root/reparse/TOCTOU strategy |
| Config / Serialization | Versioned typed inputのみ受入。未信頼のpickleなど任意code実行を既定経路で許さない | exact parser/allowlist |
| Output directory | private artifact root、権限・umask等を設計し、失敗時も保護 | filesystem support, ACL/permissions |
| Row-level CATE and individual explanations | 明示的opt-inと機微Artifact扱い、許可されたexportに限定 | 実行者・承認者の関係、Policy authority / evidence |
| Manifest/Logs | Credential・機微列・個票値を原則含めず、hashや統計量を記録 | deidentification/log retention |
| Backend | optional codeを実効版・license・安全性基準で選別 | package audit and runtime isolation |

Productの`OWNER/EDITOR/VIEWER` RBACはProduct laneの既存契約であり、**Local CLIの個票出力の認可をProduct membershipなしで説明できる設計**が必要。これは未解決のBD-01 blocking itemである。明示opt-inだけであらゆる漏洩対策が完成したと解釈しない。

既存ProductのProject RBACをLocal CLIへ強制適用しない。個票CATE/exportにはOSの実行主体・出力権限・明示opt-inを組み合わせるが、最終的な認可規則・証跡・ACLは未確定の設計事項として扱う。

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
