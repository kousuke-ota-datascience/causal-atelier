# E4-G02 Supplemental — Isolated PostgreSQL Verification Retry Procedure

## 1. 文書目的

本書は、ENH-E4 `E4-G02 Trial 01` のIndependent Testにおいて、PostgreSQL実環境不足によってBLOCKEDとなったTest Itemを、人間がisolated PostgreSQL環境を準備したうえで再実行するための手順および実行証跡を記録する。

対象Gate:

```text
E4-G02
Canonical Execution aggregate and claim
```

対象Trial:

```text
Trial 01
```

本手順はCoding Trialを新しく開始するものではない。

```text
implementation commit = unchanged
source/test/migration = unchanged
```

を前提として、**同一 E4-G02 Trial 01 に対するverification retry**を行う。

---

# 2. 背景

初回Independent Testでは、以下が確認された。

```text
PASS:
- AC-001
- AC-003
- AC-004
- relevant regression: 41 passed

BLOCKED:
- AC-002
- AC-005
- Product migration verification
```

BLOCKED理由:

```text
ARIADNE_PRODUCT_TEST_DATABASE_URL is not configured
```

および、

```text
Docker API permission denied
```

であり、implementation defectは確認されていない。

したがって、

```text
Coding Trial 02
```

へ進めず、isolated PostgreSQLを準備して同一implementation commitに対するTest Trial 01を再開する。

---

# 3. Repository

Repository:

```text
causal-atelier
```

Branch:

```text
refactor/ariadne_mvp_e4
```

Working repository example:

```text
/loc0/bigbrother/repositories/causal-atelier
```

本書配置先:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G02_Supplemental/
01_isolated_postgresql_verification_retry_procedure.md
```

---

# 4. Safety Principles

本作業では既存の開発DBを使用しない。

以下を守る。

1. temporary PostgreSQL clusterを `/tmp` 配下へ作成する。
2. localhost専用portを使用する。
3. existing Compose PostgreSQLへ接続しない。
4. root legacy migrationを使用しない。
5. Product migrationだけを使用する。
6. implementation commitを固定する。
7. source/test/migrationを変更しない。
8. existing working tree差分を変更しない。
9. verification終了後、一時PostgreSQLを削除する。

---

# 5. Verification Retryの意味

今回の作業は、

```text
E4-G02 Trial 01
        ↓
environment BLOCKED
        ↓
isolated PostgreSQL provision
        ↓
same implementation commit
        ↓
verification retry
```

である。

以下ではない。

```text
E4-G02 Trial 02
```

Trial 02を開始する条件は、

```text
Trial 01 FAIL
        ↓
source/test/migration correction
        ↓
new implementation commit
```

である。

今回はこれに該当しない。

---

# 6. Pre-flight Record

作業開始前に以下を記録する。

## 6.1 Timestamp

```bash
date --iso-8601=seconds
```

Result:

```text
2026-08-09T00:56:28+00:00
```

## 6.2 Repository

```bash
cd /loc0/bigbrother/repositories/causal-atelier

git branch --show-current
git rev-parse HEAD
git status --short
```

Result:

```text
$ cd /loc0/bigbrother/repositories/causal-atelier

$ git branch --show-current
refactor/ariadne_mvp_e4

$ git rev-parse HEAD
ab414bba01916f6e86db723c63363fc7cd7864bc

$ git status --short
 D deploy/.nfs000000000076202f00000088
?? docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/G02_Supplemental/

```

Expected branch:

```text
refactor/ariadne_mvp_e4
```

---

# 7. Implementation Commitの固定

## 7.1 Implementation Completion Reportを確認する

対象:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/
G02/
E4-G02_01_implementation_completion_report.md
```

ここに記録されている、

```text
Implementation commit:
```

のfull SHAを使用する。

環境変数へ設定する。

```bash
export IMPL_COMMIT="<FULL_IMPLEMENTATION_COMMIT_SHA>"
```

確認:

```bash
git show --stat --oneline "$IMPL_COMMIT"
git rev-parse "$IMPL_COMMIT"
```

Evidence:

