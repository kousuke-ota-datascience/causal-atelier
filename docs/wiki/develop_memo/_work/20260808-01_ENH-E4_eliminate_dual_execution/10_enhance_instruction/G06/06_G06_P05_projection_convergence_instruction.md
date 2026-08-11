# ENH-E4 E4-G06 P05 Projection Convergence Instruction

- Gate: `E4-G06`
- Trial: `01`
- Package: `P05`
- Package Name: Closure / export projection convergence
- Branch: `refactor/ariadne_mvp_e4`
- File: `10_enhance_instruction/G06/06_G06_P05_projection_convergence_instruction.md`
- Governing plan: `06_G06_P00_work_package_plan.md`
- P04 Implementation Checkpoint: `c69e57efff74d567e3e1b0fc152a252faba1e2f7`
- Migration Head: `20260809_product_0010`
- TD-004: `OPEN`

> Common Trial, checkpoint, report-format, PostgreSQL-runner, status, and Gate-decision
> rules are inherited from P00 and are intentionally not repeated here.

---

## 1. Objective

P05 establishes the G06 projection boundary:

```text
TYPED_STRUCTURAL authority
        +
GENERIC_ONLY authority
        |
        v
closure / traversal / export
        =
derived projection only
```

Every emitted lineage edge/reference must identify its authority source class:

```text
source_class = TYPED_STRUCTURAL
or
source_class = GENERIC_ONLY
```

Closure/export must not create a new lineage authority.

Primary Gate criterion:

```text
E4-G06-AC-004
closure/exportはsource classを保持し、authorityとしてwriteしない
```

---

## 2. Minimal Inputs

Before implementation inspect only:

1. this instruction;
2. P00 only when a common operational rule is needed;
3. `E4-G06_01_P04_implementation_checkpoint_report.md`;
4. current projection implementation, primarily:
   - `ProductClosureService.project_lineage()`
   - `ProductClosureService.result_lineage()`
   - `ProductClosureService.create_export()`
   - `_synthetic_export_lineage()` or its current equivalent.

Do not reread P01-P04 instruction documents unless a real contract contradiction is found.

---

## 3. Entry Check

P05 starts only after this instruction is committed.

Run:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git ls-files --error-unmatch \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G06/06_G06_P05_projection_convergence_instruction.md
```

Record the actual HEAD as `P05 Entry SHA`.

---

## 4. Starting State

P04 established:

```text
canonical typed state
    -> typed structural read edges

persisted LineageEdgeOrm
    -> GENERIC_ONLY read edges only
```

and proved structural relations remain visible with zero matching structural generic rows.

Current projection still has two P05-specific weaknesses:

```text
project_lineage edge:
    explicit: bool
```

does not explicitly identify the authority source class.

Current export builds:

```text
persisted explicit edges
+
synthetic export lineage
```

and the synthetic builder can emit snapshot-derived `USED_INPUT` relations that are not approved
P01 structural lineage relations.

P05 fixes these projection semantics without changing write authority.

---

## 5. Source-class Contract

Use one explicit output field:

```text
source_class
```

Allowed values:

```text
TYPED_STRUCTURAL
GENERIC_ONLY
```

Meaning:

```text
TYPED_STRUCTURAL
    edge was reconstructed from canonical typed Product authority

GENERIC_ONLY
    edge came from an approved persisted generic lineage authority
```

`PROJECTION_ONLY` describes the closure/export mechanism itself; it is not the authority source of
an underlying lineage edge.

If existing public responses contain:

```text
explicit: bool
```

preserve it for compatibility if needed, but do not use it as the authoritative source classifier.

Recommended compatibility mapping:

```text
typed reconstructed edge:
    source_class = TYPED_STRUCTURAL
    explicit = False

persisted generic-only edge:
    source_class = GENERIC_ONLY
    explicit = True
```

---

## 6. Project Lineage

`project_lineage()` already merges typed reconstructed and persisted generic-only relations.

P05 adds source-class labeling at the edge-construction boundary.

Expected:

```text
DatasetVersion USED_INPUT Execution
    source_class = TYPED_STRUCTURAL

Execution GENERATED Result
    source_class = TYPED_STRUCTURAL

Result GENERATED Artifact
    source_class = TYPED_STRUCTURAL

Result MOTIVATED ...
    source_class = GENERIC_ONLY
```

Deduplication must preserve the authoritative source class.

---

## 7. Result Lineage / Closure

`result_lineage()` currently computes a connected subgraph from `project_lineage()`.

That is acceptable.

P05 requirement:

```text
input edge source_class
    ->
