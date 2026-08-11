# E4-G05 Trial 01 — Phase B Exploratory Convergence Implementation Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Gate name: Product Execution Convergence
- Trial: `01`
- Phase: `B`
- Phase name: Exploratory canonical read/output convergence
- Baseline checkpoint: `b8a3f5502f82fcca8cb9634bd8368e3ebc9f0344`
- Phase A status: `PHASE_A_COMPLETE`
- Product migration head at Phase A completion: `20260809_product_0010`

---

# 1. Purpose

E4-G05 Trial 01を継続する。

今回は **Phase B — Exploratory convergence のみを完了すること**。

Phase C / D / Eには進まない。

今回のexit conditionは:

```text
PHASE_B_COMPLETE
```

であり、G05全体の:

```text
READY_FOR_TEST
```

ではない。

---

# 2. Source of Truth

参照する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
06_Ariadne_ENH-E4_G05_実装指示書.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G05/
06g01_Ariadne_ENH-E4_G05_PhaseA_実装指示書.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G04/
E4-G04_02_999_gate_decision.md

docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
00_ENH-E4_Current_Architecture_Control_Sheet.md
```

Phase Aで成立したtyped Result / Artifact semanticsを再設計しない。

---

# 3. Start-of-Work Verification

最初にactual repository stateを確認する。

```bash
git branch --show-current
git rev-parse HEAD
git rev-parse b8a3f5502f82fcca8cb9634bd8368e3ebc9f0344^{commit}
git status --short
git log -8 --oneline
git diff b8a3f5502f82fcca8cb9634bd8368e3ebc9f0344..HEAD --stat
```

Expected branch:

```text
refactor/ariadne_mvp_e4
```

Phase A checkpoint以降に変更がある場合は、内容を確認してから継続する。

Phase Aの実装を巻き戻さない。

---

# 4. Phase B Scope

Phase Bの唯一の目的は:

> **new canonical Exploratory Execution / Result / Artifactを、既存のExploratory Product-facing read / downstream-draft surfaceからcanonical authorityとして読める状態へ収束させる。**

Phase Bで対象とする主なsurface:

```text
get_execution
list_executions

list_results
get_result

create_analysis_draft

Exploratory API response projection
```

Exploratory submit自体は既にcanonical pathへ切替済みであるため、Phase Bではそのcontractを維持する。

---

# 5. Verified Current Gap

baseline/current sourceでは、Exploratory execution readはcanonical pathへ部分的に移行済みである。

一方、少なくとも以下はold Family ORMをread authorityとして使用している。

```text
ExploratoryWorkspaceService.list_results()
    -> FamilyResultOrm

ExploratoryWorkspaceService.get_result()
    -> FamilyResultOrm

ExploratoryWorkspaceService.create_analysis_draft()
    -> FamilyResultOrm
    -> FamilyExecutionOrm
```

Web API側のResult projectionも:

```text
_result(row: FamilyResultOrm)
```

を前提としている。

Phase Bではこのnew canonical data read gapを閉じる。

---

# 6. Canonical Read Authority

## 6.1 Execution

new Exploratory Executionは:

```text
canonical Execution repository/service
```

をread authorityとする。

既にcanonical化されている:

```text
get_execution
list_executions
```

を壊さない。

必要ならprojection implementationを整理してよいが、Phase BのためだけにExecution lifecycle semanticsを変更しない。

## 6.2 Result

new Exploratory Resultは:

```text
canonical Product Result
```

をread authorityとする。

Required:

```text
result_id
project ownership
execution_id
StageExecution association
result_level
result_type
scientific status
summary
payload
diagnostics
warnings
created_at
schema/version metadata
```

をfamily-facing responseへlosslessにprojectionできること。

Phase Aで保存したfamily-specific ResultType / ScientificStatusをgeneric valueへ戻してはならない。

## 6.3 Artifact

Phase BでAPIに明示的Artifact endpointが存在しない場合、新endpointを作る必要はない。

ただしExploratory Result projection / downstream operationがArtifact associationを必要とする場合:

```text
canonical Artifact metadata owner
```

から読む。

`FamilyArtifactOrm`をnew canonical outputのread authorityにしてはならない。

---

# 7. Family-Facing Response Compatibility

既存Exploratory API response contractを可能な限り維持する。

Current response concept:

```text
FamilyResultResponse
    result_id
    project_id
    execution_id
    stage_execution_id
    analysis_family
    result_type
    schema_version
    analytical_status
    summary
    payload
    diagnostics
    warnings
    created_at
