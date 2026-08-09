# ENH-E4 / G07 P02 — Product-only Migration / Bootstrap Boundary

## 1. Objective

P02 は G07 の migration/bootstrap half を確定する。

```text
E4-G07-AC-004
E4-INV-015
E4-REQ-030 / 032
E4-REQ-031 supporting evidence only
TD-005 bootstrap half
```

Target:

```text
canonical Product bootstrap
    = alembic_product.ini -> product_migrations only

root alembic.ini -> migrations
    = HISTORY_ONLY for Product bootstrap

fresh Product DB
    = Product migration state only
```

成果物は migration redesign ではなく、bootstrap authority の一意性、root legacy migration の非到達性、real PostgreSQL evidence、恒久 guard である。

---

## 2. Minimal Inputs

読むもの:

```text
10_enhance_instruction/G07/06_G07_P00_work_package_plan.md
20_implementation_reports/G07/Trial01/packages/
  E4-G07_01_P01_implementation_checkpoint_report.md
current relevant migration/bootstrap source/tests
```

P01 checkpoint commit:

```text
e10a6e3d1305cf31d61d669f6e6d41a1b41e8ce1
```

Trial、classification、PostgreSQL runner、checkpoint、verification-only package の共通規則は P00 を参照する。

実矛盾がある場合のみ architecture review の `06_target_architecture_decision_record_result.md` / `07_gate_decomposition_result.md` を参照する。

---

## 3. Entry State

開始時:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
```

Expected:

```text
branch = refactor/ariadne_mvp_e4
P01 = COMPLETE
P01 checkpoint = e10a6e3d1305cf31d61d669f6e6d41a1b41e8ce1
G07 = NOT_COMPLETE
TD-005 = OPEN
Trial = Trial01
```

P02 checkpoint には actual entry SHA を記録する。P01 後に documentation-only commit があれば current HEAD を優先する。

---

## 4. Known Facts Entering P02 — Verify Locally

Current expected state:

```text
alembic_product.ini
  script_location = product_migrations

product_migrations/env.py
  target_metadata = ProductBase.metadata
  database URL = ARIADNE_PRODUCT_DATABASE_URL
  version_table = alembic_version_product

alembic.ini
  script_location = migrations

compose.yaml
  migrate = alembic -c alembic_product.ini upgrade head

Dockerfile / Dockerfile.test
  copy alembic_product.ini
  copy product_migrations

scripts/test/run_product_postgres_tests_in_container.sh
  reset Product test DB
  -> alembic -c alembic_product.ini upgrade head
  -> alembic -c alembic_product.ini current
  -> pytest
```

G06 exit の expected Product migration head:

```text
20260809_product_0010
```

ただし actual repository head を authority とする。P02 で必ず:

```bash
uv run alembic -c alembic_product.ini heads
```

を実行し、actual head を checkpoint に記録する。

expected と異なる場合でも、current branch の正当な migration commit で説明できるなら actual head を採用する。説明不能な multiple heads / chain contradiction は調査する。

---

## 5. Scope

### In scope

```text
Product bootstrap invocation inventory
Alembic config / migration environment boundary
repository-managed production/test migration invocation
fresh PostgreSQL Product bootstrap
version-table evidence
root migration non-invocation guard
```

### Out of P02 completion scope

```text
historical application-data migration
root migrations の物理削除/書換え
legacy source archive cleanup
application startup / three-family Golden Path
CLI lifecycle boundary
G07 PASS / TD-005 closure
```

empty DB からの full startup / three-family final verification は G08 に残す。

---

## 6. Required Work

### 6.1 Establish the repository-managed Product bootstrap graph

Product DB bootstrap を起動し得る repository-managed surface を確認する。

最低対象:

```text
compose.yaml
compose.test.yaml
Dockerfile
Dockerfile.test
pyproject.toml
scripts/
Makefile/task runner if present
deploy/ operational config if present
```

補助検索例:

```bash
rg -n \
  "alembic(_product)?\.ini|alembic .*upgrade|product_migrations|(^|/)migrations" \
  compose*.yaml Dockerfile* pyproject.toml scripts Makefile deploy 2>/dev/null || true
