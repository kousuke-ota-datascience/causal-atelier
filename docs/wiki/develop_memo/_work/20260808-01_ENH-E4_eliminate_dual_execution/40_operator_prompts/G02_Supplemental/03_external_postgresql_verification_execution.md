# E4-G02 Supplemental — External PostgreSQL Verification Execution

## 1. 目的

本書は、`E4-G02 Trial 01` のIndependent Testにおいて、Test Agent固有のnetwork isolationにより直接実行できなかったPostgreSQL-dependent verificationを、Human Operatorが**同一implementation commit上で外部実行し、そのraw execution evidenceをTest Agentへ引き渡す**ための手順兼証跡である。

本作業はCoding Trialではない。

```text
E4-G02 Trial 01
        ↓
Test AgentからPostgreSQLへ到達不能
        ↓
Human Operatorが同一test commandを外部実行
        ↓
raw evidence保存
        ↓
Test Agentがevidenceを独立監査
        ↓
Gate Decision
```

Human OperatorはAcceptance CriteriaのPASS/FAILを判定しない。

---

# 2. 現在の判定

現在:

```text
E4-G02 Trial 01 = BLOCKED
```

既存evidence:

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

implementation defectは現時点で確定していない。

PostgreSQL verificationが実行できなかった理由は、Test Agent execution environmentからPostgreSQL sessionを確立できなかったためである。

---

# 3. Network切り分け済み事項

Human Operator環境では以下を確認済み。

```text
Docker PostgreSQL container:
RUNNING

PostgreSQL pg_isready:
PASS

Host TCP → 172.17.0.1:55432:
PASS

Host SQLAlchemy/psycopg → PostgreSQL:
PASS

別Docker container psql → PostgreSQL:
PASS

Test Agent → PostgreSQL:
FAIL
```

したがって本手順ではPostgreSQL container自体を再設計しない。

Human OperatorがDBへ接続可能なhost execution environmentからverification commandを実行する。

---

# 4. Fixed Verification Target

Implementation commit:

```text
166e90cd1c2d0e523fb863795a88343403d8cc44
```

Expected Product migration head:

```text
20260809_product_0007
```

対象branch:

```text
refactor/ariadne_mvp_e4
```

対象Gate / Trial:

```text
E4-G02 / Trial 01
```

これはverification retryであり、

```text
Trial 02
```

ではない。

implementation commitを変更してはならない。

---

# 5. Responsibility Boundary

## Human Operator

Human Operatorが実施する。

```text
fixed implementation worktree準備
↓
PostgreSQL connection preflight
↓
Product migration command実行
↓
PostgreSQL pytest実行
↓
targeted G02 pytest実行
↓
raw stdout/stderr + exit code保存
↓
repository safety確認
↓
Test Agentへevidence handoff
```

Human Operatorは以下を行わない。

* PASS/FAIL判定
* source修正
* test修正
* migration修正
* DB schema手動補正
* expected result書換え
* failing data削除によるテスト回避

---

## Test Agent

Test AgentはHuman Operatorが保存したraw evidenceを独立監査する。

Test Agentは、

* implementation commit一致
* command妥当性
* migration result
* pytest result
* assertions実行結果
* exit code
* source/test/migration不変性

を確認したうえで、

```text
PASS
FAIL
BLOCKED
```

を判定する。

---

# 6. Repository Paths

Repository root:

```text
/loc0/bigbrother/repositories/causal-atelier
```

本書:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G02_Supplemental/
03_external_postgresql_verification_execution.md
```

raw evidence directory:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G02_Supplemental/
03_external_postgresql_verification_execution_evidence/
```

Implementation Completion Report:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/
G02/
E4-G02_01_implementation_completion_report.md
```

Test reports:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/
G02/
```

---

# 7. Safety Rules

以下を厳守する。

1. implementation commitを固定する。
2. verification専用detached worktreeを使用する。
3. Product sourceを変更しない。
4. automated testを変更しない。
5. Product migrationを変更しない。
6. dependencyを変更しない。
7. 開発用PostgreSQLを使用しない。
8. G02専用isolated PostgreSQLだけを使用する。
9. root legacy migrationを実行しない。
10. raw logを加工してPASSに見せない。
11. failed commandもそのまま保存する。
12. 初回BLOCKED evidenceを削除しない。
13. Test AgentのGate DecisionをHuman Operatorが代行しない。

---

# 8. Expected PostgreSQL Environment

現在のG02 verification PostgreSQL:

```text
Container:
ariadne-g02-postgres

Image:
postgres:17-alpine

Database:
ariadne_g02_test

Host gateway:
172.17.0.1

Published port:
55432

Container port:
5432
```

