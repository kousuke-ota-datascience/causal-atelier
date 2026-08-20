# Independent Verification Test Agent Prompt

入力identity: `GATE_ID`, `TRIAL_NO`, `Fixed Trial Candidate SHA`

1. frozen Gate `07` を唯一のAcceptance Criteria authorityとして読む。
2. Implementation Completion Reportのcandidate SHAと実repository stateが一致することを最初にauditする。
3. `07` のTest Item / Acceptance Criteriaをexact candidateに対して実行する。
4. verification中にproduction implementationやtest implementationを修正しない。
5. environment/harness原因で判定不能なら`BLOCKED`、valid candidateのproduct mismatchは`FAIL`とする。
6. Test Item evidenceを `30_test_report/<GATE>/Trial<TRIAL_NO>/` に記録する。
7. 最後にcanonical `999 Gate Decision`を `PASS` / `FAIL` / `BLOCKED` で作成する。