closure output edge source_class unchanged
```

Closure traversal does not create or reclassify lineage authority.

No new persistence is needed.

---

## 8. Export Projection

`create_export()` must build `lineage_references` from the same authority model as P04/P05 reads:

```text
typed structural projection
+
approved generic-only projection
```

Each exported lineage reference must contain:

```text
source_class
```

The export manifest is a snapshot/projection.

Creating an export must not create `LineageEdgeOrm` rows.

---

## 9. Remove Synthetic Authority Drift

Current `_synthetic_export_lineage()` independently derives lineage from result snapshot fields.

This can produce relations such as:

```text
ResearchContextVersion --USED_INPUT--> Execution
AnalysisSpecification  --USED_INPUT--> Execution
```

which P03 intentionally removed as unapproved generic lineage and P04 intentionally did not
reconstruct as typed lineage.

P05 must not reintroduce such relations through export.

Export lineage must be selected from the approved P04 lineage projection semantics rather than
from an independent broader synthetic rule set.

Implementation choice is local:

```text
reuse a shared typed-edge reconstruction helper
```

or:

```text
filter/reuse project_lineage projection for selected results
```

Either is acceptable if the authority semantics are single and testable.

---

## 10. Export Selection Boundary

An export for selected `result_ids` should include lineage references relevant to those results and
their connected Product lineage according to the existing export contract.

P05 does not redesign the external export format beyond the additive source-class information
needed by G06.

Keep:

```text
ariadne-export-manifest/1
```

unless the current schema contract requires a version bump for additive fields.

Do not invent a new external lineage interchange format.

---

## 11. No Projection Write Authority

P05 must prove:

```text
project_lineage()
result_lineage()
create_export()
```

do not create lineage authority rows.

For an export test:

```text
LineageEdgeOrm count before export
    ==
LineageEdgeOrm count after export
```

ExportBundle/manifest persistence is allowed; it is an export artifact, not lineage authority.

---

## 12. Scope

Likely production change:

```text
src/ariadne/product/application/product_closure_service.py
```

A small shared projection helper may be added if it eliminates duplicate structural derivation.

Expected migration:

```text
NONE
```

P05 does not perform mutation-lineage audit or legacy-source cleanup.

---

## 13. Required Tests

Prefer:

```text
tests/product/test_enh_e4_g06_p05_projection_convergence.py
tests/product/test_enh_e4_g06_p05_projection_convergence_postgres.py
```

### 13.1 Project source class

Create a graph containing:

```text
one typed structural edge
one approved generic-only edge
```

Assert:

```text
typed edge.source_class == TYPED_STRUCTURAL
generic edge.source_class == GENERIC_ONLY
```

### 13.2 Closure preserves source class

Call `result_lineage()` on a graph containing both classes.

Assert the selected connected edges retain the same `source_class`.

### 13.3 Export source class

Create an export containing a result whose lineage includes typed structural and generic-only
relations.

Inspect the stored/exported manifest.

Assert each `lineage_references` item has the correct:

```text
source_class
```

### 13.4 Export does not resurrect unapproved relations

For Predictive data containing snapshot IDs, assert export does not emit:

```text
ResearchContextVersion USED_INPUT Execution
AnalysisSpecification  USED_INPUT Execution
ExecutionPlan          USED_INPUT Execution
```

unless a formal authority correction was approved before P05.

### 13.5 Export writes no lineage authority

Assert:

```text
LineageEdgeOrm count before create_export()
==
LineageEdgeOrm count after create_export()
```

### 13.6 Regression

Run the smallest directly affected P04 lineage and existing export regressions.

Do not run unrelated Gate-wide suites in P05.

---

## 14. Verification

Focused:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run pytest -q \
  tests/product/test_enh_e4_g06_p05_projection_convergence.py
```

PostgreSQL:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p05_projection_convergence_postgres.py \
  -q
```

Then run only directly affected existing lineage/export regression nodes with the standard
PostgreSQL runner.

Record exact commands/results/evidence directories per P00.

---

## 15. Acceptance Criteria

P05 is `COMPLETE` only if:

```text
AC-P05-01
project_lineage() identifies every emitted lineage edge as TYPED_STRUCTURAL or GENERIC_ONLY.

AC-P05-02
result_lineage() closure preserves that source class.

AC-P05-03
export lineage references identify their source class.

AC-P05-04
export uses the approved P04 authority projection and does not independently restore P03-removed
unapproved relations.

AC-P05-05
project/result lineage reads and export create zero new LineageEdgeOrm authority rows.

AC-P05-06
typed and generic-only lineage remain visible together where relevant.

AC-P05-07
focused real PostgreSQL verification passes.

AC-P05-08
Migration = NONE unless explicitly justified.

AC-P05-09
Implementation checkpoint and P05 package report are created.
```

Exit:

```text
E4-G06 = NOT_COMPLETE
TD-004 = OPEN
Next = P06
```

---

## 16. Checkpoint / Report

After verification create the implementation checkpoint and record:

```text
P05 Implementation Checkpoint SHA
```

Then create:

```text
20_implementation_reports/G06/Trial01/packages/
E4-G06_01_P05_implementation_checkpoint_report.md
```

Use the P00 package-report contract.

P05-specific report content:

```text
Projection source-class contract
Project-lineage source-class proof
Closure source-class preservation proof
Export source-class proof
Unapproved export relation absence
LineageEdgeOrm before/after export count
```

---

## 17. Stop Condition

Stop as `G06-P05_BLOCKED` only if the existing externally required lineage/export response contract
cannot expose source class without an incompatible schema change that requires an explicit
architecture decision.

Do not treat a normal additive response/test adjustment as a design block.

---

## 18. Final Agent Output

Keep the final response compact:

```text
Package:
G06-P05_COMPLETE / G06-P05_BLOCKED

P05 Entry SHA:
...

P05 Implementation Checkpoint SHA:
...

Changed files:
...

Project source class:
PASS / FAIL

Closure preservation:
PASS / FAIL

Export source class:
PASS / FAIL

Unapproved export relations:
0 / nonzero

LineageEdgeOrm before/after export:
... / ...

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
P06
```

Stop after P05.
