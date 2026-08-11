# Ariadne ENH-E4 E4-G03 テスト・監査指示書

* Project: Ariadne / causal-atelier
* Enhancement: ENH-E4 eliminate dual execution
* Branch: `refactor/ariadne_mvp_e4`
* Active Gate: `E4-G03`
* Gate name: Persistent StageExecution and runner boundary
* Trial: `01`
* Baseline commit: `cb28a18c07cad00cf12f01e9124651aa45aab16f`
* Expected pre-implementation Product migration head: `20260809_product_0007`
* Preflight prerequisite: Test PostgreSQL Infrastructure `PASS_READY_FOR_G03`
* Trial ID format: 2-digit zero-padded decimal (`01`–`99`)
* Test Item ID format: 3-digit zero-padded decimal (`001`–`998`; `000` reserved; `999` Gate Decision)

---

# 1. Source of Truth

本書は **E4-G03 Trial 01のTest / Audit Agentが従う唯一のGate-local verification contract** である。

作業指示者はTest Agent起動時に、対象となる具体的Implementation Completion Reportを指定する。

Expected:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G03/
E4-G03_01_implementation_completion_report.md
```

Test Agentは以下を入力として読む。

```text
1. 本07
2. 指定されたG03 Implementation Completion Report
3. implementation commitのactual Git tree/diff
4. E4-G03の06（scope確認用。07のACを拡張してはならない）
5. G02 final Gate Decision（passed-Gate regression boundary）
6. G03 Preflight verification result（PostgreSQL test infrastructure contract）
```

G03 ACの判定基準は本07で固定する。

Test Agentは06やbackground文書を読んでACを勝手に増やさない。

---

# 2. Test / Audit Agent Role

Test Agentの責務:

1. branchを確認する。
2. Implementation Completion Reportを読む。
3. implementation commit full SHAを固定する。
4. reportとactual Git diffを照合する。
5. source/test/migrationのchange boundaryを監査する。
6. E4-G03-AC-001〜005を独立検証する。
7. Product migration / schemaをreal PostgreSQLで検証する。
8. cross-family StageExecution persistenceをreal PostgreSQLで検証する。
9. repository query / attempt historyを検証する。
10. GenericExecutor architecture ownershipをstatic + behaviorで監査する。
11. failure/cancel/retry/lease consistencyを検証する。
12. G02 relevant regressionを実行する。
13. exact command / exit code / raw evidenceを保存する。
14. Gate-local Test Item reportを作成する。
15. 最後に`E4-G03_01_999_gate_decision.md`を作成する。
16. `PASS / FAIL / BLOCKED` のいずれかを判定する。
17. 判定後にsourceを修正せず停止する。

---

# 3. Prohibited Work

Test Agentは禁止:

* production source変更
* automated test source変更
* migration変更
* dependency変更
* compose/test infrastructure変更
* formatterによるsource rewrite
* bug fix
* assertion緩和
* skip / xfail追加
* failing test削除
* fixture変更によるfailure回避
* DB schema手動修正
* canonical architecture再設計
* Coding Agent report改竄
* 07にないAcceptance Criteria追加
* G04以降をtest対象へ拡張
* FAIL/BLOCKED後の修正実装
* root legacy migration実行をG03 verificationへ追加
* G02 external/manual PostgreSQL runbookの再導入

Test AgentがRepository内に作成してよいfileは原則:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G03/
```

配下のtest/audit evidenceのみ。

raw generated evidenceはrepository-managed test runnerの既定どおり:

```text
test-results/postgres/
```

または `ARIADNE_TEST_EVIDENCE_DIR` 指定先へ生成してよい。

既知のunrelated working-tree artifact:

```text
deploy/.nfs000000000076202f00000088
```

は変更・restore・stage・delete・recreateしない。

---

# 4. Gate Decision Rules

許容値:

```text
PASS
FAIL
BLOCKED
```

`PARTIAL_PASS`、`PASS_WITH_CONDITIONS`等は使用しない。

## 4.1 PASS

以下を全て満たす。