Expected environment variables:

```text
ARIADNE_PRODUCT_DATABASE_URL
ARIADNE_PRODUCT_TEST_DATABASE_URL
```

Expected DSN:

```text
postgresql+psycopg://ariadne:********@172.17.0.1:55432/ariadne_g02_test
```

本書の証跡にはpasswordを再掲する必要はない。

---

# 9. Step H01 — Original Repository Pre-flight

実行:

```bash
cd /loc0/bigbrother/repositories/causal-atelier

date --iso-8601=seconds; \
git branch --show-current; \
git rev-parse HEAD; \
git status --short; \
```

## Evidence

```text
Executed at:
<RECORD_HERE>

Branch:
<RECORD_HERE>

Original repository HEAD:
<RECORD_HERE>

Original git status:
<RECORD_HERE>

-----

bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ date --iso-8601=seconds; \
git branch --show-current; \
git rev-parse HEAD; \
git status --short; \
2026-08-09T02:16:11+00:00
refactor/ariadne_mvp_e4
578662992c86792d71062dea1b974f7e64614f7c
 D deploy/.nfs000000000076202f00000088
?? docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/30_test_report/G02/E4-G02_01_retry_005_preflight_tcp_and_protocol.md
?? docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/30_test_report/G02/E4-G02_01_retry_999b_gate_decision.md
?? docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/G02_Supplemental/03_external_postgresql_verification_execution.md

```

既存working-tree差分を変更しない。

特に既知のunrelated差分が存在する場合、そのまま保持する。

---

# 10. Step H02 — Evidence Directory作成

original repository上にevidence directoryを作成する。

```bash
export REPO_ROOT=/loc0/bigbrother/repositories/causal-atelier

export EVIDENCE_DIR="$REPO_ROOT/docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/G02_Supplemental/03_external_postgresql_verification_execution_evidence"

mkdir -p "$EVIDENCE_DIR"
```

確認:

```bash
printf '%s\n' "$EVIDENCE_DIR"
```

Evidence: 
```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ printf '%s\n' "$EVIDENCE_DIR"
/loc0/bigbrother/repositories/causal-atelier/docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/G02_Supplemental/03_external_postgresql_verification_execution_evidence
```


---

# 11. Step H03 — Implementation Commit固定

設定:

```bash
export IMPL_COMMIT=166e90cd1c2d0e523fb863795a88343403d8cc44
```

確認:

```bash
cd "$REPO_ROOT"

git show --no-patch --format=fuller "$IMPL_COMMIT"
```

証跡保存:

```bash
git show --no-patch --format=fuller "$IMPL_COMMIT" \
  2>&1 | tee "$EVIDENCE_DIR/00_implementation_commit.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/00_implementation_commit.log"
```

Expected:

```text
commit = 166e90cd1c2d0e523fb863795a88343403d8cc44
```

---

# 12. Step H04 — Detached Verification Worktree作成

一意なtemporary pathを作る。

```bash
export G02_VERIFY_WORKTREE="/tmp/causal-atelier-g02-ext-verify-$(date +%Y%m%d%H%M%S)"
```

作成:

```bash
cd "$REPO_ROOT"

git worktree add \
  --detach \
  "$G02_VERIFY_WORKTREE" \
  "$IMPL_COMMIT"
```

移動:

```bash
cd "$G02_VERIFY_WORKTREE"
```

確認:

```bash
{
  echo "WORKTREE=$G02_VERIFY_WORKTREE"
  git rev-parse HEAD
  git status --short
} 2>&1 | tee "$EVIDENCE_DIR/01_worktree_before.log"
```

Expected:

```text
HEAD:
166e90cd1c2d0e523fb863795a88343403d8cc44

git status:
clean
```

worktreeがcleanでない場合は停止する。