```text
Implementation commit: 166e90cd1c2d0e523fb863795a88343403d8cc44
<RECORD_HERE>

$ export IMPL_COMMIT="166e90cd1c2d0e523fb863795a88343403d8cc44"

$ git show --stat --oneline "$IMPL_COMMIT"
166e90c Implement ENH-E4 G02 canonical execution claim contract
 product_migrations/versions/20260809_product_0007_enh_e4_g02_canonical_execution.py | 75 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 src/ariadne/interfaces/web_api/routers/executions.py                                |  4 +++-
 src/ariadne/interfaces/web_api/schemas/__init__.py                                  |  2 ++
 src/ariadne/interfaces/worker/execution_processor.py                                | 17 +++++++++++++++--
 src/ariadne/interfaces/worker/runner.py                                             |  5 +++--
 src/ariadne/product/application/execution_service.py                                | 12 +++++++++++-
 src/ariadne/product/domain/execution.py                                             | 20 +++++++++++++++++++-
 src/ariadne/product/persistence/orm_models.py                                       | 14 ++++++++++++++
 src/ariadne/product/persistence/repositories.py                                     | 69 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 src/ariadne/product/ports/repositories.py                                           | 12 ++++++++++--
 tests/product/test_enh_e4_g02_canonical_execution.py                                | 78 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 11 files changed, 290 insertions(+), 18 deletions(-)

$ git rev-parse "$IMPL_COMMIT"
166e90cd1c2d0e523fb863795a88343403d8cc44

```

---

# 8. PostgreSQL Command Availability

以下を確認する。

```bash
command -v initdb
command -v pg_ctl
command -v pg_isready
command -v createdb
command -v psql
```

Evidence:

```text
<RECORD_HERE>
```

---

## 8.1 versioned PostgreSQL directoryの場合

`initdb` 等がPATHにない場合:

```bash
ls /usr/lib/postgresql/*/bin/initdb
```

例:

```text
/usr/lib/postgresql/17/bin/initdb
```

その場合:

```bash
export PATH="/usr/lib/postgresql/17/bin:$PATH"
```

再確認:

```bash
command -v initdb
command -v pg_ctl
command -v pg_isready
command -v createdb
command -v psql
```

---

# 9. Detached Test Worktree作成

通常working treeを変更せずimplementation commitを固定するため、temporary Git worktreeを使用する。

```bash
cd /loc0/bigbrother/repositories/causal-atelier

export G02_TEST_WORKTREE=/tmp/causal-atelier-g02-test
```

同名worktreeが存在しないことを確認する。

```bash
git worktree list
```

既存の同名temporary worktreeが今回の作業の残骸であることを確認できる場合のみ削除する。

```bash
git worktree remove "$G02_TEST_WORKTREE"
```

または存在しなければ、そのまま作成する。

```bash
git worktree add --detach \
  "$G02_TEST_WORKTREE" \
  "$IMPL_COMMIT"
```

移動:

```bash
cd "$G02_TEST_WORKTREE"
```

確認:

```bash
git rev-parse HEAD
git status --short
```

Expected:

```text
HEAD = $IMPL_COMMIT
working tree = clean
```

Evidence:

```text
<RECORD_HERE>
```

---

# 10. Isolated PostgreSQL Directory作成

temporary root:

```bash
export G02_PG_ROOT="$(mktemp -d /tmp/ariadne-g02-pg.XXXXXX)"
export G02_PG_DATA="$G02_PG_ROOT/data"
export G02_PG_SOCKET="$G02_PG_ROOT/socket"
export G02_PG_PORT=55432

mkdir -p "$G02_PG_SOCKET"
```

確認:

```bash
printf 'G02_PG_ROOT=%s\n' "$G02_PG_ROOT"
printf 'G02_PG_DATA=%s\n' "$G02_PG_DATA"
printf 'G02_PG_SOCKET=%s\n' "$G02_PG_SOCKET"
printf 'G02_PG_PORT=%s\n' "$G02_PG_PORT"
```

Evidence:

```text
<RECORD_HERE>
```

---

# 11. Port Availability

port `55432` が使用中でないことを確認する。

```bash
ss -ltn | grep ':55432 ' || true
```

Expected:

```text
no output
```

使用中の場合は、未使用のhigh portへ変更する。

例:

```bash
export G02_PG_PORT=55433
```

以降はそのportを使用する。

---

# 12. PostgreSQL Cluster Initialization

temporary clusterを初期化する。

```bash
initdb \
  -D "$G02_PG_DATA" \
  -U ariadne \
  -A trust \
  --no-locale \
  -E UTF8
```