* 全MUST Test Item完了
* E4-G03-AC-001〜005全てPASS
* mandatory negative checks PASS
* real PostgreSQL stage persistence evidenceあり
* Product migration verification PASS
* cross-family canonical stage materialization PASS
* GenericExecutor ownership audit PASS
* failure/cancel/retry/lease behavior PASS
* G02 mandatory relevant regression PASS
* tested implementation commitが全Test Itemで同一
* Test Agentによるsource/test/migration変更なし
* E4-TD-001がOPENのまま
* E4-TD-002がOPEN until G05として記録済み
* G04+先行実装なし

## 4.2 FAIL

implementation defectまたはrequired automated-test coverage defectによりG03 ACを満たさない。

例:

* Causal canonical ExecutionだけStageExecutionがない
* StageExecutionがpersistentでない
* stage attempt historyがqueryできない
* retryでattempt historyが消える
* retryで同一stageにnew StageExecution IDを作る
* GenericExecutorがDB/UoW commitする
* GenericExecutorがcanonical retry policyを実行する
* GenericExecutorがResult/Artifact metadataをpersistする
* stale lease ownerがstageを更新できる
* parent ExecutionがSUCCEEDEDなのにrequired stageがFAILED/RUNNING
* parent CANCELLED後にnew stage attemptが開始できる
* Causal zero-stage canonical writeがcommitできる
* mandatory G03 automated test codeが欠落
* G02 claim/lifecycle regressionがimplementation changeで壊れた

## 4.3 BLOCKED

environment / evidence integrityによりimplementation defectか判定不能。

例:

* implementation commitを固定不能
* wrong branch
* reportとimplementation commitが一致しない
* implementation handoff後にsource/test/migrationが変更された
* standardized PostgreSQL runnerを実行できず、Human one-command fallback evidenceも得られない
* Docker daemon / host resource不足によりrequired real PostgreSQL evidenceを取得不能
* required report/evidenceが破損し対象commitを特定不能

Environment問題をFAILにしない。

---

# 5. Trial Rules

Active Trial:

```text
E4-G03 Trial 01
```

Rules:

1. current Trialだけを判定する。
2. 過去Trial結果を寄せ集めてPASSしない。
3. PASS Trialでは全MUST Test Itemを同一implementation commitに対して完走する。
4. deterministic product failureを無意味に再実行しない。
5. environment transient failureのみ最大1回再試行可。
6. environment retry時は初回failureとretry reasonをevidenceへ残す。
7. standardized PostgreSQL runner内部のclean resetはTest再試行とは数えない。
8. Test AgentはTrial番号を勝手に進めない。
9. FAIL後の次Coding Trialは作業指示者が開始する。
10. G02 external evidenceをG03 PASS evidenceとして流用しない。

---

# 6. Fixed Implementation Target

## 6.1 Implementation commit

Implementation Completion Reportから:

```text
Implementation commit: <full SHA>
```

を取得し、全Test Itemの固定targetとする。

必ずfull SHAを使用する。

## 6.2 Report-only commit

許容:

```text
implementation commit
    ↓
only documentation/report commit(s)
    ↓
current HEAD
```

ただしimplementation commit以降に以下が変更されていないこと。

* production source
* automated tests
* Product migrations
* dependency/config affecting G03
* test infrastructure

確認例:

```bash
git diff --name-status <implementation-full-sha>..HEAD
```

source/test/migration/config差分が存在する場合は、原則:

```text
BLOCKED
```

として対象を再固定する。

## 6.3 Evidence commit

PostgreSQL raw evidenceやaudit reportを後発commitへ追加する場合、implementation commitとは分離してよい。

Gate Decisionに:

```text
implementation ref
evidence/report ref
```

を明記する。

---

# 7. Test Environment Policy

## 7.1 Python

```text
Python 3.12
```

## 7.2 Non-PostgreSQL tests

Pure unit/static/component testsでreal PostgreSQLを必要としないものは:

```bash
uv run pytest <node>
```

を使用してよい。

## 7.3 Real PostgreSQL — sole supported entry point

real PostgreSQLを必要とする全G03 verificationは、**唯一のrepository-managed entry point**:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [pytest-options]
```

を使用する。

例:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g03_persistent_stage_execution.py
```