Evidence: 
```
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ git show --no-patch --format=fuller "$IMPL_COMMIT" \
  2>&1 | tee "$EVIDENCE_DIR/00_implementation_commit.log"
commit 166e90cd1c2d0e523fb863795a88343403d8cc44
Author:     kousuke-ota-datascience <kousuke.ota.datascience@gmail.com>
AuthorDate: Sun Aug 9 00:18:18 2026 +0000
Commit:     kousuke-ota-datascience <kousuke.ota.datascience@gmail.com>
CommitDate: Sun Aug 9 00:18:18 2026 +0000

    Implement ENH-E4 G02 canonical execution claim contract
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/00_implementation_commit.log"
EXIT_CODE=0
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ export G02_VERIFY_WORKTREE="/tmp/causal-atelier-g02-ext-verify-$(date +%Y%m%d%H%M%S)"
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ cd "$REPO_ROOT"
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ git worktree add \
  --detach \
  "$G02_VERIFY_WORKTREE" \
  "$IMPL_COMMIT"
Preparing worktree (detached HEAD 166e90c)
HEAD is now at 166e90c Implement ENH-E4 G02 canonical execution claim contract
bigbrother@mandam:/loc0/bigbrother/repositories/causal-atelier$ cd "$G02_VERIFY_WORKTREE"
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ {
  echo "WORKTREE=$G02_VERIFY_WORKTREE"
  git rev-parse HEAD
  git status --short
} 2>&1 | tee "$EVIDENCE_DIR/01_worktree_before.log"
WORKTREE=/tmp/causal-atelier-g02-ext-verify-20260809021919
166e90cd1c2d0e523fb863795a88343403d8cc44
```

---

# 13. Step H05 — PostgreSQL Environment確認

同じshellに以下が設定されていること。

```bash
env | grep '^ARIADNE_PRODUCT_.*DATABASE_URL='
```

値そのものをraw evidenceへ保存する必要はない。

代わりにsanitized情報を保存する。

```bash
uv run python - <<'PY' \
  2>&1 | tee "$EVIDENCE_DIR/02_database_environment.log"
import os
from sqlalchemy.engine import make_url

for key in (
    "ARIADNE_PRODUCT_DATABASE_URL",
    "ARIADNE_PRODUCT_TEST_DATABASE_URL",
):
    value = os.environ.get(key)
    print(f"{key}_SET={bool(value)}")
    if value:
        url = make_url(value)
        print(f"{key}_DRIVER={url.drivername}")
        print(f"{key}_HOST={url.host}")
        print(f"{key}_PORT={url.port}")
        print(f"{key}_DATABASE={url.database}")
PY

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/02_database_environment.log"
```

Expected:

```text
HOST=172.17.0.1
PORT=55432
DATABASE=ariadne_g02_test
```

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ env | grep '^ARIADNE_PRODUCT_.*DATABASE_URL='
ARIADNE_PRODUCT_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@172.17.0.1:55432/ariadne_g02_test
ARIADNE_PRODUCT_TEST_DATABASE_URL=postgresql+psycopg://ariadne:ariadne@172.17.0.1:55432/ariadne_g02_test
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run python - <<'PY' \
  2>&1 | tee "$EVIDENCE_DIR/02_database_environment.log"
import os
from sqlalchemy.engine import make_url

for key in (
    "ARIADNE_PRODUCT_DATABASE_URL",
    "ARIADNE_PRODUCT_TEST_DATABASE_URL",
):
    value = os.environ.get(key)
    print(f"{key}_SET={bool(value)}")
    if value:
        url = make_url(value)
        print(f"{key}_DRIVER={url.drivername}")
        print(f"{key}_HOST={url.host}")
        print(f"{key}_PORT={url.port}")
        print(f"{key}_DATABASE={url.database}")
PY
Using CPython 3.12.3 interpreter at: /usr/bin/python3.12
Creating virtual environment at: .venv
   Building ariadne @ file:///tmp/causal-atelier-g02-ext-verify-20260809021919
Downloading playwright (45.5MiB)
      Built ariadne @ file:///tmp/causal-atelier-g02-ext-verify-20260809021919
 Downloaded playwright
Installed 117 packages in 916ms
ARIADNE_PRODUCT_DATABASE_URL_SET=True
ARIADNE_PRODUCT_DATABASE_URL_DRIVER=postgresql+psycopg
ARIADNE_PRODUCT_DATABASE_URL_HOST=172.17.0.1
ARIADNE_PRODUCT_DATABASE_URL_PORT=55432
ARIADNE_PRODUCT_DATABASE_URL_DATABASE=ariadne_g02_test
ARIADNE_PRODUCT_TEST_DATABASE_URL_SET=True
ARIADNE_PRODUCT_TEST_DATABASE_URL_DRIVER=postgresql+psycopg
ARIADNE_PRODUCT_TEST_DATABASE_URL_HOST=172.17.0.1
ARIADNE_PRODUCT_TEST_DATABASE_URL_PORT=55432
ARIADNE_PRODUCT_TEST_DATABASE_URL_DATABASE=ariadne_g02_test
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/02_database_environment.log"
EXIT_CODE=0
```

---

# 14. Step H06 — SQLAlchemy PostgreSQL Preflight

Human execution environmentから、実際のPostgreSQL sessionを確立する。

```bash
uv run python - <<'PY' \
  2>&1 | tee "$EVIDENCE_DIR/03_sqlalchemy_preflight.log"
