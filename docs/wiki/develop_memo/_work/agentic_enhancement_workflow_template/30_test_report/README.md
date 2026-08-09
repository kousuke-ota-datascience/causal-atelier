# 30_test_report — Test / Audit Evidence Specification

# 0. common

## 0.1. Purpose

`30_test_report/` は、Test / Audit Agentが実際に行った検証とGate判定を、
**人間または別のLLMが後から独立に追跡・追試・監査できる粒度**で保存する証跡ディレクトリである。

ここでは次の2種類の文書を扱う。

```text
test item report
  = 1 test itemの実行事実・結果・再現手順

gate decision report
  = 当該Gate / trialのtest item証跡を集約した最終判定
```

## 0.2. Requirement levels

### MUST
常に記載が必要。

### CONDITIONAL MUST
条件該当時に記載が必要。

### SHOULD
再現性・監査性・可読性向上のため推奨。

## 0.3. Common recording rules

### 0.3.1. Identifier format

Test evidenceの識別子は以下で統一する。

```text
Gate ID       : project-defined identifier
Trial ID      : 2-digit zero-padded decimal (01–99)
Test Item ID  : 3-digit zero-padded decimal (001–998)
Test Item 000 : reserved / do not use
Gate Decision : reserved Test Item ID 999
```

**Test Item IDは必ず3桁で記録する。**

許容例:

```text
001
002
010
120
998
```

禁止例:

```text
1
01
item1
000
999   # 通常Test Itemとしては使用不可
```

`999` はGate Decisionを表す予約IDであり、通常のTest Item IDではない。

### 0.3.2. Blank values

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

を用途に応じて使用し、必須fieldを空欄にしない。

### 0.3.3. Commits

Test対象commitは可能な限りfull SHA。

### 0.3.4. Paths

Repository内pathはrepository root相対path。

### 0.3.5. Timestamp

timezone付きISO 8601。

### 0.3.6. Commands

実行commandはコピー&ペーストで再実行可能な完全形。

禁止:

```text
同上
前回と同じ
pytestを実行
関連テストを実行
```

### 0.3.7. Secrets

credential値をreportへ記載しない。
environment variable名と必要条件だけを記録する。

### 0.3.8. Evidence integrity

Test Agentによるsource/test/migration/dependency変更は原則 `NONE`。

変更した場合、通常のPASS証跡として扱わない。

---

# 1. gate decision report

## 1.1. File naming

```text
[GATE]_[trial]_999_gate_decision.md
```

例:

```text
G3_01_999_gate_decision.md
```

## 1.2. Identifier rules

```text
Gate ID       : project-defined identifier
Trial ID      : 2-digit zero-padded decimal (01–99)
Gate Decision : reserved Test Item ID 999
```

例:

```text
G3_01_999_gate_decision.md
```

## 1.3. Purpose

Gate Decision Reportは、当該Gate / trialの個別test item証跡を集約し、
最終Gate判定を記録する。

---

## 1.4. Contents

### 1.4.1. Must

