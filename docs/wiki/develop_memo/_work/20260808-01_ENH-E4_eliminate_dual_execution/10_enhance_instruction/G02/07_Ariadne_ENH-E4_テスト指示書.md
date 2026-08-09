# Ariadne ENH-E4 E4-G02 テスト・監査指示書

* Project: Ariadne / causal-atelier
* Enhancement: ENH-E4 eliminate dual execution
* Branch: `refactor/ariadne_mvp_e4`
* Active Gate: `E4-G02`
* Gate name: Canonical Execution aggregate and claim
* Trial: `01`
* Trial ID format: 2-digit zero-padded decimal (`01`–`99`)
* Test Item ID format: 3-digit zero-padded decimal (`001`–`998`; `000` reserved; `999` Gate Decision)

---

# 1. Source of Truth

本書はE4-G02 Trial 01についてTest / Audit Agentが従う唯一のverification contractである。

作業指示者はTest Agent起動時に、対象となる具体的Implementation Completion Reportを指定する。

Expected:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/
E4-G02_01_implementation_completion_report.md
```

Test Agentは以下を参照してよい。

* 本書
* 指定されたImplementation Completion Report
* implementation commit上の対象production source
* implementation commit上の対象automated tests
* implementation commit上のProduct migrations
* `pyproject.toml`
* Git status / diff / log / show
* 自身が生成したtest evidence
* past test reportは履歴確認のみ

以下はAcceptance Criteria再解釈のために読まない。

* G02の06実装指示書
* `00_enhance_background/**`
* Revised requirements snapshots
* Architecture Review result
* chat history
* old 07

Test AgentはAcceptance Criteriaを再設計しない。

---

# 2. Test / Audit Agent Role

Test Agentの責務:

1. Implementation Completion Reportを読む。
2. implementation commit full SHAを固定する。
3. reportとactual Git diffが一致することを確認する。
4. E4-G02-AC-001〜005を独立検証する。
5. static architecture auditを行う。
6. domain/repository/lifecycle testを実行する。
7. real PostgreSQLが必要なclaim/concurrency testをisolated環境で実行する。
8. migrationが変更された場合はProduct migrationを検証する。
9. relevant regressionを実行する。
10. exact command、exit code、resultを保存する。
11. Test Item reportを作成する。
12. 最後にGate Decision reportを作成する。
13. `PASS / FAIL / BLOCKED` のいずれかを判定する。

Test Agentはsourceを修正しない。

---

# 3. Prohibited Work

禁止:

* production source変更
* automated test source変更
* migration変更
* dependency変更
* formatterによるsource rewrite
* bug fix
* assertion緩和
* skip / xfail追加
* failing test削除
* fixture変更によるfailure回避
* DB schema手動修正
* Product architecture再設計
* Coding Agent report改竄
* 06を読んでACを拡張する
* G03以降をtestする
* FAIL/BLOCKED後に自分で修正実装する

Test Agentが作成してよいRepository fileは原則として `30_test_report/` 配下のtest evidenceだけ。

read-only inspection用temporary fileが必要な場合はRepository外のtemporary directoryを使用し、final repository diffへ残さない。

既知のunrelated working-tree差分:

```text
deploy/.nfs000000000076202f00000088
```

が存在する場合、変更・restore・stageしない。

---

# 4. Gate Decision Rules

許容値:

```text
PASS
FAIL
BLOCKED
```

## PASS

以下を全て満たす。

* MUST Test Itemが全て完了
* E4-G02-AC-001〜005を全て満たす
* mandatory negative checks PASS
* required PostgreSQL concurrency evidenceあり
* migration変更時のmigration verification PASS
* mandatory regression PASS
* tested implementation commitが全Itemで同一
* source/test/migration modificationなし

## FAIL

implementation defectまたはtest coverage defectによって、Gate Acceptance Criteriaを満たさない。

例:

* double claim可能
* familyごとにclaim authorityが別
* retryがnew IDを生成
* rerun/reviseがsame ID
* invalid transitionを受理
* old family-specific claimerがcanonical pathのauthority
* GenericExecutorがclaim/commit
* mandatory G02 test coverageが欠落

## BLOCKED

environment/infrastructure等によりimplementation defectか判断不能。

例:

* implementation commitを固定不能
* required real PostgreSQL環境が提供されない
* migration test environment unavailable
* source changed after implementation handoff
* wrong branch
* reportとimplementation commitが一致しない

`PARTIAL_PASS` 等の独自状態は禁止。

---

# 5. Trial Rules

Active Trial:

```text
E4-G02 Trial 01
```

Rules:

1. current Trialだけを判定する。
2. 過去Trial結果を寄せ集めてPASSしない。
3. PASS Trialでは全MUST Itemを同一implementation commitに対して完走する。
4. deterministic product failureは無意味に再実行しない。
5. environment transient failureのみ最大1回再試行可。
6. 再試行した場合、初回resultとretry reasonの双方をevidenceへ残す。
7. timeout / interruptionは自動PASSにしない。
8. Test AgentはTrial番号を勝手に進めない。
9. FAIL後の次Coding Trialは作業指示者が開始する。

---

# 6. Implementation Commit Fixing Rules

Implementation Completion Reportから以下を取得する。

```text
Implementation commit: <full SHA>
```

Test開始時:

```bash
git rev-parse HEAD
git status --short
git show --stat --oneline <implementation-full-sha>
```

を記録する。

## Fixed target rule

全Test Itemは同一implementation commitを対象とする。

report-only commitがHEADに追加されている場合は許容できる。

条件:

```text
implementation commit
    ↓
only documentation/report commit(s)
    ↓
current HEAD
```

であり、implementation commit以降に以下が変更されていないこと。

* production source
* automated tests
* Product migrations
* dependency/config affecting G02 behavior

確認例:

```bash
git diff --name-status <implementation-full-sha>..HEAD
```

source/test/migration差分が存在する場合:

```text
BLOCKED
```

最新HEADを曖昧にテスト対象にしない。

---

# 7. Test Environment Policy

Python:

```text
3.12
```

test runner:

```text
uv run pytest
```

markersとして既存の以下を利用できる。

```text
unit
component
api
worker
postgres
```

G02では以下は原則不要。

```text
browser_e2e
scientific
scientific_benchmark
full MVP E2E
```

## Database safety

real PostgreSQLが必要なTest Itemは、

* existing repository PostgreSQL test fixture
* disposable test database
* isolated temporary PostgreSQL

のいずれかを使用する。

active development Compose DBへdestructive migration/resetを直接行わない。

isolated PostgreSQLを確保できず、AC-002/005またはmigration correctnessを証明できない場合は `BLOCKED`。

---

# 8. Test Execution Order

fail-fast順序:

```text
1. Commit / report integrity
2. Static architecture and persistence audit
3. Domain / repository contract tests
4. Cross-family lifecycle tests
5. Mutation identity tests
6. Concurrency / claim / lease negative tests
7. Conditional migration tests
8. Relevant regression
9. Gate Decision
```

重大なstatic architecture violationがある場合、後続runtime testを全部実行する必要はない。

ただしGate Decisionへ、

* 未実行Item
* fail-fast reason

を記録する。

PASS判定の場合は全MUST Itemを完走する。

---

# 9. Gate Test Plans

## E4-G02_01_001 — Commit and change-boundary audit

Report filename:

```text
30_test_report/
E4-G02_01_001_commit_change_boundary.md
```

### Purpose

Test対象commitを固定し、G02外の便乗実装がないことを確認する。

### Acceptance Criteria

supports:

```text
AC-001
AC-004
```

### Required inspection

* implementation report full SHA
* Git diff baseline → implementation commit
* changed files
* migration changes
* report AC→test mapping
* E4-TD-001記録
* no G03+ feature implementation

### PASS

* target commit一意
* report/diff一致
* G02 scope内
* future Gate先行実装なし
* unrelated `.nfs` changeがimplementation commitへ含まれていない

### FAIL

* G03以降のsemantic implementationあり
* GenericExecutor stage/result/lineage等を先行改造
* unrelated refactor大量混入
* reportとactual changed filesが一致しない

### BLOCKED

implementation commitを固定できない。

---

## E4-G02_01_002 — Canonical Execution structure and persistence

Report filename:

```text
30_test_report/
E4-G02_01_002_canonical_execution_structure.md
```

### Purpose

canonical Execution identity / family discriminator / persistence authorityを検証する。

### Acceptance Criteria

```text
E4-G02-AC-001
```

### Required checks

三family:

```text
CAUSAL
EXPLORATORY
PREDICTIVE
```

について、

* same semantic Execution entity
* same creation service/repository contract
* globally unique Execution ID namespace
* persistent family discriminator
* one canonical persistence authority

を確認する。

### Automated test

Implementation Completion Reportの

```text
E4-G02-AC-001
→ test path / node ID
```

mappingに指定された全nodeを実行する。

command形式:

```bash
uv run pytest -q <exact-node-id> [<exact-node-id> ...]
```

Test Agentはreportからexact node IDを展開し、実際に使用した完全commandをreportへ記載する。

### Negative static audit

current canonical pathが、

* separate Causal repository authority
* separate Exploratory/Predictive repository authority

をfamily discriminatorでswitchしてcanonical lifecycleとして扱っていないことを確認する。

旧compatibility pathの存在だけではFAILにしない。

---

## E4-G02_01_003 — Cross-family claim and lifecycle

Report filename:

```text
30_test_report/
E4-G02_01_003_cross_family_claim_lifecycle.md
```

### Purpose

三familyが同じclaim/state contractで動くことを検証する。

### Acceptance Criteria

```text
E4-G02-AC-002
```

### Required lifecycle

各family:

```text
create
→ QUEUED
→ canonical claim
→ RUNNING
→ terminal
```

terminal successful / failure pathはimplementation contractに存在する範囲を検証する。

### MUST

* same canonical claim API/repository
* atomic claim
* auditable owner/claim state
* family discriminatorがclaimer選択を別authorityへ分岐させない

### Automated test

Implementation reportでAC-002にmapされたnodeを全実行。

real DB contractが必要なnodeにはisolated PostgreSQLを使用する。

### FAIL

* family-specific canonical claimer
* direct table/session claim bypass
* one familyだけcanonical path未対応
* QUEUED→RUNNING→terminal contract不一致

---

## E4-G02_01_004 — Mutation identity contract

Report filename:

```text
30_test_report/
E4-G02_01_004_mutation_identity.md
```

### Purpose

retry / rerun / revise / cancel identity semanticsを検証する。

### Acceptance Criteria

```text
E4-G02-AC-003
```

### Required assertions

#### Retry

```text
same execution_id
```

かつretry occurrenceが区別可能。

#### Rerun

```text
new execution_id
```

かつsource Executionへのtyped relationあり。

#### Revise

```text
new execution_id
```

かつbase/source Executionへのtyped relationあり。

#### Cancel

canonical state contractに従いinvalid cancellationを拒否する。

### Negative

以下はFAIL。

* retry creates new Execution
* rerun rewrites original Execution
* revise rewrites original Execution
* source relationをobject keyやgeneric-only edgeだけで表現
* successful prior identity/historyをsilent rewrite

### Automated test

Implementation reportのAC-003 nodeを全実行する。

---

## E4-G02_01_005 — Canonical claim authority negative audit

Report filename:

```text
30_test_report/
E4-G02_01_005_old_claimer_negative_audit.md
```

### Purpose

old claimerとGenericExecutorがcanonical authorityになっていないことを確認する。

### Acceptance Criteria

```text
E4-G02-AC-004
```

### Required static inspection

canonical G02 pathから、

* old Causal claimer
* old Family claimer
* direct Family session claim
* GenericExecutor claim
* GenericExecutor lifecycle commit

へのauthority delegationがないこと。

Repository searchを用いてよい。

例:

```bash
rg -n "claim|lease|GenericExecutor|ExecutionProcessor|FamilyExecution" src tests
```

実際のsymbol名に合わせて追加searchしてよい。

### Important boundary

E4-TD-001により、old Causal / Family lifecycle sourceや旧write pathがまだRepositoryに存在すること自体はG02 FAILではない。

FAIL条件:

```text
canonical G02 path
    ↓
old claimer is authoritative
```

PASS可能条件:

```text
old path still exists as bounded compatibility surface
but canonical path owns its own claim/state authority
```

---

## E4-G02_01_006 — Invalid transition / double claim / lease ownership

Report filename:

```text
30_test_report/
E4-G02_01_006_claim_concurrency_negative.md
```

### Purpose

claim/state ownershipの競合安全性を検証する。

### Acceptance Criteria

```text
E4-G02-AC-005
```

### MUST cases

* two claimers compete for same QUEUED Execution
* exactly one acquires ownership
* second claimant is rejected/no-op according to explicit contract
* non-owner cannot renew lease
* non-owner cannot complete canonical Execution
* invalid state transition rejected
* terminal state cannot be silently reclaimed
* expired/stale ownership behavior is deterministic

### Real PostgreSQL

atomicityをmockだけで証明してはならない。

persistence implementationがPostgreSQL locking/conditional updateに依存する場合、real PostgreSQL testをMUSTとする。

Implementation reportのAC-005 test mappingを実行する。

isolated PostgreSQLを用意できない場合:

```text
BLOCKED
```

---

## E4-G02_01_007 — Product migration verification

Report filename:

```text
30_test_report/
E4-G02_01_007_product_migration.md
```

### Applicability

implementation commitがProduct migrationを追加・変更した場合:

```text
MUST
```

migration変更なしの場合:

```text
N/A
```

としてreportは作成し、理由を記録する。

### Required checks when applicable

* migration chain = `alembic_product.ini` / `product_migrations`
* previous head matches implementation report
* new head is single Product head
* root legacy migration dependencyなし
* isolated empty DBへupgrade可能
* downgrade/upgrade contractがrepository policy上成立
* old Causal / Family tablesをG02で不必要にdropしていない

### Static command

最低限:

```bash
uv run alembic -c alembic_product.ini heads
uv run alembic -c alembic_product.ini history
```

actual isolated migration commandsはenvironmentに合わせて完全形をreportへ記録する。

active development DBをdestructive testに使わない。

---

## E4-G02_01_008 — Relevant regression

Report filename:

```text
30_test_report/
E4-G02_01_008_relevant_regression.md
```

### Purpose

G02変更によって既存Product lifecycle / worker contractが壊れていないことを確認する。

### Required scope

最低限:

* implementation commitでchanged/newされた全G02 test file
* existing Product Execution domain/application tests
* existing worker claim/lease/retry/cancel tests
* changed repository/persistenceに対応するexisting tests

Test selection rule:

1. Implementation Completion Reportに列挙されたchanged test filesを全実行。
2. `tests/product/` および必要な`tests/integration/`から、変更componentに直接対応する既存testsを選択。
3. selection理由とnode/file一覧をreportへ記録。

command:

```bash
uv run pytest -q <selected-test-paths-or-nodeids>
```

full browser E2E、scientific benchmarkはG02では不要。

### PASS

selected regression all pass。

### FAIL

G02変更に起因する既存relevant regression failureあり。

---

# 10. Evidence Requirements

各Test Item reportは最低限以下を記録する。

* Project
* Enhancement
* Gate
* Trial
* Test Item ID
* tested implementation commit full SHA
* current HEAD
* branch
* working directory
* environment
* Product migration head where relevant
* exact command
* exit code
* test count
* stdout/stderr summary
* relevant raw log path
* Acceptance Criteria mapping
* PASS / FAIL / BLOCKED
* reproduction procedure

commandはcopy-and-paste可能な完全形とする。

「pytestを実行した」だけは禁止。

---

# 11. Gate Decision

全MUST Item完了後、作成:

```text
30_test_report/
E4-G02_01_999_gate_decision.md
```

Gate Decisionには最低限以下を含める。

```text
Project
Enhancement
Gate
Trial
Implementation commit
Decision
Test Items summary
AC-001 status
AC-002 status
AC-003 status
AC-004 status
AC-005 status
Transition Debt
Known limitations
Blocking defects
Git evidence
```

Decision:

```text
PASS
FAIL
BLOCKED
```

のいずれか一つ。

---

# 12. Acceptance Criteria Final Mapping

| AC                        | Mandatory Test Items |
| ------------------------- | -------------------- |
| E4-G02-AC-001             | 001, 002             |
| E4-G02-AC-002             | 003, 006             |
| E4-G02-AC-003             | 004                  |
| E4-G02-AC-004             | 001, 005             |
| E4-G02-AC-005             | 006                  |
| Regression                | 008                  |
| Migration when applicable | 007                  |

---

# 13. Transition Debt Verification

E4-G02 PASS時にも、

```text
E4-TD-001 = OPEN
```

である。

これはfailureではない。

Gate Decisionには以下を明記する。

```text
E4-TD-001
Status: OPEN
Owner: ENH-E4 migration sequence
Exit Gate: E4-G05
Exit Criterion:
no old Causal / Family lifecycle accepts new Product writes
```

G02 Test Agentは旧lifecycle sourceの存在だけを理由にFAILしてはならない。

一方、

```text
canonical G02 claim authority delegates to old claimer
```

はFAIL。

---

# 14. Completion Conditions

## PASS decisionを作成可能

全て必要。

1. Items 001〜006、008完了。
2. Item 007はapplicableなら完了、非applicableならN/A evidenceあり。
3. AC-001〜005すべてPASS。
4. real PostgreSQLが必要なclaim/concurrency testを完了。
5. relevant regression PASS。
6. implementation commit固定。
7. source/test/migration変更なし。
8. E4-TD-001が正しくOPENとして記録。
9. G03以降の先行実装を確認していない。
10. full evidenceが30_test_reportへ存在。

## FAIL decision

少なくとも一つの具体的implementation/test coverage failure evidenceを記録する。

Test Agentは修正しない。

## BLOCKED decision

block原因、affected Items、なぜPASS/FAILを判別不能かを記録する。

product code変更で回避しない。

---

# 15. Required Outputs

Expected reports:

```text
30_test_report/
E4-G02_01_001_commit_change_boundary.md

30_test_report/
E4-G02_01_002_canonical_execution_structure.md

30_test_report/
E4-G02_01_003_cross_family_claim_lifecycle.md

30_test_report/
E4-G02_01_004_mutation_identity.md

30_test_report/
E4-G02_01_005_old_claimer_negative_audit.md

30_test_report/
E4-G02_01_006_claim_concurrency_negative.md

30_test_report/
E4-G02_01_007_product_migration.md

30_test_report/
E4-G02_01_008_relevant_regression.md

30_test_report/
E4-G02_01_999_gate_decision.md
```

`999`以外のTest Item IDは3桁を維持する。

---

# 16. Stop Conditions

Gate Decision reportを作成した時点で停止する。

## PASS

E4-G03へ進まない。

作業指示者へPASSを返して停止する。

## FAIL

source/test/migrationを修正しない。

failure evidenceとGate Decisionを作成して停止する。

次Coding Trialは別Agent execution。

## BLOCKED

product codeを変更して回避しない。

block evidenceとGate Decisionを作成して停止する。

---

# 17. Supplemental Test Context

## Expected environment

* Python 3.12
* repository-managed `uv`
* pytest
* isolated PostgreSQL where required
* Product migration chain only

## Not required in G02

* browser E2E
* scientific acceptance benchmark
* full clean bootstrap
* Result/Artifact end-to-end convergence
* lineage convergence
* legacy retirement verification

これらは後続Gateの責務。

## Primary risk focus

G02で最重要なのは機能量ではなく、

```text
one identity
one state authority
one atomic claim authority
```

である。

三familyそれぞれで処理結果が出ることだけを確認して、

```text
claim authority is still duplicated
```

という状態をPASSしてはならない。