import os
from sqlalchemy import create_engine, text

url = os.environ["ARIADNE_PRODUCT_TEST_DATABASE_URL"]

engine = create_engine(url, pool_pre_ping=True)

with engine.connect() as connection:
    row = connection.execute(
        text(
            "select current_database(), "
            "current_user, "
            "current_setting('server_version')"
        )
    ).one()

    print("current_database=", row[0])
    print("current_user=", row[1])
    print("server_version=", row[2])

engine.dispose()

print("SQLALCHEMY_POSTGRESQL_PREFLIGHT=PASS")
PY

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/03_sqlalchemy_preflight.log"
```

Expected:

```text
current_database = ariadne_g02_test
current_user = ariadne
SQLALCHEMY_POSTGRESQL_PREFLIGHT=PASS
EXIT_CODE=0
```

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run python - <<'PY' \
  2>&1 | tee "$EVIDENCE_DIR/03_sqlalchemy_preflight.log"
import os
from sqlalchemy import create_engine, text

url = os.environ["ARIADNE_PRODUCT_TEST_DATABASE_URL"]

engine = create_engine(url, pool_pre_ping=True)

with engine.connect() as connection:
    row = connection.execute(
        text(
            "select current_database(), "
            "current_user, "
            "current_setting('server_version')"
        )
    ).one()

    print("current_database=", row[0])
    print("current_user=", row[1])
    print("server_version=", row[2])

engine.dispose()

print("SQLALCHEMY_POSTGRESQL_PREFLIGHT=PASS")
PY
current_database= ariadne_g02_test
current_user= ariadne
server_version= 17.10
SQLALCHEMY_POSTGRESQL_PREFLIGHT=PASS
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/03_sqlalchemy_preflight.log"
EXIT_CODE=0
```

## STOP

このpreflightが失敗した場合、migration / pytestを実行しない。

```text
External verification = BLOCKED
```

としてTest Agentへevidenceを渡す。

---

# 15. Step H07 — Product Migration Head確認

実行:

```bash
uv run alembic \
  -c alembic_product.ini \
  heads \
  2>&1 | tee "$EVIDENCE_DIR/04_alembic_heads.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/04_alembic_heads.log"
```

Expected head:

```text
20260809_product_0007
```

Human Operatorはheadが異なる場合にmigrationを修正しない。

そのままevidenceを保存する。

Evidence: 

```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run alembic \
  -c alembic_product.ini \
  heads \
  2>&1 | tee "$EVIDENCE_DIR/04_alembic_heads.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/04_alembic_heads.log"
20260809_product_0007 (head)
EXIT_CODE=0
```

---

# 16. Step H08 — Empty DB Current State確認

G02 test containerはdisposable environmentである。

migration適用前状態を記録する。

```bash
uv run alembic \
  -c alembic_product.ini \
  current \
  2>&1 | tee "$EVIDENCE_DIR/05_alembic_current_before.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/05_alembic_current_before.log"
```

empty DBの場合、まだProduct revisionが適用されていなくてよい。

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run alembic \
  -c alembic_product.ini \
  current \
  2>&1 | tee "$EVIDENCE_DIR/05_alembic_current_before.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/05_alembic_current_before.log"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
EXIT_CODE=0
```

---

# 17. Step H09 — Product Migration Upgrade

実行:

```bash
uv run alembic \
  -c alembic_product.ini \
  upgrade head \
  2>&1 | tee "$EVIDENCE_DIR/06_alembic_upgrade_head.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/06_alembic_upgrade_head.log"
```

Human Operatorはexit codeを解釈して修正しない。

`EXIT_CODE != 0` の場合もraw logを保持する。

migration failure時はPostgreSQL-dependent pytestを無理に続行しない。

Test Agentへmigration failure evidenceを渡す。

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run alembic \
  -c alembic_product.ini \
  upgrade head \
  2>&1 | tee "$EVIDENCE_DIR/06_alembic_upgrade_head.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/06_alembic_upgrade_head.log"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 20260805_product_0001, 20260805_0001_product_domain_baseline
INFO  [alembic.runtime.migration] Running upgrade 20260805_product_0001 -> 20260806_product_0002, ENH-E1 scientific validity foundation.
INFO  [alembic.runtime.migration] Running upgrade 20260806_product_0002 -> 20260806_product_0003, ENH-E2 outcome inheritance for Graph Version.
INFO  [alembic.runtime.migration] Running upgrade 20260806_product_0003 -> 20260807_product_0004, ENH-E3 generic workspace and exploratory persistence.
INFO  [alembic.runtime.migration] Running upgrade 20260807_product_0004 -> 20260807_product_0005, ENH-E3 G4 Research Context, Analysis Specification, and predictive references.
INFO  [alembic.runtime.migration] Running upgrade 20260807_product_0005 -> 20260807_product_0006, ENH-E3 G6 workspace closure, annotations, access, and export bundles.
INFO  [alembic.runtime.migration] Running upgrade 20260807_product_0006 -> 20260809_product_0007, ENH-E4 G02 canonical Execution discriminator and lease contract.
EXIT_CODE=0
```