```text
# {{GATE}} Trial {{TRIAL}} Gate Decision

- Project: {{PROJECT_NAME:
  MUST.
  project正式名称。}}

- Enhancement: {{ENHANCE_ID:
  MUST.
  enhancement ID。}}

- Gate: {{GATE:
  MUST.
  filenameと一致。}}

- Trial: {{TRIAL:
  MUST.
  2桁trial。filenameと一致。}}

- Status: {{STATUS:
  MUST.
  PASS / FAIL / BLOCKED のみ。
  PASS:
    当該trialで全MUST test itemが完了し、全required criterionを満たす。
  FAIL:
    implementationまたはrequired test coverageにGate通過不能な欠陥。
  BLOCKED:
    environment/infrastructure等によりdefect判定不能。}}

- Tested implementation commit: {{TESTED_IMPLEMENTATION_COMMIT:
  MUST.
  full SHA。
  全test item reportと一致。}}

- Handoff report path: {{HANDOFF_REPORT_PATH:
  MUST.
  入力implementation completion report path。}}

- Branch: {{BRANCH:
  MUST.
  test対象branch。}}

- Migration head: {{MIGRATION_HEAD:
  CONDITIONAL MUST.
  DB/migration関係Gateではactual head。
  非該当なら N/A。}}

- Test Agent source modification: {{TEST_AGENT_SOURCE_MODIFICATION:
  MUST.
  原則 NONE。}}

## 1. Item Summary

| Item | Name | Status | Report |
|---:|---|---|---|
{{ITEM_SUMMARY_ROWS:
  MUST.
  全required test itemを1行ずつ。
  Item列は3-digit zero-padded Test Item ID（001–998）で記録する。
  999はGate Decision自身の予約IDなので通常test itemとして使用しない。
  Status:
    PASS / FAIL / BLOCKED / NOT_RUN。
  PASS Gateではrequired itemにFAIL/BLOCKED/NOT_RUNがない。}}

## 2. Gate Acceptance Summary

| Acceptance Criterion | Evidence | Status |
|---|---|---|
{{GATE_ACCEPTANCE_ROWS:
  MUST.
  07のGate Acceptance Criteriaを漏れなく列挙。
  Evidenceはtest item report path等。
  Status:
    SATISFIED / NOT_SATISFIED / BLOCKED。}}

## 3. Blocking Findings

{{BLOCKING_FINDINGS:
  MUST.
  PASSなら NONE。
  FAIL/BLOCKEDなら具体findingとevidenceを記載。}}

## 4. Regression Summary

- Required regression scope: {{REQUIRED_REGRESSION_SCOPE:
  MUST.
  07要求scope。不要なら N/A。}}

- Executed: {{REGRESSION_EXECUTED:
  MUST.
  実行report/command索引。
  未実行なら NOT_RUN。}}

- Result: {{REGRESSION_RESULT:
  MUST.
  PASS / FAIL / BLOCKED / NOT_RUN / N/A。}}

## 5. Scientific / Analytical Contract Summary

{{SCIENTIFIC_ANALYTICAL_SUMMARY:
  CONDITIONAL MUST.
  scientific/statistical/analytical invariantを持つGateで、
  contract・evidence・resultを要約。
  非該当なら N/A。}}

## 6. Reproducibility Summary

| Test Item | Report | Primary Command |
|---|---|---|
{{REPRODUCIBILITY_ROWS:
  MUST.
  全MUST test itemについてreport pathと代表command。}}

## 7. Reason for Decision

{{DECISION_REASON:
  MUST.
  Acceptance Criteriaとtest evidenceに基づき、
  なぜPASS/FAIL/BLOCKEDかを論証する。}}

## 8. Next Allowed Action

{{NEXT_ALLOWED_ACTION:
  MUST.
  PASS:
    次Gate Codingのみ許可。
  FAIL:
    同一Gate次trial修正のみ許可。
  BLOCKED:
    block解消までproduct code変更で迂回しない。
  Test Agent自身は次工程へ進まない。}}
```

---

### 1.4.2. Should

```text
## 9. Supplemental Context

- Report generated at: {{REPORT_GENERATED_AT:
  SHOULD.
  timezone付きISO 8601。}}

- Total test window: {{TOTAL_TEST_WINDOW:
  SHOULD.
  最初のtest開始からGate Decisionまで。}}

- Environment summary: {{ENVIRONMENT_SUMMARY:
  SHOULD.
  主要runtime/database/browser/container version要約。}}

- Non-blocking findings: {{NON_BLOCKING_FINDINGS:
  SHOULD.
  Gate通過を妨げないfindings。}}

- Residual risks: {{RESIDUAL_RISKS:
  SHOULD.
  PASS後の既知risk。}}

- Related references: {{RELATED_REFERENCES:
  SHOULD.
  issue/PR/operator decision等。}}
```

---

# 2. test item report

## 2.1. File naming

```text
[GATE]_[trial]_[item]_[test_name].md
```

例:

```text
G3_01_001_schema_contract.md
G3_01_002_leakage_rejection.md
```

