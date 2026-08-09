# ENH-E4 / G07 P03 — CLI / Compatibility Boundary

## 1. Objective

P03 は G07 の CLI / compatibility half を確定する。

```text
E4-G07-AC-005
E4-ADR-011 / 012
E4-REQ-033..035
HD-007
```

Target:

```text
standalone scientific CLI
    = LOW_LEVEL_UTILITY
    = direct scientific operation + local files/manifest
    = no persistent Product Execution lifecycle

user-visible auditable analysis CLI, if present
    = canonical Product Execution submission boundary

legacy-named Product contract/string
    = compatibility evidenceで分類
    != legacy runtime dependency by name alone
```

P03 は standalone utility CLI を Product lifecycle orchestration へ変換する作業ではない。

---

## 2. Minimal Inputs

読むもの:

```text
10_enhance_instruction/G07/06_G07_P00_work_package_plan.md
20_implementation_reports/G07/Trial01/packages/
  E4-G07_01_P01_implementation_checkpoint_report.md
  E4-G07_01_P02_implementation_checkpoint_report.md
current CLI / compatibility source/tests
```

P02 checkpoint SHA、actual Product migration head は P02 report から取得する。

P00 の Trial / classification / checkpoint / verification-only / BLOCKED rules を継承する。

source/report 間に実矛盾がある場合のみ:

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
P01 = COMPLETE
P02 = COMPLETE
G07 = NOT_COMPLETE
TD-005 = OPEN
Trial = Trial01
```

P03 checkpoint には actual entry SHA と P02 checkpoint SHA を記録する。

P02 report が COMPLETE でない場合は P03 を開始しない。

---

## 4. Fixed Architecture Contract

### 4.1 ADR-011

Approved boundary:

```text
low-level scientific CLI
    -> canonical scientific contracts/adaptersを利用してよい
    -> local manifest/artifactを生成してよい
    -> persistent Product Execution / StageExecution / Result / Artifact lifecycleを所有しない

user-visible auditable analysis CLI
    -> canonical Product Executionへsubmit
    ->独自 lifecycle persistenceを持たない
```

CLI output は、明示的に canonical Product lifecycleへsubmitされない限り:

```text
Product Execution
Product Result
Product Artifact metadata row
```

ではない。

### 4.2 ADR-012

Compatibility terminology:

```text
legacy-named string/field/schema name
    != retired legacy runtime dependency
```

Product validation/data compatibility が実際に消費する名称は、compatibility evidence がある限り保持してよい。

名称だけを理由に rename/delete しない。

---

## 5. Current Expected Facts — Verify Locally

### 5.1 Package scripts

`pyproject.toml` には standalone scientific CLI として少なくとも:

```text
ariadne-discover
ariadne-estimate
ariadne-identify
ariadne-refute
ariadne-sensitivity
```

が `ariadne.interfaces.cli.*` へ登録されていることが期待される。

P01 により legacy API/CLI/worker は canonical deployment root ではない。

### 5.2 Current standalone CLI behavior

Expected current flow:

```text
CLI config
  -> Product domain/scientific input validation
  -> ScientificCoreAdapter
  -> local artifact(s)
  -> CliManifest / manifest.json
```

current discovery/estimation/scientific-stage implementations は repository/UoW/ORM を起動せず、local output を書く構造であることが期待される。

`tests/product/test_cli_contract.py` には discovery manifest が web/Product execution identity を持たないことを検証する既存 test があることが期待される。

### 5.3 No assumed auditable CLI

現時点で canonical persistent Execution を作る CLI が存在するとは仮定しない。

inventory の結果:

```text
AUDITABLE_PRODUCT_CLI = 0
```

であっても AC-005 は成立可能。

必要なのは:

```text
current low-level utilities が second lifecycleを作らない
+
将来 auditable CLI を追加する場合の boundary が closed-by-default である
```

こと。

---

## 6. Required Work

### 6.1 Inventory repository-managed CLI entry points

最低対象:

```text
pyproject.toml [project.scripts]
src/ariadne/interfaces/cli/
CLI-focused tests
Docker/compose/deploy surface に CLI invocation があればその箇所
```

補助検索例:

```bash
rg -n \
  "ariadne-(discover|estimate|identify|refute|sensitivity)|interfaces\.cli|project\.scripts" \
  pyproject.toml src tests compose*.yaml Dockerfile* scripts 2>/dev/null || true
```

各 material CLI entry point を次のいずれかへ分類する:

```text
LOW_LEVEL_UTILITY
AUDITABLE_PRODUCT_CLI
RETIRED_UNREACHABLE
NON_ANALYSIS_UTILITY
```

current canonical package scripts に未分類 entry point があれば P03 contract violation とする。

---

### 6.2 Establish a closed CLI classification contract

P03 は CLI entry point classification を恒久 test として固定する。

推奨 test:

```text
tests/product/test_enh_e4_g07_p03_cli_boundary.py
```

実装方式は test-local registry / source registry のどちらでもよい。

最低 contract:

```text
all repository-managed ariadne analysis CLI entry points
    -> explicitly classified

