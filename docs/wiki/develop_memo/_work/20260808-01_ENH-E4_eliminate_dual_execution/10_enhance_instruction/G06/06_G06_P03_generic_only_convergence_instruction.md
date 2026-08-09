# ENH-E4 E4-G06 P03 Generic-only Authority Convergence Instruction

- Gate: `E4-G06`
- Trial: `01`
- Package: `P03`
- Package Name: Generic-only authority convergence
- Branch: `refactor/ariadne_mvp_e4`
- File: `10_enhance_instruction/G06/06_G06_P03_generic_only_convergence_instruction.md`
- Governing plan: `06_G06_P00_work_package_plan.md`
- P02 Implementation Checkpoint: `47902c3ae6f07a811d41223eb77c2a5efbc1efa7`
- P02 Report Checkpoint: `27cc0f28c4a342c245bb4a7821ed90473dab9dd9`
- Migration Head: `20260809_product_0010`
- TD-004: `OPEN`

> Common Trial, checkpoint, report-format, PostgreSQL-runner, status, no-test-fitting,
> and Gate-decision rules are inherited from P00 and are intentionally not repeated here.

---

## 1. Objective

P03 closes the **generic persistence admission boundary**.

At P03 exit:

```text
active Product generic lineage writer
    ->
P01 authority policy
    ->
GENERIC_ONLY only persists
```

Therefore:

```text
GENERIC_ONLY
    -> generic persistence allowed

TYPED_STRUCTURAL
    -> generic persistence forbidden

unknown / unapproved tuple
    -> generic persistence forbidden
```

P03 does **not** implement typed read reconstruction or closure/export projection.

---

## 2. Minimal Inputs

Before implementation, inspect only what is needed:

1. this instruction;
2. `06_G06_P00_work_package_plan.md` only when a common operational rule is needed;
3. `E4-G06_01_P02_implementation_checkpoint_report.md`;
4. current:
   - `src/ariadne/product/domain/lineage.py`
   - active `LineageEdgeOrm` writer call sites.

Do **not** reread P01/P02 instruction documents unless a contradiction is found.

---

## 3. Entry Check

P03 implementation starts only after this instruction is committed.

Run:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git ls-files --error-unmatch \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G06/06_G06_P03_generic_only_convergence_instruction.md
```

Record the actual HEAD as `P03 Entry SHA`.

If an unexplained production/test change conflicts with P03 scope, stop as `G06-P03_BLOCKED`.

---

## 4. Fixed Authority Policy

Do not redesign P01 authority semantics.

Current policy is closed-by-default:

```text
classify_lineage_authority(source_type, relation_type, target_type)

TYPED_STRUCTURAL
GENERIC_ONLY
None  # unknown / unapproved
```

`assert_generic_lineage_allowed(...)` permits only `GENERIC_ONLY`.

P03 may correct the policy only if an approved formal contract clearly contradicts the implementation.
Do not expand the allowlist merely to preserve a current direct writer.

---

## 5. Known P03 Starting State

P02 established:

```text
active P01-classified TYPED_STRUCTURAL generic writer = 0
```

for the canonical Product path. P02 left these active Predictive tuples unclassified:

```text
ResearchContextVersion --USED_INPUT--> Execution
AnalysisSpecification  --USED_INPUT--> Execution
ExecutionPlan          --USED_INPUT--> Execution
```

Their identities are already preserved in canonical Execution snapshot/state.

P01 also identified direct generic-only writers including:

```text
Exploratory:
Result --MOTIVATED--> AnalysisSpecificationDraft

ProductClosureService annotation:
approved resource --SELECTED/REJECTED--> Annotation
```

Retired/unreachable Family processing bodies may still contain other generic writers; those are not P03 production-authority targets.

---

## 6. P03 Decision for Unknown / Unapproved Active Writers

The three Predictive `USED_INPUT` tuples above are **not approved GENERIC_ONLY tuples** in the fixed allowlist.

P03 must therefore stop their generic persistence.

Do not relabel them `TYPED_STRUCTURAL` merely to remove them.
Do not add them to `GENERIC_ONLY`.

Expected:

```text
canonical Predictive Execution snapshot/state:
preserved

