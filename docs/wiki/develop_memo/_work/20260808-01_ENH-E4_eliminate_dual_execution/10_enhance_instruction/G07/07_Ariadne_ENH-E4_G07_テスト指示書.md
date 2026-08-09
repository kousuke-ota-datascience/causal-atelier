# Ariadne ENH-E4 E4-G07 Independent Test Instruction

```text
Gate: E4-G07
Trial: 01
Role: Independent Test Agent
Plan: 10_enhance_instruction/G07/06_G07_P00_work_package_plan.md
Completion Report:
  20_implementation_reports/G07/Trial01/E4-G07_01_implementation_completion_report.md
Transition Debt: E4-TD-005
```

本 test contract は Fixed Candidate より前に作成する。
Candidate SHA / Product migration head は completion report から解決し、P01-P04 の結果に合わせて test semantics を変更しない。

---

## 1. Mission

fixed E4-G07 candidate が:

```text
E4-G07-AC-001..005
```

を満たし、`E4-TD-005` を閉じられるか独立判定する。

Coding Agent の PASS claim 自体は evidence としない。

Final decision:

```text
PASS | FAIL | BLOCKED
```

出力先:

```text
30_test_report/G07/Trial01/E4-G07_01_999_gate_decision.md
```

---

## 2. Minimal Inputs

読むもの:

```text
1. this instruction
2. G07 P00 when common rule is needed
3. E4-G07_01_implementation_completion_report.md
4. current source/tests required by each item
```

P01-P04 instruction/report は失敗・矛盾調査時のみ参照する。

---

## 3. Candidate Resolution

completion report の exact fields:

```text
Fixed Implementation/Test Candidate SHA
Product Migration Head
```

をそれぞれ:

```text
G07_CANDIDATE_SHA
G07_EXPECTED_PRODUCT_MIGRATION_HEAD
```

として使用する。

missing / ambiguous なら substantive test 前に `BLOCKED`。

---

## 4. Candidate Identity Rule

実行:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git cat-file -e <G07_CANDIDATE_SHA>^{commit}
git diff --name-only <G07_CANDIDATE_SHA>..HEAD
```

Required:

```text
branch = refactor/ariadne_mvp_e4
candidate exists
unexplained working-tree executable change = 0
post-candidate executable-state difference = 0
```

candidate 後に許容:

```text
G07 instruction/report/test-report documentation only
```

production source / tests / migration / runner / config / deployment 等が candidate 後に変わっていれば `BLOCKED`。

### Pre-authored test contract proof

取得:

```bash
git log -1 --format=%H -- \
  'docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G07/07_Ariadne_ENH-E4_G07_テスト指示書.md'
```

その SHA を `<TEST_CONTRACT_COMMIT>` とし:

```bash
git merge-base --is-ancestor \
  <TEST_CONTRACT_COMMIT> \
  <G07_CANDIDATE_SHA>
```

Required: exit `0`。

これが成立しなければ test-fitting risk のため `BLOCKED`。

---

## 5. Gate Contract

```text
AC-001 runtime:
  canonical Product runtime -> retired ariadne.legacy import/reachability = 0

AC-002 deployment:
  repository-managed deployment -> legacy API/CLI/worker invocation = 0

AC-003 shared science:
  ariadne.causal / preprocessing / shared remain usable without legacy orchestration

AC-004 bootstrap:
  Product bootstrap uses product_migrations only; root legacy migrations are not invoked

AC-005 CLI/compatibility:
  low-level CLI creates no persistent Product lifecycle;
  any auditable CLI uses canonical Execution;
  legacy-named contracts are classified by actual compatibility consumption
```

G02-G06 canonical authority must remain valid。

TD-005 exit:

```text
Product runtime legacy dependency = 0
AND
Product bootstrap legacy migration dependency = 0
```

---

## 6. Report Set

```text
30_test_report/G07/Trial01/
├── E4-G07_01_001_candidate_identity.md
├── E4-G07_01_002_runtime_deployment_boundary.md
├── E4-G07_01_003_shared_science_boundary.md
├── E4-G07_01_004_product_only_bootstrap.md
├── E4-G07_01_005_cli_compatibility_boundary.md
├── E4-G07_01_006_protected_regression.md
├── E4-G07_01_007_architecture_exit_audit.md
└── E4-G07_01_999_gate_decision.md
```

001-007 は各々 `PASS | FAIL | BLOCKED` を持つ。

---

# Test Item 001 — Candidate Identity

## 7. Checks

Section 4 を全実行する。

migration head:

```bash
uv run alembic -c alembic_product.ini heads
```

Required:

```text
completion report Product head == repository Product head
```

Record:

```text
Repository HEAD
Fixed Candidate SHA
Test Contract Commit SHA
ancestor result
post-candidate paths
candidate-equivalence result
expected / actual Product migration head
```

Output:

```text
E4-G07_01_001_candidate_identity.md
```

candidate identity failure は architecture FAIL ではなく `BLOCKED`。

---

# Test Item 002 — Runtime / Deployment Boundary

## 8. AC

Verify `AC-001`, `AC-002`。

Required:

```text
Product/API/worker -> ariadne.legacy reachability = 0
canonical API/worker roots are Product roots
legacy canonical runtime registration = 0
legacy Docker/compose runtime invocation = 0
```

`src/ariadne/legacy/` の物理存在だけでは FAIL にしない。

## 9. Verification

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_architecture.py \
  tests/product/test_enh_e4_g07_p01_runtime_boundary.py
```

