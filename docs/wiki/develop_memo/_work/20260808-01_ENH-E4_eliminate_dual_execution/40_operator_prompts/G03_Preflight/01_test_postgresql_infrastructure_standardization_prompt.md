# G03 Preflight — Test PostgreSQL Infrastructure Standardization Prompt

## 1. Task

ENH-E4 の E4-G02 は PASS 済みである。

G02 では real PostgreSQL verification のために Human Operator が都度、

- disposable PostgreSQL container 起動
- network route 切り分け
- DB URL 設定
- external migration / pytest 実行
- raw evidence 保存
- Test Agent への evidence handoff

を行う必要があり、検証運用として過剰に手作業へ依存した。

E4-G03 以降ではこの手順を通常経路にしてはならない。

本Taskでは、G03 implementation開始前の独立preflightとして、
**repository-managed Test PostgreSQL infrastructure** を標準化する。

本Taskは E4-G03 implementation ではない。
StageExecution / runner boundary / Result / Artifact / Lineage 等の ENH-E4 production architectureを変更してはならない。

---

## 2. Repository / Branch

Repository:

```text
causal-atelier
```

Required branch:

```text
refactor/ariadne_mvp_e4
```

Baseline:

```text
5888783
```

開始時に actual HEAD / branch / working tree を必ず確認すること。

既存の unrelated working-tree 差分を変更・stage・restoreしてはならない。

---

## 3. Operator Prompt Location

本promptをrepositoryへmaterializeする場合の推奨配置:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G03_Preflight/
01_test_postgresql_infrastructure_standardization_prompt.md
```

Result:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G03_Preflight/
01_test_postgresql_infrastructure_standardization_result.md
```

---

## 4. Current Verified Facts

baseline repositoryでは少なくとも以下が成立している。

### Current development PostgreSQL

```text
compose.yaml
database:
  image: postgres:17-alpine
  development DB only
```

通常開発DBはtest infrastructureとして再利用してはならない。

### Product migrations

Product migration chain:

```text
alembic_product.ini
product_migrations/
```

migration runtimeは:

```text
ARIADNE_PRODUCT_DATABASE_URL
```

を必須とする。

Product version table:

```text
alembic_version_product
```

### PostgreSQL tests

real PostgreSQL testsは:

```text
ARIADNE_PRODUCT_TEST_DATABASE_URL
```

を使用する。

pytest marker:

```text
postgres
```

が存在する。

### Runtime Docker image

current runtime Dockerfileはproduction-orientedであり、
dev dependency / pytestを通常imageへ含めない。

したがって、test executionのためにproduction runtime imageへpytest等を恒久追加することを第一選択としてはならない。

---

## 5. Goal

G03〜G08で、Human OperatorまたはAgentが次の詳細を毎回手作業しなくてよい状態を作る。

禁止したい通常運用:

```text
docker run postgres ...
export DB_URL ...
network troubleshooting ...
manual drop/create DB ...
manual alembic ...
manual pytest ...
manual evidence assembly ...
```

Target operational flow:

```text
one repository-managed command
        ↓
test PostgreSQL availability
        ↓
clean test database reset
        ↓
Product migration upgrade head
        ↓
requested PostgreSQL-dependent pytest
        ↓
raw execution evidence
        ↓
deterministic exit status
```

---

## 6. Required Architecture

原則として次の構成を実装する。

```text
compose.test.yaml
├── database_test
│     └── postgres:17-alpine
│
└── test_runner
      ├── Python 3.12
      ├── project dependencies
      ├── dev / pytest dependencies
      └── same Docker network as database_test
```

重要:

```text
test_runner → database_test
```

はDocker service name / compose networkを使用して直接接続する。

Test Agent execution environmentからhost loopbackやdocker0 gatewayへ接続できることを通常経路の前提にしてはならない。

G02で起きた、

```text
Agent network namespace
≠ host network namespace
```

問題を再発させないこと。

---

## 7. Isolation Requirements

`database_test` は通常開発DBから完全分離する。

MUST:

- development `database` serviceとDBを共有しない
- development persistent volumeを共有しない
- production/development DBへmigrationを流さない
- fixed test database nameを使用してよい
- test DB resetが安全に繰り返せる
- PostgreSQL major versionはcurrent developmentと整合させる
- credentialsはtest-localであり、production credentialを使用しない

host port公開は必須ではない。

Docker内test runnerがservice nameで接続できるなら、
host port非公開を優先してよい。

診断用途でhost portを公開する場合もdevelopment `5432` と衝突させない。

---

## 8. Test Runner Image

current production Dockerfileのruntime semanticsを不用意に変更しない。

以下のいずれかを採用してよい。

### Preferred A

```text
Dockerfile.test
```

を追加し、test runner専用imageを作る。

### Allowed B

current Dockerfileへtest-only build targetを追加する。

ただしproduction default/runtime targetのdependency surfaceを増やしてはならない。

test runnerには最低限:

- Python 3.12
- uv
- locked project dependencies
- pytest/dev dependency
- source code
- alembic_product.ini
- product_migrations
- tests

が必要。

dependency versionはcurrent `pyproject.toml` / `uv.lock` を正本とし、
新規third-party dependencyを追加しない。

---

## 9. Required Repository-managed Commands

最低限、次の責務をrepository-managed scriptへ集約する。

推奨:

```text
scripts/test/
├── reset_product_test_db.py
├── run_product_postgres_tests.sh
└── README.md
```

exact filenameは既存repository conventionがあればそれに合わせてよい。

### reset_product_test_db

MUST:

1. test PostgreSQLへ接続
2. target test DBへの既存connectionを安全にterminate
3. target test DBをdrop
4. target test DBをcreate
5. Product migration実行前のclean stateを保証

実装言語はPythonを推奨する。

host `psql` binaryの存在を必須にしてはならない。

repositoryに既にある `psycopg` / SQLAlchemyを利用してよい。

### run_product_postgres_tests

MUST:

1. `database_test` を自動起動または起動済みなら再利用
2. health/readinessを待つ
3. test DB reset
4. `alembic -c alembic_product.ini upgrade head`
5. migration current/head確認
6. requested pytest argumentsを実行
7. real PostgreSQL URLを自動設定
8. exit codeを正しく呼出元へ返す
9. raw stdout/stderrを保存可能にする
10. failure時にtest DBやdevelopment DBを手動補正しない

---

## 10. One-command UX

通常利用者から見た操作を、可能な限り一つにする。

例:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_postgres_contract.py
```

または:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_postgres_contract.py::test_claim_next_is_atomic_across_concurrent_workers
```

pytest node/path argumentsを透過的に渡せること。

`-m postgres` 等のpytest optionも必要なら渡せること。

---

## 11. Evidence Support

G02のようにraw evidenceが後から必要になるため、runnerにはevidence出力contractを持たせる。

最低限:

```text
implementation/tested commit
started_at
finished_at
database service/image
Product migration head
migration exit code
pytest command
pytest exit code
stdout/stderr
```

を取得可能にする。

推奨:

```text
--evidence-dir <path>
```

または環境変数:

```text
ARIADNE_TEST_EVIDENCE_DIR
```

をサポートする。

raw evidenceを `.log` にする場合、repository `.gitignore` によって意図せずcommit不能になる問題を考慮すること。

次のいずれかを採用する。

- `.txt` / `.md` を使用
- evidence directory専用 `.gitignore` exception
- generated raw evidenceはcommit対象外と明記しTest Reportへ必要情報を転記

どれを選ぶかresultで理由を説明する。

---

## 12. Docker Lifecycle Contract

毎TestでPostgreSQL server containerを必ずdestroy/recreateする必要はない。

Target:

```text
database_test container/service
    = reuse allowed

test database contents
    = each verification reset
```

ただし、

```text
docker compose ... down
```

後のclean recreationでも正常に動くこと。

runnerは次の両方に対応する。

### Cold start

database_testが存在しない。

### Warm start

database_testが既にhealthy。

どちらでも同じcommandが成功すること。

---

## 13. Compose Project Isolation

通常development composeとのname collisionを避ける。

test composeはproject nameを明示または一意に管理してよい。

例:

```text
ariadne-test
```

Test infrastructureのcontainer / network / volumeがdevelopment stackと混ざらないこと。

---

## 14. Database URL Contract

Docker内では最低限:

```text
ARIADNE_PRODUCT_DATABASE_URL
ARIADNE_PRODUCT_TEST_DATABASE_URL
```

の両方が同じclean test DBを指す。

例concept:

```text
postgresql+psycopg://...@database_test:5432/ariadne_test
```

host gateway IP (`172.17.0.1` 等) をrepository contractへhard-codeしてはならない。

---

## 15. Product Migration Contract

MUST:

```text
alembic_product.ini
→ product_migrations/
```

のみを使用。

root legacy migrationを実行してはならない。

reset後のempty DBに対して:

```text
upgrade head
```

が成功すること。

headはhard-coded revision IDではなく、
actual Product migration graphから取得・検証できることを優先する。

---

## 16. G02 Regression Requirement

本standardization後も、少なくともG02で利用した以下のreal PostgreSQL verificationが新runnerから成功すること。

```text
tests/product/test_postgres_contract.py
```

および:

```text
tests/product/test_postgres_contract.py::test_claim_next_is_atomic_across_concurrent_workers
```

さらに:

```text
tests/product/test_enh_e4_g02_canonical_execution.py
```

も通常pytest executionで回帰確認する。

---

## 17. Required Self-tests

implementation agent自身が最低限以下を実施する。

### ST-001 Cold start

test compose resourceなしの状態からone-command verification成功。

### ST-002 Warm reuse

database_testが既にhealthyな状態で同じcommand成功。

### ST-003 Dirty DB reset

意図的にtest DBへdata/schema stateを残した後、
runnerがclean resetしてmigration/testを成功させる。