複数node:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g03_persistent_stage_execution.py \
  tests/product/test_postgres_contract.py \
  tests/product/test_enh_e4_g02_canonical_execution.py
```

## 7.4 Standard runner contract

このcommandが以下を所有する。

```text
test-only Python image
database_test start/reuse
Compose service-name networking
health readiness
clean ariadne_test reset
Product migration upgrade head
migration head/current verification
requested pytest
timestamped raw stdout/stderr
metadata evidence
pytest exit status propagation
```

Test Agentが同じ処理を手作業で再構築してはならない。

## 7.5 Explicitly forbidden manual PostgreSQL flow

禁止:

```text
docker runで独自test runner構築
docker network IP調査
127.0.0.1へのroute workaround
172.17.0.1へのroute workaround
manual ARIADNE_PRODUCT_TEST_DATABASE_URL export
manual psql drop/create
manual alembic upgrade
manual pytest against hand-wired DSN
raw evidence手組み
```

G02で必要だったexternal/manual verificationはG03標準ではない。

## 7.6 Development DB safety

Test stackは:

```text
database_test
ariadne_test
ariadne-test-network
test-only volume
```

を使用する。

Development:

```text
database
metadata-data
```

をreset/migrateしない。

## 7.7 Agent cannot access Docker

Test Agent runtimeがDockerへ直接アクセスできない場合:

1. implementation FAILとは判定しない。
2. network probing/manual runbookへ移行しない。
3. Human Operatorへ **同じone commandだけ** を実行依頼する。
4. Human evidenceは同一implementation commitを対象とする。
5. `test-results/postgres/` または指定evidence directoryのraw metadata/outputを監査する。
6. implementation commitとevidence commit/refを分離して記録する。
7. fallback evidenceが取得できればTrialは増やさない。
8. fallback evidenceも取得不能ならGate Decisionは `BLOCKED`。

Human Operator用commandもrepository-managed entry pointのみとする。

## 7.8 Test infrastructure modification

G03 Test AgentはPreflight infrastructureを修正してtestを通してはならない。

真のinfrastructure defectを発見した場合は:

```text
BLOCKED
```

としてevidenceを残し、product implementation defectと混同しない。

---

# 8. Test Execution Order

fail-fast順序:

```text
1. Commit / report / branch integrity
2. Change-boundary and Gate-scope audit
3. Product migration / schema static audit
4. GenericExecutor static ownership audit
5. Non-PostgreSQL domain/workflow tests
6. Standardized real PostgreSQL migration + StageExecution persistence
7. Cross-family canonical stage materialization
8. Repository query / attempt history
9. Failure / retry / cancel / lease consistency
10. G02 relevant regression
11. Transition-debt / out-of-scope audit
12. Gate Decision
```

重大なstatic architecture violationがある場合、後続runtime testを全て実行する必要はない。

ただしGate Decisionへ:

* 未実行Item
* fail-fast reason
* implementation defectかenvironment blockか

を明示する。

PASS判定の場合は全MUST Itemを完走する。

---

# 9. Gate Test Plans

## E4-G03_01_001 — Commit and change-boundary audit

Report:

```text
30_test_report/G03/
E4-G03_01_001_commit_change_boundary.md
```

### Purpose

Test対象commitを固定し、G03 scope以外の便乗実装・unrelated artifact混入がないことを確認する。

### Supports

```text
AC-001
AC-003
AC-004
Gate scope
```

### MUST inspect

* branch
* baseline commit
* starting commit from implementation report
* implementation full SHA
* baseline → implementation diff
* implementation → current HEAD diff
* changed files
* Product migration changes
* test infrastructure changes
* G04+先行実装
* root legacy migration changes
* `deploy/.nfs...`混入
* E4-TD-001 state
* E4-TD-002 record

### PASS

* target commit fixed
* diff is explainable within G03
* no forbidden scope
* no unrelated artifact
* no source/test/migration change after fixed implementation commit except separately fixed new target

### FAIL

G03 implementation commit itself contains out-of-scope architecture work or required G03 implementation is absent.

### BLOCKED

target commit cannot be fixed/integrity cannot be established.

---

## E4-G03_01_002 — Product migration and StageExecution schema audit

Report:

```text
30_test_report/G03/
E4-G03_01_002_stage_schema_migration.md
```

### Purpose

persistent StageExecution / attempt historyがcanonical Product schemaとして成立していることを確認する。

### Supports

```text
AC-001
AC-002
AC-004
```

### MUST inspect

Product migration:

* parent revision = actual pre-G03 Product head
* expected baseline parent `20260809_product_0007`
* G03 new Product head
* root legacy migration unchanged
* canonical Execution FK
* StageExecution primary identity
* `(execution_id, stage_key)` uniqueness
* attempt identity/number persistence
* `(stage_execution_id, attempt_number)` uniqueness
* state
* stage key/type/order/dependency metadata
* input/output binding storage
* error/timestamps
* cancellation representation

### Real PostgreSQL MUST

Use standardized runner to prove clean Product migration to head succeeds.

The migration must be applied to reset `ariadne_test`, not a pre-mutated DB.

### PASS

Schema is sufficient to reconstruct the G03 persistent contract and Product-only migration passes.

---

## E4-G03_01_003 — Cross-family canonical StageExecution persistence

Report:

```text
30_test_report/G03/
E4-G03_01_003_cross_family_stage_persistence.md
```

### Purpose

Causal / Exploratory / Predictiveの全canonical Execution familyがpersistent StageExecution childを持つことを証明する。

### Supports

```text
AC-001
AC-004
```

### MUST use real PostgreSQL

Required family matrix:

| Family | Canonical Execution persisted | StageExecution persisted | execution_id ownership correct |
|---|---:|---:|---:|
| CAUSAL | MUST | MUST | MUST |
| EXPLORATORY | MUST | MUST | MUST |
| PREDICTIVE | MUST | MUST | MUST |

### MUST verify

* each committed canonical Execution has `>=1` stage child
* stage row references same canonical execution ID
* deterministic stage keys/order
* no family-specific second stage repository authority is used
* reload in a new UoW/session still returns stages

### Negative

Inject/construct empty or unavailable Causal plan and verify parent canonical Execution is not durably committed without stage.

### FAIL

Any canonical family value can create a persistent Execution without stage children.

---

## E4-G03_01_004 — Stage repository query and attempt-history audit

Report:

```text
30_test_report/G03/
E4-G03_01_004_stage_query_attempt_history.md
```

### Purpose

runner internalsを使わずstage state/attempt/input/outputをqueryできることを確認する。

### Supports

```text
AC-002
```

### MUST verify

Repository/application query can retrieve by:

```text
stage_execution_id
execution_id
```

and reconstruct:

* stage key/type
* ordinal/dependencies
* state
* input binding metadata
* output binding metadata
* last error
* started/finished timestamps
* ordered attempt history

### Retry history MUST verify

For one StageExecution:

```text
attempt 1 fails
attempt 2 starts/succeeds
```

then after new UoW/session reload:

```text
same stage_execution_id
attempt numbers [1,2]
attempt 1 failure preserved
attempt 2 timestamps/outcome preserved
```

No runner object may be required merely to read the data.

---

## E4-G03_01_005 — GenericExecutor responsibility boundary audit

Report:

```text
30_test_report/G03/
E4-G03_01_005_generic_executor_boundary.md
```

### Purpose

GenericExecutorがworkflow infrastructureに限定され、canonical lifecycle ownerになっていないことを証明する。

### Supports

```text
AC-003
```

### Static MUST

Inspect GenericExecutor implementation and imports.

Forbidden ownership/import/call classes include equivalents of:

```text
UnitOfWork
SQLAlchemy Session
ORM persistence
Execution repository claim
StageExecution repository commit
Result repository persistence
Artifact metadata repository persistence
lineage persistence
canonical retry policy
```

### API MUST

Verify canonical GenericExecutor contract does not expose ambiguous persistence/retry authority such as:

```text
commit=<DB persistence callback>
retryable=<canonical retry policy>
```

### Behavior MUST

A runner failure must return/raise a workflow outcome without GenericExecutor independently executing canonical retry policy or committing DB state.

GenericExecutor may still:

```text
validate plan
order stages
resolve bindings
invoke runner
produce detached outcome
observe cancellation signal to stop sequencing
```

### Mandatory negative acceptance

No:

```text
DB commit
claim
Result/Artifact metadata persistence
canonical retry policy
```

is called from GenericExecutor.

---

## E4-G03_01_006 — Failure / retry / cancel / lease consistency

Report:

```text
30_test_report/G03/
E4-G03_01_006_stage_execution_state_consistency.md
```

### Purpose

StageExecution stateとparent Execution lifecycle/claim authorityが矛盾しないことを証明する。

### Supports

```text
AC-005
AC-002
```

### MUST use real PostgreSQL where persistence/owner behavior matters

Required scenarios:

#### A. Failure without retry

```text
Execution RUNNING
Stage RUNNING
runner failure
Stage FAILED
attempt finalized
Execution FAILED
```

No `Execution SUCCEEDED` contradiction.

#### B. Retry

Starting from failed canonical Execution/stage:

```text
Execution retry -> same execution_id
reclaim -> RUNNING
same stage_execution_id
new attempt_number
old attempt preserved
```

GenericExecutor must not be component deciding this retry.

#### C. Cancellation

Verify:

* parent Execution becomes CANCELLED
* previously SUCCEEDED stage remains SUCCEEDED
* active/nonterminal stage becomes explicit cancellation state
* no new stage attempt starts after cancellation
* no stale RUNNING stage remains indefinitely as the persisted terminal picture
* cancellation does not create new Execution ID

#### D. Wrong/stale owner

Attempt stage mutation with wrong/stale owner token.

Expected:

```text
rejected
no durable stage mutation
```

#### E. Invalid parent/stage success combination

Attempt to complete Execution while required stage is FAILED/PENDING/READY/RUNNING.

Expected:

```text
rejected or transaction cannot produce durable inconsistent state
```

### FAIL

Any durable state violates the parent-stage consistency contract.

---

## E4-G03_01_007 — Atomic stage materialization negative lifecycle

Report:

```text
30_test_report/G03/
E4-G03_01_007_stage_materialization_atomicity.md
```

### Purpose

`Causal stage absent / Family only persistent`というdual architectureをcanonical new-writeで再生成できないことを独立検証する。

### Supports

```text
AC-004
AC-001
```

### MUST verify

At least:

1. Causal canonical planner returns empty/invalid plan → submit fails.
2. Stage persistence injection failure → Execution + stages rollback.
3. successful retry of submission after failure does not leave orphan/duplicate stage rows.
4. direct canonical service path never commits zero-stage canonical Execution.
5. Family path evidence alone is insufficient; Causal case is mandatory.

### Scope note

Arbitrary hand-written SQL that bypasses Product repositories is not the Product new-write contract.

The required negative boundary is canonical Product application/repository write behavior.

---

## E4-G03_01_008 — G02 regression and PostgreSQL contract

Report:

```text
30_test_report/G03/
E4-G03_01_008_g02_regression_postgres_contract.md
```

### Purpose

G03のstage workがG02のExecution identity/claim/lease authorityを壊していないことを確認する。

### MUST run

At minimum:

```text
tests/product/test_enh_e4_g02_canonical_execution.py
tests/product/test_postgres_contract.py
```

including atomic concurrent claim node.

Use standardized PostgreSQL runner for PostgreSQL-marked/required tests.

### MUST preserve

* canonical family discriminator
* shared lifecycle
* atomic claim
* one winner on concurrent claim
* lease owner/expiry
* owner-checked update/complete
* retry same execution ID
* rerun/revise new execution ID
* cancel terminal execution semantics

### FAIL

G03 implementation introduces a regression in a passed G02 contract.

Environment inability remains BLOCKED, not FAIL.

---

## E4-G03_01_009 — Transition-debt and future-Gate boundary audit

Report:

```text
30_test_report/G03/
E4-G03_01_009_transition_debt_scope_audit.md
```

### Purpose

G03がcanonical stage contractを成立させつつ、G05 convergenceを先取りしていないことを確認する。

### Supports

```text
Gate scope
AC-003
AC-004
```

### MUST verify

```text
E4-TD-001 = OPEN until G05
E4-TD-002 = OPEN until G05
```

and no implementation of:

```text
G04 Result/Artifact consolidation
G05 old lifecycle full convergence
G06 lineage authority consolidation
G07 legacy retirement
G08 final bootstrap/audit
```

### Important interpretation

Old/transitional stage behaviorが残っていることだけでG03 FAILにしない。

FAIL条件は:

* canonical G03 pathがpersistent stage contractを満たさない
* 新しいdual canonical authorityを導入した
* bounded debtを無期限authorityとして再設計した

---

# 10. Recommended Command Set

The Test Agent MUST replace placeholders with actual nodes from implementation report when needed.

## 10.1 Static/unit boundary

```bash
uv run pytest \
  tests/product/test_enh_e4_g03_generic_executor_boundary.py
