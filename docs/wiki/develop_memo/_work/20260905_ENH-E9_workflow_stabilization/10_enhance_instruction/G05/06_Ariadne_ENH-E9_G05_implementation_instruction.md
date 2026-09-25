# Ariadne ENH-E9 G05 Implementation Instruction

**Document class:** Primary Execution Contract  
**Contract status:** `FROZEN`  
**Execution mode:** `WORK_PACKAGE`  
**Required packages:** `P01`  
**First executable package:** `P01`  
**P00 role:** `PLANNING_ONLY / NON_EXECUTABLE`  
**Entry:** G01–G04 canonical `999_gate_decision = PASS`

## 1. Gate purpose

新product capabilityを追加せず、G01–G04 PASS成果を統合したrepository stateでcritical Causal browser journeyをfinalizeする。

## 2. Allowed work

- passed Gate semanticsを変えないintegration-only defect correction
- canonical Browser E2E fixture/orchestration/synchronization wiring
- documentation/evidence finalization

Passed Gate semantic/AC変更が必要ならG05でsilent修正せずowner Gateの09 amendmentへ戻す。

## 3. Critical journey

```text
Analysis Context
 -> Discovery execution
 -> Graph candidate review / comparison
 -> adopt / FIXED Graph
 -> Identification
 -> Estimation from selected Identification Result
 -> Effects
 -> Diagnostics
```

## 4. Work Package

- P01: integrated regression acceptance preparation

P00はplanning-onlyであり実行対象ではない。P01 focused verificationではBrowser E2Eを実行しない。P01完了後にCandidate Assemblyを行い、Independent Verificationへ渡すFixed Trial Candidateを確定する。

## 5. Candidate completion

G01–G04 PASS、protected regression self-check、browser environment/fixture ready、non-browser journey prerequisites/self-check PASS、candidate-affecting uncommitted changeなし、exact Fixed Trial Candidate SHA、Implementation Completion Reportを揃える。Coding側からG05 PASSを宣言しない。

Canonical Browser E2E journeyはIndependent Verificationで、すべてのnon-browser blocking verification完了後の最後のverification itemとしてのみ実行する。