product_lineage_edge:
ResearchContextVersion USED_INPUT Execution = 0
AnalysisSpecification  USED_INPUT Execution = 0
ExecutionPlan          USED_INPUT Execution = 0
```

Whether these references later appear in lineage reads is a P04 question.

---

## 7. Complete Active Writer Inventory

Before editing, inventory direct Product writes:

```bash
rg -n "LineageEdgeOrm|_lineage\(|_add_lineage\(" src/ariadne/product
```

For each reachable writer/call classify it as:

```text
GENERIC_ONLY
TYPED_STRUCTURAL
UNAPPROVED
RETIRED_UNREACHABLE
```

P03 completion requires:

```text
active unguarded generic writer = 0
active unapproved generic writer = 0
```

Do not modify retired/unreachable bodies solely to make grep output empty.

---

## 8. Important Additional Candidate

Current Exploratory code contains an active lineage call associated with fixing an AnalysisView:

```text
DatasetVersion --USED_INPUT--> AnalysisView
```

`AnalysisView` already has a typed source dataset identity.

This tuple is not an approved GENERIC_ONLY tuple in the fixed P01 policy.

If it remains reachable at P03 Entry SHA, stop its generic persistence while preserving the typed AnalysisView source relationship.

Do not add the tuple to the generic allowlist to preserve current behavior.

---

## 9. Generic-only Writer Convergence

Every **active** writer that persists a GENERIC_ONLY edge must pass through the P01 admission policy before constructing/persisting `LineageEdgeOrm`.

Acceptable implementation:

```text
existing writer
    -> assert_generic_lineage_allowed(...)
    -> LineageEdgeOrm
```

or a small shared helper that performs the same policy check and persistence.

A large repository/service redesign is not required.

Required active cases include, if reachable at P03 Entry SHA:

```text
Result --MOTIVATED--> AnalysisSpecificationDraft

approved resource --SELECTED/REJECTED--> Annotation

manual create_lineage_link() generic-only relations
```

If additional active GENERIC_ONLY writers are found, converge them too.

---

## 10. Preserve Existing Generic-only Semantics

P03 must preserve:

```text
endpoint existence validation
project-boundary validation
self-edge validation where applicable
evidence_json
existing duplicate/idempotent behavior
```

Do not redesign these semantics unless required to make an active writer obey the existing policy.

---

## 11. Retired / Unreachable Writers

Generic writers behind an established retired boundary such as:

```text
LegacyProductAuthorityDisabled
```

may remain in source for G07 cleanup.

Record them as `RETIRED_UNREACHABLE`; do not spend P03 effort rewriting them.

This includes historical Predictive/Exploratory Family process bodies if still unreachable at P03 Entry SHA.

---

## 12. Explicit Non-goals

P03 does not:

```text
implement P04 typed read reconstruction
modify closure/traversal/export semantics
perform P06 retry/rerun/revise audit
delete legacy Family source
clean historical DB rows
add a migration unless strictly required
close TD-004
declare E4-G06 PASS or READY_FOR_TEST
```

These rules are stated once here; P00 supplies the common enforcement details.

---

## 13. Expected Change Area

Likely production files:

```text
src/ariadne/product/application/predictive_workflow_service.py
src/ariadne/product/application/exploratory_service.py
src/ariadne/product/application/product_closure_service.py
```

Possibly a small shared lineage persistence helper.

`src/ariadne/product/domain/lineage.py` should normally remain unchanged.

Migration expectation:

```text
NONE
```

---

## 14. Required Tests

Prefer two focused files:

```text
tests/product/test_enh_e4_g06_p03_generic_only_convergence.py
tests/product/test_enh_e4_g06_p03_generic_only_convergence_postgres.py
```

Exact names may follow repository convention.

### 14.1 Pure/static

Prove:

```text
1. known GENERIC_ONLY tuples remain admitted;
2. unknown/unapproved tuples remain denied;
3. active direct writers cannot bypass admission policy;
4. active unapproved generic writer inventory = 0.
```

### 14.2 PostgreSQL — Predictive unknown rows

Canonical Predictive submit must succeed while creating zero rows for:

```text
ResearchContextVersion USED_INPUT Execution
AnalysisSpecification  USED_INPUT Execution
ExecutionPlan          USED_INPUT Execution
```

Canonical snapshot fields must remain present.

### 14.3 PostgreSQL — Exploratory view source

If `DatasetVersion USED_INPUT AnalysisView` is reachable:

```text
AnalysisView source_dataset_version_id:
preserved