```

## 10.2 G03 PostgreSQL + G02 regression

Preferred single standardized invocation:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g03_persistent_stage_execution.py \
  tests/product/test_postgres_contract.py \
  tests/product/test_enh_e4_g02_canonical_execution.py
```

If implementation splits G03 tests across files, pass all required PostgreSQL test files/nodes to the same supported script.

## 10.3 Evidence

Record:

```text
exact command
implementation full SHA
runner start/end timestamp
pytest exit code
outer script exit code
migration current/head
stdout/stderr evidence path
metadata evidence path
```

Do not hand-edit generated raw evidence.

---

# 11. Acceptance Criteria Matrix

| AC | Mandatory Test Items |
|---|---|
| E4-G03-AC-001 | 002, 003, 007 |
| E4-G03-AC-002 | 002, 004, 006 |
| E4-G03-AC-003 | 001, 005, 009 |
| E4-G03-AC-004 | 003, 007 |
| E4-G03-AC-005 | 006, 008 |
| G02 regression | 008 |
| Transition debt / future-Gate boundary | 001, 009 |
| Product migration | 002 |

All listed mandatory items must PASS for a G03 PASS.

---

# 12. Mandatory Negative Checks

PASS requires all relevant negatives.

## Stage persistence

* no canonical family can create zero-stage persistent Execution
* no duplicate `(execution_id, stage_key)`
* no retry-created duplicate StageExecution identity
* no lost attempt history

