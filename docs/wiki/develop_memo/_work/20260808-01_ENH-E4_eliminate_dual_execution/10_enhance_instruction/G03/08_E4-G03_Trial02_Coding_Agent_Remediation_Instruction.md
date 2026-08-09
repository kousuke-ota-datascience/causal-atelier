# E4-G03 Trial 02 — Coding Agent Remediation Instruction

* Project: Ariadne / causal-atelier
* Enhancement: ENH-E4 eliminate dual execution
* Repository: `kousuke-ota-datascience/causal-atelier`
* Branch: `refactor/ariadne_mvp_e4`
* Gate: `E4-G03`
* Gate name: Persistent StageExecution and runner boundary
* Trial: `02`
* Prior Trial Decision: `E4-G03 Trial 01 = FAIL`
* Prior implementation commit: `f455354e3724b66360bed6d3cfd4646ca1463a89`
* Prior evidence/report commit: `692a8b8899f5c862826648f2f03d88b45bf51c4f`
* Prior FAIL/report commit: `de4b120`（作業開始時にfull SHAを取得して記録すること）
* Product migration head already introduced by Trial 01: `20260809_product_0008`
* PostgreSQL verification infrastructure: `PASS_READY_FOR_G03`

---

# 1. Purpose

本指示書は **E4-G03 Trial 02 Coding Agent remediation instruction** である。

Trial 01のFAIL理由は、現時点で確認されている範囲では、

```text
production implementationが動作しないこと
```

ではなく、

```text
G03の必須Acceptance Criteriaに対するautomated acceptance coverage不足
```

である。

したがってTrial 02の第一目的は:

> **Trial 01で不足していた必須automated acceptance coverageを追加し、06/07で既に固定されているG03 contractを実際のautomated evidenceで満たせる状態にすること**

である。

Trial 02はproduction redesign Trialではない。

ただし、新たに追加した正当なacceptance testが実際のproduction defectを露呈した場合は、そのdefectを閉じるための **最小限のproduction修正** を許可する。

---

# 2. Source of Truth / Contract Hierarchy

Trial 02では以下を正本とする。

## 2.1 Gate semantic contract

既存のGate-local 06/07を変更せず使用する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G03/
06_Ariadne_ENH-E4_実装指示書.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G03/
07_Ariadne_ENH-E4_テスト指示書.md
```

06/07はTrial 01 metadataを含むが、**G03のarchitecture / acceptance / test semanticsはimmutable contractとして維持する**。

Trial 02に関するTrial番号・開始ref・remediation scopeは本指示書が差分contractとして補う。

06/07本文を書き換えてTrial 02化してはならない。

## 2.2 Trial 01 implementation handoff

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G03/
E4-G03_01_implementation_completion_report.md
```

## 2.3 Trial 01 test evidence

特に以下を必ず読む。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G03/
E4-G03_01_003_cross_family_stage_persistence.md

E4-G03_01_004_stage_query_attempt_history.md
E4-G03_01_005_generic_executor_boundary.md
E4-G03_01_006_stage_execution_state_consistency.md
E4-G03_01_007_stage_materialization_atomicity.md
E4-G03_01_008_g02_regression_postgres_contract.md
E4-G03_01_999_gate_decision.md
```

必要に応じて001/002/009も参照する。

## 2.4 Current source

作業開始時点のactual branch HEADを確認する。

Trial 01のFAIL report commit以降にsource/test/migration変更がある場合は、必ずdiffを確認し、本Trialへ影響するかを説明する。

---

# 3. Start-of-Work Repository Verification

作業開始時に必ず実行し、結果をTrial 02 Implementation Completion Reportへ記録する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log --oneline -12
```

さらに:

```bash
git show --no-patch --format=fuller f455354e3724b66360bed6d3cfd4646ca1463a89
git show --no-patch --format=fuller de4b120
```

を確認する。

Expected branch:

```text
refactor/ariadne_mvp_e4
```

Trial 02 starting commitはactual full SHAで固定する。

branchが異なる場合は作業しない。

---

# 4. Prior Trial Decision

Trial 01 Gate Decision:

```text
E4-G03 = FAIL
```

FAIL classification:

```text
required automated acceptance coverage defect
```

Trial 01では以下が成功済み。

```text
Product migration:
20260809_product_0008

standardized PostgreSQL run:
migration + G03 persistence + PostgreSQL contract + G02 regression
10 passed

GenericExecutor static/boundary suite:
5 passed
```

