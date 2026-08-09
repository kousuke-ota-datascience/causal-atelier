# ENH-E4 E4-G06 P04 Typed Read Reconstruction Instruction

- Gate: `E4-G06`
- Trial: `01`
- Package: `P04`
- Package Name: Typed lineage read reconstruction
- Branch: `refactor/ariadne_mvp_e4`
- File: `10_enhance_instruction/G06/06_G06_P04_typed_read_reconstruction_instruction.md`
- Governing plan: `06_G06_P00_work_package_plan.md`
- P03 Implementation Checkpoint: `72fc67f50e6e1c3774d4c6f3fa0bff02110258ec`
- Migration Head: `20260809_product_0010`
- TD-004: `OPEN`

> Common Trial, checkpoint, report-format, PostgreSQL-runner, status, and Gate-decision
> rules are inherited from P00 and are intentionally not repeated here.

---

## 1. Objective

P04 makes structural lineage readable from canonical typed state after P02/P03 removed
structural/unapproved generic writes.

Target:

```text
canonical typed state
    ->
structural lineage read projection

product_lineage_edge
    ->
GENERIC_ONLY relations only
```

Critical proof:

```text
matching structural generic row = 0

but

lineage read contains the structural relation
```

P04 implements read reconstruction only. Source-class/closure/export convergence belongs to P05.

---

## 2. Minimal Inputs

Before implementation inspect only:

1. this instruction;
2. P00 when a common operational rule is needed;
3. `E4-G06_01_P03_implementation_checkpoint_report.md`;
4. current read-side implementation, primarily:
   - `src/ariadne/product/application/product_closure_service.py`
   - `src/ariadne/product/application/predictive_workflow_service.py`
   - canonical Execution / Result / Artifact ORM definitions as needed.

Do not reread earlier package instructions unless a contract contradiction is found.

---

## 3. Entry Check

P04 starts only after this instruction is committed.

Run:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git ls-files --error-unmatch \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G06/06_G06_P04_typed_read_reconstruction_instruction.md
```

Record the actual HEAD as `P04 Entry SHA`.

---

## 4. P04 Starting State

P01-P03 established:

```text
P01:
source/relation/target authority classifier

P02:
active TYPED_STRUCTURAL generic writers = 0

P03:
active unapproved generic writers = 0
active GENERIC_ONLY writers are policy-guarded
```

P03 explicitly left read completeness to P04.

Known read-side facts at the P03 implementation checkpoint:

```text
ProductClosureService.project_lineage()
    already synthesizes several edges from ORM state,
    then merges persisted LineageEdgeOrm rows.

ProductClosureService.result_lineage()
    derives its connected subgraph from project_lineage().

PredictiveWorkflowService.list_lineage()
    canonical branch still returns only LineageEdgeOrm rows
    connected to execution/result/artifact IDs.
```

P04 converges these reads onto canonical typed structural authority.

---

## 5. Structural Relations to Reconstruct

Reconstruct relations already classified `TYPED_STRUCTURAL` by the fixed P01 policy.

Minimum required set:

```text
DatasetVersion --USED_INPUT--> Execution

AnalysisView --USED_INPUT--> Execution
    when canonical Execution state contains the view identity

Result --USED_INPUT--> Execution
    when canonical Execution state contains input_result_id

Execution --GENERATED--> Result

Result --GENERATED--> Artifact

Execution --DERIVED_FROM/REVISED_FROM--> Execution
    when canonical base/revision state identifies the relation
