# ENH-E4 / G08 P03 — Final Integrated Verification

## 1. Objective

current repository state が E4-G08-AC-001〜005 を統合的に満たすことを検証する。

P03 は過去 Gate PASS の再掲ではなく、**current state の verification** を行う。

---

## 2. Inputs

必須:

```text
06_G08_P00_work_package_plan.md
E4-G08_01_P02_implementation_checkpoint_report.md
current source/tests/migrations/config
```

過去 Gate report は failure の provenance 解決が必要な場合のみ参照する。

---

## 3. Entry Check

```bash
git rev-parse HEAD
git status --short
uv run alembic -c alembic_product.ini heads
```

entry SHA と migration head を記録する。

---

## 4. Verification A — AC-001 Clean Product Bootstrap

real PostgreSQL を使用する。

Repository-managed runner が Product DB reset と Product migration chain を実行するため、まず current runner contract を確認し、clean migration evidence を取得する。

少なくとも:

```text
empty/reset Product test DB
Product migration chain only
current Product head reached
Product DB を用いる application/runtime initialization が成功
```

を確認する。

利用可能な既存 PostgreSQL contract test を優先する。

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_postgres_contract.py \
  -q
```

G08 固有の startup/bootstrap assertion が既存 test に不足する場合だけ、focused G08 test を追加する。

---

## 5. Verification B — AC-002 Three-family Golden Path

対象:

```text
Causal
Exploratory
Predictive
```

各 family について current canonical path を実行し、DB 上で:

```text
Execution
StageExecution
Result
Artifact
```

を確認する。

既存 G05/G04 test を優先的に組み合わせる。

代表的な既存領域:

```text
tests/product/test_enh_e4_g04_result_artifact_postgres.py
tests/product/test_enh_e4_g05_phase_a_postgres.py
tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py
tests/product/test_enh_e4_g05_submission_convergence.py
predictive Product/API/worker tests
```

G08 では three-family を一つの evidence matrix に統合する。

Matrix:

| Family | Execution | StageExecution | Result | Artifact | Authority |
|---|---:|---:|---:|---:|---|
| Causal | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL |
| Exploratory | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL |
| Predictive | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL |

---

## 6. Verification C — AC-003 Mutation + Lineage

既存 mutation tests を優先する。

代表例:

```text
tests/product/test_enh_e4_g05_phase_c_retry_postgres.py
tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py
tests/product/test_enh_e4_g05_phase_c_revise_postgres.py
```

確認:

```text
retry:
  same Execution ID

rerun:
  new ID
  base_execution_id = original
  RERUN
  typed DERIVED_FROM

revise:
  new ID
  base_execution_id = original
  REVISED
  change_reason preserved
  typed REVISED_FROM

cancel:
  canonical state transition
```

Lineage は current G06 contract に対して:

```text
typed structural authority
GENERIC_ONLY semantic persistence
structural generic duplicate = 0
closure/export = derived
```

を確認する。

current repository 上の G06 verification tests を使用する。ファイル名が変更されている場合は current test classification から対応 test を選択し、checkpoint に node/path を記録する。

---

## 7. Verification D — AC-004 Final Authority Audit

positive authority model を current repository 上で検証する。

確認対象:

```text
canonical Execution = Product lifecycle owner
StageExecution = persistent stage owner
Result / Artifact = canonical output owner
typed relation = structural lineage owner
Product migration chain = Product bootstrap owner
GenericExecutor = subordinate mechanism
```

Static evidence と behavioral evidence を組み合わせる。

既存 architecture / authority audit tests を優先する。

代表例:

```text
tests/product/test_architecture.py
tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit.py
tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit_postgres.py
```

G07 で確立した runtime/deployment/bootstrap boundary も current state で保持されていることを確認する。

---

## 8. Verification E — AC-005 Shared Science + Zero Debt

shared science:

```text
tests/scientific/
```

および current Product adapter test を実行する。

代表例:

```text
tests/scientific/test_product_adapters.py
tests/scientific/test_identification_e1a.py
```

P02 final inventory を確認し:

```text
genuine active bounded transition = 0
OPEN TRANSITION DEBT = 0 candidate state
```

を evidence matrix に記録する。

---

## 9. Protected Regression

G02-G07 の protected semantics を current tests から代表選択して実行する。

最低 coverage:

```text
Execution identity / claim
StageExecution
Result / Artifact
three-family convergence
retry / rerun / revise
lineage authority
legacy/runtime/bootstrap boundary
shared science
```

過去 Gate の全 test suite を機械的に再実行する必要はない。

local contract と PostgreSQL contract を分けて記録する。

---

## 10. Acceptance Criteria

P03 COMPLETE 条件:

```text
AC-001 verification PASS
AC-002 verification PASS
AC-003 verification PASS
AC-004 verification PASS
AC-005 verification PASS

protected regression PASS

material Unknown = 0
```

---

## 11. Checkpoint

出力:

```text
20_implementation_reports/G08/Trial01/packages/
E4-G08_01_P03_implementation_checkpoint_report.md
```

含める:

```text
status
entry/checkpoint SHA
migration head
AC-001..005 evidence matrix
exact test commands / node paths
PostgreSQL evidence location
protected regression summary
Unknown
```

---

## 12. Exit / Handoff

P04 へ渡す:

```text
P03 AC matrix
final TD-006 inventory
all exact verification commands
current migration head
remaining documentation-only work
```