Expected:

```text
Success. You can now start the database server ...
```

Evidence:

```text
Exit code:
<RECORD_HERE>

Output summary:
<RECORD_HERE>
```

---

# 13. PostgreSQL Startup

localhostだけにbindする。

```bash
pg_ctl \
  -D "$G02_PG_DATA" \
  -l "$G02_PG_ROOT/postgres.log" \
  -o "-h 127.0.0.1 -p $G02_PG_PORT -k $G02_PG_SOCKET" \
  start
```

readiness確認:

```bash
pg_isready \
  -h 127.0.0.1 \
  -p "$G02_PG_PORT" \
  -U ariadne
```

Expected:

```text
accepting connections
```

Evidence:

```text
<RECORD_HERE>
```

PostgreSQL log:

```bash
tail -n 50 "$G02_PG_ROOT/postgres.log"
```

必要な場合のみ参照する。

---

# 14. Test Database Creation

database:

```text
ariadne_g02_test
```

を作成する。

```bash
createdb \
  -h 127.0.0.1 \
  -p "$G02_PG_PORT" \
  -U ariadne \
  ariadne_g02_test
```

接続確認:

```bash
psql \
  -h 127.0.0.1 \
  -p "$G02_PG_PORT" \
  -U ariadne \
  -d ariadne_g02_test \
  -c 'select current_database(), current_user, version();'
```

Evidence:

```text
<RECORD_HERE>
```

---

# 15. Ariadne Database URLs

temporary DBへのURLを作成する。

```bash
export G02_DATABASE_URL="postgresql+psycopg://ariadne@127.0.0.1:${G02_PG_PORT}/ariadne_g02_test"
```

Product migration:

```bash
export ARIADNE_PRODUCT_DATABASE_URL="$G02_DATABASE_URL"
```

Product PostgreSQL test:

```bash
export ARIADNE_PRODUCT_TEST_DATABASE_URL="$G02_DATABASE_URL"
```

確認:

```bash
printf 'ARIADNE_PRODUCT_DATABASE_URL=%s\n' \
  "$ARIADNE_PRODUCT_DATABASE_URL"

printf 'ARIADNE_PRODUCT_TEST_DATABASE_URL=%s\n' \
  "$ARIADNE_PRODUCT_TEST_DATABASE_URL"
```

Expected:

両方が今回作成したtemporary PostgreSQLを指す。

---

# 16. Product Migration Head Inspection

migration実行前にProduct migration chainを確認する。

```bash
uv run alembic \
  -c alembic_product.ini \
  heads
```

```bash
uv run alembic \
  -c alembic_product.ini \
  history
```

Evidence:

```text
Product head before upgrade:
<RECORD_HERE>
```

root legacy:

```text
alembic.ini
```

は使用しない。

---

# 17. Empty Database Product Migration

temporary empty DBへProduct migrationのみを適用する。

```bash
uv run alembic \
  -c alembic_product.ini \
  upgrade head
```

Exit code:

```text
<RECORD_HERE>
```

Output summary:

```text
<RECORD_HERE>
```

---

# 18. Migration Result Verification

current revision:

```bash
uv run alembic \
  -c alembic_product.ini \
  current
```

database tables:

```bash
psql \
  -h 127.0.0.1 \
  -p "$G02_PG_PORT" \
  -U ariadne \
  -d ariadne_g02_test \
  -c '\dt'
```

Product Alembic version:

```bash
psql \
  -h 127.0.0.1 \
  -p "$G02_PG_PORT" \
  -U ariadne \
  -d ariadne_g02_test \
  -c 'select * from alembic_version_product;'
```

Evidence:

```text
Current Product revision:
<RECORD_HERE>

Schema/table summary:
<RECORD_HERE>
```

---

# 19. PostgreSQL Test Availability Check

まずPostgreSQL marker testを実行する。

```bash
uv run pytest \
  -q \
  -m postgres \
  tests/product/test_postgres_contract.py
```

Expected:

以前の

```text
ARIADNE_PRODUCT_TEST_DATABASE_URL is not configured
```

によるskipが発生しない。

Evidence:

```text
Command:
<RECORD_HERE>

Exit code:
<RECORD_HERE>

Passed:
<RECORD_HERE>

Failed:
<RECORD_HERE>

Skipped:
<RECORD_HERE>
```

---