```

Also reconstruct other P01-approved TYPED_STRUCTURAL relations when the current canonical
typed model provides an unambiguous source field.

Do not reconstruct P03-removed **unapproved** tuples merely because their snapshot IDs still exist.

Examples not automatically restored as lineage:

```text
ResearchContextVersion --USED_INPUT--> Execution
AnalysisSpecification  --USED_INPUT--> Execution
ExecutionPlan          --USED_INPUT--> Execution
```

Their presence in a snapshot is not by itself an approved lineage authority contract.

---

## 6. Canonical Execution Read

`project_lineage()` must treat canonical `Execution` as the Product execution authority for all
analysis families.

At P04 exit, canonical:

```text
CAUSAL
EXPLORATORY
PREDICTIVE
```

executions must be reconstructed from canonical Execution state rather than requiring
`FamilyExecutionOrm` as the structural source.

Preserve family-specific snapshot metadata only as read attributes/input identities; do not
restore FamilyExecution as authority.

Expected examples:

```text
Execution.dataset_version_id
    -> DatasetVersion USED_INPUT Execution

canonical non-Causal analysis_view_id snapshot
    -> AnalysisView USED_INPUT Execution
```

Use actual current canonical fields at P04 Entry SHA.

---

## 7. Result / Artifact Ownership Reconstruction

Canonical ownership already carries structural lineage.

Reconstruct:

```text
Result.execution_id
    -> Execution GENERATED Result
```

and:

```text
Artifact.result_id
    -> Result GENERATED Artifact
```

where the canonical artifact belongs to a result.

If canonical artifact ownership is directly execution-scoped without a result for a valid Product
case, preserve the existing canonical ownership semantics rather than inventing a Result.

The read projection must not depend on matching `LineageEdgeOrm` rows for these relations.

---

## 8. Mutation Reconstruction Boundary

If canonical Execution state contains:

```text
base_execution_id
revision_kind
```

or the equivalent approved typed fields, reconstruct the corresponding Execution-to-Execution
structural edge.

P04 only makes the relation readable.

End-to-end retry/rerun/revise semantic acceptance remains P06.

---

## 9. `project_lineage()` Convergence

Refactor `project_lineage()` so its structural edges come from canonical typed Product state.

Recommended shape:

```text
load canonical Product nodes
    ->
derive typed structural edges
    ->
load persisted GENERIC_ONLY edges
    ->
merge/deduplicate
    ->
return graph
```

A small shared internal reconstruction helper is acceptable if it reduces duplication with
family-specific lineage reads.

Do not introduce a new persistence table.

`result_lineage()` may continue deriving its connected subgraph from `project_lineage()` if that
remains correct after convergence.

---

## 10. Predictive `list_lineage()` Convergence

Canonical Predictive `list_lineage()` must no longer be a `LineageEdgeOrm`-only read.

For the requested canonical execution, return the relevant union of:

```text
typed structural relations
+
persisted GENERIC_ONLY relations
```

At minimum, after a canonical Predictive execution exists:

```text
DatasetVersion USED_INPUT Execution
AnalysisView USED_INPUT Execution   # when present
Execution GENERATED Result          # when result exists
Result GENERATED Artifact           # when artifact exists
```

must be visible even though matching generic structural rows are absent.

Keep the current public response shape unless a minimal additive field is unavoidable.
P05 owns formal authority-source classification in projection responses.

---

## 11. Generic-only Merge

Persisted `LineageEdgeOrm` rows remain valid read inputs only for policy-approved GENERIC_ONLY
semantics established by P03.

When typed and persisted edges share the same output key, deduplicate deterministically.

P04 should not create generic rows during reads.

---

## 12. Scope

Likely production change area:

```text
src/ariadne/product/application/product_closure_service.py
src/ariadne/product/application/predictive_workflow_service.py
```

Potential small shared read helper:

```text
src/ariadne/product/application/...lineage...
```

only if useful.

Expected migration:

```text
NONE
```

P04 does not implement closure/export source classes or legacy source retirement.

---

## 13. Required Tests

Prefer:

```text
tests/product/test_enh_e4_g06_p04_typed_read_reconstruction.py
tests/product/test_enh_e4_g06_p04_typed_read_reconstruction_postgres.py
```

Exact names may follow repository convention.

### 13.1 Project lineage — canonical non-Causal execution

Create a canonical Exploratory or Predictive execution.

Assert:

```text
matching DatasetVersion/AnalysisView structural LineageEdgeOrm rows = 0
```

and:

```text
project_lineage()
contains the expected DatasetVersion/AnalysisView -> Execution edges
```

This is the primary P04 proof.

### 13.2 Result / Artifact ownership

Create/process a canonical execution producing Result and Artifact.

Assert:

```text
matching GENERATED structural LineageEdgeOrm rows = 0
```

while:

```text
project_lineage() / result_lineage()
contains:

Execution GENERATED Result
Result GENERATED Artifact
```

### 13.3 Predictive list_lineage

For a canonical Predictive execution:

```text
structural generic rows = 0
```

but:

```text
list_lineage()
contains typed structural execution/input/output relations
```

If an approved GENERIC_ONLY edge is connected to the same execution graph, assert that it is
also returned.

### 13.4 Unapproved P03 relations stay absent

Confirm P04 does not resurrect:

```text
ResearchContextVersion USED_INPUT Execution
AnalysisSpecification  USED_INPUT Execution
ExecutionPlan          USED_INPUT Execution
```

unless a formal authority correction was explicitly approved before P04 implementation.

### 13.5 Regression

Run the smallest directly affected P01-P03 and existing lineage regressions.
Do not run unrelated Gate-wide suites in P04.

---

## 14. Verification

Pure/focused:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run pytest -q \
  tests/product/test_enh_e4_g06_p04_typed_read_reconstruction.py
```

PostgreSQL:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p04_typed_read_reconstruction_postgres.py \
  -q
```

Then run directly affected existing lineage regression nodes through the standard PostgreSQL
runner.

Record exact commands/results/evidence directories according to P00.

---

## 15. Acceptance Criteria

P04 is `COMPLETE` only if:

```text
AC-P04-01
Canonical Execution is the structural read source for all Product families.

AC-P04-02
DatasetVersion/AnalysisView -> Execution typed relations remain visible with zero matching
structural generic rows.

AC-P04-03
Execution -> Result and Result -> Artifact ownership relations remain visible with zero matching
structural generic rows.

AC-P04-04
Canonical Predictive list_lineage() is not LineageEdgeOrm-only.

AC-P04-05
Persisted GENERIC_ONLY relations remain visible alongside typed structural relations.

AC-P04-06
P03-removed unapproved relations are not recreated as lineage merely from snapshot presence.

AC-P04-07
Focused real PostgreSQL verification passes.

AC-P04-08
Migration = NONE unless explicitly justified.

AC-P04-09
Implementation checkpoint and P04 package report are created.
```

Exit state:

```text
E4-G06 = NOT_COMPLETE
TD-004 = OPEN
Next = P05
```

---

## 16. Checkpoint / Report

After verification, create the implementation checkpoint and record:

```text
P04 Implementation Checkpoint SHA
```

Then create:

```text
20_implementation_reports/G06/Trial01/packages/
E4-G06_01_P04_implementation_checkpoint_report.md
```

Use the P00 report contract.

P04-specific report content:

```text
Reconstructed typed relation matrix
Read endpoints changed
Zero-generic-row proof
Generic-only merge result
Unapproved relations confirmed absent
```

---

## 17. Stop Condition

Stop as `G06-P04_BLOCKED` only if canonical typed state cannot unambiguously reconstruct a
relation that the fixed P01 contract classifies as `TYPED_STRUCTURAL`.

Report:

```text
typed relation
required source identity
actual canonical fields
missing/contradictory authority
```

Do not solve such a contradiction by restoring a structural generic writer.

---

## 18. Final Agent Output

Keep the final response compact:

```text
Package:
G06-P04_COMPLETE / G06-P04_BLOCKED

P04 Entry SHA:
...

P04 Implementation Checkpoint SHA:
...

Changed files:
...

Typed relations reconstructed:
...

Zero-generic-row proofs:
...

Predictive list_lineage:
PASS / FAIL

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
P05
```

Stop after P04.
