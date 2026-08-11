# Ariadne ENH-E4 E4-G06 Independent Test Instruction

- Gate: `E4-G06`
- Trial: `01`
- Test Role: Independent Test Agent
- File: `10_enhance_instruction/G06/07_Ariadne_ENH-E4_G06_テスト指示書.md`
- Governing Plan: `10_enhance_instruction/G06/06_G06_P00_work_package_plan.md`
- Implementation Completion Report:
  `20_implementation_reports/G06/Trial01/E4-G06_01_implementation_completion_report.md`
- Fixed Implementation/Test Candidate:
  `9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92`
- Expected Migration Head:
  `20260809_product_0010`
- Transition Debt:
  `E4-TD-004 CLOSURE_CANDIDATE`

> Common report-format, PostgreSQL-runner, Facts/Interpretation, and Gate-decision rules are
> inherited from P00 and are intentionally not duplicated here.

---

## 1. Mission

Independently determine whether fixed candidate

```text
9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92
```

satisfies E4-G06.

The Independent Test Agent must not rely on the Coding Agent's PASS claims as evidence.

Final decision:

```text
PASS
FAIL
BLOCKED
```

must be written only in:

```text
30_test_report/G06/Trial01/
E4-G06_01_999_gate_decision.md
```

---

## 2. Minimal Inputs

Read only:

1. this test instruction;
2. `06_G06_P00_work_package_plan.md` when a common rule is needed;
3. `E4-G06_01_implementation_completion_report.md`;
4. current source/tests needed for each Test Item.

Do not reread P01-P07 implementation instructions unless a specific contradiction requires it.

Package reports may be consulted only to investigate a failed or ambiguous observation.

---

## 3. Candidate Identity Rule

The fixed candidate is:

```text
9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92
```

The test instruction and completion report are committed after that candidate, so the Independent
Test Agent may execute from a later documentation-only HEAD.

Before testing, prove that no code/test/runtime/migration file differs from the fixed candidate.

Run:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git diff --name-only \
  9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92..HEAD
```

Classify every post-candidate path.

Allowed after the candidate:

```text
G06 instruction/report documentation only
```

If any production source, test source, migration, runner, configuration, or other executable state
differs from the fixed candidate:

```text
BLOCKED
```

until a new fixed candidate is formally issued.

Record:

```text
Repository HEAD
Fixed Candidate SHA
Candidate-equivalence result
Post-candidate file list
```

in Test Item 001.

---

## 4. Gate Contract

Independent verification covers exactly these G06 criteria:

```text
AC-001
Structural lineage is reconstructed from canonical typed authority.

AC-002
GENERIC_ONLY persistence is controlled by explicit semantic policy and validation.

AC-003
Active Product paths do not persist structural generic duplicate authority.

AC-004
Closure/export preserve authority source class and do not become lineage authority.

AC-005
Retry/rerun/revise preserve canonical typed lineage semantics.
```

Protected G02-G05 canonical architecture must also remain valid.

---

## 5. Test Report Set

Create:

```text
30_test_report/G06/Trial01/
├── E4-G06_01_001_candidate_identity.md
├── E4-G06_01_002_typed_structural_reconstruction.md
├── E4-G06_01_003_generic_only_policy.md
├── E4-G06_01_004_negative_authority_audit.md
├── E4-G06_01_005_projection_export.md
├── E4-G06_01_006_mutation_lineage.md
├── E4-G06_01_007_protected_regression.md
├── E4-G06_01_008_architecture_exit_audit.md
└── E4-G06_01_999_gate_decision.md
```

Each `001`–`008` report gets its own:

```text
PASS
FAIL
BLOCKED
```

test-item result.

---

# Test Item 001 — Candidate Identity

## 6. Purpose

Prove that all following tests execute against the fixed implementation/test candidate.

## 7. Checks

Record:

```bash
git rev-parse HEAD
git status --short
git diff --name-only \
  9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92..HEAD
```

Verify the candidate commit exists:

```bash
git cat-file -e \
  9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92^{commit}
```

Verify expected migration head using the repository's existing migration-head check or the same
mechanism used by the standard PostgreSQL runner.

Expected:

```text
Fixed candidate exists
Post-candidate changes are documentation-only
Migration head = 20260809_product_0010
Working tree contains no unexplained executable changes
```

Output:

```text
E4-G06_01_001_candidate_identity.md
```

---

# Test Item 002 — Typed Structural Reconstruction

## 8. Purpose

Independently verify AC-001.

Core invariant:

```text
structural generic row = 0

while

typed structural lineage remains visible
```

## 9. Required Coverage

Use canonical Product state to verify at least:

```text
DatasetVersion --USED_INPUT--> Execution