## GenericExecutor

* no DB/UoW commit
* no claim/lease ownership
* no canonical retry policy
* no Result persistence
* no Artifact metadata persistence
* no lineage persistence authority

## Execution-stage consistency

* no stage RUNNING under non-RUNNING parent
* no wrong/stale owner mutation
* no Execution SUCCEEDED with required failed/nonterminal stage
* no new attempt after cancellation
* no cancellation disguised as prerequisite skip

## Migration/environment

* no root legacy migration
* no development DB destructive reset
* no manual G02 external PostgreSQL runbook
* no test infrastructure source modification by Test Agent

## Scope

* no G04+ architecture work
* no premature TD-001/TD-002 closure

---

# 13. Test Report Contract

Every Test Item report MUST contain at least:

```text
Project
Enhancement
Gate
Trial
Test Item ID
Implementation commit full SHA
Report/evidence commit if different
Purpose
Acceptance Criteria supported
Method
Files/code inspected
Exact commands
Environment
Expected result
Actual result
Exit code
Raw evidence path
Fact findings
Interpretation
Status: PASS / FAIL / BLOCKED
```

If a command was not run:

```text
NOT_RUN
```

and reasonを明記する。

Fact / interpretationを混同しない。

---

# 14. PostgreSQL Evidence Integrity