# 20. G02 Implementation Test Mapping

以下を開く。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/
G02/
E4-G02_01_implementation_completion_report.md
```

その中の、

```text
E4-G02-AC-002 → test path / node ID
E4-G02-AC-005 → test path / node ID
```

を確認する。

Evidence:

```text
AC-002 test nodes:
<RECORD_HERE>

AC-005 test nodes:
<RECORD_HERE>
```

Implementation Completion Reportにmigration-specific test nodeが記載されている場合、それも記録する。

---

# 21. Verification Retry Execution

## 21.1 Important Rule

ここからは、

```text
E4-G02 Trial 01
```

のverification retryである。

```text
Trial 02
```

ではない。

implementation commitを変更しない。

---

## 21.2 Test Agentへ渡す環境

Test Agentを起動するshell/processが以下を保持していることを確認する。

```bash
env | grep '^ARIADNE_PRODUCT_.*DATABASE_URL='
```

Expected:

```text
ARIADNE_PRODUCT_DATABASE_URL=postgresql+psycopg://...
ARIADNE_PRODUCT_TEST_DATABASE_URL=postgresql+psycopg://...
```

---

# 22. Verification Retry Instruction

Test Agentには以下の意味の指示を与える。

```text
E4-G02 Trial 01のverification retryを実施する。

implementation commitは初回Trial 01と同一のfull SHAに固定する。

source/test/migrationを変更してはならない。

初回結果:

PASS:
- AC-001
- AC-003
- AC-004
- relevant regression: 41 passed

BLOCKED:
- AC-002
- AC-005
- Product migration verification

今回、isolated PostgreSQLが提供されている。

ARIADNE_PRODUCT_DATABASE_URL
および
ARIADNE_PRODUCT_TEST_DATABASE_URL
はisolated PostgreSQLを指している。

最初にimplementation commitが初回Testと同一であることを検証する。

同一である場合、PostgreSQL環境不足でBLOCKEDだったTest Itemを再実行する。

最低限:

- AC-002 cross-family claim/lifecycle
- AC-005 double claim / lease ownership / invalid transition
- Product migration verification

を実行する。

既にPASSした結果を再利用する場合は、
implementation commitが不変であることを証拠として記録する。

全Acceptance Criteriaが成立した場合のみ
E4-G02 Trial 01のGate DecisionをPASSとする。

FAILの場合、sourceを修正せずFAIL evidenceを残す。

environmentによって依然判定不能な場合はBLOCKEDとする。
```

---

# 23. Evidence Preservation Policy

初回BLOCKEDのTest Reportを削除・上書きしてはならない。

既存:

```text
30_test_report/G02/
```

配下の初回evidenceを保持する。

verification retry evidenceは、初回結果と区別可能なfilenameまたは明示metadataで追加する。

推奨:

```text
E4-G02_01_retry01_002_*.md
E4-G02_01_retry01_005_*.md
E4-G02_01_retry01_007_*.md
E4-G02_01_retry01_999_gate_decision.md
```

ただし既存Test Report naming policyが別途確立済みの場合はその規約を優先する。

重要なのは、

```text
initial BLOCKED evidence
+
retry evidence
```

の両方を残すことである。

---

# 24. G02 PASS Condition

最終的に以下が成立する必要がある。

```text
E4-G02-AC-001 PASS
E4-G02-AC-002 PASS
E4-G02-AC-003 PASS
E4-G02-AC-004 PASS
E4-G02-AC-005 PASS
```

および:

```text
Product migration verification PASS
Relevant regression PASS
```

implementation defectが新たに確認された場合:

```text
E4-G02 = FAIL
```

とし、Coding Trial 02へ進む。

environmentにより依然判定不能の場合:

```text
E4-G02 = BLOCKED
```

とし、Coding Trialは進めない。

全てPASSの場合:

```text
E4-G02 = PASS
```

としてG03 contractへ進む。

---

# 25. Post-verification Record

最終Gate Decision:

```text
<RECORD_HERE>
```

Implementation commit:

```text
<RECORD_HERE>
```

PostgreSQL-dependent result:

```text
AC-002:
<RECORD_HERE>

AC-005:
<RECORD_HERE>

