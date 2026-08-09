# ENH-E4 / G07 P04 — Gate Completion / TD-005 Closure Candidate / Independent Test Handoff

## 1. Objective

P04 closes Coding Agent work for E4-G07.

Coverage:

```text
E4-G07-AC-001..005
E4-TD-005 exit criterion
G02..G06 protected architecture
Independent Test readiness
```

P04 does not declare Gate PASS.

Target handoff:

```text
P01-P03 COMPLETE
+
Gate-wide evidence PASS
+
one fixed implementation/test candidate SHA
+
implementation completion report
+
pre-authored Independent Test contract available
=
READY_FOR_TEST
```

TD-005 becomes:

```text
CLOSURE_CANDIDATE
```

only. Formal `CLOSED` requires Independent Test PASS.

---

## 2. Minimal Inputs

Read:

```text
10_enhance_instruction/G07/06_G07_P00_work_package_plan.md
20_implementation_reports/G07/Trial01/packages/
  E4-G07_01_P01_implementation_checkpoint_report.md
  E4-G07_01_P02_implementation_checkpoint_report.md
  E4-G07_01_P03_implementation_checkpoint_report.md
10_enhance_instruction/G07/07_Ariadne_ENH-E4_G07_テスト指示書.md
current relevant source/tests
```

Do not reread P01-P03 instructions unless a checkpoint contradiction requires it.

P00 supplies common Trial, PostgreSQL, evidence, classification, fixed-candidate, and BLOCKED rules.

---

## 3. Entry State

Run:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
```

Required package state:

```text
P01 COMPLETE
P02 COMPLETE
P03 COMPLETE
Trial01
G07 NOT_COMPLETE
TD-005 OPEN
```

Resolve and record actual committed checkpoint SHAs for P01/P02/P03.

If a checkpoint report says `PENDING`, use git history to identify the commit containing that report; do not guess.

Read actual Product migration head from P02 report and verify it against the repository before final freeze.

---

## 4. Gate Contract

P04 must establish final Coding Agent evidence for:

```text
AC-001 runtime legacy independence
AC-002 deployment legacy independence
AC-003 shared scientific preservation
AC-004 Product-only bootstrap
AC-005 CLI lifecycle / compatibility boundary
```

TD-005 exit criterion:

```text
Product runtime does not depend on legacy runtime
AND
Product bootstrap does not depend on legacy migration chain
```

Supporting CLI invariant:

```text
low-level utility CLI does not hide a second persistent Product lifecycle
```

Physical legacy source or historical migration presence alone is not a Gate failure.

---

## 5. Pre-Freeze Consistency Audit

### 5.1 Package chain

Build a table:

```text
Package | checkpoint SHA | status | primary evidence
P01
P02
P03
```

All must be `COMPLETE`.

Confirm no later package invalidated an earlier package assertion.

Minimum cross-check:

```text
P03 current HEAD still passes P01 runtime/deployment guard
P03 current HEAD still passes P02 bootstrap guard
P03 current HEAD retains P02 PostgreSQL bootstrap facts
```

### 5.2 Current changed-file review

Inspect:

```bash
git status --short
git diff --check
```

and package-delta history as needed.

Classify any changes made after P03 checkpoint.

P04 may make a narrowly scoped integration/test-isolation correction if Gate-wide verification exposes a real defect. Such correction remains Trial01 and must be fully rerun before candidate freeze.

Do not freeze a candidate with unexplained working-tree changes.

---

## 6. Final G07 Static / Architecture Verification

Run all G07-specific static/local contracts that exist after P03.

Expected set:

```text
tests/product/test_architecture.py
tests/product/test_enh_e4_g07_p01_runtime_boundary.py
tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py
tests/product/test_enh_e4_g07_p03_cli_boundary.py
tests/product/test_cli_contract.py
```

Adjust only for actual committed filenames.

Example:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_architecture.py \
  tests/product/test_enh_e4_g07_p01_runtime_boundary.py \
  tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py \
  tests/product/test_enh_e4_g07_p03_cli_boundary.py \
  tests/product/test_cli_contract.py
```

If P02 file contains PostgreSQL-only tests, split local/static and PostgreSQL nodes according to markers rather than forcing an invalid local run.

Required static conclusions:

