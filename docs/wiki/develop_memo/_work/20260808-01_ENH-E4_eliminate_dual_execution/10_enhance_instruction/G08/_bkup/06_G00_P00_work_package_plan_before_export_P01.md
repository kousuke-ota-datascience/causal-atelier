# ENH-E4 / G08 P00 — Work Package Plan

## 1. 目的

G08 は ENH-E4 の最終 Gate である。

テーマ:

```text
E4-G08
Final clean bootstrap and architecture audit
```

G08 の目的は、G01-G07 で成立させた canonical Product architecture を最終状態として統合検証し、残存 Transition Debt をゼロにすることである。

最終状態:

```text
canonical Product Execution
canonical StageExecution
canonical Result
canonical Artifact
canonical typed structural lineage
approved generic-only semantic lineage
Product-only migration/bootstrap
retired legacy boundary
shared scientific capability
```

Transition Debt:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 CLOSED
TD-005 CLOSED
TD-006 CLOSED

OPEN TRANSITION DEBT = 0
```

G08 は新しい authority architecture を設計する Gate ではない。

実行順序は次とする。

```text
TD-006 の実体を確定
    ↓
必要な transition closure を実施
    ↓
最終 architecture を統合検証
    ↓
candidate を固定
    ↓
Independent Test
```

---

# 2. G08 実行原則

## 2.1 Minimum sufficient context

各 Package は、原則として次だけを入力とする。

```text
1. 現在の Package 指示書
2. 本 P00
3. 直前 Package の checkpoint
4. 現行 source / tests / migrations / config
```

過去 Gate の詳細文書は、次の場合のみ参照する。

```text
architecture invariant が不明
mutation semantics が不明
lineage authority が不明
過去 Gate との contradiction が発生
provenance の確認が必要
```

G01-G07 の全文書を通常入力として要求しない。

---

## 2.2 Repo facts first

現在の repository を current implementation fact の第一根拠とする。

調査結果は必要に応じて、

```text
Fact
Interpretation
Unknown
```

を区別する。

名称だけから authority や Transition Debt を判定しない。

---

## 2.3 Positive authority model

G08 で維持する authority model は次である。

```text
Product lifecycle
    -> canonical Execution

stage lifecycle
    -> StageExecution

result ownership
    -> Result

artifact metadata ownership
    -> Artifact

structural lineage
    -> typed structural authority

generic semantic lineage
    -> approved GENERIC_ONLY authority

Product bootstrap
    -> Product migration chain

scientific capability
    -> shared science modules
```

各 Package は、この positive model が成立することを確認する。

過去の代替 architecture を Package ごとに列挙しない。

---

## 2.4 実装は evidence-driven とする

G08 が最終 Gate であること自体は、cleanup の根拠にならない。

実装変更は、

```text
formal G08 AC
または
genuine TD-006 closure
```

に必要な場合だけ行う。

現行 architecture が既に要件を満たしている場合、

```text
production diff = 0
```

は正当な結果である。

---

# 3. Entry State

Formal Gate state:

```text
G01 PASS
G02 PASS
G03 PASS
G04 PASS
G05 PASS
G06 PASS
G07 PASS
```

Transition Debt:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 CLOSED
TD-005 CLOSED
TD-006 OPEN
```

G07 fixed candidate:

```text
8e4d7cd6119bc995fca7ea44183bfc7d13ed3445
```

G07 Independent Test execution HEAD:

```text
0923461bbc724bbfbc6410b7b18793ff4cf2f491
```

G07 Independent Test Contract commit:

```text
b3d03b270f3c64bf380a37a1934d871ba7406696
```

G07 Independent Test report commit:

```text
5edf48a2a2fb38aa8bb3bdfb76373e223b1bf7be
```

G07 時点の Product migration head:

```text
20260809_product_0010
```

これらは provenance であり、G08 の current HEAD ではない。

G08 開始時に現在値を取得する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short