```

class名に`Family`が残ること自体はarchitecture defectではない。

重要なのは:

```text
source authority = canonical Result
```

であること。

Allowed:

```text
canonical domain Result
    -> Exploratory-facing response projection
```

Forbidden:

```text
new canonical Result
    -> FamilyResultOrm shadow row
    -> response
```

response compatibilityのためにold writeを復活させない。

---

# 8. Schema Version Projection

Phase Aではfamily schema/version informationをcanonical metadata/payloadへlosslessに保持するcontractを成立させた。

Phase Bではfamily-facing responseの:

```text
schema_version
```

へ、そのcanonical stored valueを正しくprojectionする。

禁止:

```text
固定値を無条件に返す
ResultTypeだけから推測する
old FamilyResultOrmから補完する
```

canonical representationのactual field/locationから取得する。

---

# 9. create_analysis_draft Convergence

Current behavior concept:

```text
Exploratory Result
    -> target family CAUSAL or PREDICTIVE
    -> AnalysisSpecificationDraft
```

Phase Bではsource Result / Execution lookupをcanonical authorityへ移す。

Required:

```text
source_result_id = canonical Result ID
source Result belongs to project
source Result belongs to EXPLORATORY canonical Execution
dataset_version_id obtained from canonical Execution
analysis_view_id obtained from canonical Execution/family spec snapshot
```

既存user-visible output contract:

```text
analysis_specification_draft_id
analysis_family
dataset_version_id
analysis_view_id
source_relation
```

を原則維持する。

## 9.1 Typed downstream reuse

G04 contractを維持する。

```text
source_result_id
```

はcanonical Result IDであり:

```text
object_key
content_hash
FamilyResult row locator
```

ではない。

## 9.2 Lineage scope boundary

`create_analysis_draft()` が現在生成する:

```text
MOTIVATED
```

relationをPhase Bで全面再設計しない。

G06 lineage consolidationはfuture Gate。

Phase Bでは:

```text
canonical source Result ID
```

を使ってcurrent compatible relationを生成できることだけを求める。

lineage authorityの最終整理は行わない。

---

# 10. Historical Old-Row Compatibility

G07前なのでhistorical `FamilyResultOrm` / `FamilyExecutionOrm` sourceを削除する必要はない。

必要ならold historical rows用のread-only compatibility pathを残してよい。

ただし明確に分ける。

```text
new canonical execution/result
    -> canonical read authority

historical pre-G05 family row
    -> optional read-only compatibility
```

禁止:

```text
canonical lookup miss
    -> silently old Family tableをauthorityとして探索
```

のようなambiguous dual-readを新architectureとして作ること。

compatibility fallbackが必要な場合は:

```text
explicitly historical
bounded
new canonical IDとの衝突なし
```

をtestする。

---

# 11. Phase B Does NOT Include

今回進めない。

```text
Predictive read projection                 # Phase C
Predictive mutation delegation             # Phase C

old Exploratory claim_next shutdown        # Phase D
old Exploratory process_execution shutdown # Phase D
old Predictive lifecycle shutdown          # Phase D
full old-table row-count negative           # Phase D/E
canonical failure no-fallback final audit   # Phase D/E

cross-family Golden Path final suite        # Phase E
TD-001/002/003 final closure                # Phase E
G05 final implementation report             # Phase E
READY_FOR_TEST                              # Phase E

