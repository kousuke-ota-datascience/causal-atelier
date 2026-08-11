# Ariadne ENH-E4 E4-G05 テスト・監査指示書

* Project: Ariadne / causal-atelier
* Enhancement: ENH-E4 eliminate dual execution
* Branch: `refactor/ariadne_mvp_e4`
* Gate: `E4-G05`
* Gate name: Product Execution Convergence
* Trial: `01`
* Expected baseline repository ref: `d2b0f311fda209608629114aaae9a1ea142bdd2d` or documentation-only descendant
* Expected pre-G05 Product migration head: `20260809_product_0009`
* Prerequisite: E4-G04 Trial 02 `PASS`
* Standard Test PostgreSQL Infrastructure: mandatory
* Trial ID format: 2-digit zero-padded decimal (`01`–`99`)
* Test Item ID format: 3-digit zero-padded decimal (`001`–`998`; `000` reserved; `999` Gate Decision)

---

# 1. Source of Truth

本書は **E4-G05 Trial 01 Test / Audit Agentが従う唯一のGate-local verification contract** である。

Expected handoff:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/
E4-G05_01_implementation_completion_report.md
```

Inputs:

```text
1. 本07
2. G05 Implementation Completion Report
3. fixed implementation commit actual tree/diff
4. G05 06
5. G04 final Gate Decision
6. G03 final Gate Decision
7. architecture Gate decomposition
8. repository report templates
```

G05 ACは本07で固定する。

---

# 2. Transition Debt

G05 PASS requires:

```text
E4-TD-001 = CLOSED
E4-TD-002 = CLOSED
E4-TD-003 = CLOSED
```

Lineage handoff:

```text
E4-TD-004 = OPEN until G06
```

remaining structural generic duplicate writesを監査可能に記録する。

G05でG06 consolidationを要求しない。

---

# 3. Report Format Is Part of Test Completion

開始時に:

```text
docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template_complete/
30_test_report/
README.md

TEMPLATE_test_item_report.md
TEMPLATE_gate_decision_report.md
```

を実物参照する。

Every Test Item Report / Gate Decision Report MUST preserve all required fields.

禁止:

```text
required section/field省略
独自merge
short-form report
"same as previous"
"same command"
"上記runner"
command要約のみ
exit code省略
reproduction procedure省略
facts/interpretation混同
```

値なし:

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

`Commands Executed`にはcomplete copy-pastable actual commandを記載する。

shared commandでも各reportへ完全再掲。

**Substantive test success does not waive report-format compliance.**

---

# 4. Test Agent Role

1. branch / fixed implementation SHA確認。
2. handoff report template compliance確認。
3. implementation diff / scope監査。
4. route-to-authority inventoryをactual sourceと照合。
5. Causal Golden Path real PostgreSQL。
6. Exploratory Golden Path real PostgreSQL。
7. Predictive Golden Path real PostgreSQL。
8. cross-family claim/stage/result/artifact authority検証。
9. old family new-write停止をstatic + runtime検証。
10. old family table row-count negativeをreal PostgreSQL検証。
11. mutation/read projection convergence検証。
12. CLI boundary監査。
13. G02/G03/G04 regression。
14. TD-001/002/003 closure監査。
15. TD-004 inventory記録。
16. future-Gate scope監査。
17. template-compliant reports作成。
18. PASS / FAIL / BLOCKED判定。
19. source/test/migrationを変更せず停止。

---

# 5. Prohibited Work

```text
production source変更
test source変更
migration変更
fixture rewrite to hide defect
assertion weakening
skip/xfail追加
manual DB schema patch
manual family-row cleanup
G06 implementation
legacy source deletion
bug fix
```

Test Agentが作成してよいrepository fileは原則:

```text
30_test_report/G05/
```

のみ。

---

# 6. Gate Decision Rules

## PASS

all required:

```text
AC-001..005 SATISFIED

Causal Golden Path PASS
Exploratory Golden Path PASS
Predictive Golden Path PASS

one canonical claim authority proven
persistent canonical StageExecution all families
canonical G04 Result owner all families
canonical G04 Artifact owner all families

old family new-write runtime negative PASS
GenericExecutor boundary PASS
mutation/read projection PASS
CLI boundary PASS

G02/G03/G04 regression PASS

TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 recorded for G06