```

docs/history の文字列 hit を active bootstrap と扱わない。

各 material hit を:

```text
ACTIVE_PRODUCT_DEPENDENCY
HISTORY_ONLY
test-only bootstrap support
```

へ分類する。

Expected canonical graphs:

```text
production:
compose migrate
  -> alembic -c alembic_product.ini upgrade head
  -> product_migrations/env.py
  -> ProductBase.metadata
  -> alembic_version_product

test:
run_product_postgres_tests.sh
  -> compose.test test_runner
  -> fresh DB reset
  -> alembic_product.ini upgrade head
  -> pytest
```

### 6.2 Add a permanent bootstrap-boundary guard

推奨 test:

```text
tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py
```

既存 test に統合してもよいが、G07 AC-004 の failure reason が独立して読めること。

最低 guard:

#### A. Product config

```text
alembic_product.ini -> product_migrations
Product migration env -> ProductBase.metadata
Product version table -> alembic_version_product
Product DB URL contract -> ARIADNE_PRODUCT_DATABASE_URL
```

文字列の行番号/配置に test-fit せず、semantic contract を検証する。

#### B. Repository-managed bootstrap commands

最低:

```text
compose.yaml migrate
Dockerfile / Dockerfile.test migration assets
scripts/test/run_product_postgres_tests_in_container.sh
```

が Product chain のみを使うことを固定する。

Product bootstrap surface に:

```text
-c alembic.ini
root migrations/
```

の invocation が入れば FAIL。

#### C. Root chain classification

```text
alembic.ini -> migrations
```

の source presence 自体は FAIL にしない。

P02 classification:

```text
HISTORY_ONLY
```

Product bootstrap から reach/invoke された場合だけ architecture violation とする。

### 6.3 Verify Product migration-chain integrity

実行:

```bash
uv run alembic -c alembic_product.ini heads
uv run alembic -c alembic_product.ini history
```

必要なら:

```bash
uv run alembic -c alembic_product.ini branches
```

確認事項:

```text
one intended Product head
Product ancestry only
root migration chain is not spliced into Product chain
```

P02 のために既存 Product revisions を squash/rewrite しない。意図しない multiple heads は実 defect として扱う。

### 6.4 Prove clean Product bootstrap on real PostgreSQL

P00 指定 runner を使用する。

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py \
  tests/product/test_postgres_contract.py
```

node 分割してもよいが、以下の persistence evidence を全て含める。

Fresh DB migration後:

```text
1. alembic_version_product exists
2. current Product tables required by Product metadata/migrations exist
3. root `alembic_version` does not exist
4. known root-only/legacy schema is not regenerated
5. DB Product revision == actual repository Product head
```

head comparison は可能なら:

```text
Alembic Config/ScriptDirectory から repository head を取得
DB alembic_version_product.version_num を取得
assert same
```

とし、古い revision string の hard-code だけに依存しない。

既存 `run_product_postgres_tests.sh` の fresh DB reset flow を使う。既存 schema 上での `upgrade` 成功だけでは P02 evidence としない。

### 6.5 Strengthen legacy-schema absence evidence

既存 `test_postgres_contract.py` は Product table presence と一部 legacy table absence を持つ。

P02 では root chain 非実行の直接 evidence として最低:

```text
alembic_version_product present
alembic_version absent
```

を固定する。

root metadata と Product metadata を安全に比較できるなら:

```text
root-only tables
  = root metadata tables - ProductBase.metadata tables
```

を求め、fresh Product DB との intersection = 0 を追加してよい。

import side effect 等で不安定になる場合は、version-table evidence + known root-only table absence + command guard を優先する。

### 6.6 Production correction only for a real violation

現行 expected state が既に Product-only なら:

```text
production diff = none
+ permanent guard
+ real PostgreSQL evidence
+ HISTORY_ONLY classification
```

で COMPLETE としてよい。

修正対象となる例:

```text
Product compose/deploy が root alembic.ini を実行
Product image が root migrations を active bootstrap asset として要求
Product PG runner が root migration を実行
Product migration env が legacy/root metadata を authority にする
Product bootstrap が二つの migration chains/version tables を必要とする
```

修正は Product chain へ収束させる。historical migration deletion/rewrite で違反を隠さない。

---

## 7. Focused Verification

### 7.1 Static/bootstrap boundary

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_enh_e4_g07_p01_runtime_boundary.py \
  tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py
