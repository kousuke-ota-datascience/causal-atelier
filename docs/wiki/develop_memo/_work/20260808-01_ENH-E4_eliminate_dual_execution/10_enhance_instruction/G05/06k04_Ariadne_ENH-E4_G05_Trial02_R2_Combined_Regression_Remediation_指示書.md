# E4-G05 Trial 02 / R2 — Combined Regression Failure Classification and Remediation Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 — eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G05`
- Trial: `02`
- Remediation package: `R2`
- Remediation name: Trial 01 combined regression failure classification and remediation
- Previous remediation: `R1 — COMPLETE`
- R1 implementation/test checkpoint: `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- Current Gate status: `NOT_READY_FOR_TEST`
- Target R2 status: `R2_COMPLETE`
- Expected Product migration head: `20260809_product_0010`

---

# 1. Purpose

E4-G05 Trial 02を継続する。

Trial 01 Independent Test Agentでは、代表的なcombined regressionで:

```text
32 passed
6 failed
exit 1
```

が記録された。

R1では、そのうちPredictive retry isolated failureおよびG03 combined contaminationについて再診断し、

```text
Predictive isolated retry:
PASS

Trial 01 isolated retry failure:
NOT_REPRODUCED
ROOT_CAUSE_UNCONFIRMED

Combined-run contamination:
TEST_FIXTURE_ISOLATION_DEFECT

Isolated G03:
PASS
```

まで閉じた。

R2の目的は、

> Trial 01で残ったcombined regression failuresを1件ずつ実体化し、clean isolated standard runnerで再検証して、真のproduction defectだけを最小修正し、G05 implementation-side regressionを再び全件PASSへ戻すこと

である。

---

# 2. R2 Is Not Report-Format Remediation

今回扱わない。

```text
G05 Implementation Completion Reportの全面再生成
Phase E report-format remediation
READY_FOR_TEST再宣言
Independent Test Agent再実行
G05 Gate Decision
```

report-format failureはR3で扱う。

R2は:

```text
test / fixture / implementation regression
```

だけに集中する。

---

# 3. Do Not Assume “6 Failed = 6 Production Defects”

Trial 01 combined runの6 failureを、そのままproduction defectとみなしてはならない。

各failureを必ず以下に分類する。

```text
IMPLEMENTATION_DEFECT

TEST_FIXTURE_ISOLATION_DEFECT

TEST_CONTRACT_DEFECT

ENVIRONMENT_OR_RUNNER_DEFECT

ALREADY_CLOSED_BY_R1

REPORT_ONLY / NOT_A_RUNTIME_FAILURE

DESIGN_BLOCKED
```

classification before modificationを原則とする。

---

# 4. Source of Truth

最初に以下を実物参照する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
30_test_report/G05/
E4-G05_01_001_*.md
...
E4-G05_01_010_*.md
E4-G05_01_999_gate_decision.md
```

actual filenamesをrepositoryから取得すること。

また:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial02/
E4-G05_02_R1_predictive_retry_remediation_report.md
```

を参照する。

さらにfailureが属するactual test sourceと、
passed G02/G03/G04 authoritative contractを確認する。

---

# 5. Start-of-Work Verification

最初に:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log -20 --oneline
git diff --check
git merge-base --is-ancestor \
  ad3e3e124ee47f9cbaa2470b25263b7289795262 HEAD
echo $?
```

を実行する。

Trial 01 Test Agent reportsはimmutable inputとして扱う。

変更しない。

---

# 6. Build the Trial 01 Failure Ledger First

productionを変更する前に、Trial 01 Test Item 001–010 / 999 / raw evidenceから、
**6 failureをすべて列挙**する。

最低限以下のtableを作る。

| ID | Test node | Trial 01 result | Failure assertion | Suspected state dependency | R1 impact | Isolated rerun required |
|---|---|---|---|---|---|---|

Failure ID:

```text
F-01
F-02
F-03
F-04
F-05
F-06
```

とする。

同じroot causeによる複数failureでも、最初は別行で保持する。

---

# 7. Reconcile the “6 Failed” Count

Trial 01 reportとactual raw evidenceの:

```text
failed node count
test names
failure order
```

が一致することを確認する。

もし:

```text
999 summary says 6 failed
raw pytest shows another count
```

なら差異を記録する。

R2 reportで:

```text
authoritative failure ledger count
```

を確定する。

---

# 8. Mark R1-Closed Failures

R1で実質閉じたfailureをfailure ledger上で明示する。

例:

```text
Predictive retry isolated:
ALREADY_CLOSED_BY_R1

G03 combined state contamination:
TEST_FIXTURE_ISOLATION_DEFECT
isolated PASS
```

ただしTrial 01の6 failureのどのnodeに対応するかをactual evidenceで紐づける。

推測で「この3件だろう」としない。

---

# 9. Isolated Verification Rule