G06 lineage final consolidation
G07 legacy retirement
```

ただしPhase Bのcanonical readを成立させるために必要なminimal common repository/query extensionは許可する。

---

# 12. Old Write Authority Rule During Phase B

Phase Bではold `claim_next()` / `process_execution()`のshutdownを完了させる必要はない。

しかしPhase B実装のために新たに:

```text
FamilyExecutionOrm write
FamilyStageExecutionOrm write
FamilyResultOrm write
FamilyArtifactOrm write
```

を追加してはならない。

既にcanonical submitしたExploratory executionをread projectionのためにold tableへmirrorしてはならない。

---

# 13. Required Automated Tests

Phase B専用automated testを追加する。

Recommended:

```text
tests/product/test_enh_e4_g05_phase_b_exploratory_projection.py
tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py
```

actual splitは任意。

---

# 14. Mandatory Phase B Test Coverage

## 14.1 Canonical Result list

real PostgreSQLでcanonical Exploratory Resultを作成後:

```text
list_results(project_id)
```

がそのResultを返す。

Assert:

```text
canonical result_id
execution_id
stage_execution_id
analysis_family = EXPLORATORY
typed result_type
scientific status
schema_version
summary
payload
diagnostics
warnings
created_at
```

## 14.2 Canonical Result get

```text
get_result(project_id, result_id)
```

がcanonical Resultを返す。

Fresh Session / UoW後もsame semantic values。

## 14.3 Project / family isolation

Negative:

```text
different project Result -> EntityNotFound/rejected
non-EXPLORATORY canonical Result -> Exploratory get_resultから取得不可
```

## 14.4 API projection

Exploratory Result API projectionがcanonical Resultを:

```text
FamilyResultResponse相当
```

へ変換できる。

`FamilyResultOrm` instanceを必要条件にしてはならない。

## 14.5 create_analysis_draft

canonical Exploratory Resultをsourceに:

```text
target_family = CAUSAL
target_family = PREDICTIVE
```

の必要なケースを検証する。

Must assert:

```text
source_result_id = canonical Result ID
dataset_version_id = canonical Execution value
analysis_view_id = canonical Execution/family spec value
source relation uses canonical Result ID
```

invalid target family negativeも維持する。

## 14.6 No shadow-write

Phase B read/draft operations実行によって:

```text
FamilyResultOrm
FamilyExecutionOrm
```

のnew shadow rowを作らない。

Phase Dのfull row-count auditほど広いmatrixは不要だが、Phase Bがold-writeを追加していないことを直接testする。

---

# 15. Phase A Regression

Phase BはPhase A typed output semanticsに依存する。

Mandatory regression:

```text
tests/product/test_enh_e4_g05_phase_a_postgres.py
```

をstandard PostgreSQL runnerに含める。

At minimum preserve:

```text
Exploratory typed ResultType
schema/version preservation
StageResult ownership
Artifact association
G04 Result/Artifact contract
```

---

# 16. Standard PostgreSQL Verification

real PostgreSQL evidenceは唯一:

```bash
scripts/test/run_product_postgres_tests.sh <actual-test-path-or-node> [...]
```

を使用する。

Example shape:

```bash
scripts/test/run_product_postgres_tests.sh   tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py   tests/product/test_enh_e4_g05_phase_a_postgres.py   tests/product/test_enh_e4_g04_result_artifact_postgres.py   tests/product/test_postgres_contract.py
```

actual pathsに合わせる。

禁止:

```text
manual docker run
manual DSN
manual psql
manual alembic
manual external PostgreSQL
```

test failureがcorrect testによるproduction defectなら修正して再実行する。

---

# 17. Migration Policy

Expected starting head:

```text
20260809_product_0010
```

Phase Bはread/projection convergenceなので:

```text
new migration = NOT REQUIRED by default
```

schema changeを必要とする場合は、本当にPhase B contract上必要か確認する。

Phase A contract不足が発見された場合:

```text
Phase A regression defect
```

としてminimal corrective Product migrationを許可するが、理由をcheckpoint reportへ明記する。

root legacy migrationは変更しない。

---

# 18. Phase B Completion Criteria

以下を全て`DONE`にする。

```text
[ ] Exploratory get_execution canonical read preserved
[ ] Exploratory list_executions canonical read preserved

[ ] Exploratory list_results reads canonical Results
[ ] Exploratory get_result reads canonical Result
[ ] Result project isolation enforced
[ ] Result family isolation enforced

[ ] family-facing Result response accepts canonical Result
[ ] typed result_type preserved
[ ] scientific status preserved
[ ] schema_version preserved
[ ] summary/payload/diagnostics/warnings preserved
[ ] StageExecution association preserved

[ ] create_analysis_draft reads canonical Result
[ ] create_analysis_draft reads canonical Execution context
[ ] canonical Result ID used as source_result_id
[ ] CAUSAL draft case works where supported
[ ] PREDICTIVE draft case works where supported
[ ] invalid target family remains rejected

[ ] Phase B creates no old Family Result/Execution shadow write

[ ] Phase A regression PASS
[ ] relevant G04 regression PASS
[ ] Product PostgreSQL contract PASS
[ ] standard PostgreSQL runner PASS
[ ] git diff --check PASS