## 2.2. Identifier rules

```text
Gate ID      : project-defined identifier
Trial ID     : 2-digit zero-padded decimal (01–99)
Test Item ID : 3-digit zero-padded decimal (001–998)
000          : reserved / do not use
999          : reserved for Gate Decision

Test Item IDは常に3桁で表記し、`1` や `01` へ短縮しない。
```

例:

```text
G3_01_001_schema_contract.md
G3_01_002_leakage_rejection.md
```

## 2.3. Purpose

Test Item Reportは、
**1つの検証目的と、その検証の実行事実・結果・再現手順を記録する単位証跡**である。

---

## 2.4. Contents

### 2.4.1. Must

```text
# {{GATE}} Trial {{TRIAL}} Test {{ITEM}} — {{TEST_NAME}}

- Project: {{PROJECT_NAME:
  MUST.
  project正式名称。}}

- Enhancement: {{ENHANCE_ID:
  MUST.
  enhancement ID。}}

- Gate: {{GATE:
  MUST.
  filenameと一致。}}

- Trial: {{TRIAL:
  MUST.
  2桁trial。}}

- Test item: {{ITEM:
  MUST.
  Test Item IDは3-digit zero-padded decimalで記録する。
  Allowed range: 001–998。
  000はreserved / do not use。
  999はGate Decision専用であり、通常Test Itemには使用しない。
  filenameの[item]と完全一致すること。}}

- Status: {{STATUS:
  MUST.
  PASS / FAIL / BLOCKED / NOT_RUN。}}

- Tested implementation commit: {{TESTED_IMPLEMENTATION_COMMIT:
  MUST.
  actual tested full SHA。}}

- Handoff report path: {{HANDOFF_REPORT_PATH:
  MUST.
  implementation completion report path。}}

- Branch: {{BRANCH:
  MUST.
  actual tested branch。}}

- Migration head: {{MIGRATION_HEAD:
  CONDITIONAL MUST.
  DB/migration testではactual head。
  非該当なら N/A。}}

- Working directory: {{WORKING_DIRECTORY:
  MUST.
  command実行cwd。}}

- Started at: {{STARTED_AT:
  MUST.
  timezone付きISO 8601。}}

- Finished at: {{FINISHED_AT:
  MUST.
  timezone付きISO 8601。}}

- Duration: {{DURATION:
  MUST.
  actual duration。}}

## 1. Purpose

{{PURPOSE:
  MUST.
  検証対象contract/failure mode/invariantを具体化。}}

## 2. Acceptance Criteria

{{ACCEPTANCE_CRITERIA:
  MUST.
  PASS条件を具体的に列挙。
  07のcriterionとの対応を追える表現。}}

## 3. Preconditions / Environment

### Runtime

{{RUNTIME_ENVIRONMENT:
  MUST.
  再現に必要なOS/runtime/package manager/browser等。}}

### External Services

{{EXTERNAL_SERVICES:
  CONDITIONAL MUST.
  PostgreSQL/Redis/external API等。
  なしなら NONE。}}

### Environment Variables

{{ENVIRONMENT_VARIABLE_REQUIREMENTS:
  CONDITIONAL MUST.
  必要変数名と条件。
  secret値は記載しない。
  不要なら NONE。}}

## 4. Commands Executed

{{COMMANDS_EXECUTED:
  MUST.
  実際に実行した全commandを順番に完全形で記載。
  可能ならcommandごとのexit code/timestampも記載。}}

## 5. Exact Result

- passed: {{PASSED_COUNT:
  CONDITIONAL MUST.
  runnerが件数を返す場合の実値。
  非該当なら N/A。}}

- failed: {{FAILED_COUNT:
  CONDITIONAL MUST.
  同上。}}

- skipped: {{SKIPPED_COUNT:
  CONDITIONAL MUST.
  同上。}}

- warnings: {{WARNING_COUNT:
  CONDITIONAL MUST.
  取得可能なら実値。
  非該当なら N/A。}}

- exit code: {{EXIT_CODE:
  MUST.
  primary command actual exit code。}}

## 6. Log / Evidence

### stdout / stderr

{{STDOUT_STDERR:
  MUST.
  判定確認に必要なactual output。
  大量なら要点 + full log path。}}

### Failure traceback / assertion

{{FAILURE_TRACEBACK:
  CONDITIONAL MUST.
  FAIL/BLOCKED原因判定に存在する場合。
  PASS時は N/A。}}

### Artifact paths

{{ARTIFACT_PATHS:
  CONDITIONAL MUST.
  log/coverage/benchmark/screenshot等。
  なしなら NONE。}}

## 7. Findings

{{FINDINGS:
  MUST.
  観察事実。
  推測と分離する。}}

## 8. Required Correction

{{REQUIRED_CORRECTION:
  CONDITIONAL MUST.
  FAIL時は観察された契約違反。
  実装修正方法を設計しない。
  PASS時N/A。
  BLOCKED時はblock解消条件。}}

## 9. Reproduction Procedure

{{REPRODUCTION_PROCEDURE:
  MUST.
  人間が追試する最短手順。
  precondition/cwd/command/service/result確認を含む。}}

## 10. Expected Result

{{EXPECTED_RESULT:
  MUST.
  PASSとなる観測可能な期待結果。
  exit code/response/assertion/threshold等。}}

## 11. Decision Rationale

{{DECISION_RATIONALE:
  MUST.
  actual resultとAcceptance Criteriaを対応づけてStatusを説明。}}

## 12. Source Modification by Test Agent

{{SOURCE_MODIFICATION_BY_TEST_AGENT:
  MUST.
  原則 NONE。}}
```

