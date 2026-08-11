# Coding Agent 作業開始プロンプト — SINGLE_EXECUTION

**Document class:** Operator Artifact / Agent Entry Prompt  
**Self-containment:** MUST for routing — 本prompt内のvariables / derived path / output / stop ruleだけでGate Coding Contractを一意に起動できること。

以下の変数をexecution parametersとする。

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

## Variable expansion rule

- `{{VARIABLE}}`を再帰展開する。
- 未解決placeholderが残れば開始しない。
- globが0件または複数一致なら任意選択せず停止する。

## Derived variables

```text
WORK_ROOT=docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}
INSTRUCTION_DIR={{WORK_ROOT}}/10_enhance_instruction/{{GATE_ID}}
IMPLEMENTATION_INSTRUCTION_FILE=06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_implementation_instruction.md
IMPLEMENTATION_REPORT_DIR={{WORK_ROOT}}/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}
COMPLETION_REPORT_FILE={{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_implementation_completion_report.md
```

`{{VARIABLE_NAME}}`を再帰展開し、未解決placeholderがないことを確認せよ。

以下Gate Coding Contractを実行せよ。

```text
{{INSTRUCTION_DIR}}/{{IMPLEMENTATION_INSTRUCTION_FILE}}
```

複数一致時は任意選択せず停止せよ。

完了後、Fixed Trial Candidate SHAを固定し、Completion Reportを作成せよ。
Gate判定せず`READY_FOR_TEST`または`BLOCKED`で停止せよ。

Repository記録:

```bash
git add docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}/;\
git status;\
git commit -m "{{ENHANCE_ID}} Gate {{GATE_ID}} Trial {{TRIAL_NO}} implementation candidate";\
git push -u {{REMOTE_NAME}} {{BRANCH_NAME}};\
git log -1
```