uv run alembic -c alembic_product.ini heads
```

branch:

```text
refactor/ariadne_mvp_e4
```

---

# 4. G08 Acceptance Criteria

G08 には 5 個の mandatory AC がある。

---

## AC-001 — Clean Product bootstrap

空 DB から、

```text
Product-only migration
    ↓
current Product migration head
    ↓
application startup
```

が成功すること。

Canonical bootstrap boundary:

```text
alembic_product.ini
    ->
product_migrations/
```

検証には real PostgreSQL を使用する。

---

## AC-002 — Three-family Golden Path

次の三 family:

```text
Causal
Exploratory
Predictive
```

が共通して、

```text
Execution
    ↓
StageExecution
    ↓
Result
    ↓
Artifact
```

を生成すること。

確認対象:

```text
Execution identity authority
StageExecution persistence
Result ownership
Artifact ownership
common lifecycle ownership
```

---

## AC-003 — Mutation + lineage

次の mutation semantics を確認する。

### Retry

```text
same Execution ID
```

### Rerun

```text
new Execution ID
base_execution_id = original
revision_kind = RERUN
```

Structural projection:

```text
original Execution
    --DERIVED_FROM-->
new Execution
```

### Revise

```text
new Execution ID
base_execution_id = original
revision_kind = REVISED
change_reason preserved
```

Structural projection:

```text
original Execution
    --REVISED_FROM-->
new Execution
```

### Cancel

```text
canonical Execution state transition
```

Lineage authority:

```text
structural relation
    -> typed structural authority

generic-only semantic relation
    -> product_lineage_edge

closure / traversal / export
    -> derived projection
```

---

## AC-004 — Final authority audit

最終状態について次を確認する。

```text
canonical Product Execution
    = sole Product lifecycle authority

Product migration chain
    = sole Product bootstrap authority

typed structural lineage
    = sole structural lineage authority

GenericExecutor
    = subordinate execution mechanism
```

さらに runtime / deployment / bootstrap reachability を確認し、retired architecture が active authority を持たないことを検証する。

---

## AC-005 — Shared science + zero debt

次を同時に満たすこと。

```text
shared scientific capability remains usable

AND

OPEN TRANSITION DEBT = 0
```

---

# 5. G02-G07 Preservation Contract

G08 が維持する既確立 semantics を以下に圧縮する。

## Product lifecycle

```text
one canonical Execution authority
one identity authority
one claim / lease authority
persistent StageExecution
```

## Executor boundary

```text
GenericExecutor
    -> workflow execution implementation

Workflow / Execution
    -> lifecycle owner
```

## Output ownership

```text
Result
Artifact
    -> canonical Product ownership
```

## Family convergence

```text
Causal
Exploratory
Predictive
    -> same Product lifecycle architecture
```

## Lineage

```text
typed structural lineage
    -> structural authority

GENERIC_ONLY lineage
    -> semantic authority
```

## Runtime / bootstrap

```text
Product runtime
    -> canonical Product path

Product bootstrap
    -> Product migration chain

shared science
    -> retained capability
```

この節を、過去 Gate 契約の通常時の代替入力として使用する。

---

# 6. TD-006

TD-006:

```text
temporary compatibility / read projection
```

Exit criterion:

```text
bounded transition removed
OR
explicitly archived
```

G08 の最初の substantive task は、

```text
現在の repository において
TD-006 が具体的に何を指しているか
```

を確定することである。

P01 より前に具体的な削除対象を仮定しない。

---

# 7. TD-006 Classification

P01 では material candidate ごとに次のいずれかを付与する。

```text
REMOVE
ARCHIVE
RETAIN_NON_AUTHORITY
RETAIN_SHARED_CAPABILITY
NOT_TD
```

## REMOVE

現在も temporary transition だが、既に不要となっているもの。

---

## ARCHIVE

active transition としては終了しており、historical purpose で保持するもの。

物理削除は必須ではない。

---

## RETAIN_NON_AUTHORITY

現在も意図的な consumer を持つ stable contract だが、Product authority を持たないもの。

例:

```text
read compatibility
serialized compatibility field
stable external/internal data contract
```

---

## RETAIN_SHARED_CAPABILITY

scientific/shared capability として保持するもの。

---

## NOT_TD

調査の結果、Transition Debt ではないと確定したもの。

---

# 8. TD-006 Inventory Format

P01 の inventory は material candidate ごとに最低限以下を記録する。

```text
surface / path