matching generic lineage row:
0
```

### 14.4 PostgreSQL — approved generic-only writer

At least one active system writer, not only the manual API, must persist an approved GENERIC_ONLY edge through the policy.

Preferred examples:

```text
Result MOTIVATED AnalysisSpecificationDraft
```

or:

```text
approved resource SELECTED/REJECTED Annotation
```

Assert one persisted row and preserved evidence.

### 14.5 Regression

Run the P01/P02 focused tests affected by the changes, plus the smallest existing Product regression needed for changed paths.

Do not rerun unrelated Gate-wide suites in P03.

---

## 15. Verification Commands

Use actual test names if implementation changes them.

Pure:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run pytest -q \
  tests/product/test_enh_e4_g06_p03_generic_only_convergence.py \
  tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py \
  tests/product/test_enh_e4_g06_p02_structural_writer_cutover.py
```

PostgreSQL:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p03_generic_only_convergence_postgres.py \
  -q
```

Then run only directly affected existing regressions through the same PostgreSQL runner.

Record exact commands/results/evidence directories per P00.

---

## 16. Acceptance Criteria

P03 is `COMPLETE` only if all are true:

```text
AC-P03-01
Every active generic LineageEdgeOrm writer is inventoried.

AC-P03-02
Every active GENERIC_ONLY writer is guarded by the P01 admission policy.

AC-P03-03
No active unknown/unapproved tuple is generically persisted.

AC-P03-04
The three known Predictive unclassified USED_INPUT rows are no longer written.

AC-P03-05
DatasetVersion USED_INPUT AnalysisView is not generically persisted if still reachable.

AC-P03-06
At least one active GENERIC_ONLY system writer persists successfully with evidence preserved.

AC-P03-07
Project/endpoint validation and relevant P01/P02 regressions remain valid.

AC-P03-08
Focused real PostgreSQL verification passes.

AC-P03-09
Migration = NONE unless explicitly justified.

AC-P03-10
Implementation checkpoint and P03 package report are created.
```

At P03 exit:

```text
E4-G06 = NOT_COMPLETE
TD-004 = OPEN
Next = P04
```

---

## 17. Checkpoint / Report

After tests pass, commit production/test changes and record:

```text
P03 Implementation Checkpoint SHA
```

Then create:

```text
20_implementation_reports/G06/Trial01/packages/
E4-G06_01_P03_implementation_checkpoint_report.md
```

Use the P00 Package Checkpoint Report contract rather than copying its field definitions into this instruction.

P03-specific report additions:

```text
Active Writer Inventory
Removed Unapproved Writers
Guarded Generic-only Writers
Retired/Unreachable Writers
Predictive three-tuple result
Exploratory Dataset->View result
```

Report commit SHA is not the Implementation Checkpoint SHA.

---

## 18. Stop Condition

Stop as `G06-P03_BLOCKED` only when a real contract contradiction exists, for example:

```text
an active writer is required by an approved Product contract,
but the same source/relation/target tuple is neither approved GENERIC_ONLY
nor representable without violating a passed G02-G05 authority contract.
```

Do not block merely because a current test expected an unapproved generic edge.

Report the contradiction as Facts / Interpretation / Unknown per P00.

---

## 19. Final Agent Output

Keep final output compact:

```text
Package:
G06-P03_COMPLETE / G06-P03_BLOCKED

P03 Entry SHA:
...

P03 Implementation Checkpoint SHA:
...

Changed files:
...

Active generic writers:
<guarded / removed / retired counts>

Known Predictive unapproved rows:
0 / nonzero

Exploratory Dataset->AnalysisView generic row:
0 / nonzero / not reachable

Focused tests:
<commands and results>

PostgreSQL evidence:
<paths>

Migration:
NONE / ...

TD-004:
OPEN

Gate:
E4-G06 NOT_COMPLETE

Report:
<path>

Next:
P04
```

Stop after P03. Do not execute P04 automatically.
