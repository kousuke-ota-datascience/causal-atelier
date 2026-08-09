# E4-G02 Supplemental — Test PostgreSQL Container Verification Retry

## 1. 目的

本書は、`E4-G02 Trial 01` のIndependent Testにおいて、PostgreSQL実行環境不足により `BLOCKED` となった検証を再開するための**人間向け操作手順兼証跡**である。

今回のみ、Docker上にG02専用のdisposable PostgreSQL containerを起動する。

G02 PASS後、G03開始前に常設Test PostgreSQL infrastructureを別途整備し、G03以降では本手動操作を不要にする。

---

# 2. 現在の状態

初回 E4-G02 Trial 01 Test結果:

```text
PASS:
- E4-G02-AC-001
- E4-G02-AC-003
- E4-G02-AC-004
- relevant regression: 41 passed

BLOCKED:
- E4-G02-AC-002
- E4-G02-AC-005
- Product migration verification
```

BLOCKED理由:

```text
ARIADNE_PRODUCT_TEST_DATABASE_URL 未設定
Docker API permission denied
```

現時点でimplementation defectは確認されていない。

したがって、

```text
E4-G02 Trial 02
```

へは進まない。

同じimplementation commitを対象として、

```text
E4-G02 Trial 01 verification retry
```

を行う。

---

# 3. 責務分担

## Human Operator

人間が実施する。

```text
Docker確認
↓
G02専用PostgreSQL container起動
↓
PostgreSQL readiness確認
↓
DB接続環境変数設定
↓
Test Agent起動
↓
Test Agent終了後container停止
```

## Test Agent

Test Agentが実施する。

```text
implementation commit固定確認
↓
Product migration verification
↓
AC-002 verification
↓
AC-005 verification
↓
Gate Decision
```

Human Operatorはmigration、pytest、Gate判定を代行しない。

Test AgentはPostgreSQL containerの構築・削除を責務としない。

---

# 4. Repository

Repository root:

```text
/loc0/bigbrother/repositories/causal-atelier
```

Branch:

```text
refactor/ariadne_mvp_e4
```

本書:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G02_Supplemental/
02_g02_test_postgresql_container_verification_retry.md
```

Implementation Completion Report:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/
G02/
E4-G02_01_implementation_completion_report.md
```

Test evidence:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/
G02/
```

---

# 5. Safety Rules

以下を厳守する。

1. 開発用PostgreSQL databaseを使用しない。
2. G02専用test containerを使用する。
3. 開発用port `5432` を使用しない。
4. G02 test containerは `127.0.0.1:55432` を使用する。
5. persistent volumeを付けない。
6. root legacy migrationを使用しない。
7. source/test/migrationを変更しない。
8. implementation commitを変更しない。
9. 初回BLOCKED evidenceを削除・上書きしない。
10. Test Agent終了後、G02専用containerを削除する。

---

# 6. Step H01 — 作業開始証跡

Repository rootへ移動する。

```bash
cd /loc0/bigbrother/repositories/causal-atelier
```

日時:

```bash
date --iso-8601=seconds
```

Git状態:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
```

## Evidence

```text
Executed at:
2026-08-09T01:18:21+00:00

Branch:
refactor/ariadne_mvp_e4

HEAD:
ab414bba01916f6e86db723c63363fc7cd7864bc

git status --short:
 D deploy/.nfs000000000076202f00000088
?? docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/G02_Supplemental/
```

Expected branch:

```text
refactor/ariadne_mvp_e4
```

既存のunrelated working-tree差分が存在しても、本作業では変更しない。

特に既知の:

```text
deploy/.nfs000000000076202f00000088
```

をstage / restore / recreateしてはならない。

---

# 7. Step H02 — Docker利用可能性確認

実行:

```bash
docker info >/dev/null && echo "Docker OK"
docker ps
```

## Expected

```text
Docker OK
```

が表示され、`docker ps` がpermission errorなく終了する。

## Evidence

