# Ariadne ENH-E4 / G08 Independent Test 指示書

## 1. Test Objective

E4-G08 fixed implementation/test candidate が、ENH-E4 final architecture と Transition Debt closure condition を独立に満たすか判定する。

Mandatory Gate AC:

```text
E4-G08-AC-001
clean Product bootstrap + startup

E4-G08-AC-002
Causal / Exploratory / Predictive
-> canonical Execution / StageExecution / Result / Artifact

E4-G08-AC-003
retry / rerun / revise / cancel
+ canonical lineage authority

E4-G08-AC-004
final Product authority / legacy / migration audit

E4-G08-AC-005
shared science preserved
+ OPEN TRANSITION DEBT = 0
```

---

## 2. Independence Contract

Independent Test Agent は fixed candidate を変更しない。

test/report execution 中に production implementation を修正しない。

Acceptance semantics は本指示書と formal G08 AC を固定入力とする。

P01 final TD-006 inventory は **具体的な test target の解決**に使用し、AC の意味を変更するためには使用しない。

---

## 3. Minimal Inputs

必須:

```text
07_Ariadne_ENH-E4_G08_テスト指示書.md

20_implementation_reports/G08/Trial01/
E4-G08_01_implementation_completion_report.md

20_implementation_reports/G08/Trial01/packages/
E4-G08_01_P01_implementation_checkpoint_report.md

fixed candidate repository state
```

追加参照は、evidence contradiction または provenance 解決が必要な場合だけ行う。

---

## 4. Candidate Identity

最初に次を記録する。

```bash
git rev-parse HEAD
git status --short
git show --no-patch --format=fuller <FIXED_CANDIDATE_SHA>
```

Independent Test Contract ancestor proof:

```bash
git merge-base --is-ancestor \
  <TEST_CONTRACT_SHA> \
  <FIXED_CANDIDATE_SHA>
echo $?
```

必要に応じて candidate と execution HEAD の差分を確認する。

```bash
git diff --name-status \
  <FIXED_CANDIDATE_SHA>..HEAD
```

candidate equivalence を損なう executable source/test/migration/runner/config/deployment difference がある場合は、candidate identity item を PASS にしない。

---

# 5. Test Items

Independent Test report は Item 001〜007 と 999 を作成する。

---

## Item 001 — Candidate Identity

Report:

```text
30_test_report/G08/Trial01/
E4-G08_01_001_candidate_identity.md
```

判定:

```text
fixed candidate exists
test-contract ancestor proof PASS
execution HEAD identified
candidate equivalence established
```

Result:

```text
PASS | FAIL | BLOCKED
```

---

## Item 002 — Clean Product Bootstrap + Startup

Report:

```text
E4-G08_01_002_clean_bootstrap_startup.md
```

対象 AC:

```text
AC-001
```

real PostgreSQL を必須とする。

Repository-managed entry point:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [pytest-options]
```

最低限確認:

```text
Product test DB reset / empty bootstrap
Product migration chain only
current Product migration head reached
Product DB を使用する application/runtime startup/init path succeeds
root historical migration chain is not Product bootstrap authority
```

既存 `tests/product/test_postgres_contract.py` および current G08 bootstrap/startup test を優先して使用する。

Report に記録:

```text
command
migration head
PostgreSQL evidence path
startup evidence
Result
```

---

## Item 003 — Three-family Golden Path

Report:

```text
E4-G08_01_003_three_family_golden_path.md
```

対象 AC:

```text
AC-002
```

real PostgreSQL を使用する。

独立に:

```text
Causal
Exploratory
Predictive
```

を実行し、各 family で:

```text
Execution
StageExecution
Result
Artifact
```

を確認する。

Evidence matrix:

| Family | Execution | StageExecution | Result | Artifact | canonical ownership |
|---|---:|---:|---:|---:|---|
| Causal | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL |
| Exploratory | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL |
| Predictive | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL |

既存 G04/G05/Product E2E tests を再利用してよい。

---

## Item 004 — Mutation + Lineage

Report:

```text
E4-G08_01_004_mutation_lineage.md
```

対象 AC:

```text
AC-003
```

real PostgreSQL evidence を使用する。

確認:

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
  canonical state transition
```

Lineage authority:

```text
structural relation:
  typed structural authority

generic-only relation:
  approved GENERIC_ONLY persistence

structural generic persisted duplicate:
  0

closure/export:
  derived projection
```

