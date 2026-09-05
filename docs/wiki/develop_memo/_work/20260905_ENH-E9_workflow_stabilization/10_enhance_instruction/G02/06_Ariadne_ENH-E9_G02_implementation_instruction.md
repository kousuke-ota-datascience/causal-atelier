# Ariadne ENH-E9 G02 Implementation Instruction

**Contract status:** `DRAFT_NOT_FROZEN`  
**Execution mode:** `WORK_PACKAGE`

## Gate claim

DiscoveryからGraph比較・選択・採用までの既存workflowを、操作結果と比較対象を明確に把握できるinteractionとして成立させる。

## Prerequisites

- G01 canonical 999 PASS
- G02 residual candidatesがbaseline evidenceで`RESIDUAL`確定
- G02 06/07 + P00/Pxx FROZEN

## Allowed implementation semantics

residual確認済みpresentation/interactionだけを修正する。Graph scientific identity、comparison semantics、adoption/fix semanticsを変更しない。

## Protected contract

- FR-035–FR-039
- Graph Candidate identity
- DRAFT/FIXED Graph Version mutability
- GraphVersion lineage
- designated Outcome lineage
- current comparison API
- E8 Stage separation

## Forbidden

- new discovery algorithm
- new Graph lifecycle
- FIXED Graph direct mutation
- frontendでGraph scientific semanticsを再計算
- UI convenienceによるOutcome override

## Candidate assembly

All required Pxx `PACKAGE_COMPLETE`後、Candidate AssemblyでGate-wide regression、candidate-affecting uncommitted changeなし、Fixed Trial Candidate SHA、Implementation Completion Reportを確定する。