unclassified new analysis CLI entry point
    -> FAIL
```

current expected classification:

```text
ariadne-discover    LOW_LEVEL_UTILITY
ariadne-estimate    LOW_LEVEL_UTILITY
ariadne-identify    LOW_LEVEL_UTILITY
ariadne-refute      LOW_LEVEL_UTILITY
ariadne-sensitivity LOW_LEVEL_UTILITY
```

local repository evidence が異なれば actual set を採用し、理由を checkpoint に記録する。

---

### 6.3 Prove LOW_LEVEL_UTILITY has no persistent lifecycle authority

low-level CLI import/reachability を監査する。

Allowed examples:

```text
ariadne.interfaces.cli.*
ariadne.product.domain.*
ariadne.product.ports.scientific_core
scientific-only validation service
ariadne.scientific.*
ariadne.causal / preprocessing / shared
filesystem / hashing / manifest serialization
```

Low-level utility から active reachability があれば原則 FAIL:

```text
ariadne.product.persistence
retired ariadne.legacy runtime/persistence
SQLAlchemy/psycopg persistence bootstrap used to create Product lifecycle
canonical worker claim/lease owner
Execution repository/UoW lifecycle submission implementation
outbox/worker lifecycle orchestration used as a hidden second owner
```

重要:

```text
import name blacklistだけで authority を決めない
```

実際の call/reachability と用途を確認する。

例えば Product application module が純粋 validation helper なら、それだけで FAIL にしない。

architecture guard は少なくとも:

```text
low-level CLI root
  -> ariadne.legacy = unreachable
  -> Product persistence package = unreachable
```

を deterministic に検出する。

P01 の AST graph helper を再利用できるなら重複実装しない。

---

### 6.4 Add runtime no-persistence evidence

既存 CLI contract test を拡張または P03 test を追加し、少なくとも representative paths で:

```text
CLI succeeds using local inputs/output only
manifest is created
no Product Execution identity is created/exposed
no Product DB bootstrap is required
```

を確認する。

最低 representative coverage:

```text
discovery
+
one downstream operation
```

prefer:

```text
estimation or scientific_stage-backed identify/refute/sensitivity
```

ScientificCoreAdapter を monkeypatch して algorithm cost を避けてよい。

ただし lifecycle path 自体を mock で隠さない。

DB 非依存 evidence の一例:

```text
invalid/unreachable ARIADNE_PRODUCT_DATABASE_URL を設定
ScientificCoreAdapter を deterministic fake にする
CLI operation が local output まで成功
```

current CLI が Product DB URL を参照しない場合に限る。

この test は real PostgreSQL evidence の代替ではなく、そもそも low-level utility が persistent lifecycle を必要としないことの証明である。

---

### 6.5 Pin manifest identity boundary

Portable CLI manifest は Product persistent identity と混同させない。

最低 verify:

```text
manifest contains portable scientific provenance
manifest does not claim canonical execution identity
```

current low-level utility output について、少なくとも次の reserved persistent identity fields を accidental addition から守る:

```text
execution_id
stage_execution_id
result_id
artifact_id
```

ただし local manifest に scientific operation名、hash、analysis_spec、upstream reference があることは問題ではない。

将来 canonical Executionからexportされた manifest を扱う別機能まで禁止しない。

---

### 6.6 Define auditable CLI boundary without inventing one

inventory に `AUDITABLE_PRODUCT_CLI` が存在する場合のみ:

```text
CLI entry
  -> canonical Product submission service/API
  -> one canonical Execution
```

を実動/architecture evidence で確認する。

以下は認めない:

```text
CLI-owned Execution ORM insert
CLI-owned Stage/Result/Artifact lifecycle persistence
CLI-specific second execution table/repository
```

`AUDITABLE_PRODUCT_CLI = 0` の場合:

```text
no production feature addition required
```

とし、closed classification test と ADR-011 contract により将来境界を固定する。

P03 のためだけに新しい auditable CLI を作らない。

---

### 6.7 Inventory compatibility terminology

最低、architecture review が既知例として示す:

```text
legacy-product-snapshot/1
legacy-named Product test/data contract
```

および current source/tests の material legacy-named Product contracts を確認する。

補助検索:

```bash
rg -n "legacy[-_ ]|LEGACY" src/ariadne/product src/ariadne/interfaces tests/product
```

各 hit を:

```text
COMPATIBILITY_DATA_CONTRACT
RETIRED_RUNTIME_REFERENCE
TEST_HISTORY_ONLY
ACTIVE_VIOLATION
```

へ分類する。

`COMPATIBILITY_DATA_CONTRACT` には最低:

```text
consumer
validation/read location
evidence that rename would change compatibility contract
G07 action = retain
future residual if any
```

を記録する。

unused name が見つかっても、rename が unrelated scope なら G07 で強制しない。

---

### 6.8 Correct only real violations

修正対象例:

```text
low-level CLI が Product persistenceを直接作成
CLI専用 Execution lifecycle repository が active
legacy CLI が Product scriptとして再登録
persistent identityをlocal manifestがcanonical identityとして生成
existing auditable CLI が canonical submissionをbypass
```

既に target が成立している場合:

```text
production diff = none
+ CLI architecture guard
+ runtime contract hardening
+ compatibility inventory
```

で COMPLETE としてよい。

---

## 7. Focused Verification

### 7.1 CLI boundary tests

例:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_cli_contract.py \
  tests/product/test_enh_e4_g07_p03_cli_boundary.py
```