各runtime failureについて、production修正前に:

```text
clean DB
standard runner
single test node or semantically coherent minimal set
```

でisolated再実行する。

形式:

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r2-fXX \
scripts/test/run_product_postgres_tests.sh \
  <actual failing test path/node>
```

各failureごとに:

```text
exact command
tested SHA
evidence dir
exit code
passed
failed
skipped
expected
actual
Facts
Interpretation
```

を残す。

---

# 10. Classification Rules

## A. IMPLEMENTATION_DEFECT

isolated clean DBでも再現し、
authoritative contractとproduction behaviorが一致しない。

Action:

```text
production fix
test hardening if useful
isolated rerun
adjacent regression
```

---

## B. TEST_FIXTURE_ISOLATION_DEFECT

isolatedではPASSし、
combined order/stateでのみFAILする。

さらにactual state contamination originを特定できる。

Action:

```text
fixture/setup cleanup
or
test-specific state isolation
```

ただしproduction behaviorを変えない。

---

## C. TEST_CONTRACT_DEFECT

isolated failureが存在するが、
test expectationがG02/G03/G04/G05 authoritative contractと矛盾する。

Action:

```text
contract evidenceを明示
test expectationを修正
```

「testが落ちるから」だけでは不可。

---

## D. ENVIRONMENT_OR_RUNNER_DEFECT

wrong DB / reset failure / evidence dir / runner issue。

Action:

```text
standardized infrastructure fix
```

production defect扱いしない。

---

## E. ALREADY_CLOSED_BY_R1

R1で:

```text
isolated PASS
root-cause classification complete
required regression PASS
```

まで閉じたfailure。

Action:

```text
R2では再修正しない
ledger上でclosure evidenceのみ参照
```

---

# 11. Combined-State Contamination Must Be Reproduced Deliberately

TEST_FIXTURE_ISOLATION_DEFECTと分類する場合:

```text
isolated PASS
```

だけでは不足。

可能な範囲で:

```text
preceding test A
    ↓
failing test B
```

のminimal ordered setを特定し、
combined-state contaminationを再現する。

目的:

```text
どのtest / fixtureが何を残すのか
```

を明確にすること。

---

# 12. Do Not Make Every Test Globally Empty-DB Dependent

fixture remediationでは、

```text
各test前にDB全DROP
```

のような重い対処を無条件に増やさない。

standard runnerはtest invocation前にclean DBを提供する。

pytest invocation内の個々のtestは:

```text
自身が必要とするrow/stateを明示
自身が作ったstateに依存
他testの残留を前提にしない
```

ことを優先する。

必要ならfixture cleanup / unique project IDs / explicit terminalization等で隔離する。

---

# 13. Preserve Canonical Queue Semantics

R1で確認したglobal claim semanticsをR2で変更しない。

禁止:

```text
retry優先
family優先
test execution ID優先
requested_at hack
```

failureがqueue orderingに関係する場合はR1 evidenceとG02/G03 contractを参照する。

---

# 14. Preserve G02 / G03 / G04 Contracts

R2 remediationで以下を壊さない。

## G02

```text
canonical Execution identity
one canonical claim / lease authority
retry / rerun / revise lifecycle
```

## G03

```text
persistent StageExecution
retry same StageExecution IDs
attempt history
GenericExecutor non-authority
```

## G04

```text
canonical Result ownership
canonical Artifact ownership
typed reuse
physical ArtifactStore boundary
```

---

# 15. Preserve G05 Phase A–D Contracts

R2修正後も以下を維持する。

```text
Phase A:
typed family Result/Artifact semantics

Phase B:
Exploratory canonical read/output projection

Phase C:
Predictive canonical Golden Path
retry / rerun / revise

Phase D:
legacy claim/process explicit reject
legacy lifecycle/write shutdown
no Family new-write authority
no canonical failure fallback
```

---

# 16. No Legacy Authority as a Remediation Shortcut

R2でfailureを直すために以下を復活させない。

```text
FamilyExecution submit
FamilyExecution claim
FamilyStageExecution lifecycle
FamilyResult persistence
FamilyArtifact persistence

canonical miss -> Family fallback

canonical failure -> old process fallback
```

---

# 17. Production Fix Rule

IMPLEMENTATION_DEFECTと確定したfailureのみproductionを修正する。

各production fixについて:

```text
Failure ID
root cause
authoritative contract
minimal code change
why this fixes root cause
why it does not broaden authority
```

を記録する。

複数failureが同じroot causeなら1修正でよい。

---

# 18. Test Fix Rule

test/fixture修正の場合は:

```text
why production behavior is correct
why existing test setup is invalid or state-dependent
what isolation invariant is added
```

を記録する。

assertionを単純に削除・弱化しない。

---

# 19. Required R2 Isolated Verification

各F-01〜F-06について最終状態を必ず以下のいずれかにする。

```text
PASS_ISOLATED