no G06/G07/G08 crossing
all reports template-compliant
same tested SHA
Test Agent source modification NONE
```

## FAIL

implementation/coverage/report contract defect.

Examples:

```text
any family submits to old lifecycle
any family claims from FamilyExecutionOrm
new stage writes old family stage
new output writes FamilyResult/FamilyArtifact
dual-write
family read cannot see new canonical execution
mutation writes old lifecycle
old write method still accepts independent Product write
old table count increases
old fallback exists
GenericExecutor gains authority
required G05 test missing
TD-001/002/003 not closed
passed Gate regression
mandatory report-format defect remains
```

## BLOCKED

environment/evidence integrity prevents judgment.

Environment issue ≠ implementation FAIL.

---

# 7. Fixed Implementation Target

Get full SHA from handoff report.

All Test Items same target.

If report-only descendants exist:

```bash
git diff --name-status <implementation-sha>..HEAD
```

must show no source/test/migration/config mutation.

Unexpected code change -> BLOCKED until target re-fixed.

---

# 8. Test Environment

Pure/static:

```bash
uv run pytest <exact-node>
```

Real PostgreSQL only:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [pytest-options]
```

Forbidden:

```text
manual docker run
manual network IP
manual DSN
manual psql reset
manual alembic
manual external DB pytest
```

Docker unavailable -> Human executes same repository-managed command; Test Agent audits evidence. If unavailable -> BLOCKED.

---

# 9. Execution Order

```text
1. commit / report integrity
2. report template compliance
3. scope / diff audit
4. route-to-authority inventory
5. migration head verification
6. Causal Golden Path
7. Exploratory Golden Path
8. Predictive Golden Path
9. cross-family authority
10. old-write runtime negative
11. mutation/read/CLI
12. G02/G03/G04 regression
13. TD closure / TD-004 / future scope
14. report-format audit
15. 999
```

PASS requires all MUST items.

---

# 10. Test Plans

## E4-G05_01_001 — Commit / Report / Scope Integrity

Report:

```text
30_test_report/G05/
E4-G05_01_001_commit_report_scope_integrity.md
```

Inspect:

```text
branch
baseline
implementation SHA
report SHA
baseline->implementation diff
implementation->HEAD diff
migration head
G06/G07 crossing
passed Gate artifact modifications
test infrastructure
.nfs artifact
```

Implementation Report template compliance is mandatory.

Record all actual git/find/grep commands.

---

## E4-G05_01_002 — Route-to-Canonical-Authority Audit

Report:

```text
E4-G05_01_002_route_to_authority_audit.md
```

Supports AC-001/002/003/005.

Inventory:

```text
Causal submit
Exploratory submit
Predictive submit
get/list
cancel/retry/rerun/revise
worker/claim/process
Result write/read
Artifact write/read
Product/auditable CLI
low-level CLI
```

PASS: every Product **write** surface reaches canonical authority.

family URL/response adapter may remain.

FAIL: any user-visible new Product write reaches old Family lifecycle.

---

## E4-G05_01_003 — Causal Canonical Golden Path

Report:

```text
E4-G05_01_003_causal_golden_path.md
```

Supports AC-001/004.

Real PostgreSQL:

```text
Causal Product submit
canonical Execution
persistent StageExecution
canonical claim
processing
canonical Result/Artifact
terminal state
fresh Session reload
```

Assert old family lifecycle/output row counts unchanged.

---

## E4-G05_01_004 — Exploratory Canonical Golden Path

Report:

```text
E4-G05_01_004_exploratory_golden_path.md
```

Supports AC-002/004/005.

Real PostgreSQL through user-visible Product submission path:

```text
returned ID = canonical execution_id
family = EXPLORATORY
persistent canonical stages
canonical claim
family scientific adapter
canonical Result/Artifact
terminal state
fresh Session reload
family-facing read projection sees data
```

Preserve actual dataset/view/spec/plan/snapshot semantics.

Mandatory before/after counts:

```text
FamilyExecution
FamilyStageExecution
FamilyResult
FamilyArtifact
```

must not increase due to new Golden Path.

---

## E4-G05_01_005 — Predictive Canonical Golden Path

Report:

```text
E4-G05_01_005_predictive_golden_path.md
```

Supports AC-003/004/005.

Real PostgreSQL:

```text
returned ID = canonical execution_id
family = PREDICTIVE
persistent canonical stages
canonical claim
predictive adapter
canonical Result/Artifact
terminal state
fresh Session reload
family-facing read projection
```

Preserve actual specification/plan/seed/snapshot semantics.

Mandatory old-family row-count negative.

---

## E4-G05_01_006 — Cross-Family Authority Contract

Report:

```text
E4-G05_01_006_cross_family_authority.md
```

Supports AC-004.

| Contract | Causal | Exploratory | Predictive |
|---|---|---|---|
| canonical execution repository | MUST | MUST | MUST |
| same claim authority | MUST | MUST | MUST |
| canonical persistent stages | MUST | MUST | MUST |
| canonical Result owner | MUST | MUST | MUST |
| canonical Artifact owner | MUST | MUST | MUST |
| family lifecycle owner | MUST NOT | MUST NOT | MUST NOT |

Real PostgreSQL must prove one canonical claimer contract handles each family.

---

## E4-G05_01_007 — Old-Write Shutdown Negative Audit

Report:

```text
E4-G05_01_007_old_write_shutdown.md
```

Supports AC-005, INV-016, TD-001/002/003 closure.

Static reachable-write audit:

```text
session.add(FamilyExecutionOrm)
session.add(FamilyStageExecutionOrm)
session.add(FamilyResultOrm)
session.add(FamilyArtifactOrm)
family SELECT FOR UPDATE claim
family direct lifecycle mutation
```

Source presence alone is not automatic FAIL; Product new-write reachability is criterion.

Runtime real PostgreSQL:

```text
old table counts before
Causal/Exploratory/Predictive new Product paths
old table counts after
```

must be unchanged.

If old mutating methods remain callable:

```text
delegate canonical
or
explicit reject
```

must be behavior-tested.

Inject canonical failure and verify no fallback to old authority.

---

## E4-G05_01_008 — Mutation / Read Projection / CLI Boundary

Report:

```text
E4-G05_01_008_mutation_read_cli_boundary.md
```

Supports AC-001..005, REQ-007..010, REQ-033/034.

Mutation:

```text
cancel
retry
rerun
revise
```

for actual exposed family surfaces must use canonical semantics.

Read:

new canonical family execution/output must be visible through supported family-facing read surface.

CLI inventory:

```text
LOW_LEVEL_SCIENTIFIC
    -> no Product persistent lifecycle

AUDITABLE_PRODUCT, if any
    -> canonical submit
```

No hidden old persistence.

---

## E4-G05_01_009 — Passed-Gate Regression

Report:

```text
E4-G05_01_009_passed_gate_regression.md
```

Run required affected scope from:

```text
tests/product/test_enh_e4_g02_canonical_execution.py
tests/product/test_enh_e4_g03_*.py
tests/product/test_enh_e4_g04_*.py
tests/product/test_postgres_contract.py
```

plus G05 tests.

Preserve:

```text
G02 identity/claim/lease/mutation
G03 StageExecution/attempt/GenericExecutor
G04 Result level/ownership/compensation/typed reuse
```

---

## E4-G05_01_010 — Transition / Lineage Deferral / Report Format

Report:

```text
E4-G05_01_010_transition_scope_report_format.md
```

Must verify:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
```

with evidence refs.

TD-004:

```text
remaining structural generic lineage writes inventoried
bounded
deferred to G06
```

or `NONE observed`.

Do not require G06 completion.

No:

```text
G06 lineage final cutover
G07 legacy retirement
G08 final bootstrap
historical migration
scientific redesign
```

001〜009 reports must be field-by-field template compliant before 999.

---

# 11. Acceptance Matrix

| Criterion | Mandatory Items |
|---|---|
| AC-001 | 002, 003, 006 |
| AC-002 | 002, 004, 006 |
| AC-003 | 002, 005, 006 |
| AC-004 | 003, 004, 005, 006, 009 |
| AC-005 | 002, 007, 008, 009 |
| TD-001 closure | 007, 010 |
| TD-002 closure | 003, 004, 005, 007, 010 |
| TD-003 closure | 003, 004, 005, 006, 007, 010 |
| TD-004 handoff | 010 |
| CLI | 008 |
| Report format | 001, 010, 999 precheck |

All mandatory items PASS required.

---

# 12. Command Shape

Actual nodes are taken from handoff report.

Example pure/static:

```bash
uv run pytest -q \
  tests/product/test_enh_e4_g05_submission_convergence.py \
  tests/product/test_enh_e4_g05_old_write_negative.py \
  tests/product/test_enh_e4_g05_cli_boundary.py
```

Example PostgreSQL:

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-audit \
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_family_golden_paths_postgres.py \
  tests/product/test_enh_e4_g05_old_write_negative.py \
  tests/product/test_enh_e4_g02_canonical_execution.py \
  tests/product/test_enh_e4_g03_acceptance_postgres.py \
  tests/product/test_enh_e4_g04_result_artifact_postgres.py \
  tests/product/test_postgres_contract.py
```