```text
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker info >/dev/null && echo "Docker OK"
Docker OK
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker ps
CONTAINER ID   IMAGE                COMMAND                  CREATED        STATUS                  PORTS                       NAMES
c13e8ed52c38   nginx:1.27-alpine    "/docker-entrypoint.…"   18 hours ago   Up 18 hours             127.0.0.1:18080->80/tcp     ariadne-e1a-frontend-1
dc225749a393   ariadne-e1a-api      "uvicorn ariadne.int…"   18 hours ago   Up 18 hours (healthy)   127.0.0.1:18000->8000/tcp   ariadne-e1a-api-1
556c6c87ddaa   ariadne-e1a-worker   "ariadne-worker"         18 hours ago   Up 18 hours             8000/tcp                    ariadne-e1a-worker-1
33bde72e228c   postgres:17-alpine   "docker-entrypoint.s…"   18 hours ago   Up 18 hours (healthy)   127.0.0.1:15432->5432/tcp   ariadne-e1a-database-1
```

## STOP

以下の場合は停止する。

```text
permission denied
Cannot connect to the Docker daemon
```

Test Agentを起動しない。

```text
E4-G02 remains BLOCKED
```

とする。

---

# 8. Step H03 — 既存G02 Test Container確認

同名containerが残っていないことを確認する。

```bash
docker ps -a \
  --filter name='^/ariadne-g02-postgres$'
```

## Expected

通常は該当containerなし。

前回失敗したG02 verificationのcontainerであることが明確な場合だけ削除してよい。

```bash
docker rm -f ariadne-g02-postgres
```

他のPostgreSQL containerを削除してはならない。

## Evidence

```text
Existing ariadne-g02-postgres:

bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker ps -a \
  --filter name='^/ariadne-g02-postgres$'
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

---

# 9. Step H04 — G02 Test PostgreSQL起動

以下を実行する。

```bash
docker run --rm \
  --name ariadne-g02-postgres \
  -e POSTGRES_DB=ariadne_g02_test \
  -e POSTGRES_USER=ariadne \
  -e POSTGRES_PASSWORD=ariadne \
  -p 127.0.0.1:55432:5432 \
  -d postgres:17-alpine
```

## Evidence

```text
Container ID:
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker run --rm \
  --name ariadne-g02-postgres \
  -e POSTGRES_DB=ariadne_g02_test \
  -e POSTGRES_USER=ariadne \
  -e POSTGRES_PASSWORD=ariadne \
  -p 127.0.0.1:55432:5432 \
  -d postgres:17-alpine
143b2311333e68ad23d0cb89cd7e9af6d0e734eb3b5cacff723db9d462665b2e

```

起動状態:

```bash
docker ps \
  --filter name='^/ariadne-g02-postgres$'
```

## Evidence

```text
docker ps:
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker ps \
  --filter name='^/ariadne-g02-postgres$'
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS          PORTS                       NAMES
143b2311333e   postgres:17-alpine   "docker-entrypoint.s…"   43 seconds ago   Up 42 seconds   127.0.0.1:55432->5432/tcp   ariadne-g02-postgres

```

---

# 10. Step H05 — PostgreSQL Readiness確認

実行:

```bash
docker exec ariadne-g02-postgres \
  pg_isready \
  -U ariadne \
  -d ariadne_g02_test
```

## Expected

以下相当:

```text
/var/run/postgresql:5432 - accepting connections
```

## Evidence

```text
pg_isready:
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker exec ariadne-g02-postgres \
  pg_isready \
  -U ariadne \
  -d ariadne_g02_test
/var/run/postgresql:5432 - accepting connections

```

readyでない場合は数秒後に再確認してよい。

繰り返しreadyにならない場合:

```bash
docker logs ariadne-g02-postgres
```

を確認し、本書へ証跡を記録する。

container内部を手動修正して続行してはならない。

---

# 11. Step H06 — Host Port確認

G02 test PostgreSQLが `127.0.0.1:55432` にのみ公開されていることを確認する。

```bash
docker port ariadne-g02-postgres
```

Expected:

```text
5432/tcp -> 127.0.0.1:55432
```

## Evidence

```text
docker port:
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ docker port ariadne-g02-postgres
5432/tcp -> 127.0.0.1:55432
```

開発用 `5432` と混同しない。

---

# 12. Step H07 — Test用DB URL設定

**Test Agentを起動するのと同じshell**で実行する。

```bash
export ARIADNE_PRODUCT_DATABASE_URL='postgresql+psycopg://ariadne:ariadne@127.0.0.1:55432/ariadne_g02_test'

