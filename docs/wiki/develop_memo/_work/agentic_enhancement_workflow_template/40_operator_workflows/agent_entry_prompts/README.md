# Agent Entry Prompts — 使用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでprompt選択と共通変数原則が分かること。各実行promptも同じ規則を必要分だけ内部に再掲する。

## 1. Prompt selection

| Situation | Prompt |
|---|---|
| Single-execution Gate Coding | `coding_agent_prompt.md` |
| Planned Pxx / remediation Rxx Work Package | `work_package_coding_agent_prompt.md` |
| formal FAIL after Independent Test, Trial-level remediation orchestration | `fail_rework_coding_agent_prompt.md` |
| Independent Test / Audit | `test_agent_prompt.md` |

## 2. Common variable rule

Humanはexecution identityを指定し、path / filenameはderived variableで構成する。

Common human-supplied variables:

- `PROJECT_NAME`
- `ENHANCE_ID`
- `ENHANCE_SHORT_ID`
- `GATE_ID`
- `TRIAL_NO`
- `PACKAGE_ID` — Work Package時のみ。`P01-P99`または`R01-R99`
- `WORK_DIR_NAME`
- `REMOTE_NAME`
- `BRANCH_NAME`

Common expansion rules:

- `{{VARIABLE}}`を再帰展開する。
- 未解決placeholderが残れば開始しない。
- derived filenameをHumanが別途手入力して二重管理しない。
- globが複数fileへ一致したら任意選択せず停止する。

## 3. Trial / Package rules

- Trial番号はAgent起動回数ではない。
- Package interruption / restartだけでTrialを増やさない。
- Work Package promptはassigned `PACKAGE_ID`だけを実行する。
- Test promptはFixed Trial Candidate identity auditから開始する。

## Canonical filename rule

- canonical filename / directory nameはASCII charactersのみを使用する。
- semantic filename suffixはtechnical Englishとする。
- 日本語はdocument title / body textにのみ使用してよい。