AnalysisView --USED_INPUT--> Execution
    where applicable

Execution --GENERATED--> Result

Result --GENERATED--> Artifact
```

Use at least one non-Causal canonical execution.

Also verify canonical Execution is the read authority rather than requiring a FamilyExecution
authority.

## 10. Verification

Run the P04 PostgreSQL test against the fixed candidate:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p04_typed_read_reconstruction_postgres.py \
  -q
```

Then inspect the relevant implementation and test assertions independently.

Required observed behavior:

```text
matching structural LineageEdgeOrm rows = 0
project/result/predictive lineage read returns the structural relation
```

Output:

```text
E4-G06_01_002_typed_structural_reconstruction.md
```

---

# Test Item 003 — Generic-only Policy

## 11. Purpose

Independently verify AC-002.

## 12. Required Behavior

Verify the central classifier is based on:

```text
source type
+
relation
+
target type
```

and is closed by default.

At minimum verify:

```text
Execution DERIVED_FROM Execution
    -> TYPED_STRUCTURAL

Artifact DERIVED_FROM Artifact
    -> GENERIC_ONLY
```

This proves relation name alone does not determine authority.

Verify:

```text
approved GENERIC_ONLY tuple:
persist allowed

TYPED_STRUCTURAL tuple:
generic persist rejected

unknown/unapproved tuple:
generic persist rejected
```

and preserve:

```text
endpoint existence
project boundary
```

validation.

## 13. Verification

Run:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py
```

and:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p01_authority_policy_postgres.py \
  tests/product/test_enh_e4_g06_p03_generic_only_convergence_postgres.py \
  -q
```

Inspect the classifier and active generic writers to confirm the runtime test is exercising the
actual policy.

Output:

```text
E4-G06_01_003_generic_only_policy.md
```

---

# Test Item 004 — Negative Authority Audit

## 14. Purpose

Independently verify AC-003 and the final persisted-authority invariant.

## 15. Runtime Invariant

Run the final P06 authority audit:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p06_negative_authority_postgres.py \
  -q
```

The tested scenario must contain at least one persisted GENERIC_ONLY row.

Required:

```text
GENERIC_ONLY >= 1
TYPED_STRUCTURAL persisted = 0
unapproved persisted = 0
```

For each persisted Product `LineageEdgeOrm` row:

```text
classify_lineage_authority(
    source_type,
    relation_type,
    target_type,
)
==
GENERIC_ONLY
```

## 16. Static Writer Audit

Run:

```bash
rg -n \
  "LineageEdgeOrm|assert_generic_lineage_allowed|classify_lineage_authority" \
  src/ariadne/product
```

Classify findings as:

```text
ACTIVE_POLICY_GUARDED_GENERIC_ONLY
RETIRED_UNREACHABLE
READ_ONLY
```

Required:

```text
active unguarded Product generic writer = 0
```

Retired/unreachable source does not fail the Gate by itself.

Output:

```text
E4-G06_01_004_negative_authority_audit.md
```

---

# Test Item 005 — Projection / Export

## 17. Purpose

Independently verify AC-004.

## 18. Required Behavior

Verify:

```text
typed reconstructed edge:
source_class = TYPED_STRUCTURAL

persisted generic-only edge:
source_class = GENERIC_ONLY
```

and:

```text
result_lineage()
preserves source_class
```

and:

```text
export lineage reference
preserves source_class
```

Projection/export must not create lineage authority:

```text
LineageEdgeOrm before
==
LineageEdgeOrm after
```

Confirm export/read does not resurrect P03-removed unapproved relations such as:

```text
ResearchContextVersion USED_INPUT Execution
AnalysisSpecification  USED_INPUT Execution
ExecutionPlan          USED_INPUT Execution
```

## 19. Verification

Run:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p05_projection_convergence_postgres.py \
  -q
```

Inspect `ProductClosureService` projection/export flow enough to verify the test is not merely
asserting a mocked response.

Output:

```text
E4-G06_01_005_projection_export.md
```

---

# Test Item 006 — Mutation Lineage

## 20. Purpose

Independently verify AC-005.

## 21. Retry

Required:

```text
same Execution ID
no new Execution
no new lineage authority
```

## 22. Rerun

Required:

```text
new Execution ID
base_execution_id points to base
revision_kind = RERUN

DERIVED_FROM visible as TYPED_STRUCTURAL projection
matching generic structural row = 0
```

## 23. Revise

Required:

```text
new Execution ID
base_execution_id points to base
revision_kind = REVISED
change_reason preserved

REVISED_FROM visible as TYPED_STRUCTURAL projection
matching generic structural row = 0
```

## 24. Verification