---

# 18. Step H10 — Product Migration Current確認

upgradeが成功した場合:

```bash
uv run alembic \
  -c alembic_product.ini \
  current \
  2>&1 | tee "$EVIDENCE_DIR/07_alembic_current_after.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/07_alembic_current_after.log"
```

Expected:

```text
20260809_product_0007
```

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run alembic \
  -c alembic_product.ini \
  current \
  2>&1 | tee "$EVIDENCE_DIR/07_alembic_current_after.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/07_alembic_current_after.log"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
20260809_product_0007 (head)
EXIT_CODE=0
```

---

# 19. Step H11 — Product Migration Table確認

Product version tableをread-only確認する。

```bash
uv run python - <<'PY' \
  2>&1 | tee "$EVIDENCE_DIR/08_product_migration_revision.log"
import os
from sqlalchemy import create_engine, text

engine = create_engine(
    os.environ["ARIADNE_PRODUCT_TEST_DATABASE_URL"],
    pool_pre_ping=True,
)

with engine.connect() as connection:
    rows = connection.execute(
        text("select version_num from alembic_version_product")
    ).all()

    print("alembic_version_product=", rows)

engine.dispose()
PY

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/08_product_migration_revision.log"
```

Human Operatorは値を書き換えない。

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run python - <<'PY' \
  2>&1 | tee "$EVIDENCE_DIR/08_product_migration_revision.log"
import os
from sqlalchemy import create_engine, text

engine = create_engine(
    os.environ["ARIADNE_PRODUCT_TEST_DATABASE_URL"],
    pool_pre_ping=True,
)

with engine.connect() as connection:
    rows = connection.execute(
        text("select version_num from alembic_version_product")
    ).all()

    print("alembic_version_product=", rows)

engine.dispose()
PY

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/08_product_migration_revision.log"
alembic_version_product= [('20260809_product_0007',)]
EXIT_CODE=0
```

---

# 20. Step H12 — Real PostgreSQL Contract Suite

G02 verificationでBLOCKEDしていたreal PostgreSQL contract suiteを実行する。

対象:

```text
tests/product/test_postgres_contract.py
```

実行:

```bash
uv run pytest \
  -q \
  -m postgres \
  tests/product/test_postgres_contract.py \
  2>&1 | tee "$EVIDENCE_DIR/09_postgres_contract_pytest.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/09_postgres_contract_pytest.log"
```

このtest fileには最低限、

```text
product migration/schema contract
transaction / constraint contract
legacy/current Product compatibility contract
concurrent claim atomicity contract
```

のPostgreSQL verificationが含まれる。

Human Operatorは失敗したtestをskipしない。

失敗した場合はそのままraw evidenceとして保存する。

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run pytest \
  -q \
  -m postgres \
  tests/product/test_postgres_contract.py \
  2>&1 | tee "$EVIDENCE_DIR/09_postgres_contract_pytest.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/09_postgres_contract_pytest.log"
....                                                                     [100%]
4 passed in 0.85s
EXIT_CODE=0
```

---

# 21. Step H13 — Concurrent Claim Test単体 Evidence

AC-005にとって重要なconcurrent claim assertionを単体でも記録する。

実行:

```bash
uv run pytest \
  -q \
  tests/product/test_postgres_contract.py::test_claim_next_is_atomic_across_concurrent_workers \
  2>&1 | tee "$EVIDENCE_DIR/10_atomic_claim_pytest.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/10_atomic_claim_pytest.log"
```

このtestでは二つのworkerが同一QUEUED Executionをclaimし、成功claimが一件だけであることをassertする。

Human Operatorはassertion結果を解釈・補正しない。

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run pytest \
  -q \
  tests/product/test_postgres_contract.py::test_claim_next_is_atomic_across_concurrent_workers \
  2>&1 | tee "$EVIDENCE_DIR/10_atomic_claim_pytest.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/10_atomic_claim_pytest.log"
.                                                                        [100%]
1 passed in 0.69s
EXIT_CODE=0
```
---

# 22. Step H14 — G02 Targeted Domain Contract

implementation reportでG02へ追加されたtargeted testを実行する。

