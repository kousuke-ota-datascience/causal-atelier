# Ariadne ENH-E4 E4-G04 テスト・監査指示書

* Project: Ariadne / causal-atelier
* Enhancement: ENH-E4 eliminate dual execution
* Branch: `refactor/ariadne_mvp_e4`
* Gate: `E4-G04`
* Gate name: Result / Artifact ownership boundary
* Trial: `01`
* Baseline ref: `14bc705`
* Expected pre-G04 Product migration head: `20260809_product_0008`
* Expected G04 Product migration head: `20260809_product_0009`（actual implementation reportを正とする）
* Prerequisite: E4-G03 Trial 02 `PASS`
* PostgreSQL verification infrastructure: repository-managed standardized runner
* Trial ID format: 2-digit zero-padded decimal (`01`–`99`)
* Test Item ID format: 3-digit zero-padded decimal (`001`–`998`; `000` reserved; `999` Gate Decision)

---

# 1. Source of Truth

本書は **E4-G04 Trial 01 Test / Audit Agentが従う唯一のGate-local verification contract** である。

作業指示者はTest Agent起動時に具体的Implementation Completion Reportを指定する。

Expected:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G04/
E4-G04_01_implementation_completion_report.md
```

Test Agentは以下を読む。

```text
1. 本07
2. 指定されたG04 Implementation Completion Report
3. fixed implementation commitのactual tree/diff
4. G04 06 — scope/implementation contract確認
5. G03 final Gate Decision
6. Current Architecture Control Sheet
7. repository report templates/specifications
```

G04 ACは本07で固定する。

Test Agentはbackground文書から新しいGate ACを追加しない。

---

# 2. Report Format Is Part of Test Completion

G03 Trial 01のreport format逸脱を再発させない。

## 2.1 Test report specification

Test Agentは作業開始時に必ず実物参照する。

```text
docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template_complete/
30_test_report/
README.md

docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template_complete/
30_test_report/
TEMPLATE_test_item_report.md

docs/wiki/develop_memo/_work/
agentic_enhancement_workflow_template_complete/
30_test_report/
TEMPLATE_gate_decision_report.md
```

## 2.2 Strict compliance

Every Test Item Report and final Gate Decision Report MUST conform to the repository-defined specification/template.

禁止:

```text
required section省略
required field省略
required sectionの独自merge
prose summaryだけでrequired fieldを代替
"same as above"
"previous command"
"pytestを実行"
"関連testを実行"
のような再実行不能command記述
独自のshort report format
```

必須fieldに値がない場合:

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を使い、field自体は削除しない。

## 2.3 Commands

`Commands Executed`には**実際に実行した全commandを、コピー&ペーストで再実行可能な完全形で記載する**。

一つのshared runner commandで複数Test Itemを検証した場合も、各Test Item reportでそのcomplete commandを再掲する。

禁止:

```text
"Test 002と同じ"
"same command"
"上記runner"
```

## 2.4 Completion rule

**Substantive test success does not waive report-format compliance.**

Test自体がPASSでもmandatory report fieldsが欠落しているTest Itemは:

```text
contract-compliant completed Test Item
```

ではない。

Gate PASS前にTest Agentは001〜009全reportをfield-by-field auditする。

format defectを自分で見つけた場合、source/test/migrationを変更せずreport自身を正規templateへ修正してからGate Decisionを作成する。

---

# 3. Test / Audit Agent Role

Test Agentの責務:

1. branch / implementation commitを固定する。
2. Implementation Completion Reportのtemplate complianceを監査する。
3. reportとactual source/test/migration diffを照合する。
4. Product migrationをreal PostgreSQLで検証する。
5. E4-G04-AC-001〜005を独立検証する。
6. Result level/cardinality persistenceを監査する。
7. Result/Artifact typed ownershipを監査する。
8. ArtifactStore physical boundaryを監査する。
9. compensation/reconciliation failure behaviorを実行検証する。
10. object_key semantic identity negativeを検証する。
11. Artifact-only family contractを検証する。
12. downstream typed reuseを検証する。
13. G02/G03 passed-Gate regressionを実行する。
14. TD-001/002/003とfuture-Gate scopeを監査する。
15. 各Test Item Reportをtemplate完全準拠で作成する。
16. final Gate Decision Reportをtemplate完全準拠で作成する。
17. `PASS / FAIL / BLOCKED` を判定する。
18. source/test/migrationを修正せず停止する。

---

# 4. Prohibited Work

Test Agentは禁止:

```text
production source変更
automated test source変更
migration変更
dependency変更
test infrastructure変更
bug fix
assertion緩和
skip/xfail追加
fixture変更によるfailure回避
DB schema手動修正
scientific semantics再設計
G05以降のimplementation
Coding Agent reportの事実改竄
07にないAcceptance Criteria追加
```

Test Agentがrepositoryへ作成してよいものは原則:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G04/
```