```text
canonical runtime -> ariadne.legacy reachability = 0
repository deployment legacy runtime invocation = 0
shared science import boundary = PASS
Product bootstrap root legacy invocation = 0
low-level CLI persistent lifecycle authority = 0
unclassified analysis CLI = 0
```

---

## 7. Final Product Migration / PostgreSQL Evidence — Mandatory

### 7.1 Migration graph

Run:

```bash
uv run alembic -c alembic_product.ini heads
uv run alembic -c alembic_product.ini history
```

Record actual Product head.

Required:

```text
intended Product head count = 1
Product chain is not spliced with root legacy chain
```

### 7.2 Fresh Product bootstrap

Use the standard runner and the P02 bootstrap/PostgreSQL contract tests.

At minimum:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py \
  tests/product/test_postgres_contract.py \
  -q
```

Use actual P02 test nodes if the file separates static and PostgreSQL cases.

Required evidence:

```text
fresh reset PASS
Product migration upgrade PASS
alembic_version_product exists
DB Product revision == repository Product head
root alembic_version absent
root-only/legacy schema regenerated = 0
```

Record runner metadata/evidence path.

P02 prior evidence is not enough by itself; P04 reruns bootstrap evidence against the final pre-freeze implementation state.

---

## 8. Protected G02-G06 Regression

G07 changes architecture boundaries, packaging, bootstrap, and CLI. Verify canonical authorities were not reactivated or displaced.

### 8.1 Fast canonical contract set

Reuse the representative local selection established in P01 when still applicable:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_enh_e4_g02_canonical_execution.py \
  tests/product/test_enh_e4_g03_generic_executor_boundary.py \
  tests/product/test_enh_e4_g04_result_artifact_contract.py \
  tests/product/test_enh_e4_g05_submission_convergence.py \
  tests/product/test_enh_e4_g06_p06_mutation_lineage.py \
  tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py
```

Record actual pass count; do not hard-code the earlier P01 count as final evidence.

### 8.2 Representative PostgreSQL preservation

Run the established representative persistence set:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g03_acceptance_postgres.py \
  tests/product/test_enh_e4_g04_result_artifact_postgres.py \
  tests/product/test_enh_e4_g05_phase_a_postgres.py \
  tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_revise_postgres.py \
  tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown_postgres.py \
  -q
```

If repository test names changed legitimately, use the current equivalent nodes and explain the mapping.

Coverage intent:

```text
persistent StageExecution
canonical Result/Artifact ownership
three-family canonical submission/convergence
single Product authority
retry/rerun/revise semantics
legacy lifecycle shutdown
```

G06 lineage regression already belongs to the local protected set; add G06 PostgreSQL lineage tests only if G07 changed lineage/runtime code or current evidence creates ambiguity.

---

## 9. Final Residual Legacy Inventory

Merge P01-P03 inventories into one Gate-wide table.

Required columns:

```text
path/surface
classification
runtime reachable?
deployment reachable?
bootstrap reachable?
persistent authority?
shared capability required?
G07 final action
G08 residual
evidence
```

Minimum surfaces:

```text
src/ariadne/legacy/
Product/API/worker runtime roots
pyproject scripts/package exclusion
Dockerfile / .dockerignore / compose.yaml
ariadne.causal / preprocessing / shared / scientific
alembic_product.ini / product_migrations
root alembic.ini / migrations
standalone scientific CLI
compatibility terminology contracts
```

Final classification must distinguish:

```text
RETIRED_UNREACHABLE
HISTORY_ONLY
RETAIN_SHARED_CAPABILITY
LOW_LEVEL_UTILITY
COMPATIBILITY_DATA_CONTRACT
ACTIVE_PRODUCT_DEPENDENCY (canonical/boundary control)
```

Any `ACTIVE_PRODUCT_DEPENDENCY` on retired legacy runtime or root legacy migration prevents READY_FOR_TEST.

---

## 10. TD-005 Closure-Candidate Decision

Set:

```text
TD-005 = CLOSURE_CANDIDATE
```

only if all are true:

```text
1. Product runtime legacy dependency = 0
2. repository-managed Product deployment legacy runtime invocation = 0
3. Product bootstrap legacy migration dependency = 0
4. fresh PostgreSQL Product bootstrap proves Product-only migration state
5. shared scientific capability remains available
6. low-level CLI persistent lifecycle authority = 0
7. no unresolved G07 BLOCKED condition
```

Do not close TD-006 in P04.

Examples that may remain for G08:

```text
physical legacy source/archive cleanup
bounded compatibility terminology/read residuals
final whole-architecture zero-debt audit
```

These residuals must be non-authoritative and explicitly listed.

---

## 11. Compile / Repository Hygiene

Before freeze:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run python -m compileall -q src/ariadne tests/product

git diff --check
git status --short
```