### ST-004 Migration

clean DBからProduct migration headまで成功。

### ST-005 PostgreSQL contract

`tests/product/test_postgres_contract.py` PASS。

### ST-006 Concurrent claim

atomic concurrent claim node PASS。

### ST-007 Failure propagation

存在しないpytest nodeまたは意図的に失敗する安全なcommandで、
runnerがnon-zeroを返すこと。

テスト自体を改変して故意にfailureを作ってはならない。

### ST-008 Development isolation

development DB/container/volumeへ変更がない。

---

## 18. Allowed Changes

必要な範囲で変更可:

```text
compose.test.yaml
Dockerfile.test
Dockerfile                  # test-only targetの場合のみ
scripts/test/**
tests/test-infrastructure-specific tests
README / testing docs
.gitignore                  # evidence policyに必要な最小変更のみ
```

既存 `compose.yaml` は、
shared definitionを安全に再利用する最小変更が必要な場合のみ変更してよい。

production runtime semanticsを変えてはならない。

---

## 19. Forbidden Changes

禁止:

- ENH-E4 G03 production implementation
- StageExecution implementation
- Result/Artifact consolidation
- Lineage changes
- legacy retirement
- application domain semantics changes
- production database credentials変更
- development DBをtest DBとして利用
- existing Product migration rewrite
- root legacy migration変更
- scientific logic変更
- new third-party dependency
- test assertion weakening
- skip/xfailによる回避

---

## 20. Agent Network Constraint

重要:

Test Agent自身がDocker socketやhost networkへアクセスできない環境があり得る。

その場合でも、本standardizationを失敗扱いにしないための境界を明確化する。

MUST:

- real test executionはrepository-managed single commandで再現可能
- commandはHuman Operatorからも実行可能
- HumanはDB準備手順を個別実行する必要がない
- raw evidenceを保存可能
- Audit Agentは生成evidenceをread-only監査可能

つまりfallbackは:

```text
Human:
  one command only
        ↓
repository runner:
  DB + migration + tests + evidence
        ↓
Audit Agent:
  evidence review
```

とする。

G02のような複数手順の手動runbookへ戻してはならない。

---

## 21. Required Documentation

最低限、testing infrastructureの利用方法をrepository内へ記録する。

内容:

- first use
- normal use
- run one node
- run postgres marker
- evidence output
- stop/cleanup
- cold/warm behavior
- development DB isolation
- troubleshooting
- Agent cannot access Docker/network の場合の single-command Human fallback

---

## 22. Result File

生成:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
G03_Preflight/
01_test_postgresql_infrastructure_standardization_result.md
```

最低限の構造:

```markdown
# Test PostgreSQL Infrastructure Standardization Result

## 1. Metadata
## 2. Starting Repository State
## 3. Current Test Infrastructure Before Change
## 4. Implemented Architecture
## 5. Files Changed
## 6. database_test Contract
## 7. test_runner Contract
## 8. DB Reset Contract
## 9. Product Migration Contract
## 10. One-command Runner Contract
## 11. Evidence Contract
## 12. Cold Start Self-test
## 13. Warm Reuse Self-test
## 14. Dirty DB Reset Self-test
## 15. PostgreSQL Contract Test Result
## 16. Concurrent Claim Test Result
## 17. Failure Propagation Test
## 18. Development Isolation Audit
## 19. Git Diff / Commit
## 20. Remaining Limitations
## 21. Decision
```

---

## 23. Decision Values

Result decisionは以下のみ。

```text
READY_FOR_INDEPENDENT_INFRA_AUDIT
INCOMPLETE_TEST_INFRASTRUCTURE
BLOCKED_ENVIRONMENT
DESIGN_BLOCKED
```

本AgentはG03を開始しない。

---

## 24. Completion Criteria

`READY_FOR_INDEPENDENT_INFRA_AUDIT` には全て必要。

1. test PostgreSQLはdevelopment DBから分離。
2. database_test lifecycleがrepository-managed。
3. test runnerがdatabase_testと同一Docker networkで実行可能。
4. host/docker0 IP hard-codeなし。
5. one-commandでDB start/readiness/reset/migration/pytestまで実行。
6. cold start成功。
7. warm reuse成功。
8. dirty DB reset成功。
9. Product migration成功。
10. real PostgreSQL contract suite成功。
11. atomic concurrent claim成功。
12. non-zero failure propagation確認。
13. development DB/volume無変更。
14. raw evidence出力方法あり。
15. Human fallbackはone commandのみ。
16. production runtime dependency surfaceを不用意に増やしていない。
17. G03 implementationへ越境していない。
18. implementation commitを作成。
19. result document作成。

---

## 25. Stop Condition

以下のいずれかで停止する。

- standardization完了 → independent infra auditへ
- Docker/runtime environmentで実装自体が不能
- production architecture変更が必要
- G03 production codeへの変更が必要

G03 implementationには進まない。
