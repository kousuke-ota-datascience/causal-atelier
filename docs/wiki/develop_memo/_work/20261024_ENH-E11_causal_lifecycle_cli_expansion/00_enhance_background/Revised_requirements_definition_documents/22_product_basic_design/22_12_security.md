# 22_12_security


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
| Output directory | private artifact root、owner UIDと0700/0600を検証し、失敗時も保護 | local ext4/XFS、dirfd/path・mode |
| Row-level CATE and individual explanations | Study単独の明示opt-inと機微Artifact扱い、private local FSでの限定export | 一般Linux実行者自身のopt-in、owner-only mode・Method別列/行/byte制限。外部Approver/署名鍵・独立ACL/namespace証明不要 |
| Manifest/Logs | Credential・機微列・個票値を原則含めず、hashや統計量を記録 | deidentification/log retention |
| Backend | optional codeを実効版・license・安全性基準で選別 | package audit and runtime isolation |

Productの`OWNER/EDITOR/VIEWER` RBACはProduct laneの既存契約であり、**Local CLIの個票出力の認可をProduct membershipなしで説明できる設計**が必要。これは未解決のBD-01 blocking itemである。明示opt-inだけであらゆる漏洩対策が完成したと解釈しない。

既存ProductのProject RBACをLocal CLIへ強制適用しない。個票CATE/exportには一般Linux EUID/private ext4-XFS所有root、0700/0600、安全なdirfdとStudy単独の明示opt-inを適用する。独立ACL/xattr証明・mount namespace追跡・CI/container環境種別検出は要求しない。同一UID/rootに対する隔離は保証しない。

**当該機能に適用する設計制約（関連Requirement）**

- **`FR-121`**：全project-scoped routeでpersisted ProjectMembership role（OWNER/EDITOR/VIEWER）に基づくauthorizationをservice action前に検証する
- **`FR-124a`**：Artifact metadata/downloadでProject境界とsafe content dispositionを検証するcurrent contractを維持する
- **`FR-124b`**：legacy/generic routeを含むArtifact downloadでProjectMembership authorizationを一貫適用する
- **`NFR-008a`**：current input validation、path traversal防止、secret非露出等のsafeguardを維持する
- **`AR-020`**：prediction row / local explanationをpotentially sensitive outputとして扱い、Project roleに応じてdetail exposureを制御する
 

### 15.6 Source追跡で確認したProduct APIの認可Gap（PREP-02）

**CURRENT（2026-11-17、GitHub Source静的照合）**：`ProductClosureService`には`_require_role(session, project_id, user_id, roles)`等のMembership検査がある。一方、`ProjectDataService.get_project/list_projects/update_project/archive_project`や`WorkspaceLifecycleService`のResearch Context read/mutateでは、そのService methodがactorを受け取らない／Membership検査を実行していない経路が存在する。Route-levelの権限検証も当該Sourceで確認できない。

**REQUIRED:** FR-121の全Project-scoped操作のdeny-by-defaultは引き続きNormative。単にServiceにRole関数が存在することと、全Endpointが同じ検査を通過することは異なる。外部認証Gatewayの有無は未検証であり、デプロイ環境全体における認可不備の最終判定ではない。

**Disposition:** `23_10`§5.1.2で操作ごとの差分・Source blob・負例を追跡。Product Web/APIのGapはDEC09に従いE11 Local CLIへ転嫁せず、別Product修正のOwner・Issue・Test Evidenceを設定する。E11側でこのGapを解消済みと主張しない。安全な受入以前の状態は`SOURCE_GAP_IDENTIFIED / INTEGRATION_TEST_NOT_RUN`。


### 15.7 PREP-02 Local security authority decision (2026-11-17)

[DEC-PREP02-A historical](../combined_review/decisions/94_20261117_dec_prep02_owner_architecture_choices.md): Original ACL/mount/namespace proof requirement was superseded ONLY for owner-only local ext4/XFS under 2026-11-21 SIM-01 (combined_review/131). Current same-UID/mode/secure-path and G01 atomic publisher remain; no external threat isolation is claimed.

## Local scientific individual-row output

個票中間成果物は、versioned Studyの単一明示選択と実行EUID所有のprivate ext4/XFS TrustedRootで出力可否を判定する。Directory0700・File0600、列/行/byte最小化、G01 atomic Publisher/Readerを維持し、FR-195/NFR-031とProduct RBACを保護する。

## Local scientific row output boundary

個票中間成果物は、versioned Studyで明示要求され、Linux非root実行者が所有するprivate ext4/XFS TrustedRoot、厳格なMethod別出力Schema・許可列・資源上限を満たした場合のみ生成する。個票反復前に適格性を確認し、集計・Manifest・ログへ個票値を露出しない。独立署名承認や二重CLI確認は行わない。既存Product RBACとは別のLocal実行境界であり、同一UID process/特権管理者への隔離を保証しない。公開は既存の原子的Publisher・独立Readerに限定する。


### TrustedRoot-bound local privacy authorization at seal

A supplied decision is not itself a security capability. Authorization to stage and publish must match the *same* validated Study/run/JCS request digest, effective user, verified current TrustedRoot FD (not merely equal path text) and authorized aggregate-only output class. Recompute the local stateless privacy evaluator on actual staged Study and artifact inventory at seal; do not accept a decision for a different run/root/actor, a denied outcome or a changed row artifact. Fail before Marker and atomic rename, then recheck live root/UID and sealed inventory at commit. G01 remains aggregate-only; future G05 row opt-in policy is not expanded. No external signature, trust anchor or key handling is introduced.