CLOSED_BY_R1

NOT_RUNTIME_FAILURE

DESIGN_BLOCKED
```

R2_COMPLETEには:

```text
DESIGN_BLOCKED = 0
```

が必要。

---

# 20. Re-run the Original Combined Scope

個別remediation完了後、
Trial 01で失敗した**元のcombined regression scope**を、
standard runnerで再実行する。

可能ならTest Agent reportに記録されたactual commandをそのまま使う。

形式:

```bash
ARIADNE_TEST_EVIDENCE_DIR=/tmp/ariadne-g05-t02-r2-combined \
scripts/test/run_product_postgres_tests.sh \
  <original G05 + G02/G03/G04 regression scope>
```

Expected:

```text
exit 0
failed = 0
```

ただし、Trial 01 combined command自体がfixture-isolation contract上不適切であることがR2で確定した場合:

```text
original command
    -> known invalid combined-state composition

corrected semantically-equivalent standardized invocations
    -> all PASS
```

をreportする。

この場合、なぜ分割が必要かを具体的に説明する。

---

# 21. If Original Combined Invocation Still Fails Only Due Known Fixture Isolation

以下を満たす場合のみ、
original all-in-one invocationのexit 1をR2 completion blockerとしなくてよい。

```text
[ ] each failing node isolated PASS
[ ] contamination origin identified
[ ] fixture-isolation defect documented
[ ] production contract unchanged/correct
[ ] corrected standardized test partition exists
[ ] every acceptance contract covered
[ ] no actual runtime defect remains
```

単に:

```text
isolatedで通るからOK
```

では不十分。

---

# 22. Recommended Test Partition

G03等にglobal-empty assumptionsが残る場合、
acceptance bundleをsemantic partitionsへ分ける。

例:

```text
Bundle A:
G05 family convergence / G02 / G04

Bundle B:
G03 isolated StageExecution contract

Bundle C:
Predictive retry

Bundle D:
Predictive rerun/revise
```

actual failure analysisに基づいて最小化する。

---

# 23. Mandatory Post-Remediation Regression

最低限:

```text
R1 Predictive isolated retry

G02 claim/lifecycle

G03 StageExecution

G04 Result/Artifact

Phase B Exploratory

Phase C C1
Phase C C2
Phase C C3a
Phase C C3b
Phase C C4

Phase D D1
Phase D D2
Phase D D3
```

の関連testをfinal regressionへ含める。

---

# 24. Standard PostgreSQL Runner Only

real PostgreSQL:

```bash
scripts/test/run_product_postgres_tests.sh ...
```

のみ。

禁止:

```text
manual docker
manual DSN
manual psql
manual Alembic
ad-hoc external PostgreSQL pytest
```

---

# 25. Non-PostgreSQL Regression

R2修正が:

```text
service construction
DI
boundary
domain
repository pure behavior
```

へ影響した場合は関連unit/boundary testも実行する。

exact command / exit codeを記録する。

---

# 26. Migration Policy

Expected:

```text
20260809_product_0010
```

R2 regression remediationでは原則:

```text
new migration = NONE
```

schema defectが真に原因の場合のみ例外。

old Family table dropは禁止。

---

# 27. R2 Completion Criteria

以下を全てDONEにする。

```text
[ ] Trial 01 six-failure ledger complete

[ ] all six failures mapped to actual test nodes/evidence

[ ] R1-closed failures explicitly identified

[ ] every remaining runtime failure isolated rerun complete

[ ] each failure root cause classified

[ ] no unclassified failure remains

[ ] production fixes only for confirmed IMPLEMENTATION_DEFECT

[ ] fixture fixes only for confirmed isolation defects

[ ] no assertion weakened without contract evidence

[ ] R1 retry remains PASS

[ ] G02 regression PASS

[ ] G03 isolated regression PASS

[ ] G04 regression PASS

[ ] Phase B regression PASS

[ ] Phase C regressions PASS

[ ] Phase D regressions PASS

[ ] no Family new-write authority reintroduced

[ ] no canonical failure fallback introduced

[ ] original combined scope re-run OR
    corrected standardized partition justified and PASS

[ ] all acceptance-covered runtime tests failed = 0

[ ] migration head verified

[ ] git diff --check PASS

[ ] R2 checkpoint commit created

[ ] R2 remediation report created
```

---

# 28. R2 Checkpoint Commit

production/test/fixture remediation完了後にcheckpoint commit。

Suggested:

```text
E4-G05 Trial 02 R2 combined regression remediation
```

commit前:

```bash
git status --short
git diff --check
git diff --cached --name-status
```

Trial 01 Test Agent reportsをstageしない。

commit後:

```bash
git rev-parse HEAD
git status --short
```

---

# 29. R2 Remediation Report

作成:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G05/Trial02/
E4-G05_02_R2_combined_regression_remediation_report.md
```