current consumer

runtime reachable?
deployment reachable?
bootstrap reachable?

persistent authority?
new-write authority?

compatibility consumer?
shared capability?

temporary transition?

classification

required action

evidence
```

最終的に material candidate に未分類を残さない。

---

# 9. G07 からの Known Residual

以下は P01 の調査開始点とする。

判定結果そのものとして固定しない。

## `src/ariadne/legacy/`

G07 時点:

```text
runtime reachable      no
deployment reachable   no
bootstrap reachable    no
persistent authority   no
```

---

## root `alembic.ini` / `migrations/`

G07 時点:

```text
Product bootstrap authority = none
historical migration surface
```

---

## shared scientific modules

代表例:

```text
ariadne.causal
ariadne.preprocessing
ariadne.shared
ariadne.scientific
```

期待 role:

```text
RETAIN_SHARED_CAPABILITY
```

---

## standalone scientific CLI

G07 時点:

```text
low-level utility
non-persistent
non-lifecycle-owner
```

---

## compatibility / read projection

G07 で残された主な TD-006 investigation target。

P01 で actual consumer と semantics を確認する。

---

# 10. Work Package Structure

G08 は以下の 4 Package で進める。

```text
P01
TD-006 inventory / closure decision

P02
transition closure

P03
final integrated verification

P04
candidate freeze / completion
```

Package の責務は重複させない。

---

# 11. P01 — TD-006 Inventory / Closure Decision

ファイル:

```text
06_G08_P01_td006_inventory_and_closure_decision.md
```

目的:

```text
TD-006 の actual scope を確定する
```

Required work:

1. G08 entry SHA を記録する。
2. current Product migration head を記録する。
3. G07 residual を current repository 上で再確認する。
4. compatibility/read-projection candidate の current consumer を特定する。
5. material candidate を Section 7 で分類する。
6. genuine TD-006 を特定する。
7. P02 の必要作業を確定する。

P01 の主要出力:

```text
authoritative TD-006 inventory
```

P01 が答えるべき問い:

```text
何が genuine TD-006 なのか

その closure action は何か
```

Checkpoint:

```text
20_implementation_reports/G08/Trial01/packages/
E4-G08_01_P01_implementation_checkpoint_report.md
```

---

# 12. Independent Test Contract

P01 により actual TD-006 scope が確定した後、final candidate freeze より前に Independent Test 指示書を作成する。

```text
10_enhance_instruction/G08/
07_Ariadne_ENH-E4_G08_テスト指示書.md
```

Test contract は以下から構成する。

```text
G08 AC-001..005
+
P01 で確定した TD-006 scope
```

Test contract commit SHA を記録する。

Independent Test 実行前に、その commit が fixed candidate の ancestor であることを確認する。

---

# 13. P02 — Transition Closure

ファイル:

```text
06_G08_P02_transition_closure.md
```

Input:

```text
P01 TD-006 inventory
```

目的:

```text
genuine TD-006 を exit criterion に到達させる
```

処理:

```text
REMOVE
    -> transition を除去

ARCHIVE
    -> non-active historical status を明示

RETAIN_NON_AUTHORITY
    -> stable non-authority contract であることを確認

RETAIN_SHARED_CAPABILITY
    -> 保持

NOT_TD
    -> ENH-E4 cleanup 対象外
