# ENH-E4 / G08 P01 — TD-006 Inventory and Closure Decision

## 1. Objective

TD-006 の actual scope を current repository から確定し、P02 の処理対象を固定する。

P01 の成果物は「cleanup 候補一覧」ではなく、**consumer / reachability / authority に基づく Transition Debt inventory** である。

---

## 2. Inputs

必須:

```text
06_G08_P00_work_package_plan.md
current repository
G07 Gate Decision
G07 implementation completion report
```

G07 文書は residual provenance の確認だけに使用する。

---

## 3. Entry Check

次を記録する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
uv run alembic -c alembic_product.ini heads
```

記録項目:

```text
branch
entry SHA
working tree state
current Product migration head
```

---

## 4. Known Facts at Entry

G07 formal result:

```text
G07 PASS
TD-005 CLOSED
TD-006 OPEN
```

TD-006 formal definition:

```text
temporary compatibility / read projection
```

Exit:

```text
bounded transition removed
OR
explicitly archived
```

G07 residual investigation seeds:

```text
retired legacy source
historical root migration surface
shared science
standalone scientific CLI
compatibility/read projection contracts
```

これらをそのまま TD-006 とみなさない。

---

## 5. Required Work

### 5.1 Candidate inventory

current repository から material candidate を抽出する。

少なくとも次を確認する。

```text
compatibility/read projection の current consumer
retired source の runtime/deployment/bootstrap reachability
root migration surface の Product bootstrap reachability
shared science の current Product/scientific consumer
standalone CLI の persistent lifecycle ownership
```

既に repository 内に archive/test classification がある場合は、その classification 自体と current reachability を evidence として評価する。

### 5.2 Classification

各 material candidate について以下を記録する。

| Field | Value |
|---|---|
| surface / path | concrete path or contract |
| current consumer | consumer or none |
| runtime reachable | yes/no |
| deployment reachable | yes/no |
| bootstrap reachable | yes/no |
| persistent authority | yes/no |
| new-write authority | yes/no |
| compatibility consumed | yes/no |
| shared capability | yes/no |
| temporary transition | yes/no |
| classification | one of five classes |
| P02 action | concrete action or none |
| evidence | source/test/config reference |

Classification:

```text
REMOVE
ARCHIVE
RETAIN_NON_AUTHORITY
RETAIN_SHARED_CAPABILITY
NOT_TD
```

判断基準:

```text
REMOVE:
  temporary transition で、current consumer に不要

ARCHIVE:
  active transition は終了し、historical retention のみ必要

RETAIN_NON_AUTHORITY:
  current consumer が存在する stable contract だが authority を持たない

RETAIN_SHARED_CAPABILITY:
  scientific/shared capability として必要

NOT_TD:
  Transition Debt の semantic scope 外
```

### 5.3 Genuine TD-006 set

inventory から genuine TD-006 だけを抽出し、P02 action set を作る。

形式:

```text
TD-006-ITEM-01
surface:
classification:
action:
verification:

TD-006-ITEM-02
...
```

genuine item が 0 件の場合も、その fact を evidence 付きで記録する。

---

## 6. Focused Verification

P01 は broad regression を行わない。

必要な verification は classification に必要なものだけとする。

例:

```bash
git grep -n "<candidate-term>" -- src tests deploy configs scripts
```

ただし grep は candidate discovery の補助であり、authority 判定は consumer/reachability で行う。

必要に応じて focused local test を実行する。

---

## 7. Acceptance Criteria

P01 COMPLETE 条件:

```text
current Product migration head recorded

material candidate inventory complete

各 candidate に five-class classification がある

genuine TD-006 set が明示されている

各 genuine item に P02 action がある

material Unknown が 0
```

architecture decision の追加が必要で分類不能な material item がある場合は `BLOCKED` とする。

---

## 8. Checkpoint

出力:

```text
20_implementation_reports/G08/Trial01/packages/
E4-G08_01_P01_implementation_checkpoint_report.md
```

Checkpoint に含める:

```text
status
entry/checkpoint SHA
migration head
TD-006 inventory
genuine TD-006 set
P02 action set
tests/commands
Unknown
```

---

## 9. Exit / Handoff

P01 COMPLETE 後、P02 は **P01 で確定した action set のみ**を入力として実行する。

P01 完了時点では:

```text
TD-006 remains OPEN
```

である。
