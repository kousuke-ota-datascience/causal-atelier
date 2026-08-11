# ENH-E4 / G07 P01 — Runtime / Deployment / Shared-Science Boundary

## 1. Objective

P01 は G07 の以下を確定する。

```text
AC-001 canonical Product runtime が retired legacy runtime に依存しない
AC-002 repository-managed deployment が legacy runtime root を起動・登録しない
AC-003 shared scientific capability が legacy orchestration から独立して保持される
```

Coverage:

```text
E4-REQ-001,002,026..029
E4-INV-013,014
```

成果物は legacy source の物理削除ではない。

```text
runtime/deployment から legacy authority への到達不能性
+ shared science preservation
+ 恒久的 architecture guard
```

を成立させる。

---

## 2. Minimal Inputs

最初に読むもの:

```text
10_enhance_instruction/G07/06_G07_P00_work_package_plan.md
30_test_report/G06/Trial01/E4-G06_01_999_gate_decision.md
current relevant source/tests
```

Trial、classification、checkpoint、BLOCKED 条件は P00 を参照し、本書では再掲しない。

source/P00 間に実矛盾を見つけた場合のみ:

```text
40_operator_prompts/architecture_review/
  06_target_architecture_decision_record_result.md
  07_gate_decomposition_result.md
```

を参照する。

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
G06 = PASS
TD-004 = CLOSED
TD-005 = OPEN
Trial = Trial01
```

P00 に G07 entry SHA が記録済みなら引き継ぐ。未記録なら P01 checkpoint に実測値を記録する。

---

## 4. Current Expected Facts — Verify Locally

### 4.1 Runtime / packaging

`pyproject.toml` は少なくとも:

```text
ariadne-api    -> ariadne.interfaces.web_api.app:main
ariadne-worker -> ariadne.interfaces.worker.runner:main
```

を登録し、wheel から:

```text
src/ariadne/legacy/**
```

を除外していることが期待される。

standalone scientific CLI は P03 の主対象であり、P01 では production runtime root と混同しない。

### 4.2 Deployment

期待状態:

```text
.dockerignore : src/ariadne/legacy を除外
Dockerfile    : canonical Product API を起動
compose.yaml  : worker は ariadne-worker を起動
```

compose migration service の authority 完了判定は P02 に委ねる。

### 4.3 Existing guard gap

現行 `tests/product/test_architecture.py` は `src/ariadne/product` と `interfaces/web_api` の legacy import を監査していることが期待される。

current evidence では canonical worker root:

```text
src/ariadne/interfaces/worker
```

が同一 guard の対象に含まれていない。

また shared-science guard は `ariadne.scientific` を中心としており、G07 AC-003 が明示する:

```text
ariadne.causal
ariadne.preprocessing
ariadne.shared
```

の legacy-orchestration independence を直接固定していない可能性がある。

### 4.4 Expected runtime wiring

worker は Product application/persistence と `ScientificCoreAdapter` を使用し、`ScientificCoreAdapter` は Product scientific port と `ariadne.scientific.*` adapter に接続していることが期待される。

上記は expected facts。local repository evidence を優先する。

---

## 5. Required Work

### 5.1 Establish actual canonical runtime roots

repository-managed production roots を確定する。

最低 start points:

```text
src/ariadne/product/
src/ariadne/interfaces/web_api/
src/ariadne/interfaces/worker/
```

そこから runtime に到達する必要な:

```text
src/ariadne/adapters/
src/ariadne/scientific/
src/ariadne/causal/
src/ariadne/preprocessing/
src/ariadne/shared/
```

を追跡する。

判定対象:

```text
Product runtime source roots
API / worker entry points
runtime adapters
scientific adapter path
pyproject package/scripts
Dockerfile / compose.yaml / .dockerignore
```

`grep hit != runtime reachability` とする。

---

### 5.2 Add a non-vacuous legacy reachability guard

architecture test を追加または強化し、canonical runtime roots から:

```text
ariadne.legacy
ariadne.legacy.*
```

への active runtime dependency を検出する。

最低 coverage:

```text
Product package
web API
worker
```

既存 `test_architecture.py` を拡張してもよい。G07 専用 test を作る場合の推奨名:

```text
tests/product/test_enh_e4_g07_p01_runtime_boundary.py
```

#### Required detection quality

direct import だけでなく、可能なら repository 内 `ariadne.*` dependency を追跡して transitive reachability も検出する。

例:

```text
web_api -> product service -> adapter -> ariadne.legacy.*
```

が存在すれば FAIL。

AST import graph 等の軽量 deterministic 実装でよい。failure 時に少なくとも:

```text
canonical root
reached legacy module / import path
```

が分かること。

dynamic import mechanism が実在する場合だけ追加監査する。

---

### 5.3 Enforce deployment boundary

architecture/static contract で次を固定する。

#### `pyproject.toml`

```text
ariadne-api / ariadne-worker が Product interfaces を指す
legacy API/CLI/worker が canonical Product production root として登録されない
wheel/package が src/ariadne/legacy/** を含めない
```

#### `.dockerignore`

```text
Product image build context から src/ariadne/legacy を除外
```

#### `Dockerfile`

```text
canonical Product API を起動
legacy API/worker/CLI root を invoke しない
```

#### `compose.yaml`

```text
API/worker が canonical Product roots を使用
```

migration service は inventory に含めるが、Product-only migration chain の AC 判定は P02 に残す。

---

### 5.4 Preserve shared scientific capability

次を `RETAIN_SHARED_CAPABILITY` として扱う。

```text
ariadne.causal
ariadne.preprocessing
ariadne.shared
ariadne.scientific
```

確認すること:

1. retained shared/scientific modules から `ariadne.legacy` orchestration/runtime への dependency がない。
2. Product scientific adapter path が legacy orchestration を経由しない。
3. legacy boundary hardening 後も intended Product/shared imports が成立する。

最低 contract:

```text
retained shared roots -> no legacy runtime dependency
ScientificCoreAdapter import succeeds
worker -> ScientificCoreAdapter wiring remains importable
```

`ariadne.shared` 内の compatibility-only component 等は consumer を確認して分類する。directory 名だけで削除しない。

scientific algorithm、統計手法、numerical tolerance は変更しない。

---

### 5.5 Start residual legacy inventory

P00 §11 inventory を開始する。

最低 material surfaces:

```text
src/ariadne/legacy/
pyproject.toml runtime/package surface
.dockerignore
Dockerfile
compose.yaml
Product API root
Product worker root
Product scientific adapter path
ariadne.causal
ariadne.preprocessing
ariadne.shared
root/historical migration surface observed here
```

各 surface について:

```text
path/surface
classification
Product runtime reachable? yes/no
Product deployment reachable? yes/no
Product bootstrap reachable? yes/no/DEFER_P02
persistent authority? yes/no
shared capability required? yes/no
G07 action
G08 residual, if any
verification evidence
```

を checkpoint に残す。

legacy directory の全ファイル列挙は不要。architecture 上 material な単位でまとめる。

---

### 5.6 Correct only real violations

`ACTIVE_PRODUCT_DEPENDENCY` が見つかった場合のみ correction する。

許容例:

```text
legacy import -> canonical Product implementation
legacy runtime registration -> canonical root
package/deployment surface から legacy runtime を除外
shared science import -> orchestration-independent path
```

既に invariant が成立しているなら:

```text
production diffなし
+ architecture guard strengthening
+ inventory/evidence
```

で COMPLETE としてよい。

G02–G06 authority semantics を変更しない。

---

## 6. Focused Verification

P01 は通常 DB semantics を変更しないため、real PostgreSQL evidence は必須ではない。DB behavior に波及した場合のみ P00 の PostgreSQL rule を適用する。

### 6.1 Architecture tests

例:

```bash
uv run pytest -q \
  tests/product/test_architecture.py \
  tests/product/test_enh_e4_g07_p01_runtime_boundary.py
```

実際の変更 test path に合わせて調整する。

### 6.2 Shared/import regression

最低限、API/worker/scientific/shared import が壊れていないことを確認する。

```bash
uv run python - <<'PY'
import ariadne.interfaces.web_api.app
import ariadne.interfaces.worker.runner
import ariadne.scientific.core_adapter
import ariadne.causal
import ariadne.preprocessing
import ariadne.shared
print("G07-P01 import smoke: PASS")
PY
```

package structure 上 root import が成立しない namespace は、実在 module に置換する。存在しない public import を新要件にしない。

必要なら existing focused regression として:

```text
tests/product/test_cli_contract.py
```

の shared-scientific adapter 関連 node だけを使ってよい。CLI lifecycle acceptance 自体は P03 に残す。

### 6.3 Deployment evidence

checkpoint 用補助 evidence:

```bash
grep -n "ariadne-api\|ariadne-worker\|ariadne.legacy" pyproject.toml
grep -n "ariadne/legacy" .dockerignore
grep -n "ariadne.interfaces\|ariadne.legacy" Dockerfile compose.yaml
```

これは architecture test の代替ではない。legacy string hit は P00 classification に従って判定する。

### 6.4 Optional built-package verification

既存 tooling で安定して実行できるなら wheel を build し:

```text
ariadne/legacy/** が含まれない
canonical API/worker/scientific package contract が成立する
```

ことを追加 evidence にしてよい。

P01 のためだけに packaging toolchain を再設計しない。

---

## 7. Acceptance Criteria

### P01-AC-01 — Runtime reachability

```text
Product package
Product web API
Product worker
```

から retired `ariadne.legacy` runtime への active dependency = 0。

worker を含む恒久 guard が存在し、可能な範囲で transitive dependency も検出する。

### P01-AC-02 — Deployment boundary

```text
pyproject entry points
Dockerfile
compose.yaml
package/build exclusion
```

が legacy API/worker/orchestration を canonical Product runtime として登録・起動しない。

legacy source の物理存在は FAIL 条件ではない。

### P01-AC-03 — Shared science preserved

```text
ariadne.causal
ariadne.preprocessing
ariadne.shared
ariadne.scientific / ScientificCoreAdapter path
```

が retained され、legacy orchestration 非依存であることを import/architecture evidence で示す。

### P01-AC-04 — No legacy authority revival

P01 correction により legacy:

```text
Execution / Result / Artifact / ArtifactLineage / Lineage
```

persistence が Product runtime authority として再導入されていない。

G06 lineage authority model を変更しない。

### P01-AC-05 — Residual inventory ready

material runtime/deployment/shared surfaces が P00 vocabulary で分類され、P02/P03/P04 が再調査なしに利用できる。

### P01-AC-06 — Passed-Gate preservation

```text
G02 canonical Execution
G03 persistent StageExecution
G04 Result/Artifact authority
G05 family convergence
G06 lineage authority
```

を保持する。

すべて PASS で P01 `COMPLETE`。

---

## 8. Checkpoint Report

作成先:

```text
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G07/Trial01/packages/
E4-G07_01_P01_implementation_checkpoint_report.md
```

最低内容:

```text
# E4-G07 Trial01 P01 Implementation Checkpoint
Status: COMPLETE | BLOCKED
Entry SHA:
Checkpoint SHA:

## Facts Established
- actual runtime roots
- actual deployment roots
- actual shared-science boundary
- active legacy dependency result

## Changes
- production
- tests
- docs/report

## Verification
- command
- PASS/FAIL
- material findings

## Residual Legacy Inventory
- P00 §11 columns

## Acceptance
P01-AC-01 PASS/FAIL
P01-AC-02 PASS/FAIL
P01-AC-03 PASS/FAIL
P01-AC-04 PASS/FAIL
P01-AC-05 PASS/FAIL
P01-AC-06 PASS/FAIL

## P02 Entry
- migration/bootstrap observations
- items deferred to P02
```

P01 checkpoint は Gate PASS、TD-005 CLOSED、READY_FOR_TEST を宣言しない。

---

## 9. P02 Handoff

P01 COMPLETE 後:

```text
06_G07_P02_product_only_migration_bootstrap.md
```

へ進む。

引き渡し:

```text
P01 checkpoint SHA
runtime/deployment root inventory
residual legacy classification
migration/bootstrap surface observed in P01
P01 architecture guard test paths
```

P02 が real PostgreSQL evidence により:

```text
alembic_product.ini -> product_migrations
```

のみを canonical Product bootstrap authority として確定する。

P01 では TD-005 を閉じない。
