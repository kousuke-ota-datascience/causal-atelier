# FAIL Rework Coding Agent 作業開始プロンプト

**Document class:** Operator Artifact / Agent Entry Prompt  
**Self-containment:** MUST for remediation routing — formal FAIL後のTrial-level remediation inputを、本promptだけで一意に特定できること。

このpromptはIndependent Test / Auditのformal FAIL後のnext Trialにのみ使用する。

```text
PROJECT_NAME={{PROJECT_NAME}}
ENHANCE_ID={{ENHANCE_ID}}
ENHANCE_SHORT_ID={{ENHANCE_SHORT_ID}}
GATE_ID={{GATE_ID}}
FAILED_TRIAL_NO={{FAILED_TRIAL_NO}}
TRIAL_NO={{TRIAL_NO}}
WORK_DIR_NAME={{WORK_DIR_NAME}}
REMOTE_NAME={{REMOTE_NAME}}
BRANCH_NAME={{BRANCH_NAME}}
```

## 1. Expansion rule

- `{{VARIABLE}}`を再帰展開する。
- 未解決placeholderが残れば開始しない。
- globが複数一致したら任意選択しない。

## 2. Derived paths

```text
WORK_ROOT=docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}
GATE_INSTRUCTION_DIR={{WORK_ROOT}}/10_enhance_instruction/{{GATE_ID}}
PATH_08_PATTERN={{GATE_INSTRUCTION_DIR}}/08_*_{{GATE_ID}}_{{TRIAL_NO}}_Remediation_Instruction.md
FAILED_GATE_DECISION={{WORK_ROOT}}/30_test_report/{{GATE_ID}}/Trial{{FAILED_TRIAL_NO}}/*_999_gate_decision.md
```

08を開き、`Remediation Mode`を確認する。

## 3. Input policy by 08 mode

### DELTA

08が列挙するrequired parent contract sectionsのみを追加contextとして読む。06 / 07全量を無条件に読み込まない。Inputs:

- 08 DELTA
- 08が明示した06 / 07 sections
- failed Gate Decision / Test evidence
- required current facts

### CONSOLIDATED

08をnext Trialの主たるeffective remediation contractとして使用する。Original 06 / 07はhistorical traceabilityであり、08が明示的に要求しない限りexecution contextへ追加しない。

## 4. Work Package remediation

08がRxx decompositionを指定する場合、このpromptで複数Rxxを一括実行しない。`work_package_coding_agent_prompt.md`相当のrouting ruleでassigned `Rxx`を1件ずつ起動する。

## 5. Candidate rule

failed candidate evidenceを上書きせず、新しいTrial candidateを生成し、新しいFixed Trial Candidate SHAを固定する。

Gate判定せず`READY_FOR_TEST`または明示的`BLOCKED`で停止する。
