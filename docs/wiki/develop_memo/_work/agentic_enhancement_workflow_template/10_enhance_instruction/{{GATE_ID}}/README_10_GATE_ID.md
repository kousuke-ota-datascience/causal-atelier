# {{GATE_ID}} Gate-local Instruction Set — 作成・運用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけで当該Gate directoryのartifact役割・作成順序・freeze ruleが分かること。

## 1. Required artifacts

- `06_*_implementation_instruction.md` — Gate Coding Contract。Gate implementation semanticsをself-containedに固定する。
- `07_*_test_instruction.md` — Gate Verification Contract。Acceptance Criteria、Test Itemのprimary test layer、Gate blocking Browser E2E（applicableな場合）のcritical journey / command / environment / synchronization / evidence / decision semanticsをself-containedに固定する。

## 2. Conditional artifacts

- `06_{{GATE_ID}}_P00_work_package_plan.md` — Work Package Modeのorchestration plan。implementation packageではない。
- `06_{{GATE_ID}}_Pxx_*.md` — planned Work Package。Agentへ直接渡せるself-contained execution contract。
- `08_{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_Remediation_Instruction.md` — formal FAIL後のみ。current Trialはこのcanonical pathでexactly oneに解決する。DELTA / CONSOLIDATED modeを選ぶ。
- `08_{{GATE_ID}}_Rxx_*.md` — remediation Work Package。Agentへ直接渡せるself-contained execution contract。
- `09_*Gate_Contract_Amendment.md` — original semantic contract / AC自体の欠陥をHuman-approved changeとして記録する。

## 3. Freeze / Trial rule

- 06 / 07はGate execution開始前にfreezeする。
- Package interruption / restart / self-check correctionではTrial番号を増やさない。
- Independent Verificationのformal FAIL後にnext Trialを作る。
- FAIL後に06 / 07をsilent rewriteしない。remediationなら08、contract defectなら09を使う。
- formal FAIL後にnormal Pxx executionへ直接戻らない。current Trial 08を作成・freezeし、execution modeに対応するremediation routeへ進む。
- `40_fail_remediation_01_fail_rework_coding_agent_prompt.md`を使用する場合、current 08は`CONSOLIDATED + SINGLE_EXECUTION`でself-containedにする。

## 4. Reference rule

06 / 07 / Pxx / Rxxはnormative semanticsを本文内へ持つ。source / evidence / previous decision / parent artifact pathはtraceabilityとして参照してよい。

08 DELTAだけは、still-valid parent contractへのnormative referenceを意図的に許容する。08 CONSOLIDATEDはnext Trialのeffective contractを本文内へ統合する。

## 5. Amendment ledger rule

09がAPPROVED / APPLIEDになった場合、`00_enhance_background/80_contract_amendment_log.md`へappend-only entryを追加し、09 / re-baseline artifact / approval / Git traceabilityを記録する。