のreport/evidence documentationのみ。

generated raw evidenceはstandardized runnerのevidence directoryへ保存してよい。

既知unrelated artifact:

```text
deploy/.nfs000000000076202f00000088
```

は触らない。

---

# 5. Gate Decision Rules

Allowed:

```text
PASS
FAIL
BLOCKED
```

## 5.1 PASS

全て必要:

```text
all MUST Test Items complete
AC-001..005 all SATISFIED
Product migration PASS
real PostgreSQL ownership persistence PASS
compensation failure tests PASS
object_key negative PASS
artifact-only contract PASS
G02/G03 regression PASS
GenericExecutor non-authority preserved
TD-001 OPEN
TD-002 OPEN
TD-003 OPEN until G05
no G05+ scope crossing
tested implementation commit consistent
Test Agent source modification NONE
all Test Item Reports template-compliant
Gate Decision Report template-compliant
all exact commands reproducible
```

## 5.2 FAIL

implementation defectまたはrequired automated coverage defect。

Examples:

```text
Result level not persistent
StageResult without stage accepted
ExecutionResult with stage accepted
wrong execution/stage ownership accepted
Artifact result/stage ownership mismatch accepted
object_key accepted as semantic Result/Artifact identity
ArtifactStore failure leaves committed false metadata
DB failure leaves untracked physical object with no compensation evidence
compensation failure is silently ignored
artifact-only behavior is accidental/not explicit
family-specific canonical metadata owner remains in new G04 canonical path
GenericExecutor persists Result/Artifact
required G04 automated test missing
G02/G03 passed contract regression
```

Report format failure that remains unresolved at Gate Decision time also prevents PASS. It is an audit/process contract defect, not necessarily a production defect.

## 5.3 BLOCKED

environment/evidence integrity makes defect判定不能。

Examples:

```text
implementation SHA cannot be fixed
wrong branch
source/test/migration changed after handoff
standard runner unavailable and Human one-command evidence unavailable
Docker/resource failure prevents required PostgreSQL evidence
ArtifactStore test environment unavailable for reasons independent of product code
```

Environment問題をimplementation FAILにしない。

---

# 6. Fixed Implementation Target

Implementation Completion Reportから:

```text
Implementation commit: <full SHA>
```

を取得する。

全Test Itemで同じtargetを使用する。

report-only descendantsは許可されるが:

```bash
git diff --name-status <implementation-sha>..HEAD
```

でsource/test/migration/dependency/test-infrastructure差分がないことを確認する。

差分があれば原則BLOCKEDとしてtargetを再固定する。

---

# 7. Test Environment

## 7.1 Pure unit/static

real PostgreSQL不要:

```bash
uv run pytest <exact-node-or-file>
```

## 7.2 Real PostgreSQL