既存 mutation test:

```text
tests/product/test_enh_e4_g05_phase_c_retry_postgres.py
tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py
tests/product/test_enh_e4_g05_phase_c_revise_postgres.py
```

および current G06 lineage verification test を使用する。

current path が異なる場合は exact path/node を report に記録する。

---

## Item 005 — Final Authority Audit

Report:

```text
E4-G08_01_005_final_authority_audit.md
```

対象 AC:

```text
AC-004
```

Positive authority model:

```text
Execution = Product lifecycle authority
StageExecution = persistent stage authority
Result / Artifact = canonical output ownership
typed relation = structural lineage authority
Product migrations = Product bootstrap authority
GenericExecutor = subordinate mechanism
shared science = capability, not lifecycle authority
```

current source/config/deployment/migration と behavioral tests から検証する。

既存 authority/architecture tests を優先する。

代表例:

```text
tests/product/test_architecture.py
tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit.py
tests/product/test_enh_e4_g05_phase_d_d3_global_authority_audit_postgres.py
```

G07 で確立した runtime/deployment/bootstrap boundary も current candidate で保持されていることを確認する。

---

## Item 006 — Shared Science + Transition Debt

Report:

```text
E4-G08_01_006_shared_science_transition_debt.md
```

対象 AC:

```text
AC-005
```

shared science は current scientific regression を実行する。

代表:

```bash
uv run pytest -q \
  tests/scientific/test_identification_e1a.py \
  tests/scientific/test_product_adapters.py
```

TD-006 は P01 final inventory の全 material item を独立再評価する。

各 row が:

```text
REMOVE
ARCHIVE
RETAIN_NON_AUTHORITY
RETAIN_SHARED_CAPABILITY
NOT_TD
```

の定義に適合することを evidence で確認する。

Required final state:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 CLOSED
TD-005 CLOSED
TD-006 CLOSED

OPEN TRANSITION DEBT = 0
```

---

## Item 007 — Protected Final Regression

Report:

```text
E4-G08_01_007_protected_final_regression.md
```

G02-G07 の protected semantics を current candidate で検証する。

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

P03 completion report の protected regression selection を starting set として使用する。

Independent Agent はその selection が上記 coverage を満たすことを確認した上で実行する。

local と PostgreSQL の結果を分けて記録する。

---

# 6. PostgreSQL Evidence Contract

DB semantics が material な Item 002/003/004/005/007 では、必要部分を repository-managed runner で実行する。

```bash
scripts/test/run_product_postgres_tests.sh \
  <pytest-path-or-node> \
  [pytest-options]
```

Runner evidence location を report に記録する。

mock/in-memory result は real DB semantics の代替としない。

---

# 7. Result Rule

各 Item:

```text
PASS
FAIL
BLOCKED
```

`PASS` は required evidence が揃い acceptance semantics を満たす場合のみ。

execution infrastructure が利用不能で required evidence を取得できない場合は `BLOCKED`。

architecture/test failure は `FAIL`。

---

# 8. Gate Decision

Report:

```text
30_test_report/G08/Trial01/
E4-G08_01_999_gate_decision.md
```

Gate PASS 条件:

```text
Item 001 PASS
Item 002 PASS
Item 003 PASS
Item 004 PASS
Item 005 PASS
Item 006 PASS
Item 007 PASS

AC-001 PASS
AC-002 PASS
AC-003 PASS
AC-004 PASS
AC-005 PASS

TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 CLOSED
TD-005 CLOSED
TD-006 CLOSED

OPEN TRANSITION DEBT = 0
```

一つでも mandatory Item/AC が FAIL の場合:

```text
E4-G08 Trial01: FAIL
E4-G08: FAIL
```

required independent evidence が取得不能なら:

```text
E4-G08 Trial01: BLOCKED
E4-G08: BLOCKED
```

---

# 9. 999 Report Minimum Content

```text
Gate / Trial
Decision
Fixed Candidate SHA
Independent Test execution HEAD
Independent Test Contract SHA
Candidate equivalence
Product migration head

Item 001..007 results
AC-001..005 mapping
Transition Debt final state

Facts
Interpretation
Unknown

Final ENH-E4 decision
```

G08 PASS の場合:

```text
E4-G08 Trial01: PASS
E4-G08: PASS

TD-006: CLOSED
OPEN TRANSITION DEBT = 0

ENH-E4 final architecture gate complete
```
