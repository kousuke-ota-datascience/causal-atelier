# 30_test_report — Independent Verification Specification v3

## 0. Purpose

Fixed Trial Candidateに対する独立Test / Audit evidenceを、Gate / Trial単位で保存する。

## 1. Directory

```text
30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/
  ..._001_*.md
  ...
  ..._999_gate_decision.md
```

## 2. Acceptance target

Gate acceptance対象は**Fixed Trial Candidate**である。

- package checkpoint単独をGate acceptance対象にしない。
- Coding self-checkをIndependent Verificationへ代用しない。
- completion reportからFixed Trial Candidate SHAを取得する。
- Tested Repository Stateとの差分を最初に監査する。

## 3. Authority

- Test Item Report = item-level observed evidence
- 999 Gate Decision = final PASS / FAIL / BLOCKED authority

## 4. Trial transition

- formal FAIL -> next Trial remediation
- BLOCKED != FAIL
- package failureはここでformal FAILになるまでTrial FAILではない

## 5. Immutability

判定済みTrial directoryを次Trialの結果で上書きしない。