唯一のsupported entry point:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [pytest-options]
```

このrunnerが:

```text
database_test start/reuse
health readiness
clean ariadne_test reset
Product migration upgrade head
migration head/current verification
requested pytest
raw evidence
exit propagation
```

を所有する。

## 7.3 Forbidden manual flow

禁止:

```text
manual docker run
network IP調査
127.0.0.1 / 172.17.0.1 workaround
manual DSN
manual psql reset
manual alembic
manual pytest against external DB
```

## 7.4 Docker unavailable

Test AgentがDockerへアクセス不能:

1. product FAILとしない。
2. manual workaroundへ行かない。
3. Human Operatorへ同じrepository-managed one commandだけを依頼。
4. evidenceのtested SHA / command / exit / logを監査。
5. evidence取得不能ならBLOCKED。

---

# 8. Execution Order

fail-fast:

```text
1. branch / commit / handoff report integrity
2. Implementation Completion Report template compliance
3. Gate scope / change-boundary audit
4. Product migration/schema static audit
5. Result level/cardinality unit/domain tests
6. real PostgreSQL Result/Artifact ownership
7. ArtifactStore compensation/reconciliation
8. object_key / typed reuse negative
9. Artifact-only family contract
10. G02/G03 regression
11. transition debt / future-Gate boundary
12. Test Item report format-compliance audit
13. Gate Decision
```

PASS時は全MUST item完走。

---

# 9. Test Plans

## E4-G04_01_001 — Commit / Report / Change Boundary Audit

Report:

```text
30_test_report/G04/
E4-G04_01_001_commit_report_change_boundary.md
```

### Purpose

fixed implementation target、handoff report、G04 scope、report-format complianceを監査する。

### Supports

```text
Gate integrity
AC-001..005 traceability
```

### MUST inspect

```text
branch
baseline ref/full SHA
starting commit
implementation full SHA
report commit
baseline -> implementation diff
implementation -> HEAD diff
Product migration
changed tests
G02/G03 files changed?
G05+ scope?
root legacy migration?
test infrastructure?
unrelated .nfs artifact?
```

### Implementation Report Format MUST

Implementation Completion Reportがrepository templateの全required field/sectionを保持していること。

Missing required field:

```text
FAIL as handoff/report contract defect
```

unless it prevents target identification, in which case BLOCKED.

### Commands

actual complete git commandsをreportへ記載する。

Source inspectionのみでも`NOT_RUN`ではなく、実行した`git`/`grep`/inspection commandを完全形で記録する。

---

## E4-G04_01_002 — Product Migration / Result Level / Cardinality Audit

Report:

```text
30_test_report/G04/
E4-G04_01_002_result_schema_cardinality.md
```

### Supports

```text
AC-001
AC-002
Product migration
```

### MUST inspect

```text
G04 Product migration parent/head
result_level persistence
allowed level values
execution FK
stage FK/association
ExecutionResult stage prohibition
StageResult stage requirement
same-execution ownership enforcement
result_type != result_level
cardinality/output contract
scientific payload/status preservation
```

### Real PostgreSQL

Clean Product migration to G04 head must PASS.

### Mandatory negatives

```text
ExecutionResult + stage -> rejected
StageResult + no stage -> rejected
StageResult + foreign Execution's stage -> rejected
invalid level -> rejected
```

---

## E4-G04_01_003 — Canonical Result / Artifact Ownership Persistence

Report:

```text
30_test_report/G04/
E4-G04_01_003_result_artifact_ownership_persistence.md
```

### Supports

```text
AC-001
AC-002
```

### MUST use real PostgreSQL

Verify canonical service/repository path for:

```text
ExecutionResult
StageResult
Artifact linked to Execution
Artifact linked to Stage
Artifact linked to Result
Artifact with optional Result when contract allows
```

After new Session/UoW reload:

```text
same result_id
same artifact_id
same canonical execution_id
correct stage/result association
```

### Cross-family representation

Must prove G04 canonical ownership contract can represent:

```text
CAUSAL
EXPLORATORY
PREDICTIVE
```

without family-specific canonical metadata repositories.

This does not require G05 route cutover.

### Ownership negatives

wrong execution/stage/result links rejected.

---

## E4-G04_01_004 — Artifact Semantic ID / Typed Downstream Reuse

Report:

```text
30_test_report/G04/
E4-G04_01_004_typed_reuse_object_key_negative.md
```

### Supports

```text
AC-004
AC-002
```

### MUST verify

```text
Result reuse uses result_id + typed role/context
Artifact reuse uses artifact_id
object_key is looked up only after Artifact metadata
content_hash is integrity evidence, not identity
DatasetVersion/GraphVersion typed IDs remain typed
```

### Mandatory negatives

```text
object_key passed as Result ID -> rejected/not resolved
object_key-only Artifact ownership -> rejected
content_hash-only semantic identity -> rejected
untyped Family Result string bridge -> not accepted by new canonical contract
```

Do not require G05 all-route cutover.

---

## E4-G04_01_005 — ArtifactStore Compensation / Reconciliation

Report:

```text
30_test_report/G04/
E4-G04_01_005_artifact_store_compensation.md
```

### Supports

```text
AC-003
INV-010
```

### MUST behavior-test

At least:

#### A. physical store fails before metadata commit

Expected:

```text
no committed false Artifact metadata
no falsely complete dependent metadata
UoW rollback
already-stored siblings compensated
```

#### B. DB commit fails after store success

Expected:

```text
physical object compensating-deleted
metadata not committed
failure surfaced
```

#### C. partial multi-artifact failure

Expected:

```text
known written subset
deterministic cleanup
no false metadata for missing object
```

#### D. cleanup itself fails

Expected:

```text
not silent success
orphan locator/reconciliation context observable
```

### PostgreSQL

DB durability/rollback assertions use real PostgreSQL.

Physical store failure injection may use deterministic test double/local store.

---

## E4-G04_01_006 — Artifact-Only Family Contract

Report:

```text
30_test_report/G04/
E4-G04_01_006_artifact_only_family_contract.md
```

### Supports

```text
AC-005
AC-001
```

### MUST verify

Causal / Exploratory / Predictive workflow/output contracts have explicit artifact-only decision.

For each relevant output contract determine:

```text
Result required?
Result optional?
Result forbidden?
Artifact-only allowed?
Allowed Result level?
```

### Mandatory behavioral coverage

If current workflow has an actual allowed artifact-only output:

```text
allowed case -> persists Artifact without fake Result
```

Also at least one disallowed case:

```text
artifact-only attempt -> rejected
```

If no family has allowed artifact-only output after actual inventory:

```text
all explicit false
```

is acceptable; do not invent scientific behavior.

---

## E4-G04_01_007 — Canonical Ownership Service / GenericExecutor Boundary Audit

Report:

```text
30_test_report/G04/
E4-G04_01_007_output_owner_generic_executor_boundary.md
```

### Supports

```text
AC-002
AC-003
Gate architecture
```

### Static + behavior MUST

Canonical output persistence authority is one common service/repository boundary.

GenericExecutor MUST NOT:

```text
write Result
write Artifact metadata
call ArtifactStore as canonical owner
commit UoW
decide ownership/cardinality
```

family-specific services MUST NOT become separate new canonical metadata owners.

Old transitional paths may remain only under TD-003.

---

## E4-G04_01_008 — G02 / G03 / PostgreSQL Regression

Report:

```text
30_test_report/G04/
E4-G04_01_008_g02_g03_regression.md
```

### Purpose

G04 output ownership changeがpassed Execution/Stage contractsを壊していないこと。

### MUST run

At minimum affected required nodes from:

```text
tests/product/test_enh_e4_g02_canonical_execution.py
tests/product/test_enh_e4_g03_*.py
tests/product/test_postgres_contract.py
```

### Preserve

```text
Execution family/lifecycle/claim/lease
retry/rerun/revise/cancel
persistent StageExecution
attempt history
stage owner checks
GenericExecutor non-authority
zero-stage prevention
```

G04 testのためG03 `output_binding`をResult authorityとして読み替えない。

---

## E4-G04_01_009 — Transition Debt / Scope / Report-Format Audit

Report:

```text
30_test_report/G04/
E4-G04_01_009_transition_scope_report_format_audit.md
```

### Purpose

Gate scope、transition debt、001〜008 report format complianceをfinal decision前に監査する。

### MUST verify

```text
E4-TD-001 OPEN until G05
E4-TD-002 OPEN until G05
E4-TD-003 OPEN until G05
```

G04 implementation does not perform:

```text
G05 full convergence
G06 lineage cutover
G07 legacy retirement
G08 final bootstrap
```

### Dual-write audit

TD-003がsame-request indefinite dual-writeとして実装されていない。

### Report format audit

001〜008の各Test Item Reportについてrepository templateのrequired fieldsをfield-by-field確認する。

最低限:

```text
Project
Enhancement
Gate
Trial
Test item
Status
Tested implementation commit
Handoff report path
Branch
Migration head / N/A
Working directory
Started at
Finished at
Duration
Purpose
Acceptance Criteria
Runtime environment
External Services
Environment Variables
Commands Executed — complete exact commands
Exact Result
exit code
stdout/stderr
failure traceback / N/A
artifact paths / NONE
Findings
Required Correction / N/A
Reproduction Procedure
Expected Result
Decision Rationale
Source Modification by Test Agent
```

省略/独自mergeが残っていればGate PASSへ進まない。

Test Agent自身でreportをtemplate準拠へ直すことは許可される。production/test/migration変更は禁止。

---

# 10. Acceptance Criteria Matrix

| AC / Contract | Mandatory Test Items |
|---|---|
| E4-G04-AC-001 | 002, 003, 006 |
| E4-G04-AC-002 | 002, 003, 007 |
| E4-G04-AC-003 | 005, 007 |
| E4-G04-AC-004 | 004 |
| E4-G04-AC-005 | 006 |
| Product migration | 002 |
| G02/G03 regression | 008 |
| Transition debt / future Gate | 001, 009 |
| Report format compliance | 001, 009, 999 pre-decision check |

全mandatory itemがPASSしなければG04 PASS不可。

---

# 11. Recommended Command Set

actual implementation test files/nodesをImplementation Completion Reportから取得する。

Example pure tests:

```bash
uv run pytest -q \
  tests/product/test_enh_e4_g04_result_artifact_contract.py \
  tests/product/test_enh_e4_g04_typed_reuse.py