対象:

```text
tests/product/test_enh_e4_g02_canonical_execution.py
```

全体:

```bash
uv run pytest \
  -q \
  tests/product/test_enh_e4_g02_canonical_execution.py \
  2>&1 | tee "$EVIDENCE_DIR/11_g02_targeted_contract.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/11_g02_targeted_contract.log"
```

Evidence: 

```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run pytest \
  -q \
  tests/product/test_enh_e4_g02_canonical_execution.py \
  2>&1 | tee "$EVIDENCE_DIR/11_g02_targeted_contract.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/11_g02_targeted_contract.log"
.....                                                                    [100%]
5 passed in 0.18s
EXIT_CODE=0
```

---

# 23. Step H15 — AC-002 Targeted Evidence

AC-002に対応するstate contract node:

```text
test_g02_002_common_state_machine_rejects_invalid_terminal_transition
```

を単体実行する。

```bash
uv run pytest \
  -q \
  tests/product/test_enh_e4_g02_canonical_execution.py::test_g02_002_common_state_machine_rejects_invalid_terminal_transition \
  2>&1 | tee "$EVIDENCE_DIR/12_ac002_targeted.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/12_ac002_targeted.log"
```

Human OperatorはこれだけをもってAC-002 PASSと判定しない。

最終AC判定はTest Agentの責務。

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run pytest \
  -q \
  tests/product/test_enh_e4_g02_canonical_execution.py::test_g02_002_common_state_machine_rejects_invalid_terminal_transition \
  2>&1 | tee "$EVIDENCE_DIR/12_ac002_targeted.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/12_ac002_targeted.log"
.                                                                        [100%]
1 passed in 0.14s
EXIT_CODE=0
```

---

# 24. Step H16 — AC-005 Lease Contract Evidence

lease contract node:

```text
test_g02_005_lease_is_explicit_and_clearable
```

を実行する。

```bash
uv run pytest \
  -q \
  tests/product/test_enh_e4_g02_canonical_execution.py::test_g02_005_lease_is_explicit_and_clearable \
  2>&1 | tee "$EVIDENCE_DIR/13_ac005_lease_contract.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/13_ac005_lease_contract.log"
```

AC-005のatomicityについてはStep H13のreal PostgreSQL concurrent claim testも併せてTest Agentが監査する。

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ uv run pytest \
  -q \
  tests/product/test_enh_e4_g02_canonical_execution.py::test_g02_005_lease_is_explicit_and_clearable \
  2>&1 | tee "$EVIDENCE_DIR/13_ac005_lease_contract.log"

printf 'EXIT_CODE=%s\n' "${PIPESTATUS[0]}" \
  | tee -a "$EVIDENCE_DIR/13_ac005_lease_contract.log"
.                                                                        [100%]
1 passed in 0.15s
EXIT_CODE=0
```

---

# 25. Step H17 — Verification Worktree Post-check

全test command終了後:

```bash
{
  echo "HEAD:"
  git rev-parse HEAD

  echo
  echo "STATUS:"
  git status --short

  echo
  echo "DIFF:"
  git diff --stat
} 2>&1 | tee "$EVIDENCE_DIR/14_worktree_after.log"
```

Expected:

```text
HEAD:
166e90cd1c2d0e523fb863795a88343403d8cc44

STATUS:
clean

DIFF:
none
```

source/test/migration差分が存在した場合はそのまま記録し、Test Agentへ報告する。

Human Operatorがrestoreして証拠を消してはならない。

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ {
  echo "HEAD:"
  git rev-parse HEAD

  echo
  echo "STATUS:"
  git status --short

  echo
  echo "DIFF:"
  git diff --stat
} 2>&1 | tee "$EVIDENCE_DIR/14_worktree_after.log"
HEAD:
166e90cd1c2d0e523fb863795a88343403d8cc44

STATUS:

DIFF:
```

Addendum Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ git status --short 
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ git status
Not currently on any branch.
nothing to commit, working tree clean
```

---

# 26. Step H18 — Evidence Inventory

raw evidence一覧を保存する。

```bash
{
  date --iso-8601=seconds
  echo
  find "$EVIDENCE_DIR" \
    -maxdepth 1 \
    -type f \
    -printf '%f\n' \
    | sort
} 2>&1 | tee "$EVIDENCE_DIR/15_evidence_inventory.log"
```

