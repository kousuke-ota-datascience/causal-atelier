# {{GATE_ID}} Gate-local Instruction Set — 作成・運用ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけで当該Gate directoryのartifact役割・作成順序・freeze ruleが分かること。

## 1. Required artifacts

- `06_*_implementation_instruction.md` — Gate Coding Contract。Gate implementation semanticsをself-containedに固定する。
- `07_*_test_instruction.md` — Gate Verification Contract。Acceptance Criteriaをself-containedに固定する。

## 2. Conditional artifacts

- `06_{{GATE_ID}}_P00_work_package_plan.md` — Work Package Modeのorchestration plan。implementation packageではない。
- `06_{{GATE_ID}}_Pxx_*.md` — planned Work Package。Agentへ直接渡せるself-contained execution contract。
- `08_*Remediation_Instruction.md` — formal FAIL後のみ。DELTA / CONSOLIDATED modeを選ぶ。
- `08_{{GATE_ID}}_Rxx_*.md` — remediation Work Package。Agentへ直接渡せるself-contained execution contract。
- `09_*Gate_Contract_Amendment.md` — original semantic contract / AC自体の欠陥をHuman-approved changeとして記録する。

## 3. Freeze / Trial rule

- 06 / 07はGate execution開始前にfreezeする。
- Package interruption / restart / self-check correctionではTrial番号を増やさない。
- Independent Verificationのformal FAIL後にnext Trialを作る。
- FAIL後に06 / 07をsilent rewriteしない。remediationなら08、contract defectなら09を使う。

## 4. Reference rule

06 / 07 / Pxx / Rxxはnormative semanticsを本文内へ持つ。source / evidence / previous decision / parent artifact pathはtraceabilityとして参照してよい。

08 DELTAだけは、still-valid parent contractへのnormative referenceを意図的に許容する。08 CONSOLIDATEDはnext Trialのeffective contractを本文内へ統合する。