```

P02 は P01 で必要性が確認された変更だけを行う。

必要な production change が存在しなければ、

```text
production diff = 0
```

でもよい。

Checkpoint:

```text
20_implementation_reports/G08/Trial01/packages/
E4-G08_01_P02_implementation_checkpoint_report.md
```

---

# 14. P03 — Final Integrated Verification

ファイル:

```text
06_G08_P03_final_integrated_verification.md
```

目的:

```text
current candidate architecture が
G08 AC-001..005 を統合的に満たすことを検証する
```

---

## P03-A Clean bootstrap

Real PostgreSQL で、

```text
empty DB
    ↓
Product migration
    ↓
current Product head
    ↓
application startup
```

を確認する。

---

## P03-B Three-family Golden Path

```text
Causal
Exploratory
Predictive
```

について、

```text
Execution
StageExecution
Result
Artifact
```

を確認する。

---

## P03-C Mutation

```text
retry
rerun
revise
cancel
```

について、Section 4 の semantics を確認する。

---

## P03-D Lineage

確認対象:

```text
typed structural authority
GENERIC_ONLY semantic authority
derived closure/export
```

---

## P03-E Authority audit

Section 2.3 の positive authority model が current runtime / deployment / bootstrap で成立していることを確認する。

---

## P03-F Shared science

representative shared scientific capability が利用可能であることを確認する。

---

## P03-G Protected regression

G02-G07 の preservation contract を代表する regression test を実行する。

個別 Gate の test suite 全量を機械的に再実行する必要はない。

current architecture の protected semantics を十分にカバーする test selection を使用する。

Checkpoint:

```text
20_implementation_reports/G08/Trial01/packages/
E4-G08_01_P03_implementation_checkpoint_report.md
```

---

# 15. P04 — Gate Completion / Candidate Freeze

ファイル:

```text
06_G08_P04_gate_completion_instruction.md
```

目的:

```text
Independent Test に渡す
one fixed implementation/test candidate を確定する
```

Required work:

1. P01-P03 の completion を確認する。
2. G08 AC-001..005 の evidence matrix を作成する。
3. TD-006 inventory の全 item が resolved していることを確認する。
4. implementation-side state として、

   ```text
   TD-006 = CLOSURE_CANDIDATE
   OPEN TRANSITION DEBT = 0
   ```

   を確認する。
5. final verification を実行する。
6. repository hygiene を確認する。
7. fixed candidate SHA を記録する。
8. Independent Test Contract SHA と ancestor proof を記録する。
9. implementation completion report を作成する。
10. 条件を満たした場合のみ `READY_FOR_TEST` とする。

Completion report:

```text
20_implementation_reports/G08/Trial01/
E4-G08_01_implementation_completion_report.md
```

P04 は formal Gate PASS を判定しない。

---

# 16. PostgreSQL Verification

DB semantics が material な検証では real PostgreSQL を使用する。

Standard runner:

```bash
scripts/test/run_product_postgres_tests.sh \
  <pytest-path-or-node> \
  [pytest-options]
