# ENH-E4 E4-G06 P06 Mutation / Negative Authority Audit Instruction

- Gate: `E4-G06`
- Trial: `01`
- Package: `P06`
- Package Name: Mutation lineage + negative authority audit
- Branch: `refactor/ariadne_mvp_e4`
- File: `10_enhance_instruction/G06/06_G06_P06_mutation_negative_audit_instruction.md`
- Governing plan: `06_G06_P00_work_package_plan.md`
- P05 Implementation Checkpoint: `502592d7de7af10274d544c9778bbcd1347461d3`
- Migration Head: `20260809_product_0010`
- TD-004: `OPEN`

> Common Trial, checkpoint, report-format, PostgreSQL-runner, status, and Gate-decision
> rules are inherited from P00 and are intentionally not repeated here.

---

## 1. Objective

P06 verifies that the lineage authority model remains correct under Product mutation and that no
active persisted generic lineage row claims typed structural authority.

P06 has two acceptance themes only:

```text
A. mutation semantics
   retry / rerun / revise

B. negative authority audit
   every persisted Product LineageEdgeOrm row
   must classify as GENERIC_ONLY
```

P06 should prefer tests/audits over new architecture.

---

## 2. Minimal Inputs

Before implementation inspect only:

1. this instruction;
2. P00 when a common operational rule is needed;
3. `E4-G06_01_P05_implementation_checkpoint_report.md`;
4. current:
   - `ExecutionService.retry_execution()`
   - canonical rerun/revise submission path
   - P04/P05 mutation-edge reconstruction in `ProductClosureService`
   - `classify_lineage_authority()`
   - active `LineageEdgeOrm` writers.

Do not reread earlier package instructions unless an actual contradiction appears.

---

## 3. Entry Check

P06 starts only after this instruction is committed.

Run:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git ls-files --error-unmatch \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G06/06_G06_P06_mutation_negative_audit_instruction.md
```

Record the actual HEAD as `P06 Entry SHA`.

---

## 4. Starting State

P01-P05 established:

```text
P01:
closed-by-default authority classifier

P02:
active TYPED_STRUCTURAL generic writers = 0

P03:
active unapproved generic writers = 0
active GENERIC_ONLY writers are policy-guarded

P04:
typed structural relations reconstructed on reads

P05:
projection/export preserve source_class and do not create lineage authority
```

Current canonical mutation model uses typed Execution state:

```text
retry:
    same Execution identity

rerun/revise:
    new Execution identity
    base_execution_id
    revision_kind
    change_reason where required
```

P04 read reconstruction derives the Execution-to-Execution lineage edge from this typed state.

---

## 5. Retry Semantics

Verify canonical retry:

```text
before retry:
execution_id = X

after retry:
execution_id = X
```

Expected:

```text
same Execution row
retry_count / retry state advances according to existing lifecycle
failed StageExecution rows become retryable according to current contract
no new Execution row
no new structural LineageEdgeOrm row
```

The lineage graph may continue to show the same existing structural relationships of Execution `X`;
retry itself does not create a new Execution-to-Execution lineage relation.

Use existing lifecycle behavior; P06 does not redesign retry.

---

## 6. Rerun Semantics

Create a rerun from a completed/valid base Execution without changing the effective execution
conditions.

Expected:

```text
new.execution_id != base.execution_id

new.base_execution_id == base.execution_id

new.revision_kind == "RERUN"
```

Read projection must contain:

```text
base Execution --DERIVED_FROM--> new Execution
source_class = TYPED_STRUCTURAL
```

and there must be no matching persisted generic structural row.

Use the current relation direction already implemented by P04.

---

## 7. Revise Semantics

Create a revised Execution by changing an allowed execution condition and supplying the required
change reason.

Expected:

```text
new.execution_id != base.execution_id

new.base_execution_id == base.execution_id

new.revision_kind == "REVISED"

new.change_reason:
non-empty
```

Read projection must contain:

```text
base Execution --REVISED_FROM--> new Execution
source_class = TYPED_STRUCTURAL
```

with no matching persisted generic structural row.

Existing validation for changed revisions remains authoritative.

---

## 8. Family Coverage

The canonical mutation contract is shared.

P06 does not need three duplicated full mutation suites if the common service path is already
covered directly.

Required coverage:

```text
1. common canonical ExecutionService mutation semantics;
2. at least one non-Causal family rerun/revise regression;
3. existing affected Causal/common mutation regression where available.
```

Prefer existing G05 rerun/revise tests rather than recreating equivalent scenarios.

---

## 9. Runtime Negative Authority Audit

This is the main G06 hardening proof.

In a clean PostgreSQL test scenario, create representative Product data that includes:

```text
canonical executions/results/artifacts
at least one retry
at least one rerun or revise
at least one approved GENERIC_ONLY lineage edge
projection/export invocation if useful
```

Then load all persisted `LineageEdgeOrm` rows in the tested project.

For every row:

```text
classify_lineage_authority(
    row.source_type,
    row.relation_type,
    row.target_type,
)
==
LineageAuthority.GENERIC_ONLY
```

Required summary assertion:

```text
persisted TYPED_STRUCTURAL rows = 0
persisted unapproved rows = 0
```

This replaces relation-specific spot checks with a direct authority invariant.

---

## 10. Static Writer Audit

Run a focused source audit:

```bash
rg -n \
  "LineageEdgeOrm|assert_generic_lineage_allowed|classify_lineage_authority" \
  src/ariadne/product