For any standard runner invocation, generated metadata/raw evidence should identify at least:

* tested git commit
* timestamp
* Compose project
* database service/image
* pytest command
* runner exit code
* raw stdout/stderr path

Evidenceがimplementation commitと異なるworktree/sourceをtestしていないことを確認する。

If Human Operator executes the one-command fallback, Test Agent MUST inspect:

```text
tested implementation SHA
evidence timestamp
exact runner command
outer exit status
raw output
```

before accepting it.

---

# 15. Gate Decision

全MUST Test Item完了後、作成:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G03/
E4-G03_01_999_gate_decision.md
```

Gate Decisionには最低限:

```text
Project
Enhancement
Gate
Trial
Baseline commit
Implementation commit
Evidence/report commit(s)
Decision
Test Items summary
E4-G03-AC-001 status
E4-G03-AC-002 status
E4-G03-AC-003 status
E4-G03-AC-004 status
E4-G03-AC-005 status
Product migration result
Standardized PostgreSQL verification result
G02 regression result
E4-TD-001 state
E4-TD-002 state
Known limitations
Blocking defects
Git evidence
Unrelated working-tree state
```

を含める。

Decision:

```text
PASS
FAIL
BLOCKED
```

の一つ。

---

# 16. Gate Decision Semantics

## PASS

Meaning:

```text
all canonical family values have persistent StageExecution contract
stage state/attempt/bindings are externally queryable
GenericExecutor is not persistence/claim/retry authority
canonical Causal zero-stage new write is impossible
stage failure/cancel/retry is consistent with Execution lifecycle
G02 remains intact
TD-002 is bounded and deferred to G05
```

PASS後も:

```text
E4-TD-001 OPEN
E4-TD-002 OPEN
```

でよい。

G03 PASSはG05 convergence完了を意味しない。

## FAIL

Implementation/required test codeがG03 contractを満たさない。

Test Agentは修正しない。

## BLOCKED

Required evidenceを取得できず、implementation correctnessを判定不能。

Environment問題なら、その事実をimplementation defectと分離する。

---

# 17. Required Outputs

Expected Gate-local reports:

```text
30_test_report/G03/
E4-G03_01_001_commit_change_boundary.md

