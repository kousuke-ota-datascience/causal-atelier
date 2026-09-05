# Ariadne ENH-E9 G05 Implementation Instruction

**Document class:** Primary Execution Contract  
**Contract status:** `FROZEN`  
**Execution mode:** `SINGLE_EXECUTION`  
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

## 4. Candidate completion

G01–G04 PASS、protected regression self-check、browser environment/fixture ready、journey self-check PASS、candidate-affecting uncommitted changeなし、exact Fixed Trial Candidate SHA、Implementation Completion Reportを揃える。Coding側からG05 PASSを宣言しない。
