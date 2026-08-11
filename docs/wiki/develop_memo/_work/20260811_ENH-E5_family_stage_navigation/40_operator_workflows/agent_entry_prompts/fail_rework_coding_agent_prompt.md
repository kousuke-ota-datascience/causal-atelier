# FAIL Rework Coding Agent Prompt — ENH-E5

formal FAIL後のreworkでは、Human/Planningによりfreezeされたcurrent Trial Remediation Contract（08、またはassigned Rxx）だけをnormative sourceとして使用する。

- `DELTA` 08が別contract section参照を必要とする場合、Operatorが事前にeffective contextをconsolidateしてAgentへ渡すことを優先する。
- Coding Agent自身がFAIL evidence、旧06/07、00〜30、ADR等を横断探索してremediation scopeを再設計しない。
- required correctionがcurrent remediation contractだけで一意に決まらない場合は`BLOCKED_CONTRACT_AMBIGUITY`。
- repositoryはimplementation substrateとして参照可。
