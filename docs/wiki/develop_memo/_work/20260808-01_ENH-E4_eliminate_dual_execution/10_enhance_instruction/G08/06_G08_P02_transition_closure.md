# ENH-E4 / G08 P02 — Transition Closure

## 1. Objective

P01 で genuine TD-006 と確定した bounded transition を exit criterion に到達させる。

P02 は repository-wide cleanup を行わない。

---

## 2. Inputs

必須:

```text
06_G08_P00_work_package_plan.md
E4-G08_01_P01_implementation_checkpoint_report.md
current repository
```

P01 checkpoint の `P02 action set` を authoritative work list とする。

---

## 3. Entry State

確認:

```bash
git rev-parse HEAD
git status --short
```

P01 checkpoint の:

```text
genuine TD-006 set
classification
P02 action
```

を読み込む。

---

## 4. Required Work

各 P01 item を classification に従って処理する。

### REMOVE

```text
temporary compatibility/read transition を除去
current canonical consumer を保持
再導入を検出できる focused test/guard を保持または追加
```

### ARCHIVE

```text
active transition ではないことを明示
historical/non-authoritative role を repository 内で識別可能にする
runtime/deployment/bootstrap authority がない状態を維持
```

物理 relocation は、それ自体が closure に必要な場合だけ行う。

### RETAIN_NON_AUTHORITY

production behavior を変えない。

次を focused evidence で確認する。

```text
current consumer exists
stable contract
no lifecycle/write/bootstrap/structural-lineage authority
```

### RETAIN_SHARED_CAPABILITY

変更対象外とし、shared capability を保持する。

### NOT_TD

ENH-E4 の変更対象外とする。

---

## 5. Tests

変更した surface に対して focused test を実行する。

既存 test が acceptance semantics を十分に表現している場合は再利用する。

新規 test は、P01 で確定した transition closure を current repository で検証するために必要な場合だけ追加する。

DB semantics を変更する item がある場合は:

```bash
scripts/test/run_product_postgres_tests.sh <focused-test> -q
```

を使用する。

---

## 6. TD-006 Closure Candidate Audit

P02 終了時、P01 inventory の全 item を再評価する。

必要な状態:

```text
REMOVE
  -> removed and verified

ARCHIVE
  -> explicitly non-active/historical and verified

RETAIN_NON_AUTHORITY
  -> stable non-authority contract verified

RETAIN_SHARED_CAPABILITY
  -> preserved

NOT_TD
  -> unchanged unless incidental documentation/test classification was required
```

genuine active bounded transition:

```text
0
```

を目標状態とする。

---

## 7. Acceptance Criteria

P02 COMPLETE 条件:

```text
P01 action set fully processed

genuine active bounded transition = 0

focused verification PASS

canonical Product authority preserved

material Unknown = 0
```

production diff が不要であった場合、`production diff = 0` を明示して COMPLETE としてよい。

---

## 8. Checkpoint

出力:

```text
20_implementation_reports/G08/Trial01/packages/
E4-G08_01_P02_implementation_checkpoint_report.md
```

記録:

```text
status
entry/checkpoint SHA
P01 item -> final disposition
files changed
tests/commands
genuine active bounded transition count
remaining issue
Unknown
```

P02 完了時の implementation-side state:

```text
TD-006 = CLOSURE_CANDIDATE
```

Formal `TD-006 CLOSED` は Independent Test が判定する。

---

## 9. Exit / Handoff

P03 へ渡す情報:

```text
final TD-006 inventory
changed surfaces
focused verification result
current migration head if changed
```
