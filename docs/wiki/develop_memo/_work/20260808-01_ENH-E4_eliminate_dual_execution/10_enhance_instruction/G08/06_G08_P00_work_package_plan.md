# ENH-E4 / G08 P00 — Work Package Plan

## 1. 目的

G08 は ENH-E4 の最終 Gate である。

テーマ:

```text
E4-G08
Final clean bootstrap and architecture audit
```

目的:

```text
G01-G07 で成立した canonical Product architecture を最終統合検証する
+
TD-006 を解消する
+
OPEN TRANSITION DEBT = 0 を成立させる
```

G08 は新しい authority architecture を設計する Gate ではない。

実行順序:

```text
P01: TD-006 の実体を確定
  ↓
P02: 必要な transition closure を実施
  ↓
P03: final architecture を統合検証
  ↓
P04: candidate freeze / completion
  ↓
Independent Test
```

---

## 2. 共通入力

各 Package は原則として次だけを読む。

1. 当該 Package 指示書
2. 本 P00
3. 直前 Package の checkpoint
4. 現行 source / tests / migrations / config

過去 Gate 文書は、architecture invariant・mutation semantics・lineage authority・provenance に不明点または contradiction がある場合のみ参照する。

通常実行で G01-G07 の全文書を再読しない。

---

## 3. Entry State

```text
G01 PASS
G02 PASS
G03 PASS
G04 PASS
G05 PASS
G06 PASS
G07 PASS

TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 CLOSED
TD-005 CLOSED
TD-006 OPEN
```

G07 fixed candidate:

```text
8e4d7cd6119bc995fca7ea44183bfc7d13ed3445
```

G07 Independent Test report commit:

```text
5edf48a2a2fb38aa8bb3bdfb76373e223b1bf7be
```

G07 時点 Product migration head:

```text
20260809_product_0010
```

G08 開始時に current state を再取得する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
uv run alembic -c alembic_product.ini heads
```

対象 branch:

```text
refactor/ariadne_mvp_e4
```

---

## 4. Positive Authority Model

G08 で維持する final authority model:

```text
Product lifecycle
  -> canonical Execution

stage lifecycle
  -> persistent StageExecution

result ownership
  -> canonical Result

artifact metadata ownership
  -> canonical Artifact

structural lineage
  -> typed structural authority

generic semantic lineage
  -> approved GENERIC_ONLY authority

Product bootstrap
  -> alembic_product.ini / product_migrations

scientific capability
  -> retained shared science
```

`GenericExecutor` は workflow 実行機構であり lifecycle owner ではない。

---

## 5. Mandatory Acceptance Criteria

### E4-G08-AC-001 — Clean Product bootstrap

空 DB から:

```text
Product-only migration
  -> current Product migration head
  -> application startup
```

が成功する。

DB semantics は real PostgreSQL で確認する。

### E4-G08-AC-002 — Three-family Golden Path

```text
Causal
Exploratory
Predictive
```

の各 family が共通して:

```text
Execution
-> StageExecution
-> Result
-> Artifact
```

を canonical ownership の下で生成する。

### E4-G08-AC-003 — Mutation + lineage

確認対象:

```text
retry:
  same Execution ID

rerun:
  new Execution ID
  base_execution_id = original
  revision_kind = RERUN
  typed DERIVED_FROM

revise:
  new Execution ID
  base_execution_id = original
  revision_kind = REVISED
  change_reason preserved
  typed REVISED_FROM

cancel:
  canonical Execution state transition
```

Lineage:

```text
structural relation
  -> typed structural authority

generic-only semantic relation
  -> product_lineage_edge

closure / traversal / export
  -> derived projection
```

### E4-G08-AC-004 — Final authority audit

Section 4 の positive authority model が current runtime / deployment / bootstrap 上で成立し、retired architecture が active authority を持たない。

### E4-G08-AC-005 — Shared science + zero debt

```text
shared scientific capability remains usable
AND
OPEN TRANSITION DEBT = 0
```

---

## 6. TD-006

Formal definition:

```text
E4-TD-006
Authority / transition:
temporary compatibility / read projection

Exit:
bounded transition removed
OR
explicitly archived
```

P01 より前に、具体的な削除対象を仮定しない。

Candidate は semantics / consumer / reachability / authority で分類する。

分類:

```text
REMOVE
ARCHIVE
RETAIN_NON_AUTHORITY
RETAIN_SHARED_CAPABILITY
NOT_TD
```

---

## 7. Known Investigation Seeds

G07 からの調査開始点:

```text
src/ariadne/legacy/
root alembic.ini / migrations/
shared scientific modules
standalone scientific CLI
compatibility/read projection terminology/contracts
```

これらは TD-006 と確定した対象ではない。

current repository の evidence で分類する。

---

## 8. Package Structure

```text
P01
TD-006 inventory / closure decision

P02
transition closure

P03
final integrated verification

P04
candidate freeze / completion
```

P02 は P01 の inventory だけを処理対象とする。

P03 は current architecture の final verification を担当する。

P04 は candidate identity と Independent Test handoff を担当する。

---

## 9. Real PostgreSQL

Repository-managed runner:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [pytest-options]
```

real PostgreSQL を使用する主対象:

```text
migration / clean bootstrap
Execution persistence
StageExecution persistence
Result / Artifact persistence
mutation persistence
lineage persistence
```

Product DB の再構築は canonical Product migration chain で行う。

---

## 10. Trial / Candidate

Current Trial:

```text
Trial01
```

Trial number は formal Independent Test FAIL の後だけ増加する。

P04 で one fixed implementation/test candidate SHA を固定する。

Independent Test では必要に応じて:

```text
fixed candidate
test execution HEAD
test report commit
```

を区別する。

---

## 11. Independent Test Contract

G08 Independent Test Instruction は final candidate freeze より前に固定する。

Test contract は:

```text
G08 AC-001..005
+
P01 が確定する TD-006 scope
```

から構成する。

実装結果を見て acceptance semantics を変更しない。

---

## 12. Checkpoint

P01-P04 の checkpoint は最低限次を記録する。

```text
status: COMPLETE | BLOCKED
entry SHA
checkpoint SHA
files changed
facts established
work performed
tests / commands
remaining issue
Unknown
next entry condition
```

---

## 13. G08 Completion

Coding-side completion:

```text
P01 COMPLETE
P02 COMPLETE
P03 COMPLETE
P04 COMPLETE

AC-001..005 evidence complete
TD-006 = CLOSURE_CANDIDATE
OPEN TRANSITION DEBT = 0 candidate state

fixed candidate SHA established
Independent Test Contract fixed
READY_FOR_TEST
```

Formal PASS は Independent Test が判定する。

```text
AC-001 PASS
AC-002 PASS
AC-003 PASS
AC-004 PASS
AC-005 PASS

TD-001..TD-006 CLOSED
OPEN TRANSITION DEBT = 0
```