```

Example PostgreSQL:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g04_result_artifact_postgres.py \
  tests/product/test_enh_e4_g04_artifact_compensation.py \
  tests/product/test_postgres_contract.py \
  tests/product/test_enh_e4_g02_canonical_execution.py \
  tests/product/test_enh_e4_g03_acceptance_postgres.py
```

**これらは例。reportには実際に実行したcomplete commandを記録する。**

---

# 12. Evidence Integrity

Standard runner evidenceについて記録:

```text
tested implementation full SHA
exact command
start/end timestamps
migration current/head
pytest exit code
outer script exit code
stdout/stderr path
metadata evidence path
```

one shared runner commandで複数Test Itemを検証した場合、各reportでcomplete commandを再掲し、それぞれのassertion/nodeが何を証明したか分ける。

Raw generated evidenceを手編集しない。

---

# 13. Mandatory Negative Checks

## Result

```text
no implicit level
no StageResult without stage
no ExecutionResult with stage
no cross-execution stage link
no level/type conflation
```

## Artifact

```text
no object_key semantic identity
no hash semantic identity
no cross-execution stage/result link
no accidental Artifact-only output
no physical-store authority in metadata repository
```

## Compensation

```text
no committed false metadata after store failure
no silent physical orphan after DB failure
no silent success when compensation fails
```