---

### 2.4.2. Should

```text
## 13. Supplemental Execution Context

- Runtime version commands: {{RUNTIME_VERSION_COMMANDS:
  SHOULD.}}

- Dependency snapshot: {{DEPENDENCY_SNAPSHOT:
  SHOULD.}}

- Random seed: {{RANDOM_SEED:
  SHOULD for stochastic tests.}}

- Test data / fixture identity: {{TEST_DATA_IDENTITY:
  SHOULD when data-dependent.}}

- Resource usage: {{RESOURCE_USAGE:
  SHOULD when performance/timeout-related.}}

- Retry history: {{RETRY_HISTORY:
  SHOULD when retry occurred.}}

- Related evidence: {{RELATED_EVIDENCE:
  SHOULD.}}
```

---

# 3. Relationship between reports

## 3.1. Evidence direction

```text
07 Test Instruction
       ↓
Implementation Completion Report
       ↓
Test Item Reports
       ↓
Gate Decision Report
```

Gate Decision Reportは、個別test item reportに存在しない実行事実を創作しない。

## 3.2. PASS consistency

PASS時:

- tested implementation commitが全reportで一致
- 全MUST test item存在
- required itemにFAIL/BLOCKED/NOT_RUNなし
- Gate Acceptance Criteriaが全てSATISFIED
- blocking finding NONE
- Test Agent source modification NONE
- required regression完了
- required scientific/analytical test完了

## 3.3. FAIL consistency

```text
Gate FAIL reason
  ↓
Acceptance Criterion not satisfied
  ↓
Test Item Report
  ↓
Actual command
  ↓
Actual result / assertion / evidence
```

## 3.4. BLOCKED consistency

BLOCKED時:

- block種別
- blocked item
- product defectと区別不能な理由
- block解消に必要な外部条件
- product code変更で迂回しないこと

を追跡可能にする。

---

# 4. Human re-testability checklist

```text
Q1. どのcommitをtestすればよいか？
Q2. どのdirectoryで実行するか？
Q3. どのserviceが必要か？
Q4. どのenvironment variableが必要か？
Q5. exact commandは何か？
Q6. expected resultは何か？
Q7. actual resultは何か？
Q8. FAILならどのcontract違反か？
Q9. Gate判定はどのevidenceに依存するか？
Q10. Test Agentはsourceを変更していないか？
```