Run the P06 mutation test and relevant existing G05 mutation regressions:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_enh_e4_g06_p06_mutation_lineage.py
```

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_revise_postgres.py \
  -q
```

Output:

```text
E4-G06_01_006_mutation_lineage.md
```

---

# Test Item 007 — Protected Regression

## 25. Purpose

Verify G06 did not regress the canonical authority established by G02-G05.

## 26. Required Coverage

Run the established representative PostgreSQL set:

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

Coverage intent:

```text
persistent StageExecution
canonical Result/Artifact ownership
canonical family submission
Exploratory convergence
Product authority
rerun/revise
legacy lifecycle shutdown
```

Output:

```text
E4-G06_01_007_protected_regression.md
```

---

# Test Item 008 — Architecture Exit Audit

## 27. Purpose

Determine whether G06 can actually close TD-004 and hand off to G07.

This is an architecture audit, not another broad test run.

## 28. Audit Questions

Answer each with evidence:

```text
1. Is canonical typed state the sole authority for structural lineage?

2. Is generic persistence restricted to approved GENERIC_ONLY relations?

3. Can any active Product writer still persist TYPED_STRUCTURAL or unapproved lineage?

4. Do lineage reads reconstruct structural relations without requiring duplicate generic rows?

5. Do closure/export preserve source class without becoming authority?

6. Do retry/rerun/revise preserve the typed mutation model?

7. Are remaining Family/legacy lineage references only read compatibility or unreachable source,
   rather than active Product authority?

8. Is any unresolved lineage authority responsibility still assigned to TD-004?
```

A remaining legacy read adapter or unreachable legacy implementation does not by itself block G06;
source retirement belongs to G07.

Required conclusion if all answers support the target:

```text
TD-004 exit criterion satisfied
```

Output:

```text
E4-G06_01_008_architecture_exit_audit.md
```

---

# Final Gate Decision

## 29. Decision Inputs

`999` must consider all Test Items:

```text
001 Candidate identity
002 Typed structural reconstruction
003 Generic-only policy
004 Negative authority audit
005 Projection/export
006 Mutation lineage
007 Protected regression
008 Architecture exit audit
```

Do not substitute the Coding Agent Completion Report for any mandatory independent result.

---

## 30. PASS

Return `PASS` only if:

```text
all Test Items 001-008 = PASS

AC-001..005 independently satisfied

fixed candidate identity preserved

no active structural/unapproved generic authority remains

protected G02-G05 architecture remains valid

TD-004 exit criterion is satisfied
```

Then `999` records:

```text
E4-G06:
PASS

TD-004:
CLOSED

Next Gate:
E4-G07
```

Control Sheet promotion remains an operator action after the Gate Decision.

---

## 31. FAIL

Return `FAIL` when a reproducible defect in the fixed candidate violates a G06 Acceptance Criterion
or protected passed-Gate contract.

Record:

```text
failed Test Item
exact tested SHA/state
exact command
expected
actual
reproduction procedure
affected AC
Facts
Interpretation
```

A formal `FAIL` is what permits Trial02 remediation.

---

## 32. BLOCKED

Return `BLOCKED` when the Independent Test Agent cannot validly determine PASS/FAIL, for example:

```text
fixed candidate cannot be reconstructed
post-candidate executable state differs from candidate
required standard PostgreSQL verification environment is unavailable
formal contracts are contradictory and prevent an unambiguous expected result
```

Do not use `BLOCKED` for an ordinary candidate defect.

---

## 33. Gate Decision File

Create:

```text
30_test_report/G06/Trial01/
E4-G06_01_999_gate_decision.md
```

Minimum content:

```text
Gate / Trial
Decision: PASS / FAIL / BLOCKED
Fixed Candidate SHA
Repository/Tested State
Migration Head

Test Item summary:
001 ... PASS/FAIL/BLOCKED
...
008 ... PASS/FAIL/BLOCKED

AC-001..005 mapping

Persisted authority audit summary
Active writer audit summary
Projection/export summary
Mutation summary
Protected regression summary

TD-004:
CLOSED only if PASS
otherwise OPEN

Next Gate:
G07 only if PASS

Facts
Interpretation
Unknown / Unconfirmed
```

---

## 34. Independent Test Agent Final Output

Keep the chat response compact:

```text
E4-G06 Trial01:
PASS / FAIL / BLOCKED

Fixed Candidate:
9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92

Test Items:
001 ...
002 ...
003 ...
004 ...
005 ...
006 ...
007 ...
008 ...

TD-004:
CLOSED / OPEN

Gate Decision:
30_test_report/G06/Trial01/E4-G06_01_999_gate_decision.md

Next:
G07 / Trial02 remediation / resolve BLOCKED condition
```

Do not modify production code while acting as the Independent Test Agent.
