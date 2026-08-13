# Agent Entry Prompts — 使用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでprompt選択と共通変数原則が分かること。各実行promptも同じ規則を必要分だけ内部に再掲する。

## 1. Prompt selection

| Current state | Prompt |
|---|---|
| Normal `SINGLE_EXECUTION` Gate | `10_normal_execution_01_single_execution_coding_agent_prompt.md` |
| Normal `WORK_PACKAGE` assigned Pxx | `10_normal_execution_02_work_package_coding_agent_prompt.md` |
| Normal `WORK_PACKAGE` — all required Pxx completed | `20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md` |
| Independent Gate verification | `30_independent_verification_01_test_agent_prompt.md` |
| formal FAIL — next Trial `CONSOLIDATED + SINGLE_EXECUTION` remediation | `40_fail_remediation_01_fail_rework_coding_agent_prompt.md` |
| Work Package Gateの自動control-plane | `50_orchestration_01_gate_orchestrator_prompt.md` |

**禁止:** formal FAIL後に`10_normal_execution_02_work_package_coding_agent_prompt.md`へ戻らない。

Numeric prefixは無条件な実行順ではなくworkflow responsibility categoryを表す。

```text
00 = shared convention
10 = normal execution
20 = candidate assembly
30 = independent verification
40 = formal fail remediation
50 = orchestration
```

## 2. Common variable rule

Humanはexecution identityを指定し、path / filenameはderived variableで構成する。

Common human-supplied variables:

- `PROJECT_NAME`
- `ENHANCE_ID`
- `ENHANCE_SHORT_ID`
- `GATE_ID`
- `TRIAL_NO`
- `PACKAGE_ID` — normal Work Package時のみ。`P01-P99`
- `WORK_ROOT` — enhancement work directory root
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
- Normal Work Package promptはassigned `Pxx`だけを実行する。formal FAIL remediation Trialでは使用しない。
- Candidate Assemblyはall required Pxx=`PACKAGE_READY`後にのみ通常assemblyを行う。
- formal FAIL remediation direct entryはcurrent Trial 08をexactly oneに解決し、`CONSOLIDATED + SINGLE_EXECUTION`であることを確認する。
- Test promptはFixed Trial Candidate identity auditから開始する。

## 4. Browser E2E common policy

Browser E2Eを含むverificationの共通authoring / operational policyは`../BROWSER_E2E_GATE_POLICY.md`に置く。ただし各entry promptは実行時に必要なfailure handlingを自身に保持し、Test AgentのAcceptance authorityはfreeze済み07から移さない。

## Canonical filename rule

- canonical filename / directory nameはASCII charactersのみを使用する。
- semantic filename suffixはtechnical Englishとする。
- 日本語はdocument title / body textにのみ使用してよい。