Evidence: 
```
bigbrother@mandam:/tmp/causal-atelier-g02-ext-verify-20260809021919$ {
  date --iso-8601=seconds
  echo
  find "$EVIDENCE_DIR" \
    -maxdepth 1 \
    -type f \
    -printf '%f\n' \
    | sort
} 2>&1 | tee "$EVIDENCE_DIR/15_evidence_inventory.log"
2026-08-09T02:35:50+00:00

00_implementation_commit.log
01_worktree_before.log
02_database_environment.log
03_sqlalchemy_preflight.log
04_alembic_heads.log
05_alembic_current_before.log
06_alembic_upgrade_head.log
07_alembic_current_after.log
08_product_migration_revision.log
09_postgres_contract_pytest.log
10_atomic_claim_pytest.log
11_g02_targeted_contract.log
12_ac002_targeted.log
13_ac005_lease_contract.log
14_worktree_after.log
15_evidence_inventory.log
```

---

# 27. Required Raw Evidence Files

正常に手順が進んだ場合、最低限以下を残す。

```text
03_external_postgresql_verification_execution_evidence/
├── 00_implementation_commit.log
├── 01_worktree_before.log
├── 02_database_environment.log
├── 03_sqlalchemy_preflight.log
├── 04_alembic_heads.log
├── 05_alembic_current_before.log
├── 06_alembic_upgrade_head.log
├── 07_alembic_current_after.log
├── 08_product_migration_revision.log
├── 09_postgres_contract_pytest.log
├── 10_atomic_claim_pytest.log
├── 11_g02_targeted_contract.log
├── 12_ac002_targeted.log
├── 13_ac005_lease_contract.log
├── 14_worktree_after.log
└── 15_evidence_inventory.log
```

途中STOPの場合、実行済みのlogだけを残してよい。

不足logを偽造しない。

---

# 28. Human Execution Record

以下をHuman Operatorが埋める。

## Execution metadata

```text
Executed by:
<RECORD_HERE>

Started at:
<RECORD_HERE>

Finished at:
<RECORD_HERE>

Implementation commit:
166e90cd1c2d0e523fb863795a88343403d8cc44

Verification worktree:
<RECORD_HERE>
```

## PostgreSQL

```text
Container:
ariadne-g02-postgres

Endpoint:
172.17.0.1:55432

Database:
ariadne_g02_test

SQLAlchemy preflight exit:
<RECORD_HERE>
```

## Migration

```text
alembic heads exit:
<RECORD_HERE>

upgrade head exit:
<RECORD_HERE>

current after upgrade exit:
<RECORD_HERE>

Observed Product migration revision:
<RECORD_HERE>
```

## Tests

```text
PostgreSQL contract suite exit:
<RECORD_HERE>

Atomic claim test exit:
<RECORD_HERE>

G02 targeted contract exit:
<RECORD_HERE>

AC-002 targeted node exit:
<RECORD_HERE>

AC-005 lease node exit:
<RECORD_HERE>
```

## Repository integrity

```text
Implementation worktree HEAD unchanged:
<YES / NO>

Implementation worktree clean after verification:
<YES / NO>

Production source modified:
<YES / NO>

Automated tests modified:
<YES / NO>

Migration modified:
<YES / NO>
```

---

# 29. Human Operator Decision Boundary

Human Operatorは以下のような結論を書かない。

禁止:

```text
AC-002 PASS
AC-005 PASS
G02 PASS
implementation is correct
```

Human Operatorが記録してよいのはobserved factsだけ。

例:

```text
Command:
uv run pytest ...

Exit code:
0

Observed:
4 passed
```

Acceptance Criteriaの意味付けはTest Agentへ委ねる。

---

# 30. Test Agent Handoff

Human execution終了後、Test Agentへ以下を渡す。

```text
E4-G02 Trial 01 external PostgreSQL verification evidenceを監査せよ。

これはCoding Trial 02ではない。

Test Agent自身のnetwork environmentからPostgreSQLへの接続を
再試行する必要はない。

Human Operatorが同一implementation commitを固定したdetached worktree上で
migration / PostgreSQL testを実行し、raw execution evidenceを保存している。

対象implementation commit:

166e90cd1c2d0e523fb863795a88343403d8cc44

Primary evidence:

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G02_Supplemental/
03_external_postgresql_verification_execution.md

Raw evidence:

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G02_Supplemental/
03_external_postgresql_verification_execution_evidence/

以下を独立監査せよ。

1. implementation commitが166e90cd...で固定されているか。
2. verification前後でsource/test/migrationが不変か。
3. PostgreSQL connection preflightが成立したか。
4. Product migration headが期待値と一致するか。
5. empty isolated DBへのProduct migrationが成功したか。
6. migration後current revisionが期待headか。
7. real PostgreSQL contract suiteが実際に実行されたか。
8. concurrent claim testが実際にassertionまで到達したか。
9. AC-002関連test evidenceが有効か。
10. AC-005関連test evidenceが有効か。
11. 初回PASS済みAC-001/003/004および41-test regression evidenceを
    implementation commit不変を根拠として再利用可能か。
12. evidence欠損・command mismatch・改変の疑いがないか。

Human Operatorの結論を無条件に採用してはならない。
raw log / exit code / actual assertionsを自分で監査すること。

判定:

すべてのAcceptance Criteriaおよびmigration verificationが成立:
E4-G02 = PASS

implementation defectを確認:
E4-G02 = FAIL

evidence不足または判定不能:
E4-G02 = BLOCKED

source/test/migrationを変更してはならない。

既存BLOCKED evidenceを削除・上書きしてはならない。

今回の監査evidenceおよびGate Decisionを:

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/
G02/

へ追加すること。

Gate Decision後、G03へ進まず停止せよ。
```

