# ENH-E4 E4-G06 P07 Gate Completion Instruction

- Gate: `E4-G06`
- Trial: `01`
- Package: `P07`
- Package Name: Gate-wide completion / fixed candidate / test handoff
- Branch: `refactor/ariadne_mvp_e4`
- File: `10_enhance_instruction/G06/06_G06_P07_gate_completion_instruction.md`
- Governing plan: `06_G06_P00_work_package_plan.md`
- P06 Implementation Checkpoint: `ab466bfaa02aad154c1a5cd5b8f0506b9b535684`
- Migration Head: `20260809_product_0010`
- TD-004: `OPEN`

> Common Trial, checkpoint, report-format, PostgreSQL-runner, status, and Gate-decision
> rules are inherited from P00 and are intentionally not repeated here.

---

## 1. Objective

P07 closes the Coding Agent side of E4-G06 Trial01.

P07 does not introduce a new lineage architecture.

It must:

```text
1. verify P01-P06 as one integrated G06 candidate;
2. run the required protected regressions;
3. perform final structural/generic authority audits;
4. freeze one Implementation/Test Candidate SHA;
5. create the Trial01 Implementation Completion Report;
6. hand the fixed candidate to the Independent Test Agent.
```

Successful P07 exit status:

```text
READY_FOR_TEST
```

not:

```text
E4-G06 PASS
```

---

## 2. Minimal Inputs

Before execution inspect only:

1. this instruction;
2. P00 when a common operational rule is needed;
3. P01-P06 package checkpoint reports;
4. current test files directly referenced by those reports.

Do not reread P01-P06 instruction documents unless a package report is internally insufficient or
contradictory.

---

## 3. Entry Check

P07 starts only after this instruction is committed.

Run:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git ls-files --error-unmatch \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G06/06_G06_P07_gate_completion_instruction.md
```

Record the actual HEAD as `P07 Entry SHA`.

All P01-P06 reports must exist under:

```text
20_implementation_reports/G06/Trial01/packages/
```

---

## 4. Fixed Package Chain

P07 must preserve the following implementation history.

```text
P01  Authority policy
      ad982f55b73e9602ba7430f6a4820c1bd96b009d

P02  Structural writer cutover
      47902c3ae6f07a811d41223eb77c2a5efbc1efa7

P03  Generic-only convergence
      72fc67f50e6e1c3774d4c6f3fa0bff02110258ec

P04  Typed read reconstruction
      c69e57efff74d567e3e1b0fc152a252faba1e2f7

P05  Projection convergence
      502592d7de7af10274d544c9778bbcd1347461d3

P06  Mutation / negative authority audit
      ab466bfaa02aad154c1a5cd5b8f0506b9b535684
```

P07 may fix a newly discovered integration defect, but if production code changes, the final tested
state must receive a new implementation checkpoint SHA before candidate freeze.

---

## 5. G06 Integrated Contract

P07 verifies the following five Gate criteria as one system.

```text
AC-001
Structural lineage is reconstructed from canonical typed authority.

AC-002
Generic-only lineage is admitted through explicit semantic policy and project/endpoint validation.

AC-003
Active Product paths do not persist structural generic duplicate authority.

AC-004
Closure/export preserve authority source class and do not write lineage authority.

AC-005
Retry/rerun/revise preserve canonical typed lineage semantics.
```

P07 does not reinterpret these criteria.

---

## 6. Gate-wide Test Set

Run all G06 focused tests introduced by P01-P06.

Discover exact files first:

```bash
find tests/product -maxdepth 1 -type f \
  -name 'test_enh_e4_g06_p0*.py' \
  -print | sort
```

Run pure/non-PostgreSQL tests in one or more clean semantic partitions.

Example:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py \
  tests/product/test_enh_e4_g06_p02_structural_writer_cutover.py \
  tests/product/test_enh_e4_g06_p03_generic_only_convergence.py \
  tests/product/test_enh_e4_g06_p04_typed_read_reconstruction.py \
  tests/product/test_enh_e4_g06_p05_projection_convergence.py \
  tests/product/test_enh_e4_g06_p06_mutation_lineage.py
```

Use actual existing filenames.

---