これらの成功はTrial 02で無視してよいという意味ではない。

Trial 02では、新しいimplementation/test commitに対してrequired regressionを再実行する。

---

# 5. Trial 02 Primary Remediation Scope

Trial 02では、以下7領域の必須coverageを閉じる。

## R-01 Cross-family real PostgreSQL persistence

現在のreal PostgreSQL testがCAUSAL手作業stage round-trip中心である問題を閉じる。

automated real PostgreSQL testで少なくとも:

```text
CAUSAL
EXPLORATORY
PREDICTIVE
```

それぞれについて、canonical pathから:

```text
Execution persisted
StageExecution >= 1 persisted
StageExecution.execution_id == Execution.execution_id
new UoW / new Sessionでreload可能
```

を検証する。

**単なるStagePlanMaterializerのin-memory loopでは不十分。**

Canonical application/service pathを通すこと。

Family-specific transitional persistenceをcanonical evidenceとして使用してはならない。

---

## R-02 Repository query / complete round-trip

real PostgreSQL上で、runnerを呼ばずにrepository/application queryから以下を再構築できることを自動検証する。

```text
list_for_execution(execution_id)
get(stage_execution_id)

stage_key
stage_type
ordinal
dependencies
status
input_binding
output_binding
last_error
started_at
finished_at
attempt history
```

新しいSession/UoWでreloadする。

少なくとも1ケースは依存関係を持つmulti-stage planを使用し、ordered `list_for_execution()` がpersistent planを正しく再構成することを確認する。

---

## R-03 Persistent retry / attempt history

real PostgreSQL上で、同一canonical stageについて:

```text
attempt 1 -> FAILED
retry authorization / reclaim
attempt 2 -> RUNNING -> SUCCEEDED
```

を成立させる。

Must assert:

```text
same execution_id
same stage_execution_id
attempt numbers == [1, 2]
attempt 1 preserved
attempt 1 error preserved
attempt 1 timestamps preserved
attempt 2 persisted
new Session/UoWでも同じhistoryを取得可能
```

retryのauthorityがGenericExecutorではないことも壊してはならない。

---

## R-04 GenericExecutor behavioral negative

既存static testだけでは不十分。

runner failureを実際に発生させるbehavior testを追加する。

Test double / spy / monkeypatch等を用いてよいが、最低限次を証明する。

runner failure時にGenericExecutor自身が:

```text
DB/UoW commitしない
Execution claimしない
lease renewしない
canonical retry decisionをしない
StageExecution persistenceしない
Result persistenceしない
Artifact metadata persistenceしない
lineage persistenceしない
```

GenericExecutorはfailure outcomeを返す/raiseするだけで、canonical lifecycle authorityを所有しない。

static source substring assertionだけでこの項目を代替してはならない。

---

## R-05 Persistent failure / cancellation / stale lease / invalid success

real PostgreSQLが必要なstate/ownership scenarioはreal PostgreSQLで検証する。

最低限:

### R-05-A Failure without retry

```text
Execution RUNNING
Stage RUNNING
attempt failure
Stage FAILED
attempt finalized
Execution FAILED
```

をpersistent stateとして確認する。

### R-05-B Cancellation

verify:

```text
parent Execution = CANCELLED
already-SUCCEEDED stage remains SUCCEEDED
nonterminal stage = explicit CANCELLED
new attempt cannot start after cancellation
no stale durable RUNNING stage
same Execution ID
```

### R-05-C Wrong/stale owner

wrong ownerまたはexpired/stale lease ownerでstage mutationを試行し:

```text
operation rejected
durable stage state unchanged
```

を確認する。

### R-05-D Invalid success

required stageが:

```text
PENDING
READY
RUNNING
FAILED
```

のいずれかである状態からparent Execution `SUCCEEDED` を成立させようとしても、durable inconsistent stateを生成できないこと。

---

## R-06 Materialization failure transaction rollback

canonical submit/create pathでstage materialization/persistenceが失敗した場合に:

```text
Executionのみcommit
```

されないことをreal PostgreSQLで検証する。

最低限:

1. Causal empty/invalid canonical plan → durable Executionなし。
2. Stage persistence/materialization failure injection → Execution + stages rollback。
3. failure後の再submissionでorphan/duplicate stage rowsなし。
4. `(execution_id, stage_key)` duplicateをごまかすためのmanual cleanupに依存しない。

Unit-level `StagePlanMaterializer` rejectionだけでは不十分。