Reports must contain actual complete commands, not these examples unless actually run.

---

# 13. Evidence Integrity

Each runner invocation:

```text
tested full SHA
exact command
start/end timestamps
migration current/head
pytest exit code
outer runner exit
stdout/stderr path
metadata path
```

shared command must be fully repeated in each relevant report.

---

# 14. Mandatory Negative Checks

Submission:

```text
no Exploratory old execution write
no Predictive old execution write
no duplicate canonical+old write
```

Claim:

```text
no family-specific Product claim authority
```

Stage:

```text
no new FamilyStageExecution lifecycle
```

Output:

```text
no new FamilyResult
no new FamilyArtifact
no bypass of G04 owner
```

Lifecycle:

```text
no family direct mutation authority
no old fallback after canonical failure
```

GenericExecutor:

```text
no claim/commit/retry/output persistence
```

CLI:

```text
no hidden old Product lifecycle
no forced Product persistence for low-level utility
```

Scope:

```text
no G06 cutover
no broad legacy deletion
no historical migration
```

---

# 15. Gate Decision

Create after all MUST items:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G05/
E4-G05_01_999_gate_decision.md
```

Use `TEMPLATE_gate_decision_report.md` exactly.

---

# 16. 999 Pre-Decision Checklist

```text
[ ] 001 template-compliant
[ ] 002 template-compliant
[ ] 003 template-compliant
[ ] 004 template-compliant
[ ] 005 template-compliant
[ ] 006 template-compliant
[ ] 007 template-compliant
[ ] 008 template-compliant
[ ] 009 template-compliant
[ ] 010 template-compliant

[ ] same implementation SHA
[ ] exact commands
[ ] exit codes
[ ] evidence path or NONE
[ ] expected/actual
[ ] reproduction procedure
[ ] facts/interpretation separation
[ ] Test Agent source modification NONE

[ ] AC-001 SATISFIED
[ ] AC-002 SATISFIED
[ ] AC-003 SATISFIED
[ ] AC-004 SATISFIED
[ ] AC-005 SATISFIED

[ ] TD-001 CLOSED
[ ] TD-002 CLOSED
[ ] TD-003 CLOSED
[ ] TD-004 recorded

[ ] old table row-count negative PASS
[ ] no old fallback
[ ] passed-Gate regression PASS
```

---

# 17. Gate Decision Semantics

## PASS

All three families use:

```text
one canonical Product Execution identity
one claim/lease authority
persistent StageExecution
canonical Result owner
canonical Artifact owner
```

and:

```text
old Product lifecycle accepts no new write
GenericExecutor remains subordinate
TD-001/002/003 closed
```

G05 PASS does not mean G06 lineage consolidation is complete.

## FAIL

Convergence contract not met. Test Agent does not fix production.

## BLOCKED

Required evidence unavailable due environment/integrity.

---

# 18. Required Outputs

```text
30_test_report/G05/
E4-G05_01_001_commit_report_scope_integrity.md
E4-G05_01_002_route_to_authority_audit.md
E4-G05_01_003_causal_golden_path.md
E4-G05_01_004_exploratory_golden_path.md
E4-G05_01_005_predictive_golden_path.md
E4-G05_01_006_cross_family_authority.md
E4-G05_01_007_old_write_shutdown.md
E4-G05_01_008_mutation_read_cli_boundary.md
E4-G05_01_009_passed_gate_regression.md
E4-G05_01_010_transition_scope_report_format.md
E4-G05_01_999_gate_decision.md
```

---

# 19. Stop Conditions

PASS:

```text
STOP
do not start G06
do not modify source/test/migration
do not update Control Sheet
return evidence to operator
```

FAIL:

```text
create failure reports + 999
do not fix code
do not start next Trial
```

BLOCKED:

```text
record environment/evidence block
do not use manual PostgreSQL workaround
do not modify product code to bypass environment
```

---

# 20. Primary Audit Question

G05 Test Agent must answer:

> **If a new user-visible Product analysis is submitted, is there any Causal / Exploratory / Predictive path by which its identity, claim, stage, Result, or Artifact can still become authoritative outside the canonical Product aggregate?**

If answer is:

```text
YES
UNKNOWN
```

G05 cannot PASS.

Only:

```text
NO, proven by positive Golden Paths + old-write negative evidence
```

permits PASS.
