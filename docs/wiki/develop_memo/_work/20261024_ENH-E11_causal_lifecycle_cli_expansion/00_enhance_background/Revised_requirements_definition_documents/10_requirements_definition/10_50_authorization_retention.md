# 10_50_authorization_retention

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## 7.1. Project Authorization / Sensitive Output Boundary

Persisted Project roleは次の3値のみとする。

- `OWNER`
- `EDITOR`
- `VIEWER`

| Action | OWNER | EDITOR | VIEWER |
| --- | --- | --- | --- |
| Project READ | allow | allow | allow |
| WRITE / MUTATE | allow | allow | deny |
| Execution submit/cancel/retry/rerun/revise | allow | allow | deny |
| Export create | allow | allow | deny |
| Membership administration | allow | deny | deny |
| Explicit sensitive output | allow | allow | deny |

独立`EXECUTE` roleは追加しない。prediction row / local explanationはpotentially sensitive outputとして扱う。configurable sensitive-column governanceは`DEFERRED`でありcurrent mandatory acceptanceへ含めない。



## 9. 権限要件

Project-scoped Resourceおよび操作の認可は、§7.1で定義するpersisted Project role `OWNER / EDITOR / VIEWER`をauthorityとする。

* Project-scoped Resourceへアクセスするには、対象Projectに対するmembershipと必要なProject権限を持たなければならない。
* `OWNER / EDITOR / VIEWER`はProjectをreadできる。
* Context、Analysis View、Analysis Specification、Annotationその他のProject ResourceのWRITE / MUTATEは`OWNER / EDITOR`のみ許可する。
* Executionのsubmit / cancel / retry / rerun / reviseは`OWNER / EDITOR`のみ許可する。
* Exportの作成は`OWNER / EDITOR`のみ許可する。
* Project membershipの管理は`OWNER`のみ許可する。
* prediction row / local explanation等のexplicit sensitive outputは`OWNER / EDITOR`のみ取得可能とし、`VIEWER`には返さない。
* 独立した`EXECUTE` Project roleは設けない。
* 認可失敗時は、権限を持たない利用者がResourceの存在を推測できない応答を選択できる。
* system-level Operator authorizationはcurrent Project authorization contractには含めず、`DEFERRED / FUTURE`として扱う。

## 10. データ保持要件とDeferred Audit / Retention Boundary

Current contractで有効なcurrent data-retention contractは次のとおりとする。

* Dataset Version、Result、Artifact metadataおよびExecution snapshotはappend-onlyを基本とする。
* Projectをarchiveしても、Projectに属する既存の分析Resourceをarchive操作だけを理由として物理削除しない。
* Annotationについて、current contractで保持されている変更履歴を維持する。

以下はRequirementとして維持するが、current delivery対象には含めない。

* general operational audit trail (`FR-122`): `DEFERRED / FUTURE`
* configurable retention/deletion policy (`FR-126`): `DEFERRED / FUTURE`

したがってCurrent contractでは、general Audit recordの共通field contract、configurable retention期間、Artifactの一般的な物理削除policyおよび削除audit contractを必須acceptanceとして要求しない。
