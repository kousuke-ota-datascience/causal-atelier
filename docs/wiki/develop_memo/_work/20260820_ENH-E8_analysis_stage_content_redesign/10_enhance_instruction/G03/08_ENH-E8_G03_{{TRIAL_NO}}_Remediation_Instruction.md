# ENH-E8 G03 Trial{{TRIAL_NO}} Remediation Instruction

- Document class: Remediation Contract
- Status: `TEMPLATE`
- Gate: `G03`
- Trial: `{{TRIAL_NO}}`

## 使用条件

retrospective Independent Verificationによりcanonical G03 Gate Decision = `FAIL` が発行された場合のみ使用する。

## Input

- failed Fixed Verification Candidate SHA
- failing G03 Test Item / Acceptance Criterion
- independent verification evidence
- `06_Ariadne_ENH-E8_G03_implementation_instruction.md`
- `07_Ariadne_ENH-E8_G03_test_instruction.md`

## Remediation rule

1. failed evidenceに直接対応する最小修正を定義する。
2. G03のsemantic claim / Acceptance Criteriaをsilentに変更しない。
3. ENH-E8 G01/G02のpassed contractをregressionさせない。
4. hidden Identification controlsの再表示、required属性の無条件除去、lineage authorityのcurrent form値への戻しをworkaroundとして使用しない。
5. 06/07自体のsemantic defectが判明した場合はremediationを中止し、`09` Gate Contract Amendmentへ送る。
6. remediation後は新しいFixed Trial Candidateを作り、次TrialでIndependent Verificationを行う。

Remediation completionはGate PASSではない。
