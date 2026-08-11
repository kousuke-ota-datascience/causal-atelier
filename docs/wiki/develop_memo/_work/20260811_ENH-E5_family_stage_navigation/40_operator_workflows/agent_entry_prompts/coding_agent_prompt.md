# Coding Agent Prompt — ENH-E5 `SINGLE_EXECUTION` Gate

入力: `GATE_ID`, `TRIAL_NO`。

1. 対象branch/repository stateを確認する。
2. **freeze済み`06_Ariadne_ENH-E5_<GATE_ID>_implementation_instruction.md`だけをnormative implementation contractとして読む。**
3. 07、00〜30、ADR、Gate decomposition、他Gate文書、過去Enhancement、issue、外部Webを仕様補完のために読まない。
4. current repositoryはimplementation substrateとして調査してよい。ただし仕様authorityとして扱わない。
5. 06だけではrequired behaviorを一意に判断できない場合、他資料を探索せず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
6. Active Gate scopeのみを実装する。
7. 06で要求されたfocused / Gate-wide self-verificationを実行する。
8. exact candidate SHAとimplementation completion reportを記録する。
9. `READY_FOR_TEST`または明示的`BLOCKED_*`で停止する。
10. PASS/FAIL Gate Decisionを出さない。

> 実装方法をrepositoryから発見してよい。仕様をrepositoryや別文書から発見してはならない。