independent inspection:

```text
pyproject.toml scripts/wheel exclusion
.dockerignore
Dockerfile
compose.yaml
Product/API/worker roots
```

P01 AST guard が worker と transitive import を実際に監査することも確認する。

Output:

```text
E4-G07_01_002_runtime_deployment_boundary.md
```

---

# Test Item 003 — Shared Scientific Boundary

## 10. AC

Verify `AC-003`。

Required:

```text
ariadne.causal usable
ariadne.preprocessing usable
ariadne.shared usable
ScientificCoreAdapter path usable
shared/scientific -> retired legacy orchestration = unreachable
```

## 11. Verification

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run python - <<'PY'
import ariadne.interfaces.worker.runner
import ariadne.scientific.core_adapter
import ariadne.causal
import ariadne.preprocessing
import ariadne.shared
print('E4-G07 shared science smoke: PASS')
PY
```

P01 architecture test も evidence とし、guard が retained shared roots を監査することを source inspection で確認する。

namespace root が意図的に importable でない場合のみ actual public module に置換し理由を記録する。

Output:

```text
E4-G07_01_003_shared_science_boundary.md
```

---

# Test Item 004 — Product-only Bootstrap

## 12. AC

Verify `AC-004` と TD-005 bootstrap half。

## 13. Migration Graph

```bash
uv run alembic -c alembic_product.ini heads
uv run alembic -c alembic_product.ini history
```

Required:

```text
actual Product head == completion report head
intended Product head count = 1
Product chain is not spliced with root legacy chain
```

Inspect:

```text
alembic_product.ini -> product_migrations
product_migrations/env.py -> Product metadata/version table
compose migration command
Product PG runner bootstrap
root alembic.ini -> migrations
```

Root chain required classification:

```text
HISTORY_ONLY for Product bootstrap
```

## 14. Real PostgreSQL — Mandatory

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py \
  tests/product/test_postgres_contract.py \
  -q
```

mixed static/PG file の場合は actual PG nodes を使用する。

Required fresh-DB evidence:

```text
reset PASS
Product migration PASS
alembic_version_product exists
DB Product revision == repository head
root alembic_version absent
root-only/legacy schema regenerated = 0
```

runner evidence path を記録する。

Output:

```text
E4-G07_01_004_product_only_bootstrap.md
```

---

# Test Item 005 — CLI / Compatibility Boundary

## 15. AC

Verify `AC-005`, `E4-REQ-033..035`。

### CLI classification

actual `[project.scripts]` と `src/ariadne/interfaces/cli/` を監査する。

Expected low-level set includes:

```text
ariadne-discover
ariadne-estimate
ariadne-identify
ariadne-refute
ariadne-sensitivity
```

actual candidate set を authority とする。

Required:

```text
unclassified analysis CLI = 0
LOW_LEVEL_UTILITY hidden Product persistence owner = 0
```

`AUDITABLE_PRODUCT_CLI` が存在する場合は canonical Product Execution submission を使用すること。

`AUDITABLE_PRODUCT_CLI = 0` は valid。

## 16. Verification

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_cli_contract.py \
  tests/product/test_enh_e4_g07_p03_cli_boundary.py