30_test_report/G03/
E4-G03_01_002_stage_schema_migration.md

30_test_report/G03/
E4-G03_01_003_cross_family_stage_persistence.md

30_test_report/G03/
E4-G03_01_004_stage_query_attempt_history.md

30_test_report/G03/
E4-G03_01_005_generic_executor_boundary.md

30_test_report/G03/
E4-G03_01_006_stage_execution_state_consistency.md

30_test_report/G03/
E4-G03_01_007_stage_materialization_atomicity.md

30_test_report/G03/
E4-G03_01_008_g02_regression_postgres_contract.md

30_test_report/G03/
E4-G03_01_009_transition_debt_scope_audit.md

30_test_report/G03/
E4-G03_01_999_gate_decision.md
```

`999`以外のTest Item IDは3桁を維持する。

If environment fallback evidence is external/generated, report may reference it without copying generated raw files into source directories.

---

# 18. Stop Conditions

Gate Decision reportを作成した時点で停止する。

## PASS

* G04へ進まない
* source/test/migrationを変更しない
* 作業指示者へG03 PASSを返して停止

## FAIL

* source/test/migrationを修正しない
* failure evidence + Gate Decisionを作成
* 次Coding Trialを自分で開始しない

## BLOCKED

* product codeを変更してenvironmentを回避しない
* G02型manual PostgreSQL workaroundを始めない
* block evidence + Gate Decisionを作成
* 作業指示者へ必要なenvironment actionを最小限で返す

---

# 19. Supplemental Context

## 19.1 Expected environment

```text
Python 3.12
repository-managed uv
pytest
repository-managed compose.test.yaml
database_test
Product migration chain only
```

## 19.2 Not required in G03

```text
browser E2E
scientific benchmark
Result/Artifact end-to-end convergence
lineage convergence
legacy retirement verification
full clean bootstrap
CLI architecture audit
```

これらはfuture Gateの責務。

## 19.3 Primary risk focus

G03で最重要なのは、単にstage tableが追加されたことではない。

監査対象のauthority graphは:

```text
canonical Execution claim/lease authority
          │
          v
persistent StageExecution lifecycle authority
          │
          v
GenericExecutor = subordinate workflow infrastructure
          │
          v
scientific runner
```

である。

次のような見かけ上の実装をPASSしてはならない。

```text
StageExecution table exists
but Causal canonical writes do not create rows

or

attempt history exists
but GenericExecutor still decides canonical retry and commits persistence

or

family stages persist
but canonical Causal remains ephemeral
```

反対に、G05で閉じると明示されたold/transitional stage pathが残っていることだけでG03をFAILにしてはならない。

G03の判定対象は、**canonical G03 contractが成立したか**、かつ **GenericExecutorがauthorityを奪っていないか** である。
