# ENH-E8 G01 Trial{{TRIAL_NO}} Remediation Instruction

- Document class: Remediation Contract
- Status: `TEMPLATE`
- Gate: `G01`
- Trial: `{{TRIAL_NO}}`

## 使用条件

canonical `999 Gate Decision = FAIL` が発行された場合のみ使用する。

## Input

- failed Fixed Trial Candidate SHA
- failing Test Item / Acceptance Criteria
- independent verification evidence
- frozen `06` / `07`

## Remediation rule

1. failed evidenceに直接対応する最小修正を定義する。
2. frozen Gate claim / Acceptance Criteriaをsilentに変更しない。
3. 06/07自体のsemantic defectが判明した場合はremediationを中止し、`09` Gate Contract Amendmentへ送る。
4. remediation後は新しいFixed Trial Candidateを作り、次TrialでIndependent Verificationを行う。

Remediation completionはGate PASSではない。
