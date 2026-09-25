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
| Independent Verification `BLOCKED` — test implementation / orchestration / environment defect, product FAIL未成立、`SAME_TRIAL` continuation明示 | `31_blocked_test_repair_01_test_infrastructure_agent_prompt.md` |
| formal FAIL — next Trial `CONSOLIDATED + SINGLE_EXECUTION` remediation | `40_fail_remediation_01_fail_rework_coding_agent_prompt.md` |
| Work Package Gateの自動control-plane | `50_orchestration_01_gate_orchestrator_prompt.md` |

**禁止:**

- formal FAIL後に`10_normal_execution_02_work_package_coding_agent_prompt.md`へ戻らない。
- test-side `BLOCKED` を product FAIL とみなして `40_fail_remediation_01_fail_rework_coding_agent_prompt.md` へ送らない。
- `31` は canonical `999_gate_decision` が同一Trial repair/reverificationを一意に指示する場合だけ使用する。

Numeric prefixは無条件な実行順ではなくworkflow responsibility categoryを表す。

```text
00 = shared convention
10 = normal execution
20 = candidate assembly
30 = independent verification
31 = blocked test-side repair / SAME_TRIAL recovery
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
- `REMEDIATION_PACKAGE_ID` — formal FAIL remediation時のみ
- `WORK_ROOT` — enhancement work directory root
- `WORK_DIR_NAME`
- `REMOTE_NAME`
- `BRANCH_NAME`

`31` blocked-test-repair がHumanから受け取るruntime variableは `GATE_ID`, `TRIAL_NO` のみ。candidate SHA / repair SHAはrepository stateから導出する。

Common expansion rules:

- `{{VARIABLE}}`を再帰展開する。
- 未解決placeholderが残れば開始しない。
- derived filenameをHumanが別途手入力して二重管理しない。
- globが複数fileへ一致したら任意選択せず停止する。

## 3. Trial / Package / repair rules

- Trial番号はAgent起動回数ではない。
- Package interruption / restartだけでTrialを増やさない。
- Normal Work Package promptはassigned `Pxx`だけを実行する。formal FAIL remediation Trialでは使用しない。
- Candidate Assemblyはall required Pxx=`PACKAGE_READY`後にのみ通常assemblyを行う。
- formal FAIL remediation direct entryはcurrent Trial 08をexactly oneに解決し、`CONSOLIDATED + SINGLE_EXECUTION`であることを確認する。
- Test promptはFixed Trial Candidate identity auditから開始する。
- `31` repairでは既存Fixed Trial Candidateを維持し、new Trialやcandidate reassemblyを行わない。
- `31` repairはproduction / 06 / 07 / Pxx / canonical 999 decisionを変更しない。repair後のGate decision更新はIndependent Test Agentが同一Trial continuationで行う。
- repairにproduct semantic changeが必要なら`31`は停止し、operator reviewへ戻す。

## 4. Browser E2E common policy

Browser E2Eを含むverificationの共通authoring / operational policyは`../BROWSER_E2E_GATE_POLICY.md`に置く。ただし各entry promptは実行時に必要なfailure handlingを自身に保持し、Test AgentのAcceptance authorityはfreeze済み07から移さない。

Browser E2E が `TEST_IMPLEMENTATION_DEFECT` / `TEST_ORCHESTRATION_DEFECT` / `TEST_ENVIRONMENT_DEFECT` でBLOCKEDとなり、product correctnessを判定できない場合は、formal product remediationではなく `31` repair routeを使用できる。ただしcanonical 999が `SAME_TRIAL` continuationを明示することが前提である。

## Canonical filename rule

- canonical filename / directory nameはASCII charactersのみを使用する。
- semantic filename suffixはtechnical Englishとする。
- 日本語はdocument title / body textにのみ使用してよい。

<!-- BEGIN MANAGED: AGENT_ENTRY_PROMPT_CONTROL -->
## 2. Agent Entry Prompts

### 2.1. Purpose

このdirectoryはAgent execution entry pointのgeneric templateを保持する。

**template directory上のpromptをAgentへ直接渡してはならない。** Enhancement開始時にEnhancement-specific instanceを `{{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/` へ生成し、Enhancement-fixed variablesを全て展開してから使用する。

### 2.2. Prompt inventory

| File | Role | Runtime variables |
|---|---|---|
| `10_normal_execution_01_single_execution_coding_agent_prompt.md` | Single Execution Coding Agent | `GATE_ID`, `TRIAL_NO` |
| `10_normal_execution_02_work_package_coding_agent_prompt.md` | Work Package Coding Agent | `GATE_ID`, `PACKAGE_ID`, `TRIAL_NO` |
| `20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md` | Fixed Trial Candidate Assembly | `GATE_ID`, `TRIAL_NO` |
| `30_independent_verification_01_test_agent_prompt.md` | Independent Verification | `GATE_ID`, `TRIAL_NO` |
| `31_blocked_test_repair_01_test_infrastructure_agent_prompt.md` | BLOCKED test-side SAME_TRIAL Repair | `GATE_ID`, `TRIAL_NO` |
| `40_fail_remediation_01_fail_rework_coding_agent_prompt.md` | Formal FAIL Remediation Coding | `GATE_ID`, `REMEDIATION_PACKAGE_ID`, `TRIAL_NO` |
| `50_orchestration_01_gate_orchestrator_prompt.md` | Gate-wide Orchestration | `GATE_ID`, `TRIAL_NO` |

### 2.3. Instantiation MUST

Enhancement開始時に `../tools/instantiate_agent_entry_prompts.py` または同等の手順でこのdirectoryをEnhancement work rootへinstance化する。

instance化完了条件:

1. Enhancement-side `agent_entry_prompts/` が存在する。
2. Enhancement-fixed placeholdersが0件である。
3. `WORK_ROOT` がexactly one Enhancement rootを指す。
4. branch / remote identityが具体値である。

未達ならAgent executionを開始しない。

### 2.4. Agent Execution Readiness

Document/template complianceとAgent Execution Readinessを別判定する。

| Axis | Required check |
|---|---|
| Artifact completeness | 必須instance artifactが存在する |
| Content completeness | required section/fieldを省略していない |
| Execution resolvability | Human entryからEnhancement/Gate/Package/Trial等が一意 |
| Information isolation | Agentが許可されたnormative sourceだけで実行可能 |

template-side `40_operator_workflows/tools/validate_agent_execution_readiness.py` をnormal execution / assembly / independent verification / formal FAIL remediation / orchestrationのreadiness確認に使用する。`31` blocked-test-repairはcanonical 999がeligibility authorityなので、`31` prompt自身のMandatory repository preflightを必ず完遂してからrepairを開始する。

### 2.5. Information isolation

Work Package Coding Agentのnormative workflow documentはassigned Pxxだけとする。

```text
Normative workflow document reachable by Work Package Coding Agent = assigned Pxx only
```

Human/auditor向けtraceability linkをCoding Agentのread dependencyにしてはならない。

Independent Test AgentはGate 07をverification authorityとして使用する。Gate 07をCoding Agentのacceptance-answer keyとして露出させてはならない。

Blocked Test Repair Agentはcanonical 999/blocker evidenceをrepair authority、frozen 07をverification scope boundaryとして使用し、06/Pxx等からrepair scopeを補完しない。

### 2.6. README identity

このdirectoryのlocal README canonical filenameは `README_40_agent_entry_prompts.md` とする。root以外の無印 `README.md` は禁止する。

filenameは手作業で決めず、`40_operator_workflows/tools/readme_naming.py` のpath-derived naming functionから導出する。
<!-- END MANAGED: AGENT_ENTRY_PROMPT_CONTROL -->