[ ] Phase B checkpoint report created
[ ] Phase B checkpoint commit created
```

---

# 19. Phase Checkpoint Report — Mandatory

Phase Bの実行結果を**本instruction fileへ追記しない**。

以下へ独立reportとして出力する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/PhaseB/
E4-G05_01_PhaseB_implementation_checkpoint_report.md
```

このreportはGate-level:

```text
E4-G05_01_implementation_completion_report.md
```

とは別物である。

Gate-level completion reportはPhase E完了後のみ作成する。

---

# 20. Phase Checkpoint Report Format

repository標準Implementation Completion Reportのcommon evidence rulesを継承するが、**Gate completion reportをそのまま名乗らない**。

以下のfield/sectionを必須とする。

```text
# E4-G05 Trial 01 Phase B Implementation Checkpoint Report

- Project
- Enhancement
- Gate
- Trial
- Phase
- Phase Status: PHASE_B_COMPLETE | DESIGN_BLOCKED
- Branch
- Phase baseline checkpoint
- Phase starting commit
- Phase checkpoint implementation commit
- Report commit
- Migration head
- Started at
- Finished at

## 1. Input
- Phase implementation instruction
- Previous phase checkpoint/report

## 2. Scope Implemented

## 3. Files Changed
### Added
### Modified
### Deleted

## 4. Implementation Details

## 5. Automated Test Code Added / Changed

## 6. Migration

## 7. Changes to Passed Gates / Earlier G05 Phases

## 8. Known Limitations / Remaining G05 Work

## 9. Explicit Out-of-Scope Work

## 10. Git Evidence
- git rev-parse HEAD
- git status --short
- diff stat

## 11. Phase Verification Evidence
- exact commands
- exit codes
- passed/failed/skipped counts
- raw evidence paths
- tested checkpoint SHA/state

## 12. Next-Phase Handoff
- Next phase: Phase C
- Ready for Phase C: YES / NO
- Gate READY_FOR_TEST: NO

## 13. Design Block
- Contradiction
- Observed facts
- Impact
- Decision required
```

required fieldに値がない場合:

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を使用し、省略しない。

Phase reportで:

```text
READY_FOR_TEST
Gate PASS
Test Agent handoff
```

を宣言しない。

---

# 21. Phase B Checkpoint Commit

Phase B completion criteriaを全て満たした後にcheckpoint commitを作成する。

Suggested message:

```text
E4-G05 Trial 01 Phase B complete
```

commitには:

```text
Phase B production source
Phase B automated tests
corrective migration if required
Phase B checkpoint report
```

を含めてよい。

ただしreport commitを分ける場合は:

```text
Phase B implementation checkpoint SHA
Phase B report commit SHA
```

をreport内で明確に区別する。

commit前:

```bash
git status --short
git diff --check
git diff --cached --name-status
```

commit後:

```bash
git rev-parse HEAD
git status --short
```

を記録する。

---

# 22. Stop Conditions

今回turnを終了してよいのは以下のみ。

## PHASE_B_COMPLETE

```text
all Phase B completion criteria DONE
standard PostgreSQL verification PASS
Phase B checkpoint report created
Phase B checkpoint commit created
```

最後に:

```text
PHASE_B_COMPLETE
Checkpoint SHA: <full SHA>
Report: <repository-relative path>
```

を報告して停止する。

## DESIGN_BLOCKED

approved G02/G03/G04/G05 architectureでは解消不能なsemantic contradictionがある場合のみ。

必ず:

```text
exact contradiction
actual source/schema evidence
why permitted implementation choice cannot solve it
required human decision
```

をcheckpoint reportへ記録する。

---

# 23. Stop Reasons NOT Accepted

以下を理由に途中停止しない。

```text
FamilyResultOrmをまだ参照している箇所を発見した
router response model修正が必要
create_analysis_draft修正が必要
canonical repository query追加が必要
testがFAILした
Phase C以降が未完了
G05全体が未完了
final implementation reportが未作成
```

今回はG05全体ではなく、**Exploratory Phase Bだけを閉じること**が目的である。

---

# 24. Final Instruction

E4-G05 Trial 01 Phase Bを:

```text
PHASE_B_COMPLETE
```

まで完遂せよ。

Phase B完了後、このrunではPhase Cへ進まないこと。