### 7.2 P01/P02 boundary regression

最低:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_enh_e4_g07_p01_runtime_boundary.py \
  tests/product/test_enh_e4_g07_p02_bootstrap_boundary.py \
  tests/product/test_enh_e4_g07_p03_cli_boundary.py
```

P02 test が PostgreSQL marker 専用なら static node のみ local run に含め、DB node は P02 evidence を参照する。

### 7.3 Optional Product PostgreSQL regression

P03 が persistence/application lifecycle code を変更していない場合、追加 PostgreSQL run は必須ではない。

persistence/submission path を変更した場合のみ:

```bash
scripts/test/run_product_postgres_tests.sh \
  <affected canonical submission/lifecycle tests> \
  -q
```

を追加する。

### 7.4 Static inventory evidence

checkpoint には:

```text
actual [project.scripts] classification
CLI import/reachability result
persistent authority reachability count
compatibility terminology table
```

を残す。

---

## 8. Acceptance Criteria

### P03-AC-01 — CLI classification complete

全 repository-managed analysis CLI entry point が明示分類され、未分類 entry point = 0。

### P03-AC-02 — Low-level utility no persistence

`LOW_LEVEL_UTILITY` から:

```text
retired legacy runtime authority
Product persistence lifecycle authority
```

への active ownership/reachability = 0。

### P03-AC-03 — Portable manifest boundary

代表 low-level CLI が local input/output のみで実行でき、manifest が canonical Product persistent identity を生成/主張しない。

### P03-AC-04 — Auditable boundary

```text
AUDITABLE_PRODUCT_CLI = 0
```

または、存在する全 auditable CLI が canonical Product Execution submission を使用する。

独自 persistent lifecycle owner = 0。

### P03-AC-05 — Compatibility terminology evidence

material legacy-named Product contracts が evidence により分類され、名称だけを legacy runtime dependency と誤判定していない。

### P03-AC-06 — Prior G07 boundaries preserved

P01 runtime/deployment/shared-science boundary と P02 Product-only bootstrap boundary が PASS を維持する。

すべて PASS で P03 `COMPLETE`。

P03 は `G07 PASS`、`TD-005 CLOSED`、`READY_FOR_TEST` を宣言しない。

---

## 9. Checkpoint Report

作成先:

```text
docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G07/Trial01/packages/
E4-G07_01_P03_implementation_checkpoint_report.md
```

最低内容:

```text
# E4-G07 Trial01 P03 Implementation Checkpoint
Status: COMPLETE | BLOCKED
Entry SHA:
P02 checkpoint SHA:
Checkpoint SHA:

## Facts Established
- actual CLI entry points
- classification
- low-level no-persistence result
- auditable CLI presence/absence
- compatibility terminology facts

## Changes
- production
- tests
- docs/report

## Verification
- command
- PASS/FAIL
- material findings

## CLI Classification
- entry point / target / classification / persistence authority / evidence

## Compatibility Inventory
- name / consumer / classification / action / evidence

## Acceptance
P03-AC-01 PASS/FAIL
P03-AC-02 PASS/FAIL
P03-AC-03 PASS/FAIL
P03-AC-04 PASS/FAIL
P03-AC-05 PASS/FAIL
P03-AC-06 PASS/FAIL

## P04 Entry
- fixed facts from P01-P03
- actual Product migration head
- residual legacy inventory
- all G07 guard test paths
```

report commit SHA が事前に不明なら:

```text
Checkpoint SHA = PENDING — repository commit containing this checkpoint
```

でよい。P04 は actual committed SHA を取得する。

---

## 10. P04 Handoff

P03 COMPLETE 後:

```text
06_G07_P04_gate_completion_instruction.md
```

へ進む。

引き渡し:

```text
P01/P02/P03 checkpoint SHAs
runtime/deployment/shared boundary evidence
Product-only bootstrap + PostgreSQL evidence
CLI classification + no-persistence evidence
compatibility terminology inventory
actual Product migration head
all G07-specific tests
residual legacy inventory
```

P04 が Gate-wide regression、TD-005 closure candidate 判定、fixed implementation/test candidate freeze を行う。