```

representative CLI source も inspect し、low-level flow が:

```text
local input/config
-> scientific validation / ScientificCoreAdapter
-> local artifact / portable manifest
```

であり、以下を所有しないことを確認する:

```text
Execution repository/UoW/ORM lifecycle
Stage/Result/Artifact persistence lifecycle
retired legacy lifecycle
```

low-level manifest が canonical persistent identity を生成/主張しないこと:

```text
execution_id
stage_execution_id
result_id
artifact_id
```

### Compatibility terminology

material legacy-named Product contracts（存在する場合 `legacy-product-snapshot/1` を含む）について consumer を確認する。

Required principle:

```text
consumed name -> COMPATIBILITY_DATA_CONTRACT
name alone    -> not legacy runtime authority
```

名称だけを理由に FAIL にしない。

Output:

```text
E4-G07_01_005_cli_compatibility_boundary.md
```

---

# Test Item 006 — Protected G02-G06 Regression

## 17. Local Contract Set

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_enh_e4_g02_canonical_execution.py \
  tests/product/test_enh_e4_g03_generic_executor_boundary.py \
  tests/product/test_enh_e4_g04_result_artifact_contract.py \
  tests/product/test_enh_e4_g05_submission_convergence.py \
  tests/product/test_enh_e4_g06_p06_mutation_lineage.py \
  tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py
```

actual pass count を記録する。

## 18. PostgreSQL Preservation Set

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g03_acceptance_postgres.py \
  tests/product/test_enh_e4_g04_result_artifact_postgres.py \
  tests/product/test_enh_e4_g05_phase_a_postgres.py \
  tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_revise_postgres.py \
  tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown_postgres.py \
  -q
```

Coverage:

```text
canonical Execution
persistent StageExecution
Result/Artifact authority
Causal/Exploratory/Predictive convergence
retry/rerun/revise
legacy lifecycle shutdown
G06 lineage policy
```

legitimate test rename があれば current equivalent と mapping を記録し、coverage を落とさない。

Output:

```text
E4-G07_01_006_protected_regression.md
```

---

# Test Item 007 — Architecture Exit Audit

## 19. Audit Questions

source + items 001-006 evidence から答える:

```text
1. Product runtime can reach retired legacy authority?          expected NO
2. deployment invokes legacy API/CLI/worker?                    expected NO
3. shared science works without legacy orchestration?           expected YES
4. Product bootstrap can invoke root legacy migrations?         expected NO
5. fresh Product DB is Product-only migration state?            expected YES
6. low-level CLI owns persistent Product lifecycle?             expected NO
7. existing auditable CLI bypasses canonical Execution?         expected NO
8. legacy-named contracts classified by real consumption?       expected YES
9. G02-G06 old authority revived?                               expected NO
10. all residual legacy surfaces explicitly non-authoritative?  expected YES
```

Final required statement:

```text
Product runtime legacy dependency = 0
Product bootstrap legacy migration dependency = 0
low-level CLI hidden persistent lifecycle = 0
shared scientific capability = preserved
```

### Residuals

Allowed when evidence-supported:

```text
RETIRED_UNREACHABLE
HISTORY_ONLY
RETAIN_SHARED_CAPABILITY
LOW_LEVEL_UTILITY
COMPATIBILITY_DATA_CONTRACT
```

active retired runtime/migration authority is not allowed。

physical archive/source cleanup may remain for G08/TD-006 if non-authoritative。

Test Item 007 may state:

```text
TD-005 CLOSABLE
```

but not `CLOSED`。

Output:

```text
E4-G07_01_007_architecture_exit_audit.md
```

---

## 20. Final Decision Rule

Create:

```text
30_test_report/G07/Trial01/E4-G07_01_999_gate_decision.md
```

### PASS

Only if:

```text
001 PASS
002 PASS
003 PASS
004 PASS
005 PASS
006 PASS
007 PASS
```

Then:

```text
E4-G07 Trial01: PASS
E4-G07: PASS
TD-005: CLOSED
TD-006: OPEN / governed by G08
Next Gate: E4-G08
```

### FAIL

candidate-equivalent testing が成立し、G07 architecture criterion に実違反がある場合。

```text
E4-G07 Trial01: FAIL
TD-005: OPEN
Trial02 remediation required
```

### BLOCKED

例:

```text
candidate missing/ambiguous
post-candidate executable change
pre-authored test contract proof failure
required PostgreSQL evidence unavailable
completion report lacks candidate/migration identity
```

`BLOCKED != FAIL`。BLOCKED 自体では Trial increment しない。

---

## 21. 999 Minimum Content

```text
Fixed Candidate SHA
Repository HEAD
candidate-equivalence result
Test Contract Commit + ancestor proof
Product Migration Head
001..007 results
AC-001..005 matrix
TD-005 decision
protected G02-G06 result
material residual classifications
Facts / Interpretation / Unknown
Final PASS / FAIL / BLOCKED
Next action
```

Trial01 の formal G07 decision は Independent Test Agent のみが記録する。