---

# 30. R2 Report Required Metadata

```text
# E4-G05 Trial 02 R2 Combined Regression Remediation Report

- Gate
- Trial
- Remediation package
- Status
- Branch
- Trial 01 failed implementation SHA
- R1 checkpoint
- R2 starting commit
- R2 checkpoint commit
- Migration head
- Started at
- Finished at
```

値なしfieldは:

```text
N/A
NONE
UNKNOWN
NOT_RUN
```

---

# 31. R2 Report Required Sections

```text
## 1. Trial 01 Failure Input

## 2. Six-Failure Ledger

## 3. R1 Closure Mapping

## 4. Isolated Reproduction Matrix

## 5. Root Cause Classification
### F-01
### F-02
### F-03
### F-04
### F-05
### F-06

## 6. Remediation
### Production Fixes
### Test / Fixture Fixes
### Runner Fixes
Use N/A where not applicable.

## 7. Files Changed

## 8. Original Combined Scope Re-run

## 9. Corrected Standardized Test Partition
if required

## 10. G02 / G03 / G04 Regression

## 11. G05 Phase Regression
### Phase B
### Phase C
### Phase D
### R1

## 12. No-Legacy-Authority Regression

## 13. Migration

## 14. Exact Verification Evidence
For each run:
- command
- evidence dir
- tested SHA/state
- exit code
- passed/failed/skipped
- expected
- actual
- Facts
- Interpretation

## 15. Git Evidence

## 16. Remaining Trial 02 Work

## 17. R2 Decision
R2_COMPLETE | DESIGN_BLOCKED
```

---

# 32. Facts vs Interpretation

failure分類ごとに必ず分ける。

Example:

```text
Facts:
- F-03 fails only when executed after X.
- Isolated F-03 passes on clean standard runner.
- X leaves a QUEUED Execution with requested_at earlier than F-03 target.

Interpretation:
- production claim_next follows FIFO contract.
- F-03 assumes global queue emptiness that its own setup does not enforce.
- classification = TEST_FIXTURE_ISOLATION_DEFECT.
```

---

# 33. R2 Report Commit Procedure

R2 checkpoint commit後にreportを作る。

initial:

```text
Report commit: PENDING
```

report initial commit:

```text
E4-G05 Trial 02 R2 remediation report
```

SHA取得後、
Report commit fieldへinitial report commit SHAを記録。

必要ならmetadata correction commit。

self-referenceしない。

---

# 34. Remaining Work After R2

R2完了後は:

```text
R3:
G05 Implementation Completion Report
template-compliant full regeneration

Final Trial 02 acceptance:
fixed implementation SHA
full acceptance verification
READY_FOR_TEST
```

を残す。

R2ではreport-format remediationへ進まない。

---

# 35. Stop Reasons NOT Accepted

以下を途中停止理由として認めない。

```text
6 failuresを一覧化した

isolatedでは通った

fixture問題だと分かった

combined commandが不適切だった

production defectを1件修正した

残りfailureが別原因だった

regressionをまだ回していない

R3が残っている
```

R2 scope内failureはすべて分類・closureする。

---

# 36. DESIGN_BLOCKED

許可するのは:

```text
passed G02/G03/G04/G05 contract同士が矛盾し、
test/fixture/productionの局所修正では
正しいbehaviorを一意に決められない
```

場合のみ。

単なる複数failure、fixture contamination、production bugはDESIGN_BLOCKEDではない。

---

# 37. Final Stop Condition

正しい終了条件:

```text
R2_COMPLETE
```

最後に必ず:

```text
E4-G05 Trial 02
R2_COMPLETE

R1 checkpoint:
ad3e3e124ee47f9cbaa2470b25263b7289795262

R2 checkpoint:
<full SHA>

Trial 01 failure ledger:
6 / 6 classified

IMPLEMENTATION_DEFECT:
<count>

TEST_FIXTURE_ISOLATION_DEFECT:
<count>

TEST_CONTRACT_DEFECT:
<count>

ENVIRONMENT_OR_RUNNER_DEFECT:
<count>

ALREADY_CLOSED_BY_R1:
<count>

Remaining unclassified:
0

Runtime acceptance failures after remediation:
0

Predictive isolated retry:
PASS

G02:
PASS

G03 isolated:
PASS

G04:
PASS

Phase B:
PASS

Phase C:
PASS

Phase D:
PASS

Family old-authority writes:
NONE

Canonical failure -> old fallback:
NONE

Migration head:
20260809_product_0010

Remaining Trial 02:
- R3 G05 completion report format remediation
- final Trial 02 acceptance / READY_FOR_TEST

Gate:
NOT_READY_FOR_TEST
```

を報告して停止する。

R2完了後、このrunでR3へ進まないこと。
