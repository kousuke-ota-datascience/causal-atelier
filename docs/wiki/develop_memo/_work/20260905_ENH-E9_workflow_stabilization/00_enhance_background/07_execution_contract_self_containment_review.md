# ENH-E9 Execution Contract Self-Containment Review

- Review date: `2026-09-06`
- Review scope: G03–G05 execution contracts and shared Coding/Test Agent rules
- Review status: `REBASELINE_REQUIRED`
- Semantic Gate claim / Acceptance Criteria change: `NONE`

## 1. Objective

ENH-E9の目的は、新しいanalytical capabilityを追加することではなく、E8後に残ったworkflow usability gapと既存Causal Diagnostics requirementへのbackend conformance gapを、Stage responsibility / navigation semantics / Result-Execution-Graph lineageを変えず閉じることである。

Coding executionではassigned Pxxだけをnormative implementation contractとする。このため各Pxxは、parent Gate 06/07、P00、other Pxxを仕様補完目的で読まなくても実装判断できるself-contained contractでなければならない。

## 2. Review findings

### G01

`999_gate_decision = PASS`済み。terminal authorityを保護するため遡及変更しない。

### G02

Trial01 Fixed Trial Candidateは既にassemble済みで`READY_FOR_TEST`。candidate provenanceを保護するため06/07/P01–P03を本reviewでは遡及変更しない。Independent Verificationを先に完了する。

### G03

Gate claim/AC自体は十分に定義されているが、P01はE7/E8のself-contained execution contractに比べ、baseline fact、source-of-truth boundary、negative requirements、required evidence、stop ruleが薄い。

さらに2026-09-06 review時点のremote branchにはG02 canonical `999_gate_decision`が存在せず、G02 implementation completionは`READY_FOR_TEST`である。したがってG03 entry `G02 PASS`はcanonical evidence上未成立である。

**Decision:** review開始前に開始されたG03 Trial01/P01 Coding executionはFixed Trial Candidate evidenceへ使用しない。G02 canonical 999 PASS後、re-baselined P01 contractを用いてP01を最初から実行する。

### G04

P01–P04が短すぎ、assigned Pxx単独では必要なscientific semanticsを一意に解決できない箇所がある。特に以下はself-containment defectである。

- P01が`G04 06`にapplicability contractを委譲している。
- P02が`G04 06 contract`およびP01で決めるextreme-rule semanticsへ依存している。
- P03が`G04 06/07`をcompletion semanticsとして参照している。
- P04のstructured field shape / nullability / authority boundaryが不足している。

**Decision:** G04 P01–P04へ、必要なcontract fragmentを意図的に重複して内包する。重複はinformation isolationのための仕様複製であり、PxxがGate semanticsを変更するものではない。

### G05

P01のintegration-only correction許容範囲とstop conditionが粗い。Passed Gate semanticsを再設計せず、fixture/orchestration/synchronization/contract-compatible wiringだけを許可するよう具体化する。

## 3. Required Pxx minimum structure

未通過Gateの各Pxxは最低限、以下を持つ。

1. Identity / dependency
2. Objective
3. Baseline facts relevant to assigned responsibility
4. Required behavior / machine-observable output
5. Authoritative semantics / source-of-truth boundary
6. Protected invariants
7. Explicitly forbidden behavior
8. Implementation substrate hints（仕様authorityではない）
9. Focused verification with required cases
10. Completion boundary
11. Stop / ambiguity rule

## 4. Browser E2E policy

- Package CodingではBrowser E2Eを実行しない。
- G03/G04ではBrowser E2EをGate acceptance proofに使用しない。
- G05 Independent Verificationで、static/unit/integration/contract/protected-regressionが完了・評価された後、最後のverification itemとしてのみcritical Browser E2Eを実行する。
- Browser E2Eはcross-layer connectivity proofであり、G04 numeric/scientific correctnessのprimary proofではない。

## 5. Rebaseline classification

本reviewによる修正はGate claim / Acceptance Criteriaを変更しないため09 Gate Contract Amendmentではない。execution decomposition / self-containment / verification handoffのhardeningとしてrebaselineする。

Gate semanticsまたはAC自体を変更する必要が新たに判明した場合のみ、既存ruleどおり09 amendmentへ移行する。