Migration:
<RECORD_HERE>
```

Final Test Report:

```text
<RECORD_HERE>
```

Completed at:

```text
<RECORD_HERE>
```

---

# 26. Temporary PostgreSQL Shutdown

verification終了後:

```bash
pg_ctl \
  -D "$G02_PG_DATA" \
  stop
```

確認:

```bash
pg_isready \
  -h 127.0.0.1 \
  -p "$G02_PG_PORT" \
  -U ariadne || true
```

Expected:

```text
no response
```

Evidence:

```text
<RECORD_HERE>
```

---

# 27. Temporary Worktree Removal

元Repositoryへ戻る。

```bash
cd /loc0/bigbrother/repositories/causal-atelier
```

確認:

```bash
git worktree list
```

temporary G02 worktreeを削除する。

```bash
git worktree remove "$G02_TEST_WORKTREE"
```

再確認:

```bash
git worktree list
```

---

# 28. Temporary PostgreSQL Files Removal

PostgreSQL停止確認後:

```bash
rm -rf "$G02_PG_ROOT"
```

確認:

```bash
test ! -e "$G02_PG_ROOT" && echo "temporary PostgreSQL removed"
```

---

# 29. Original Repository Safety Check

最後に元Repositoryで:

```bash
cd /loc0/bigbrother/repositories/causal-atelier

git status --short
```

本手順によってproduction source/test/migrationに新しい変更が発生していないことを確認する。

既存のunrelated working tree差分はそのままでよい。

特に既知の:

```text
deploy/.nfs000000000076202f00000088
```

等を本作業で変更・restore・stageしてはならない。

---

# 30. Completion Record

## Environment

```text
PostgreSQL binary version:
<RECORD_HERE>

Temporary port:
<RECORD_HERE>

Temporary DB:
ariadne_g02_test
```

## Git

```text
Branch:
<RECORD_HERE>

Implementation commit:
<RECORD_HERE>
```

## Migration

```text
Product migration head:
<RECORD_HERE>

Upgrade result:
<RECORD_HERE>
```

## Verification

```text
AC-002:
<RECORD_HERE>

AC-005:
<RECORD_HERE>

Migration verification:
<RECORD_HERE>

Regression evidence reused/reexecuted:
<RECORD_HERE>
```

## Gate

```text
E4-G02 final decision:
<PASS | FAIL | BLOCKED>
```

## Cleanup

```text
Temporary PostgreSQL stopped:
<YES / NO>

Temporary PostgreSQL removed:
<YES / NO>

Temporary worktree removed:
<YES / NO>

Original repository unchanged by verification:
<YES / NO>
```

---

# 31. Completion Criteria

本Supplemental procedure完了条件:

1. implementation commitを固定した。
2. isolated PostgreSQLを作成した。
3. existing development DBを使用していない。
4. Product migrationのみをisolated DBへ適用した。
5. `ARIADNE_PRODUCT_DATABASE_URL` を設定した。
6. `ARIADNE_PRODUCT_TEST_DATABASE_URL` を設定した。
7. PostgreSQL-dependent testがskipされないことを確認した。
8. AC-002を再検証した。
9. AC-005を再検証した。
10. migrationを再検証した。
11. 初回BLOCKED evidenceを保持した。
12. retry evidenceを追加した。
13. G02 Gate Decisionを更新した。
14. temporary PostgreSQLを停止・削除した。
15. temporary worktreeを削除した。
16. original repositoryへsource/test/migration変更を残していない。

---

# 32. Stop Conditions

以下の場合は作業を停止する。

## STOP — PostgreSQL unavailable

`initdb` / `pg_ctl` 等を利用できず、人間権限でisolated PostgreSQLを作成できない。

その場合:

```text
E4-G02 remains BLOCKED
```

## STOP — Implementation commit mismatch

初回Test対象implementation commitと現在対象commitが異なる。

その場合、既存PASS evidenceを再利用しない。

作業指示者へ報告する。

## STOP — Migration failure

empty isolated DBへのProduct migrationが失敗する。

これは環境問題かimplementation defectかをTest Agentに判定させる。

migrationを手動修正しない。

## STOP — Test failure

AC-002 / AC-005等でimplementation defectが確認された。

sourceを修正しない。

```text
E4-G02 = FAIL
```

としてevidenceを残す。

## STOP — Environment still insufficient

PostgreSQLを用意した後も必要なverificationを実施不能。

```text
E4-G02 = BLOCKED
```

としてevidenceを残す。