---

# 31. Evidence Commit

Human execution evidenceとTest Agent audit evidenceは、production implementation commitとは分離する。

Test Agent audit完了後、documentation/evidenceだけをstageする。

`git add .` は使用しない。

最低限、対象fileを明示してstageする。

例:

```bash
git add \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/G02_Supplemental/03_external_postgresql_verification_execution.md \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/G02_Supplemental/03_external_postgresql_verification_execution_evidence/
```

Test Agentが生成したG02 reportも明示的にstageする。

unrelated working-tree差分を含めない。

---

# 32. Cleanup

Test Agentによるevidence auditとGate Decisionが完了した後、temporary verification worktreeを削除する。

original repositoryへ戻る。

```bash
cd /loc0/bigbrother/repositories/causal-atelier
```

確認:

```bash
git worktree list
```

削除:

```bash
git worktree remove "$G02_VERIFY_WORKTREE"
```

G02 PostgreSQLが不要になったら停止する。

```bash
docker stop ariadne-g02-postgres
```

`--rm` 起動containerであればstop後に削除される。

確認:

```bash
docker ps -a \
  --filter name='^/ariadne-g02-postgres$'
```

---

# 33. Final Safety Check

original repositoryで:

```bash
cd /loc0/bigbrother/repositories/causal-atelier

git status --short
```

確認事項:

```text
production source unexpected diff:
NONE

automated test unexpected diff:
NONE

migration unexpected diff:
NONE

G02 evidence:
PRESENT
```

既存のunrelated差分は変更しない。

---

# 34. Completion Criteria

本Human operationの完了条件は以下。

1. implementation commitを固定した。
2. detached worktreeを使用した。
3. isolated PostgreSQL connection preflightを実施した。
4. Product migration headを確認した。
5. Product migration upgradeを実行した。
6. migration current revisionを記録した。
7. real PostgreSQL contract suiteを実行した。
8. concurrent claim testを実行した。
9. G02 targeted testを実行した。
10. AC-002 targeted evidenceを記録した。
11. AC-005 targeted evidenceを記録した。
12. 全commandのstdout/stderrを保存した。
13. 全commandのexit codeを保存した。
14. verification後worktree integrityを確認した。
15. source/test/migrationを変更していない。
16. Human OperatorがGate判定していない。
17. raw evidenceをTest Agentへhandoffした。
18. Test Agentが独立Gate Decisionを作成した。

---

# 35. Stop Conditions

## BLOCKED — SQLAlchemy preflight failure

Human environmentからPostgreSQL protocol connectionが成立しない。

migration/testへ進まない。

---

## BLOCKED / FAIL candidate — Migration command failure

Product migrationが失敗。

Human Operatorは修正しない。

raw evidenceをTest Agentへ渡す。

---

## FAIL candidate — pytest assertion failure

pytestが実際のassertion failureへ到達。

Human Operatorは再実装しない。

raw evidenceをTest Agentへ渡す。

---

## BLOCKED — Evidence integrity failure

implementation commit不一致、worktree dirty、required raw log欠損等。

Test Agentへその事実を渡す。

---

## PASS candidate

全required commandが正常完了してもHuman OperatorはPASSを宣言しない。

Test Agentによる独立監査を必須とする。

---

# 36. G02後の方針

E4-G02がPASSした場合、本外部実行方式を恒久運用にはしない。

G03開始前に、

```text
Test PostgreSQL infrastructure standardization
```

を行う。

目的:

```text
persistent test PostgreSQL service
+
stable connectivity from verification environment
+
automated DB reset
+
Product migration initialization
+
Agentが毎回Human OperatorへDB操作を依頼しない運用
```

を確立する。

G03〜G08では、人間による今回の手動verification pathを通常経路にしない。