Required:

```text
compile PASS
no diff-check errors
no unexplained executable working-tree changes
```

---

## 12. Fixed Candidate Freeze

### 12.1 Test contract prerequisite

The pre-authored test contract must already exist:

```text
10_enhance_instruction/G07/
07_Ariadne_ENH-E4_G07_テスト指示書.md
```

Its test semantics are not to be rewritten based on P01-P03 outcomes.

It resolves candidate identity from the final completion report rather than containing a future hard-coded SHA.

### 12.2 Freeze procedure

After all required verification is PASS and all implementation/test/config/migration changes are committed:

```bash
git status --short
git rev-parse HEAD
```

The clean HEAD at this point becomes:

```text
Fixed Implementation/Test Candidate SHA
```

Record it immediately.

Any later executable change invalidates the candidate and requires a new freeze + rerun.

Later G07 instruction/report/test-report documentation commits may exist after the candidate, but Independent Test must prove candidate equivalence before testing.

---

## 13. Implementation Completion Report

Create:

```text
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G07/Trial01/
E4-G07_01_implementation_completion_report.md
```

Minimum structure:

```text
# E4-G07 Trial01 Implementation Completion Report

## Identification
- Gate / Trial
- P04 Entry SHA
- P01/P02/P03 checkpoint SHAs
- Fixed Implementation/Test Candidate SHA
- Product Migration Head
- TD-005 = CLOSURE_CANDIDATE

## Package Chain
P01/P02/P03 COMPLETE

## G07 Acceptance Matrix
AC-001..005 with evidence and PASS/FAIL

## Gate-wide Verification
- G07 static/local tests
- final Product migration graph
- final real PostgreSQL bootstrap
- protected G02-G06 regression
- compile/diff hygiene

## Final Residual Legacy Inventory
- P00 §11 columns

## Facts / Interpretation / Unknown

## G08 Residuals
- only bounded non-authoritative residuals

## Handoff
Coding Agent P04: COMPLETE
Gate: READY_FOR_TEST | NOT_READY
Fixed Candidate: <SHA>
Independent Test Contract: READY | NOT_READY
TD-005: CLOSURE_CANDIDATE | OPEN
```

Do not put `G07 PASS` in this report.

---

## 14. P04 Acceptance Criteria

### P04-AC-01 — Package completion

P01/P02/P03 are committed and `COMPLETE`.

### P04-AC-02 — All G07 ACs have final-state evidence

```text
AC-001 PASS
AC-002 PASS
AC-003 PASS
AC-004 PASS
AC-005 PASS
```

at the final pre-freeze implementation state.

### P04-AC-03 — Protected architecture preserved

Representative G02-G06 local/PostgreSQL regressions PASS.

### P04-AC-04 — TD-005 closure candidate justified

Runtime + bootstrap legacy dependency = 0, CLI hidden lifecycle = 0, shared science preserved.

### P04-AC-05 — Candidate fixed

One clean committed implementation/test candidate SHA is frozen after all executable changes and required verification.

### P04-AC-06 — Test handoff ready

Independent Test contract exists and completion report identifies the candidate unambiguously.

All PASS:

```text
P04 = COMPLETE
Gate = READY_FOR_TEST
TD-005 = CLOSURE_CANDIDATE
```

Otherwise:

```text
P04 = BLOCKED or NOT_COMPLETE
Gate != READY_FOR_TEST
```

---

## 15. Independent Test Handoff

When P04 is COMPLETE, hand off only:

```text
10_enhance_instruction/G07/07_Ariadne_ENH-E4_G07_テスト指示書.md
20_implementation_reports/G07/Trial01/E4-G07_01_implementation_completion_report.md
Fixed Implementation/Test Candidate SHA recorded in that report
current repository
```

Independent Test Agent decides:

```text
PASS
FAIL
BLOCKED
```

and writes final decision under:

```text
30_test_report/G07/Trial01/
E4-G07_01_999_gate_decision.md
```

Only Independent Test PASS may produce:

```text
E4-G07 PASS
TD-005 CLOSED
Next Gate = G08
```