```

Real PostgreSQL を必要とする主な対象:

```text
migration
clean bootstrap
application startup
Execution persistence
StageExecution persistence
Result / Artifact persistence
mutation persistence
lineage persistence
```

G08 は pre-production / clean rebuild 前提である。

DB reset が必要な場合は canonical Product migration により再構築する。

---

# 17. Trial Rule

Current Trial:

```text
Trial01
```

Trial number は、

```text
formal Independent Test FAIL
```

の後だけ増加する。

P01-P04 内の implementation/self-test failure は Trial01 内で修正する。

---

# 18. Checkpoint Rule

各 Package checkpoint は最低限次を記録する。

```text
status
entry SHA
checkpoint SHA
files changed
facts established
work performed
tests / commands
remaining issue
Unknown
next entry condition
```

status:

```text
COMPLETE
BLOCKED
```

Checkpoint は Gate PASS を宣言しない。

---

# 19. Fixed Candidate Rule

Independent Test 前に、

```text
one fixed implementation/test candidate SHA
```

を確定する。

その後 documentation commit が存在してもよい。

ただし Independent Test report では、

```text
fixed candidate
test execution HEAD
test report commit
```

を区別する。

SHA が異なる場合は candidate equivalence を確認する。

---

# 20. TD-006 Closure Condition

Implementation-side closure candidate は、P01 の全 material candidate が次のいずれかに解決された状態とする。

```text
REMOVE
ARCHIVE
RETAIN_NON_AUTHORITY
RETAIN_SHARED_CAPABILITY
NOT_TD
```

かつ genuine active bounded transition が、

```text
0
```

であること。

P01-P04 は、

```text
TD-006 = CLOSURE_CANDIDATE
```

までを扱う。

Formal:

```text
TD-006 CLOSED
```

は Independent Test が判定する。

---

# 21. G08 Completion Matrix

P04 の completion report には最低限以下を含める。

| AC     | Evidence                                                                           |
| ------ | ---------------------------------------------------------------------------------- |
| AC-001 | empty DB → Product migration → application startup                                 |
| AC-002 | Causal / Exploratory / Predictive → Execution / StageExecution / Result / Artifact |
| AC-003 | retry / rerun / revise / cancel + lineage                                          |
| AC-004 | final authority model / reachability audit                                         |
| AC-005 | shared science + TD-006 closure candidate + zero open debt                         |

Prior Gate PASS は provenance として利用できる。

Current G08 verification の代替にはしない。

---

# 22. Independent Test の最終判定

Formal G08 PASS 条件:

```text
E4-G08-AC-001 PASS
E4-G08-AC-002 PASS
E4-G08-AC-003 PASS
E4-G08-AC-004 PASS
E4-G08-AC-005 PASS
```

Transition Debt:

```text
TD-001 CLOSED
TD-002 CLOSED
TD-003 CLOSED
TD-004 CLOSED
TD-005 CLOSED
TD-006 CLOSED

OPEN TRANSITION DEBT = 0
```

Formal decision vocabulary:

```text
PASS
FAIL
BLOCKED
```

---

# 23. Recommended Independent Test Report Structure

```text
30_test_report/G08/Trial01/
├── E4-G08_01_001_candidate_identity.md
├── E4-G08_01_002_clean_bootstrap_startup.md
├── E4-G08_01_003_three_family_golden_path.md
├── E4-G08_01_004_mutation_lineage.md
├── E4-G08_01_005_final_authority_audit.md
├── E4-G08_01_006_shared_science_transition_debt.md
├── E4-G08_01_007_protected_final_regression.md
└── E4-G08_01_999_gate_decision.md
```

最終的な item 分割は Independent Test 指示書で確定する。

G08 AC-001..005 の意味は変更しない。

---

# 24. 次工程

P00 完了後、次を作成する。

```text
10_enhance_instruction/G08/
06_G08_P01_td006_inventory_and_closure_decision.md
```

P01 は本 P00 の共通ルールを再掲しない。

P01 に必要なのは次だけである。

```text
Objective
Entry facts
Known residual candidates
Investigation procedure
Classification output
Acceptance criteria
Checkpoint
P02 handoff
```

---

# 25. P00 Exit

P00 完了時点で確立される execution contract:

```text
G08 AC-001..005

G02-G07 preservation contract

TD-006 discovery-first

five classification outcomes

P01 -> P02 -> P03 -> P04

real PostgreSQL for DB semantics

Independent Test Contract before candidate freeze

one fixed candidate

OPEN TRANSITION DEBT = 0
```

P00 自体は、

```text
production behavior を変更しない
Transition Debt を close しない
G08 AC を PASS 判定しない
```

P00 の役割は、G08 を実行するための最小共通コンテキストを確立することである。