## Architecture

```text
no GenericExecutor output persistence
no new family-specific canonical metadata owner
no indefinite same-request dual-write
```

## Scope

```text
no G05 convergence
no G06 lineage final cutover
no G07 legacy retirement
no G08 bootstrap
no root migration changes
```

## Reporting

```text
no omitted mandatory fields
no abbreviated report schema
no "same as previous" commands
no missing exit code
no missing reproduction procedure
```

---

# 14. Gate Decision Report

全MUST Test Item完了後:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G04/
E4-G04_01_999_gate_decision.md
```

を作成する。

**必ず**:

```text
agentic_enhancement_workflow_template_complete/
30_test_report/
README.md

TEMPLATE_gate_decision_report.md
```

へfield-by-field準拠する。

Template-required sectionsを削除/統合しない。

---

# 15. Gate Decision Format-Compliance Precheck

999作成前に以下を実施する。

```text
[ ] 001 exists and template-compliant
[ ] 002 exists and template-compliant
[ ] 003 exists and template-compliant
[ ] 004 exists and template-compliant
[ ] 005 exists and template-compliant
[ ] 006 exists and template-compliant
[ ] 007 exists and template-compliant
[ ] 008 exists and template-compliant
[ ] 009 exists and template-compliant

[ ] tested implementation SHA identical across reports
[ ] complete exact commands present
[ ] exit codes present
[ ] evidence paths present or NONE
[ ] expected results present
[ ] decision rationale present
[ ] Test Agent source modification NONE
```

その後999をtemplateどおり作成する。

---

# 16. Gate Decision Semantics

## PASS

Meaning:

```text
explicit Result semantic levels established
canonical typed Result/Artifact ownership established
one canonical metadata ownership boundary established
ArtifactStore remains physical-only
compensation/reconciliation is executable and verified
object_key is not semantic identity
Artifact-only family semantics explicit
G02/G03 preserved
TD-003 bounded until G05
all reports auditable/reproducible
```

PASS後も:

```text
TD-001 OPEN
TD-002 OPEN
TD-003 OPEN
```

でよい。

G04 PASSはG05 convergence完了ではない。

## FAIL

Implementationまたはrequired coverage/report contractがG04を満たさない。

Test Agentは修正実装しない。

## BLOCKED

required evidence取得不能でcorrectness判定不能。

environmentとproduct defectを分ける。

---

# 17. Required Outputs

```text
30_test_report/G04/
E4-G04_01_001_commit_report_change_boundary.md
E4-G04_01_002_result_schema_cardinality.md
E4-G04_01_003_result_artifact_ownership_persistence.md
E4-G04_01_004_typed_reuse_object_key_negative.md
E4-G04_01_005_artifact_store_compensation.md
E4-G04_01_006_artifact_only_family_contract.md
E4-G04_01_007_output_owner_generic_executor_boundary.md
E4-G04_01_008_g02_g03_regression.md
E4-G04_01_009_transition_scope_report_format_audit.md
E4-G04_01_999_gate_decision.md
```

---

# 18. Stop Conditions

Gate Decision作成後停止。

## PASS

```text
G05へ自分で進まない
source/test/migration変更しない
Current Architecture Control Sheetを更新しない
作業指示者へPASS evidenceを返す
```

Control Sheet更新は作業指示者がG04 final PASSを確認した後の別作業。

## FAIL

```text
failure report + 999作成
source修正しない
next Coding Trialを自分で始めない
```

## BLOCKED

```text
environment workaroundとしてproduct codeを変更しない
manual PostgreSQL flowへ戻らない
block evidence + 999作成
```

---

# 19. Primary Risk Focus

G04で監査するべき本質はtable名ではなくauthorityである。

PASS可能:

```text
Execution / Stage
      │
      v
explicit Result semantic ownership
      │
      v
one canonical Result/Artifact application authority
      ├─ Product metadata transaction
      └─ ArtifactStore physical bytes
             │
             └─ explicit compensation/reconciliation
```

PASS不可:

```text
product_resultとproduct_family_resultの名前だけ残して
service ownershipも意味も二重

or

一つのtableに統合したが
ExecutionResult/StageResult semantic differenceを消した

or

Artifact IDはあるがobject_keyをdownstream identityとして使い続ける

or

ArtifactStore failureを正常系metadataが隠す

or

test自体はpassしたがreportからexact commandを再現できない
```

G04では**ownership semantics / storage boundary / recoverability / auditability**を同時に成立させる。