---

## R-07 Causal zero-stage durable write prevention

real PostgreSQL上で、canonical Causal application pathから:

```text
zero StageExecution childのvalid persistent Execution
```

を作れないことを独立検証する。

対象はcanonical Product write pathであり、raw SQLによるcontract bypassは対象ではない。

このtestはR-06と統合してよいが、pytest node / assertion上でAC-004 evidenceとして識別できるようにする。

---

# 6. Implementation-Firstではなく Test-First Remediation

Trial 02は以下の順序で進める。

```text
1. Trial 01 failure evidenceを読む
2. current sourceを読む
3. 必須acceptance testsを追加する
4. 追加testを実行する
5. FAILした場合、failureが:
   a. test defect
   b. environment issue
   c. actual production defect
   のどれかを切り分ける
6. actual production defectの場合のみproduction codeを最小修正
7. 新規test + G02 regressionを再実行
8. READY_FOR_TEST handoff
```

禁止:

```text
先にproduction codeを「念のため」書き直す
architectureを再設計する
06/07を書き換える
Trial 01 reportを修正する
```

---

# 7. Production Change Policy

## 7.1 Default

Trial 02のdefault production change:

```text
NONE
```

まずtestsを追加する。

## 7.2 Production modification is allowed only when

新しいrequired acceptance testが、06/07に照らして明確なproduction defectを再現した場合。

その場合は:

1. failing pytest nodeを記録する。
2. expected vs actualを記録する。
3. defectが06/07のどのcontract違反か特定する。
4.最小production修正を行う。
5. targeted testを再実行する。
6. required G03 suite + G02 regressionを再実行する。
7. Implementation Completion Reportへproduction change reasonを記録する。

## 7.3 Forbidden production changes

* G04 Result/Artifact architecture
* G05 convergence
* G06 lineage
* G07 legacy retirement / CLI
* G08 bootstrap
* root legacy migration
* scientific algorithm
* test infrastructure redesign
* unrelated cleanup

---

# 8. Product Migration Policy

Trial 01で:

```text
20260809_product_0008
```

が導入済み。

Trial 02のdefault:

```text
new migration = NOT REQUIRED
```

test coverage追加だけならmigrationを追加してはならない。

新しいacceptance testがactual schema defectを露呈し、その修正にschema changeが本当に必要な場合のみ、06/07 contractに従って新Product migrationを検討する。

その場合は理由をreportへ明示し、root legacy migrationは変更しない。

---

# 9. Test File Strategy

既存test:

```text
tests/product/test_enh_e4_g03_persistent_stage_execution.py
tests/product/test_enh_e4_g03_generic_executor_boundary.py
```

を拡張してよい。

coverageが明確になるなら、新しいG03 test fileへ分割してよい。

例:

```text
tests/product/test_enh_e4_g03_cross_family_postgres.py
tests/product/test_enh_e4_g03_stage_lifecycle_postgres.py
tests/product/test_enh_e4_g03_materialization_atomicity_postgres.py
```

命名は例であり強制しない。

重要なのは各ACとpytest nodeの対応が一意に追跡できること。

---

# 10. Required AC → Automated Node Mapping

Trial 02 Completion Reportでは少なくとも以下の粒度でexact node mappingを提示する。

## AC-001

Must map to nodes proving:

```text
CAUSAL real PostgreSQL
EXPLORATORY real PostgreSQL
PREDICTIVE real PostgreSQL
persistent reload
```

## AC-002

Must map to nodes proving:

```text
list_for_execution
get by stage ID
dependencies
input/output
timestamps/errors
attempt [1,2] history
new-session reload
```

## AC-003

Must map to:

```text
static architecture boundary
runner-failure behavioral negative
```

## AC-004

Must map to:

```text
Causal zero-stage durable-write prevention
materialization/persistence rollback
no orphan/duplicate after failed transaction
```

## AC-005

Must map to:

```text
failure -> parent FAILED
retry same IDs / appended attempt
cancellation
wrong/stale owner rejection
invalid Execution success rejection
```

単一nodeが複数項目を検証してもよいが、report上でどのassertionがどのcontractを証明するかを明示する。

---

# 11. Standardized PostgreSQL Verification

real PostgreSQLを必要とするtestは必ずrepository-managed runner:

```bash
scripts/test/run_product_postgres_tests.sh <pytest-path-or-node> [pytest-options]
```

を使用する。

Trial 02でG02型manual verificationへ戻ってはならない。