## 7. Gate-wide PostgreSQL Verification

Run every G06 PostgreSQL test file through the standard runner.

Prefer semantic partitions rather than one oversized invocation if fixture/state isolation benefits
from separation.

Minimum coverage must collectively prove:

```text
authority policy
structural writer removal
generic-only persistence
typed read reconstruction
projection/export
mutation lineage
negative persisted-authority audit
```

Example pattern:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p01_authority_policy_postgres.py \
  -q
```

Repeat for the actual P02-P06 PostgreSQL test files.

Every invocation must record:

```text
exact command
exit code
passed
failed
skipped
evidence directory
tested implementation state
```

per P00.

---

## 8. Protected G02-G05 Regression

P07 must show G06 did not regress the canonical architecture established by previous Gates.

Use the smallest representative PostgreSQL regression set that covers:

```text
canonical Execution creation / submission
persistent StageExecution processing
canonical Result / Artifact ownership
Causal / Exploratory / Predictive Product convergence
rerun / revise
legacy Product-authority shutdown
```

Prefer existing G05 tests already used successfully during P02-P06.

Do not rerun every historical ENH-E4 test unless needed.

The Completion Report must list the exact selected nodes/files and why they cover the protected
architecture.

---

## 9. Final Persisted Authority Audit

Run one clean PostgreSQL scenario containing representative G06 behavior.

After:

```text
canonical execution/result/artifact creation
generic-only lineage creation
retry
rerun/revise
project/result lineage reads
export
```

load every persisted Product `LineageEdgeOrm` row in the tested project.

Required invariant:

```text
for every row:
classify_lineage_authority(
    source_type,
    relation_type,
    target_type,
)
==
GENERIC_ONLY
```

Required counts:

```text
TYPED_STRUCTURAL persisted rows = 0
unapproved persisted rows = 0
GENERIC_ONLY persisted rows >= 1
```

The audit must be non-vacuous.

P06 evidence may be reused only by rerunning the test against the final P07 candidate state.

---

## 10. Final Active Writer Audit

Run:

```bash
rg -n \
  "LineageEdgeOrm|assert_generic_lineage_allowed|classify_lineage_authority" \
  src/ariadne/product
```

Final classification:

```text
ACTIVE_POLICY_GUARDED_GENERIC_ONLY
RETIRED_UNREACHABLE
READ_ONLY
```

Required:

```text
active unguarded Product generic writer = 0
```

Retired/unreachable legacy implementation may remain for G07.

---

## 11. Final Projection Audit

Confirm against the final candidate:

```text
typed reconstructed edge
    source_class = TYPED_STRUCTURAL

persisted generic-only edge
    source_class = GENERIC_ONLY

result_lineage()
    preserves source_class

export
    preserves source_class

project/result/export
    create no LineageEdgeOrm rows
```

Also confirm P03-removed unapproved relations remain absent from export/read lineage.

---

## 12. Final Mutation Audit

Confirm:

```text
retry:
same Execution ID
no new lineage authority

rerun:
new Execution
typed base_execution_id
DERIVED_FROM projection
no persisted structural edge

revise:
new Execution
typed base_execution_id
revision_kind=REVISED
change_reason preserved
REVISED_FROM projection
no persisted structural edge
```

This may be satisfied by the final P06 test rerun if executed against the P07 candidate state.

---

## 13. Migration / Repository Checks

Expected migration head:

```text
20260809_product_0010
```

Expected P07 migration:

```text
NONE
```

Also run:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run python -m compileall -q src/ariadne tests/product
```

If repository-wide compileall is impractical, limit it to changed G06 production/tests and record
the exact scope.

Run:

```bash
git diff --check
git status --short
```

No unexplained production/test changes may remain before fixed candidate freeze.

---

## 14. Integration Defect Rule

If P07 finds a real integration defect:

```text
fix it within Trial01
    ->
rerun the affected focused tests
    ->
rerun the required Gate-wide regression/audits
    ->
create a new implementation checkpoint
```

Trial remains `01`.

Do not create Trial02 unless the Independent Test Agent formally returns `FAIL`.

---

## 15. Fixed Implementation/Test Candidate

After all P07 verification passes:

1. ensure the tested production/test state is committed;
2. run:

```bash
git rev-parse HEAD
```

3. record that SHA as:

```text
E4-G06 Trial01 Fixed Implementation/Test Candidate
```

If the Completion Report is committed afterward:

```text
report commit SHA
    !=
Fixed Implementation/Test Candidate SHA
```

The report-only commit must not replace the tested candidate identity.

---

## 16. Implementation Completion Report

Create:

```text
20_implementation_reports/G06/Trial01/
E4-G06_01_implementation_completion_report.md
```

This report is the P07 transaction record; no separate P07 package checkpoint report is required.

Use the P00 Completion Report contract.

Minimum content:

```text
Gate / Trial
P07 Entry SHA
Fixed Implementation/Test Candidate SHA
Migration head

P01-P06 package table:
    package
    implementation checkpoint SHA
    status

G06 AC-001..005 completion matrix

all P07 exact verification commands/results
PostgreSQL evidence directories

final persisted authority audit counts
final active writer audit
final projection audit
final mutation audit

protected G02-G05 regression coverage

changed production/test files since P06, if any

Facts
Interpretation
Unknown / Unconfirmed

TD-004:
CLOSURE_CANDIDATE
pending Independent Test

Gate:
READY_FOR_TEST
```

---

## 17. Independent Test Handoff

P07 successful exit means only:

```text
Coding Agent:
READY_FOR_TEST
```

The Independent Test Agent must test the exact fixed candidate SHA.

Before handoff confirm the G06 Independent Verification Contract exists and is committed:

```text
10_enhance_instruction/G06/
07_Ariadne_ENH-E4_G06_テスト指示書.md
```

If it does not yet exist, report:

```text
READY_FOR_TEST implementation candidate prepared
TEST_CONTRACT_NOT_READY
```

and stop. Do not invent the Independent Test procedure inside the Completion Report.

---

## 18. TD-004 State

Coding Agent P07 may report:

```text
TD-004:
CLOSURE_CANDIDATE
pending Independent Test Agent PASS
```

P07 must not set:

```text
TD-004 CLOSED
```

Formal closure occurs only after G06 Independent Test PASS and Gate Decision.

---

## 19. Acceptance Criteria

P07 is complete only if:

```text
AC-P07-01
All P01-P06 focused tests pass against one final candidate state.

AC-P07-02
Required real PostgreSQL G06 tests pass against that candidate.

AC-P07-03
Representative G02-G05 protected regressions pass.

AC-P07-04
Final persisted authority audit:
TYPED_STRUCTURAL = 0
unapproved = 0
GENERIC_ONLY >= 1.

AC-P07-05
Active unguarded Product generic writer count = 0.

AC-P07-06
Projection/export source-class and non-write invariants pass.

AC-P07-07
Retry/rerun/revise mutation invariants pass.

AC-P07-08
Migration head remains valid and no unauthorized migration exists.

AC-P07-09
One Fixed Implementation/Test Candidate SHA is frozen.

AC-P07-10
E4-G06_01_implementation_completion_report.md is complete.

AC-P07-11
Coding Agent status is READY_FOR_TEST.

AC-P07-12
TD-004 remains pending Independent Test rather than being prematurely CLOSED.
```

---

## 20. Final Agent Output

Keep final output compact:

```text
Package:
G06-P07_COMPLETE / G06-P07_BLOCKED

P07 Entry SHA:
...

Fixed Implementation/Test Candidate SHA:
...

Migration head:
...

P01-P06 package status:
all COMPLETE / ...

G06 focused tests:
...

PostgreSQL verification:
...

Protected G02-G05 regressions:
...

Persisted lineage audit:
GENERIC_ONLY = ...
TYPED_STRUCTURAL = 0
unapproved = 0

Active unguarded writers:
0

Projection audit:
PASS / FAIL

Mutation audit:
PASS / FAIL

TD-004:
CLOSURE_CANDIDATE
pending Independent Test

Gate:
READY_FOR_TEST

Completion Report:
20_implementation_reports/G06/Trial01/
E4-G06_01_implementation_completion_report.md

Independent Test Contract:
READY / NOT_READY
```

Stop after P07. Do not perform the Independent Test Agent role.