```

P01 guard を併走し、migration correction が runtime/deployment boundary を壊していないことを確認する。

### 7.2 Migration graph

```bash
uv run alembic -c alembic_product.ini heads
uv run alembic -c alembic_product.ini history
```

actual head を checkpoint に残す。

### 7.3 Real PostgreSQL — mandatory

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py \
  tests/product/test_postgres_contract.py
```

checkpoint に最低:

```text
runner evidence log/metadata path
reset_exit_code
migration_exit_code
migration_current_exit_code
pytest outcome
repository Product head
DB version_num
alembic_version_product existence
root alembic_version absence
root-only/legacy schema absence result
```

を記録する。

### 7.4 Passed-Gate preservation

P02 が migration/config/test のみなら、P01 の G02–G06 42-test selection の再実行は必須ではない。

最低:

```text
P01 runtime boundary guard
Product PostgreSQL contract
```

を通す。

Product ORM/schema/runtime lifecycle code を変更した場合のみ、影響する G02–G06 focused regressions を追加する。

---

## 8. Acceptance Criteria

### P02-AC-01 — Bootstrap path

repository-managed Product bootstrap graph が確定し、canonical migration chain は:

```text
alembic_product.ini -> product_migrations
```

のみ。

### P02-AC-02 — Root chain history-only

```text
alembic.ini -> migrations
```

は Product production/test bootstrap から invoke されず、`HISTORY_ONLY` と evidence 付きで分類される。

### P02-AC-03 — Permanent guard

Product bootstrap へ root migration invocation を追加すると FAIL する恒久 contract test が存在する。

### P02-AC-04 — Real PostgreSQL

fresh PostgreSQL で:

```text
Product upgrade head PASS
alembic_version_product present
DB Product revision == repository Product head
root alembic_version absent
root-only/legacy schema regenerated = 0
```

が確認される。

### P02-AC-05 — Product chain integrity

Product migration chain は intended single head を持ち、root chain と splice/dual-bootstrap されていない。

### P02-AC-06 — Scope/preservation

historical migration rewrite、legacy source deletion、新 persistent authority を導入せず、P01 runtime/deployment boundary も PASS を維持する。

すべて PASS で P02 `COMPLETE`。

P02 は `G07 PASS`、`TD-005 CLOSED`、`READY_FOR_TEST` を宣言しない。

---

## 9. Checkpoint Report

作成先:

```text
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G07/Trial01/packages/
E4-G07_01_P02_implementation_checkpoint_report.md
```

最低内容:

```text
# E4-G07 Trial01 P02 Implementation Checkpoint
Status: COMPLETE | BLOCKED
Entry SHA:
P01 checkpoint SHA: e10a6e3d1305cf31d61d669f6e6d41a1b41e8ce1
Checkpoint SHA:

## Facts Established
- canonical bootstrap graph
- actual Product migration head
- root migration classification

## Changes
- production/bootstrap
- tests
- docs/report

## Static Verification
- command / PASS-FAIL / finding

## PostgreSQL Verification
- runner command
- evidence log/metadata
- reset/migration/current/pytest results
- repository head == DB version
- version-table evidence
- root-only/legacy schema absence

## Residual Legacy Inventory
- root alembic.ini / migrations
- production/test bootstrap surfaces

## Acceptance
P02-AC-01 PASS/FAIL
P02-AC-02 PASS/FAIL
P02-AC-03 PASS/FAIL
P02-AC-04 PASS/FAIL
P02-AC-05 PASS/FAIL
P02-AC-06 PASS/FAIL

## P03 Entry
- fixed bootstrap facts
- remaining CLI / compatibility surfaces
```

report 自身を含む commit SHA が事前に不明なら `Checkpoint SHA = PENDING — repository commit containing this checkpoint` でよい。P03 が actual P02 checkpoint SHA を引き継ぐ。

---

## 10. P03 Handoff

P02 COMPLETE 後:

```text
06_G07_P03_cli_compatibility_boundary.md
```

へ進む。

引き渡し:

```text
P02 checkpoint commit SHA
canonical bootstrap graph
actual Product migration head
root migrations = HISTORY_ONLY evidence
real PostgreSQL evidence path
P01/P02 guard test paths
updated residual legacy inventory
```

P03 は migration authority を再検討せず、standalone scientific CLI / persistent lifecycle boundary / compatibility terminology に限定する。

TD-005 の正式 closure は P04 Gate-wide completion まで行わない。