禁止:

```text
manual docker run
manual network route probing
127.0.0.1 / 172.17.0.1 workaround
manual DSN export
manual psql reset
manual alembic
manual pytest against hand-wired PostgreSQL
```

---

# 12. Existing Full-Pytest External DB Issue

Trial 01ではstandardized runner外の:

```text
uv run pytest
```

がpre-existing external DB:

```text
172.17.0.1:55432
ariadne_g02_test
```

を参照し、`product_stage_execution` absentで失敗する事象が記録されている。

Trial 02ではこれを:

```text
known environment/configuration issue
```

として扱う。

この問題をG03 production defectとみなしてproduct codeを変更してはならない。

また、この問題を解消するためにG03 scopeでtest infrastructureを再設計してはならない。

standardized PostgreSQL runnerの成功/失敗をG03 real PostgreSQL verification authorityとする。

必要ならnon-PostgreSQL unit/static testsのみを明示的node指定で実行する。

---

# 13. Mandatory Regression

最低限、Trial 02のfixed implementation/test commitに対して:

```text
tests/product/test_enh_e4_g03_*.py
tests/product/test_postgres_contract.py
tests/product/test_enh_e4_g02_canonical_execution.py
```

のrequired subsetを実行する。

実際に追加したG03 test filesをすべてstandardized runnerへ渡す。

例:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g03_persistent_stage_execution.py \
  tests/product/test_enh_e4_g03_cross_family_postgres.py \
  tests/product/test_enh_e4_g03_stage_lifecycle_postgres.py \
  tests/product/test_enh_e4_g03_materialization_atomicity_postgres.py \
  tests/product/test_postgres_contract.py \
  tests/product/test_enh_e4_g02_canonical_execution.py
```

実ファイル名に合わせて調整する。

GenericExecutor pure behavior/static testsは:

```bash
uv run pytest -q <exact node/file>
```

でもよい。

---

# 14. Evidence Discipline for Coding Agent Self-check

Coding AgentはGate Test Reportを作らないが、自身のImplementation Completion Reportにはself-check evidenceを正確に記録する。

各実行について最低限:

```text
Exact command
Test target / node
Exit code
Passed/failed/skipped count
PostgreSQL evidence path if applicable
Implementation/test commit SHA
```

を記録する。

「passed」だけでは不十分。

実行していないcommandは実行したように書かない。

---

# 15. Trial 01 Test Report Artifact Handling

以下はTrial 01 evidenceとしてimmutable。

```text
30_test_report/G03/E4-G03_01_001_...
...
30_test_report/G03/E4-G03_01_999_gate_decision.md
```

Coding Agentは:

```text
修正しない
追記しない
整形しない
renameしない
```

Trial 01 Test Agentのreport-format不備もTrial 02 Coding Agentが修正してはならない。

Trial 02 Test Agentが新しい:

```text
E4-G03_02_001_...
...
E4-G03_02_999_gate_decision.md
```

を作る。

Test Agent reporting contractの遵守は07の責務であり、Coding Agentがtest reportを先に生成してはならない。

---

# 16. Trial 02 Implementation Completion Report

作成:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G03/
E4-G03_02_implementation_completion_report.md
```

Status:

```text
READY_FOR_TEST
```

またはsemantic contradictionがある場合のみ:

```text
DESIGN_BLOCKED
```

Gate PASS/FAILは書かない。

---

# 17. Required Completion Report Contents

最低限:

## Metadata

```text
Project
Enhancement
Gate
Trial
branch
Trial 02 starting full SHA
Trial 01 implementation full SHA
Trial 01 FAIL/report full SHA
Trial 02 implementation/test full SHA
report commit if different
Product migration head
```

## Prior FAIL summary

Trial 01 FAIL理由を7 remediation領域へmappingする。

## Changed files

次を分離:

```text
test changes
production changes
migration changes
documentation/report changes
```

production changeがない場合:

```text
Production changes: NONE
```

と明示する。

## Test coverage added

R-01〜R-07ごとに:

```text
pytest exact node
what it proves
real PostgreSQL / pure unit
```

を記載する。

## Production defect findings

各新規testについて:

```text
PASS immediately
or
initial FAIL -> actual production defect -> fixed
```

を追跡可能にする。

actual production defectがなかった場合:

```text
No production defect was exposed by the added mandatory acceptance tests.
```

と明示する。

## AC mapping

E4-G03-AC-001〜005 → exact pytest nodes。

## Self-check

