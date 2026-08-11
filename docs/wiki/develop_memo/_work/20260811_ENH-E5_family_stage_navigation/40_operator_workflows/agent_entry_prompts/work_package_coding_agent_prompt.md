# Work Package Coding Agent Prompt — ENH-E5

入力: `GATE_ID`, `TRIAL_NO`, `PACKAGE_ID`。

1. Operatorが指定したfreeze済み`06_<GATE_ID>_<PACKAGE_ID>_*.md`を正確に1つ特定する。
2. **assigned Pxxだけをnormative implementation contractとして読む。**
3. 06 Gate Contract、07、P00、他Pxx、00〜30、ADR、過去Enhancement、issue、外部Webを仕様補完のために読まない。
4. current repositoryはimplementation substrateとして調査してよいが仕様authorityではない。
5. assigned Pxxだけではentry condition / scope / protected invariant / required behaviorを一意に判断できない場合、`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
6. Package scopeとfocused verificationのみを実行する。
7. Package checkpoint/status reportを作成し、checkpoint SHAを記録する。
8. assigned Pxxで明示されない限りFixed Trial Candidateをassembleしない。
9. Package completeをGate PASSと表現しない。