```

Classify remaining write sites as:

```text
ACTIVE_POLICY_GUARDED_GENERIC_ONLY
RETIRED_UNREACHABLE
READ_ONLY
```

P06 complete requires:

```text
active unguarded Product generic writer = 0
```

Do not delete retired/unreachable legacy bodies merely to make grep output empty.

---

## 11. Projection Non-write Regression

P05 already proved projection/export does not create lineage authority.

P06 only needs a compact regression:

```text
LineageEdgeOrm count/classification before projection/export
==
LineageEdgeOrm count/classification after projection/export
```

Do not reimplement P05.

---

## 12. Scope

Expected P06 change is primarily tests.

Production changes are appropriate only if the audit finds an actual active authority defect.

Likely test files:

```text
tests/product/test_enh_e4_g06_p06_mutation_lineage.py
tests/product/test_enh_e4_g06_p06_negative_authority_postgres.py
```

Exact names may follow repository convention.

Expected migration:

```text
NONE
```

---

## 13. Required Tests

### 13.1 Retry

Assert:

```text
same execution ID
no new execution
no new LineageEdgeOrm
existing lifecycle retry behavior preserved
```

### 13.2 Rerun

Assert:

```text
new execution ID
base_execution_id points to source
revision_kind = RERUN

project_lineage():
DERIVED_FROM typed structural edge visible

matching generic structural row = 0
```

### 13.3 Revise

Assert:

```text
new execution ID
base_execution_id points to source
revision_kind = REVISED
change_reason preserved

project_lineage():
REVISED_FROM typed structural edge visible

matching generic structural row = 0
```

### 13.4 Runtime invariant

Assert every persisted Product generic lineage row classifies as:

```text
GENERIC_ONLY
```

and at least one such row exists, so the assertion is not vacuous.

### 13.5 Regression

Run the smallest affected P04/P05 lineage tests and existing rerun/revise lifecycle regressions.

Do not run the full Gate-wide suite; P07 owns Gate-wide completion.

---

## 14. Verification

Focused:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run pytest -q \
  tests/product/test_enh_e4_g06_p06_mutation_lineage.py
```

PostgreSQL:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p06_negative_authority_postgres.py \
  -q
```

Then run only directly affected existing mutation/lineage regression nodes via the standard
PostgreSQL runner.

Record exact commands/results/evidence directories per P00.

---

## 15. Acceptance Criteria

P06 is `COMPLETE` only if:

```text
AC-P06-01
Retry preserves the same canonical Execution identity and creates no lineage authority row.

AC-P06-02
Rerun creates a new Execution with typed base relation and exposes DERIVED_FROM as
TYPED_STRUCTURAL without a generic structural row.

AC-P06-03
Revise creates a new Execution with typed revision state and exposes REVISED_FROM as
TYPED_STRUCTURAL without a generic structural row.

AC-P06-04
Every persisted LineageEdgeOrm row in the focused runtime audit classifies as GENERIC_ONLY.

AC-P06-05
The runtime audit contains at least one persisted GENERIC_ONLY row.

AC-P06-06
Active unguarded Product generic writer count = 0.

AC-P06-07
Projection/export does not alter the persisted lineage authority set.

AC-P06-08
Focused PostgreSQL verification and directly affected regressions pass.

AC-P06-09
Migration = NONE unless explicitly justified.

AC-P06-10
Implementation checkpoint and P06 package report are created.
```

Exit:

```text
E4-G06 = NOT_COMPLETE
TD-004 = OPEN
Next = P07
```

---

## 16. Checkpoint / Report

After verification create the P06 implementation checkpoint and record:

```text
P06 Implementation Checkpoint SHA
```

Then create:

```text
20_implementation_reports/G06/Trial01/packages/
E4-G06_01_P06_implementation_checkpoint_report.md
```

Use the P00 report contract.

P06-specific report content:

```text
Retry identity proof
Rerun typed-lineage proof
Revise typed-lineage proof

Persisted authority audit:
    total LineageEdgeOrm rows
    GENERIC_ONLY count
    TYPED_STRUCTURAL count
    unapproved count

Active writer audit
Projection non-write regression
```

---

## 17. Stop Condition

Stop as `G06-P06_BLOCKED` only if mutation behavior required by passed architecture cannot be
represented by the canonical typed Execution fields currently available.

A normal regression failure or active writer bug should be fixed within P06 rather than treated as a
design block.

---

## 18. Final Agent Output

Keep final output compact:

```text
Package:
G06-P06_COMPLETE / G06-P06_BLOCKED

P06 Entry SHA:
...

P06 Implementation Checkpoint SHA:
...

Changed files:
...

Retry:
PASS / FAIL

Rerun:
PASS / FAIL

Revise:
PASS / FAIL

Persisted lineage audit:
total = ...
GENERIC_ONLY = ...
TYPED_STRUCTURAL = ...
unapproved = ...

Active unguarded writers:
0 / nonzero

Focused tests:
...

PostgreSQL evidence:
...

Migration:
NONE / ...

TD-004:
OPEN

Gate:
E4-G06 NOT_COMPLETE

Report:
...

Next:
P07
```

Stop after P06.