各commandの:

```text
exact command
exit code
test count
evidence path
tested SHA
```

## Regression

G02 contract / PostgreSQL contract結果。

## Transition debt

```text
E4-TD-001 OPEN until G05
E4-TD-002 OPEN until G05
```

## Scope

G04+未実装を明示。

## Environment note

standard runner外のold external DB issueが観測された場合はenvironment/configurationとして分離。

## Working tree

known unrelated artifactを分離して記録。

---

# 18. Implementation/Test Commit Policy

Trial 02ではtest additionsもimplementation artifactの一部としてfixed commitへ含める。

推奨:

```text
Trial 02 implementation/test commit
  ├─ required acceptance test additions
  ├─ actual defectが出た場合のみminimal production fix
  └─ schema fixが必要な場合のみProduct migration
```

Implementation Completion Reportは別commitでよい。

Test Agentには:

```text
fixed Trial 02 implementation/test commit
report/evidence ref
```

を明確に分けてhandoffする。

---

# 19. Git Integrity

commit前:

```bash
git status --short
git diff --check
git diff --cached --name-status
```

known unrelated artifact:

```text
deploy/.nfs000000000076202f00000088
```

は:

```text
stageしない
restoreしない
delete/recreateしない
implementation commitへ含めない
```

Trial 01 instruction/report artifactsも不要に触らない。

---

# 20. Stop Conditions

## READY_FOR_TEST

以下が全て成立したら停止する。

1. R-01〜R-07のrequired automated coverageが存在する。
2. 追加testがfixed Trial 02 commitに含まれる。
3. actual defectが出た場合はminimal fix済み。
4. required G03 tests pass。
5. standardized real PostgreSQL verification pass。
6. G02 regression pass。
7. Product migration current/headが期待値と整合。
8. no G04+ scope crossing。
9. TD-001/TD-002 remain OPEN。
10. Trial 02 Implementation Completion Report作成。
11. exact commands / exit codes / evidence paths記録。
12. Trial 01 test reports untouched。
13. unrelated working-tree artifact untouched。

その後:

```text
Test Agentへhandoff
```

し、自分でGate Decisionを作らない。

## DESIGN_BLOCKED

追加された正当なacceptance testを満たすために、06/07と矛盾する新architecture decisionが必要になった場合のみ。

単なるtest failureはDESIGN_BLOCKEDではない。

environment failureもDESIGN_BLOCKEDではない。

---

# 21. Explicit Non-Goals

Trial 02では以下を行わない。

```text
06/07の改訂
Trial 01 report修正
G04 Result/Artifact consolidation
G05 convergence
G06 lineage
G07 legacy retirement
G08 final bootstrap
test PostgreSQL infrastructure redesign
old external DB cleanup
scientific implementation redesign
unrelated repository cleanup
```

---

# 22. Final Coding Agent Handoff Format

Coding Agentの最終応答は少なくとも以下を含む。

```text
Status: READY_FOR_TEST / DESIGN_BLOCKED

Trial 02 starting SHA:
Trial 02 implementation/test SHA:
Report SHA if different:

Production changes:
- NONE
or
- <minimal fixes and reason>

Test additions:
- R-01 ...
- R-02 ...
- ...
- R-07 ...

Product migration:
- current/head
- new migration NONE / <revision>

Self-check:
- <exact command> -> <exit/result>
- <exact command> -> <exit/result>

PostgreSQL evidence:
- <path>

G02 regression:
- PASS / unavailable with reason

E4-TD-001:
- OPEN until G05

E4-TD-002:
- OPEN until G05

Known environment issue:
- old external DB issue, if observed

Unrelated working-tree state:
- recorded, untouched
```

---

# 23. Primary Decision Rule

Trial 02で最も重要な判断規則はこれである。

```text
Missing acceptance evidence
        ↓
Add the missing test
        ↓
Does the test pass?
   ├─ YES
   │    ↓
   │  production implementation remains unchanged
   │
   └─ NO
        ↓
   Is the test correct and environment valid?
        ├─ NO → fix test / environment classification only
        └─ YES
             ↓
        actual G03 production defect
             ↓
        minimal production fix
```

**coverage不足を理由にproduction architectureを書き直してはならない。**

同時に、**「sourceを見る限り正しそう」という理由でrequired automated evidenceを省略してもならない。**

Trial 02の成功条件は、G03 contractを推測ではなく、06/07が要求するautomated acceptance evidenceで閉じることである。
