# Coding Agent 作業開始プロンプト — WORK_PACKAGE

以下の変数を、この作業のexecution parametersとする。

```text
PROJECT_NAME={{PROJECT_NAME}}
ENHANCE_ID={{ENHANCE_ID}}
ENHANCE_SHORT_ID={{ENHANCE_SHORT_ID}}
GATE_ID={{GATE_ID}}
PACKAGE_ID={{PACKAGE_ID}}
TRIAL_NO={{TRIAL_NO}}
WORK_DIR_NAME={{WORK_DIR_NAME}}
REMOTE_NAME={{REMOTE_NAME}}
BRANCH_NAME={{BRANCH_NAME}}
```

## 1. Derived variables

```text
WORK_ROOT=docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}
INSTRUCTION_DIR={{WORK_ROOT}}/10_enhance_instruction/{{GATE_ID}}
IMPLEMENTATION_INSTRUCTION_ID=06_{{GATE_ID}}_{{PACKAGE_ID}}
IMPLEMENTATION_INSTRUCTION_PATTERN={{IMPLEMENTATION_INSTRUCTION_ID}}_*.md
IMPLEMENTATION_REPORT_DIR={{WORK_ROOT}}/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/packages
IN_PROGRESS_REPORT_FILE={{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_in_progress.md
CHECKPOINT_REPORT_FILE={{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_implementation_checkpoint_report.md
```

`{{VARIABLE_NAME}}`を再帰的に展開せよ。未解決`{{...}}`を残して実行してはならない。

## 2. Execution instruction

以下を実行せよ。

```text
{{INSTRUCTION_DIR}}/{{IMPLEMENTATION_INSTRUCTION_PATTERN}}
```

remediation package `Rxx`は`fail_rework_coding_agent_prompt.md`および08 Remediation Instructionに従う。本promptの標準planned packageはP01-P99である。

対象globに複数ファイルが一致し、対象を一意に決定できない場合は任意選択してはならない。

Work Package scopeを越えて実装してはならない。

## 3. Execution status report

実装が完了、中断、または継続不能になったら、`implementation_checkpoint_report`とは別に以下へ状況報告を記録せよ。

```text
{{IMPLEMENTATION_REPORT_DIR}}/{{IN_PROGRESS_REPORT_FILE}}
```

最低限:

- Gate ID
- Trial No.
- Package ID
- execution status
- completed work
- remaining work
- observed failures / blockers
- executed verification
- relevant commit SHA
- next action required

## 4. Checkpoint report

`PACKAGE_COMPLETE`を主張する場合、以下も作成せよ。

```text
{{IMPLEMENTATION_REPORT_DIR}}/{{CHECKPOINT_REPORT_FILE}}
```

implementation checkpoint full SHAとreport-only commit SHAを分離して記録せよ。

Package completionをGate PASS / verified current stateとして表現してはならない。

## 5. Repository recording

状況報告作成後、以下を実行せよ。

```bash
git add docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}/;\
git status;\
git commit -m "{{ENHANCE_ID}} Gate {{GATE_ID}} Trial {{TRIAL_NO}} Package {{PACKAGE_ID}} implementation checkpoint";\
git push -u {{REMOTE_NAME}} {{BRANCH_NAME}};\
git log -1
```

最後にexecution statusとrelevant SHAを明示して停止せよ。next packageへ勝手に進まないこと。