export ARIADNE_PRODUCT_TEST_DATABASE_URL="$ARIADNE_PRODUCT_DATABASE_URL"
```

確認:

```bash
env | grep '^ARIADNE_PRODUCT_.*DATABASE_URL='
```

## Expected

以下2変数が存在する。

```text
ARIADNE_PRODUCT_DATABASE_URL
ARIADNE_PRODUCT_TEST_DATABASE_URL
```

両方とも:

```text
127.0.0.1:55432/ariadne_g02_test
```

を指す。

## Evidence

```text
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ env | grep '^ARIADNE_PRODUCT_.*DATABASE_URL='
ARIADNE_PRODUCT_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@127.0.0.1:55432/ariadne_g02_test
ARIADNE_PRODUCT_TEST_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@127.0.0.1:55432/ariadne_g02_test
```

---

# 13. Step H08 — Test Agent起動

ここから先のmigration/test/Gate判定は人間が実施しない。

Test Agentへ以下の指示を渡す。

```text
E4-G02 Trial 01 の verification retry を実施せよ。

これは Coding Trial 02 ではない。
初回 E4-G02 Trial 01 と同一 implementation commit を
検証対象とすること。

対象 Implementation Completion Report:

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/
G02/
E4-G02_01_implementation_completion_report.md

初回Test結果:

PASS:
- E4-G02-AC-001
- E4-G02-AC-003
- E4-G02-AC-004
- relevant regression: 41 passed

BLOCKED:
- E4-G02-AC-002
- E4-G02-AC-005
- Product migration verification

初回BLOCKED理由はPostgreSQL実環境不足であり、
implementation defectは確認されていない。

今回はHuman Operatorによりisolated PostgreSQLが準備済みである。

以下の環境変数がTest Agent processから利用できることを確認せよ。

- ARIADNE_PRODUCT_DATABASE_URL
- ARIADNE_PRODUCT_TEST_DATABASE_URL

最初にImplementation Completion Reportから
implementation commitのfull SHAを取得し、
初回Test対象と同じimplementation commitを
検証していることを確認すること。

source / automated test / migration / dependencyを変更してはならない。

PostgreSQL環境不足でBLOCKEDだった項目を再検証する。

最低限:

1. Product migration verification
2. E4-G02-AC-002 cross-family claim/lifecycle verification
3. E4-G02-AC-005 double claim / lease ownership /
   invalid transition verification

初回PASS evidenceを再利用する場合は、
implementation commitが不変であることを
evidenceとして明記すること。

初回BLOCKED evidenceを削除・上書きしてはならない。

verification retry evidenceは:

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/
G02/

配下へ追加すること。

全Acceptance Criteriaが成立した場合のみ:

E4-G02 = PASS

と判定する。

implementation defectを検出した場合:

E4-G02 = FAIL

とし、sourceを修正せずevidenceを残すこと。

環境上依然判定不能な場合:

E4-G02 = BLOCKED

とすること。

Gate Decision作成後、G03には進まず停止せよ。
```

---

# 14. Step H09 — Test Agent実行中の禁止事項

Test Agent実行中、人間は以下を行わない。

* test DBへの手動migration
* test tableの手動作成
* SQLによるtest failure回避
* source code変更
* test code変更
* migration変更
* database schema手動補正
* container restartによるtest result隠蔽

Test Agentからenvironment issueが報告された場合は、その内容を確認してから対応する。

implementation failureを人間がenvironment側で補正してはならない。

---

# 15. Step H10 — Test Agent結果記録

Test Agent終了後、結果を記録する。

```text
Test Agent completed at:
<RECORD_HERE>

Implementation commit:
<RECORD_HERE>

AC-001:
<PASS / FAIL / BLOCKED>

AC-002:
<PASS / FAIL / BLOCKED>

AC-003:
<PASS / FAIL / BLOCKED>

AC-004:
<PASS / FAIL / BLOCKED>

AC-005:
<PASS / FAIL / BLOCKED>

Product migration verification:
<PASS / FAIL / BLOCKED>

Relevant regression:
<PASS / FAIL / BLOCKED>

