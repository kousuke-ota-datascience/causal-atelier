# Test / Audit Agent 作業開始プロンプト

**Document class:** Operator Artifact / Agent Entry Prompt  
**Self-containment:** MUST for routing — variables / path derivation / candidate identification / output / stop ruleを本prompt内に持つ。Acceptance semanticsは特定された07 primary contractに含まれる。

以下の変数を、この作業のexecution parametersとする。

```text
PROJECT_NAME={{PROJECT_NAME}}
ENHANCE_ID={{ENHANCE_ID}}
ENHANCE_SHORT_ID={{ENHANCE_SHORT_ID}}
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
WORK_DIR_NAME={{WORK_DIR_NAME}}
REMOTE_NAME={{REMOTE_NAME}}
BRANCH_NAME={{BRANCH_NAME}}
```

## 1. Derived variables

```text
WORK_ROOT=docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}
TEST_INSTRUCTION_DIR={{WORK_ROOT}}/10_enhance_instruction/{{GATE_ID}}
TEST_INSTRUCTION_ID=07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_test_instruction
TEST_INSTRUCTION_FILE={{TEST_INSTRUCTION_ID}}.md
IMPLEMENTATION_REPORT_DIR={{WORK_ROOT}}/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}
COMPLETION_REPORT_PATTERN={{IMPLEMENTATION_REPORT_DIR}}/*_{{GATE_ID}}_{{TRIAL_NO}}_implementation_completion_report.md
TEST_REPORT_DIR={{WORK_ROOT}}/30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}
```

`{{VARIABLE_NAME}}`を再帰展開し、未解決`{{...}}`を残して実行してはならない。

## 2. Audit instruction

以下Test / Audit指示書を実行せよ。

```text
{{TEST_INSTRUCTION_DIR}}/{{TEST_INSTRUCTION_FILE}}
```

指定fileが存在しない場合、類似名を任意に選択せず停止せよ。

## 3. Fixed Candidate identification — FIRST

Completion Reportを特定し、そこからFixed Trial Candidate SHAを取得せよ。

次を記録すること。

- Fixed Trial Candidate SHA
- actual Tested Repository State / HEAD
- 両者が異なる場合のdiff
- post-candidate change classification

candidate identityが確定できない場合、本体Acceptance Testを続行せず`BLOCKED`とする。

Work Package checkpoint / Coding self-checkをGate PASSの代替証拠として扱ってはならない。

## 4. Test evidence

Test Contractに従い、各Test Item Reportと必要な999 Gate Decisionを以下へ記録せよ。

```text
{{TEST_REPORT_DIR}}/
```

## 5. Repository recording

Test / Audit artifact作成後:

```bash
git add docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}/;\
git status;\
git commit -m "{{ENHANCE_ID}} Gate {{GATE_ID}} Trial {{TRIAL_NO}} test";\
git push -u {{REMOTE_NAME}} {{BRANCH_NAME}};\
git log -1
```

最後に以下を明示して停止せよ。

- Gate ID
- Trial No.
- Fixed Trial Candidate SHA
- Tested Repository State
- final audit status
- Gate Decision
- test artifact commit SHA
