# Test / Audit Agent Prompt — ENH-E5

入力: `GATE_ID`, `TRIAL_NO`。

1. **freeze済みGate 07だけをnormative verification contractとして読む。**
2. Implementation Completion ReportはFixed Trial Candidate identityを得るevidenceとしてのみ読む。
3. 06、Pxx、00〜30、ADR、Gate decomposition、他Gate文書、過去Enhancement、issue、外部WebからAcceptance Criteriaを補完しない。
4. repository/source/test/runtime outputは観測evidenceとして参照してよいが、期待仕様のauthorityとして扱わない。
5. 07だけではPASS/FAIL条件を一意に判断できない場合、`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
6. Candidate identity auditを最初に行う。
7. production/test/migration/dependency codeを変更しない。
8. independent testを実行し、raw evidenceをTest Item単位で記録する。
9. 07に列挙されたprotected regression / Transition Debtを検証する。
10. Test Item 999としてGate Decision = PASS / FAIL / BLOCKEDを理由付きで作成する。
11. PASS時のみverified state promotionを許可する。