Final Gate Decision:
<PASS / FAIL / BLOCKED>
```

Gate Decision evidence:

```text
<RECORD_TEST_REPORT_PATH_HERE>
```

---

# 16. Gate Decision Interpretation

## PASS

以下が成立した場合:

```text
AC-001 PASS
AC-002 PASS
AC-003 PASS
AC-004 PASS
AC-005 PASS
Product migration verification PASS
Relevant regression PASS
```

最終:

```text
E4-G02 = PASS
```

次工程:

```text
G03開始前
→ Test PostgreSQL infrastructure標準化
→ G03 contract authoring
```

---

## FAIL

PostgreSQL実環境でimplementation defectが確認された場合:

```text
E4-G02 = FAIL
```

次工程:

```text
E4-G02 Coding Trial 02
```

Human Operatorがsourceを修正してはならない。

---

## BLOCKED

isolated PostgreSQLを提供しても、environment/infrastructure上の理由で判定不能の場合:

```text
E4-G02 = BLOCKED
```

Coding Trial 02へ進まない。

---

# 17. Step H11 — Test PostgreSQL停止

Test Agentが完全に終了した後、人間が実行する。

```bash
docker stop ariadne-g02-postgres
```

`--rm` で起動しているため、stop後containerは自動削除される。

確認:

```bash
docker ps -a \
  --filter name='^/ariadne-g02-postgres$'
```

## Expected

該当containerなし。

## Evidence

```text
docker stop:
<RECORD_HERE>

Container remaining after stop:
<YES / NO>
```

Expected:

```text
NO
```

---

# 18. Step H12 — 開発DBが無変更であることを確認

G02専用containerが削除され、通常開発用database containerへ操作していないことを確認する。

必要に応じて:

```bash
docker ps
```

を確認する。

本作業では開発用PostgreSQL databaseにmigration/testを書き込んでいないこと。

Evidence:

```text
Development database touched by this procedure:
NO
```

---

# 19. Step H13 — Repository Safety Check

Repository rootへ戻る。

```bash
cd /loc0/bigbrother/repositories/causal-atelier
```

実行:

```bash
git status --short
```

本verification retryによってproduction source/test/migration差分が追加されていないことを確認する。

Test Agentが生成した認可済みtest evidenceは存在してよい。

既存unrelated差分はそのままでよい。

## Evidence

```text
git status --short:
<RECORD_HERE>
```

---

# 20. Completion Record

## Human Environment Provisioning

```text
Docker available:
<YES / NO>

Test container:
ariadne-g02-postgres

PostgreSQL image:
postgres:17-alpine

Database:
ariadne_g02_test

Host endpoint:
127.0.0.1:55432

PostgreSQL ready:
<YES / NO>
```

## Verification

```text
Implementation commit unchanged:
<YES / NO>

AC-002 verification completed:
<YES / NO>

AC-005 verification completed:
<YES / NO>

Product migration verification completed:
<YES / NO>
```

## Gate

```text
E4-G02 final decision:
<PASS / FAIL / BLOCKED>
```

## Cleanup

```text
Test Agent stopped:
<YES / NO>

Test PostgreSQL stopped:
<YES / NO>

Test PostgreSQL container removed:
<YES / NO>

Development database untouched:
<YES / NO>

Production source/test/migration unchanged:
<YES / NO>
```

---

# 21. Completion Criteria

本Supplemental operationは以下を全て満たした場合に完了とする。

1. DockerがHuman Operatorから利用可能。
2. G02専用PostgreSQL containerを起動。
3. `postgres:17-alpine` を使用。
4. `ariadne_g02_test` databaseを使用。
5. `127.0.0.1:55432` のみを使用。
6. 開発用databaseを使用していない。
7. `ARIADNE_PRODUCT_DATABASE_URL` 設定済み。
8. `ARIADNE_PRODUCT_TEST_DATABASE_URL` 設定済み。
9. Test Agentへ同一Trial 01 verification retryとしてhandoff。
10. implementation commit固定確認済み。
11. migration verification実施済み。
12. AC-002再検証済み。
13. AC-005再検証済み。
14. Gate Decision記録済み。
15. 初回BLOCKED evidenceを保持。
16. verification retry evidenceを追加。
17. Test終了後containerを停止。
18. containerを削除。
19. 開発DBを変更していない。
20. production source/test/migrationを変更していない。

---

# 22. G03以降への申し送り

本Docker container手順はG02を完了させるためのtemporary Supplemental operationである。

G02 PASS後、G03開始前に以下を標準化する。

```text
persistent Test PostgreSQL service
+
stable Test DB URL
+
automated test DB reset
+
Product migration initialization
```

目標:

```text
G03〜G08では
Human Operatorによる毎回のdocker runを不要にする。
```

その標準化作業はG02 implementation scopeには含めない。
